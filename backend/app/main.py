from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.api import auth, generations, search
from app.middleware.auth import AuthMiddleware

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Al-Hashadeh Educational Material Generator",
    description="Production-ready system for generating educational materials using the Al-Hashadeh methodology",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up CORS – origins come from CORS_ORIGINS env var (comma-separated)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(generations.router, prefix="/generations", tags=["generations"])
app.include_router(search.router, prefix="/search", tags=["search"])


@app.get("/")
async def root():
    return {"message": "Welcome to Al-Hashadeh Educational Material Generator"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}