"""
Middleware for rate limiting and security
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time


class RateLimiter:
    """
    Rate limiter using sliding window algorithm.
    Follows SRP: Only responsible for rate limiting logic.
    """
    
    def __init__(self, max_requests: int = 100, window_minutes: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in time window
            window_minutes: Time window in minutes
        """
        self.max_requests = max_requests
        self.window_seconds = window_minutes * 60
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, client_identifier: str) -> Tuple[bool, Optional[str]]:
        """
        Check if request is allowed for client.
        
        Args:
            client_identifier: Unique identifier (IP address, user ID, etc.)
            
        Returns:
            Tuple of (is_allowed, error_message_if_not_allowed)
        """
        now = time.time()
        
        # Get requests for this client
        client_requests = self.requests[client_identifier]
        
        # Remove old requests outside the window
        window_start = now - self.window_seconds
        client_requests[:] = [req_time for req_time in client_requests if req_time > window_start]
        
        # Check if limit exceeded
        if len(client_requests) >= self.max_requests:
            # Calculate time until oldest request expires
            oldest_request = min(client_requests)
            wait_seconds = int(window_start + self.window_seconds - now)
            wait_minutes = max(1, wait_seconds // 60)
            
            return False, f"Rate limit exceeded. Please wait {wait_minutes} minute(s) before making another request."
        
        # Add current request
        client_requests.append(now)
        
        return True, None
    
    def get_remaining_requests(self, client_identifier: str) -> int:
        """Get remaining requests for client in current window"""
        now = time.time()
        window_start = now - self.window_seconds
        client_requests = [
            req_time for req_time in self.requests[client_identifier]
            if req_time > window_start
        ]
        return max(0, self.max_requests - len(client_requests))


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting.
    Follows OCP: Can be extended without modifying core functionality.
    """
    
    def __init__(self, app, rate_limiter: RateLimiter):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        # Endpoints that should be rate limited
        self.protected_paths = ["/api/calculate-nadi", "/api/calculate-nadi-complete"]
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Only apply rate limiting to protected paths
        if any(request.url.path.startswith(path) for path in self.protected_paths):
            # Get client identifier (IP address)
            client_ip = request.client.host if request.client else "unknown"
            
            # Check rate limit
            is_allowed, error_message = self.rate_limiter.is_allowed(client_ip)
            
            if not is_allowed:
                return Response(
                    content=f'{{"error": "Rate limit exceeded", "detail": "{error_message}"}}',
                    status_code=429,
                    media_type="application/json"
                )
            
            # Add remaining requests to response headers
            remaining = self.rate_limiter.get_remaining_requests(client_ip)
            response = await call_next(request)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Limit"] = str(self.rate_limiter.max_requests)
            
            return response
        
        # No rate limiting for other paths
        return await call_next(request)

