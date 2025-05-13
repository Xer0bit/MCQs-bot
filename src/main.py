from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import sys
from .api.routes import router

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('mcq_generator.log', mode='w', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return FileResponse("src/static/index.html")
