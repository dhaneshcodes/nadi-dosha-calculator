#!/usr/bin/env python3
"""
Unified Server for Nadi Dosha Calculator
Combines FastAPI application with proxy functionality for external APIs

Usage: python server.py
Then open: http://localhost:8000
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import urllib.request
import urllib.parse
import time
import os
from pathlib import Path
from server.utils.logger import setup_logger

# Setup logger
logger = setup_logger("server")

# Import routes from server package
from server.api.routes import router
from server.api.middleware import RateLimitMiddleware, RateLimiter

# Configure the app
app = FastAPI(
    title="Nadi Dosha Calculator",
    description="Enhanced astronomical calculations for Nadi Dosha compatibility",
    version="1.0.0"
)

# Add CORS middleware (must be before rate limiting)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Add rate limiting middleware
rate_limiter = RateLimiter(max_requests=100, window_minutes=60)
app.add_middleware(RateLimitMiddleware, rate_limiter=rate_limiter)

# Include calculation API routes (router already has /api prefix)
app.include_router(router)

# Proxy endpoints for external APIs
@app.get("/api/nominatim")
async def proxy_nominatim(request: Request):
    """Proxy requests to Nominatim API"""
    try:
        logger.debug(f"Proxying Nominatim request: {request.query_params}")
        # Get query parameters
        query_params = dict(request.query_params)
        query_string = urllib.parse.urlencode(query_params)
        
        # Build Nominatim URL
        nominatim_url = f'https://nominatim.openstreetmap.org/search?{query_string}'
        
        # Make request with proper headers
        req = urllib.request.Request(
            nominatim_url,
            headers={
                'User-Agent': 'NadiDoshaCalculator/1.0 (Educational Purpose)',
                'Accept': 'application/json'
            }
        )
        
        # Rate limiting (1 request per second)
        time.sleep(1)
        
        # Get response
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        return Response(
            content=data,
            media_type='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logger.error(f"Nominatim proxy error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f'Proxy error: {str(e)}')


@app.get("/api/photon")
async def proxy_photon(request: Request):
    """Proxy requests to Photon API"""
    try:
        query_params = dict(request.query_params)
        query_string = urllib.parse.urlencode(query_params)
        photon_url = f'https://photon.komoot.io/api/?{query_string}'
        
        req = urllib.request.Request(photon_url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        return Response(
            content=data,
            media_type='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logger.error(f"Photon proxy error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f'Proxy error: {str(e)}')


@app.get("/api/timeapi")
async def proxy_timeapi(request: Request):
    """Proxy requests to TimeAPI"""
    try:
        query_params = dict(request.query_params)
        query_string = urllib.parse.urlencode(query_params)
        timeapi_url = f'https://timeapi.io/api/TimeZone/coordinate?{query_string}'
        
        req = urllib.request.Request(timeapi_url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        return Response(
            content=data,
            media_type='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logger.error(f"TimeAPI proxy error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f'Proxy error: {str(e)}')


@app.get("/api/geocode")
async def proxy_geocode(request: Request):
    """Proxy requests to geocode.prateekanand.com API (CORS fix)"""
    try:
        logger.debug(f"Proxying geocode request: {request.query_params}")
        
        query_params = dict(request.query_params)
        query_string = urllib.parse.urlencode(query_params)
        geocode_url = f'https://geocode.prateekanand.com/geocode?{query_string}'
        
        req = urllib.request.Request(
            geocode_url,
            headers={
                'Accept': 'application/json',
                'User-Agent': 'NadiDoshaCalculator/1.0'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        return Response(
            content=data,
            media_type='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logger.error(f"Geocode proxy error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f'Proxy error: {str(e)}')


# Serve static files (HTML, CSS, JS) - serve from current directory
# Note: FastAPI serves static files, but we need to handle root path specially
static_dir = Path(__file__).parent

@app.get("/")
async def serve_index():
    """Serve index.html"""
    from fastapi.responses import FileResponse
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Nadi Dosha Calculator API", "docs": "/docs"}

@app.get("/{filename}")
async def serve_static(filename: str):
    """Serve static files (CSS, JS, etc.)"""
    from fastapi.responses import FileResponse
    from fastapi import HTTPException
    
    # Security: only serve specific file types
    allowed_extensions = {'.css', '.js', '.html', '.ico', '.png', '.jpg', '.svg'}
    file_path = static_dir / filename
    
    if not file_path.exists() or file_path.suffix not in allowed_extensions:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Prevent directory traversal
    if not file_path.resolve().is_relative_to(static_dir.resolve()):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return FileResponse(file_path)


if __name__ == '__main__':
    import uvicorn
    
    PORT = int(os.getenv("PORT", "8000"))  # Use port 8000 (Nginx proxies from port 80)
    
    print('=' * 70)
    print('Nadi Dosha Calculator - Unified Server')
    print('=' * 70)
    print(f'\n🚀 Server running at: http://localhost:{PORT}')
    print(f'\n📡 API Endpoints:')
    print(f'   - POST /api/calculate-nadi - Calculate Nadi Dosha')
    print(f'   - GET  /api/nominatim - Nominatim geocoding (proxy)')
    print(f'   - GET  /api/photon - Photon geocoding (proxy)')
    print(f'   - GET  /api/geocode - Geocode API (proxy, CORS fix)')
    print(f'   - GET  /api/timeapi - TimeAPI timezone (proxy)')
    print(f'   - GET  /docs - API Documentation (Swagger)')
    print(f'\n📄 Static Files:')
    print(f'   - / - Main application (index.html)')
    print(f'\n✨ Features:')
    print(f'   - Server-side calculations (protected)')
    print(f'   - Rate limiting (100 requests/hour per IP)')
    print(f'   - CORS enabled')
    print(f'\nPress Ctrl+C to stop the server\n')
    print('=' * 70)
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)

