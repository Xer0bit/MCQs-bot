from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..services.mcq_service import MCQService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
mcq_service = MCQService()

@router.get("/generate_mcqs")
async def generate_mcqs(topic: str, number: int):
    logger.info(f"Received MCQ generation request - Topic: {topic}, Number: {number}")
    try:
        mcqs = await mcq_service.generate_mcqs(topic, number)
        logger.info("Successfully generated MCQs")
        return JSONResponse(content={"success": True, "mcqs": mcqs})
    except Exception as e:
        logger.error(f"Error generating MCQs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
