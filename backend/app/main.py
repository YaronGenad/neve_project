from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth
from app.middleware.auth import AuthMiddleware

app = FastAPI(
    title="Al-Hashadeh Educational Material Generator",
    description="Production-ready system for generating educational materials using the Al-Hashadeh methodology",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to Al-Hashadeh Educational Material Generator"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}