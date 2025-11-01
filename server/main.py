"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.api.routes import router
from server.api.middleware import RateLimitMiddleware, RateLimiter
from server import __version__

# Initialize FastAPI app
app = FastAPI(
    title="Nadi Dosha Calculator API",
    description="Enhanced astronomical calculations for Nadi Dosha compatibility",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
rate_limiter = RateLimiter(max_requests=100, window_minutes=60)
app.add_middleware(RateLimitMiddleware, rate_limiter=rate_limiter)

# Include routers
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Nadi Dosha Calculator API",
        "version": __version__,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

