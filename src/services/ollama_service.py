import aiohttp
import os
import json
import logging
from typing import List
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.api_url = os.getenv("OLLAMA_API_URL")
        self.model = os.getenv("MODEL_NAME")

    async def generate_mcqs(self, topic: str, num_questions: int) -> List[dict]:
        logger.info(f"Generating {num_questions} MCQs for topic: {topic}")
        all_mcqs = []
        
        for i in range(num_questions):
            prompt = f"""Generate 1 multiple choice question about {topic}.
            Follow this exact format:

            <<<MCQ>>>
            Question:
            [Short, clear question about {topic}]

            Options:
            [A] [option text]
            [B] [option text]
            [C] [option text]
            [D] [option text]

            Answer: [A/B/C/D]

            Explanation:
            [One-line explanation]

            Domain:
            [Subject area]
            <<<MCQ_END>>>
            """
            
            try:
                mcq = await self._generate_single_mcq(prompt, i + 1)
                if mcq:
                    all_mcqs.append(mcq)
            except Exception as e:
                logger.error(f"Error generating question {i + 1}: {str(e)}")
                continue
                
        return all_mcqs

    async def _generate_single_mcq(self, prompt: str, question_num: int) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                request_data = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
                
                async with session.post(self.api_url, json=request_data) as response:
                    result = await response.json()
                    if 'error' in result:
                        raise Exception(f"Ollama API Error: {result['error']}")
                    
                    return self._parse_single_mcq(result['response'], question_num)
                    
        except Exception as e:
            logger.error(f"Error in API call for question {question_num}: {str(e)}")
            raise

    def _parse_single_mcq(self, response: str, question_num: int) -> dict:
        logger.info(f"\n=== Parsing Question {question_num} ===")
        logger.debug(f"Raw response:\n{response}")
        
        try:
            # Clean up the response first
            content = response
            if '<<<MCQ>>>' in response:
                content = response.split('<<<MCQ>>>')[1].split('<<<MCQ_END>>>')[0]
            
            mcq = {
                'id': f'Q{question_num}',
                'question': '',
                'options': [],
                'correct_answers': [],
                'explanation': '',
                'domain': ''
            }

            # Extract question (handle both formats)
            if 'Question:' in content:
                question_part = content.split('Question:')[1]
                question_lines = []
                for line in question_part.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith('[A]') or line.startswith('Options:'):
                        break
                    question_lines.append(line)
                mcq['question'] = ' '.join(question_lines).strip()

            # Extract options
            options_part = ''
            if 'Options:' in content:
                options_part = content.split('Options:')[1].split('Answer:')[0]
            else:
                # Try to find options directly
                options_section = []
                capture = False
                for line in content.split('\n'):
                    if line.strip().startswith('[A]'):
                        capture = True
                    if capture and line.strip().startswith('Answer:'):
                        break
                    if capture:
                        options_section.append(line)
                options_part = '\n'.join(options_section)

            # Parse options
            for line in options_part.split('\n'):
                line = line.strip()
                if line.startswith('[') and ']' in line:
                    letter = line[1:line.index(']')]
                    text = line[line.index(']')+1:].strip()
                    if letter in ['A', 'B', 'C', 'D']:
                        mcq['options'].append({
                            'text': text,
                            'letter': letter,
                            'number': ord(letter) - ord('A') + 1
                        })

            # Extract answer (handle multiple formats)
            if 'Answer:' in content:
                ans_part = content.split('Answer:')[1].split('Explanation:' if 'Explanation:' in content else 'Domain:')[0]
                # Handle both [A] and just A format
                ans_text = ans_part.strip()
                if '[' in ans_text and ']' in ans_text:
                    letter = ans_text[ans_text.index('[')+1:ans_text.index(']')]
                else:
                    letter = ans_text.strip()[0]  # Take first character
                if letter in ['A', 'B', 'C', 'D']:
                    mcq['correct_answers'] = [ord(letter) - ord('A') + 1]

            # Extract explanation
            if 'Explanation:' in content:
                expl_part = content.split('Explanation:')[1].split('Domain:')[0]
                mcq['explanation'] = ' '.join(line.strip() for line in expl_part.splitlines() if line.strip())

            # Extract domain
            if 'Domain:' in content:
                domain_part = content.split('Domain:')[1]
                mcq['domain'] = domain_part.split('\n')[0].strip()

            # Validate
            if (mcq['question'] and 
                len(mcq['options']) == 4 and 
                mcq['correct_answers']):
                mcq['explanation'] = mcq['explanation'] or "No explanation provided"
                mcq['domain'] = mcq['domain'] or "General"
                logger.info(f"Q{question_num}: Successfully parsed MCQ")
                return mcq
            else:
                missing = []
                if not mcq['question']: missing.append('question')
                if len(mcq['options']) != 4: missing.append('options')
                if not mcq['correct_answers']: missing.append('answer')
                logger.error(f"Q{question_num}: Missing required fields: {', '.join(missing)}")
                return None

        except Exception as e:
            logger.error(f"Q{question_num}: Error while parsing: {str(e)}")
            logger.exception("Detailed error:")
            return None
