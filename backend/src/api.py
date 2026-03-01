from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .scan import find_services
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging so you can see what's happening
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ghost.api")

app = FastAPI()

# Allow frontend to call backend (localhost and 127.0.0.1 - browser sends Origin based on URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    logger.info("Backend started; /api/scan and /health are available")


@app.middleware("http")
async def log_requests(request, call_next):
    """Log every incoming request so you can see if the frontend is reaching the backend."""
    logger.info("Incoming request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("Response status: %s for %s %s", response.status_code, request.method, request.url.path)
    return response


@app.get("/api/scan")
def scan_emails():
    """Scan for email services"""
    logger.info("GET /api/scan called")
    try:
        logger.info("Calling find_services()...")
        services = find_services()
        result = sorted(list(services))
        logger.info("Scan completed successfully, found %d services: %s", len(result), result)
        return {
            "success": True,
            "services": result
        }
    except Exception as e:
        logger.exception("Scan failed: %s", e)
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/health")
def health_check():
    """Check if API is running"""
    logger.info("GET /health called")
    return {"status": "ok"}