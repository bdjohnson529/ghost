from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .scan import find_services
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scan")
def scan_emails():
    """Scan for email services"""
    try:
        services = find_services()
        return {
            "success": True,
            "services": sorted(list(services))
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/health")
def health_check():
    """Check if API is running"""
    return {"status": "ok"}