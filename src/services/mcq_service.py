from .ollama_service import OllamaService
from typing import List
import logging

logger = logging.getLogger(__name__)

class MCQService:
    def __init__(self):
        self.ollama_service = OllamaService()

    async def generate_mcqs(self, topic: str, num_questions: int) -> List[List[str]]:
        logger.info(f"MCQ Service processing request for topic: {topic}")
        mcqs = await self.ollama_service.generate_mcqs(topic, num_questions)
        logger.info("Converting MCQs to CSV format")
        return self._format_for_csv(mcqs)

    def _format_for_csv(self, mcqs: List[dict]) -> List[List[str]]:
        logger.debug("Formatting MCQs for CSV output")
        csv_rows = [["ID", "Question", 
                    "Option A", "Option B", "Option C", "Option D",
                    "Correct Answer", "Explanation", "Domain"]]
        
        for mcq in mcqs:
            # Sort options by letter and ensure all 4 options exist
            options = {opt['letter']: opt['text'] for opt in mcq['options']}
            sorted_options = [options.get(letter, '') for letter in ['A', 'B', 'C', 'D']]
            
            # Get correct answer letter
            correct_index = mcq['correct_answers'][0] - 1
            correct_letter = chr(ord('A') + correct_index)
            
            row = [
                mcq['id'],
                mcq['question'].strip(),
                *[opt.strip() for opt in sorted_options],
                correct_letter,
                mcq['explanation'].strip(),
                mcq['domain'].strip()
            ]
            csv_rows.append(row)
        
        logger.info(f"Generated CSV with {len(csv_rows)} rows")
        return csv_rows
