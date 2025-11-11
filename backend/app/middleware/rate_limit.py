"""Simple rate limiting middleware."""
from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter.
    
    For production, use Redis or similar distributed cache.
    """
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Max requests per minute per IP
            requests_per_hour: Max requests per hour per IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Storage: {ip: [(timestamp, count), ...]}
        self._minute_buckets = defaultdict(list)
        self._hour_buckets = defaultdict(list)
    
    def _clean_old_entries(self, ip: str):
        """Remove expired entries."""
        now = datetime.now()
        
        # Clean minute buckets (older than 1 minute)
        minute_ago = now - timedelta(minutes=1)
        self._minute_buckets[ip] = [
            (ts, count) for ts, count in self._minute_buckets[ip]
            if ts > minute_ago
        ]
        
        # Clean hour buckets (older than 1 hour)
        hour_ago = now - timedelta(hours=1)
        self._hour_buckets[ip] = [
            (ts, count) for ts, count in self._hour_buckets[ip]
            if ts > hour_ago
        ]
    
    def check_rate_limit(self, ip: str) -> tuple[bool, str]:
        """
        Check if request is within rate limits.
        
        Args:
            ip: Client IP address
            
        Returns:
            Tuple of (allowed: bool, error_message: str)
        """
        self._clean_old_entries(ip)
        now = datetime.now()
        
        # Count requests in last minute
        minute_count = sum(count for _, count in self._minute_buckets[ip])
        if minute_count >= self.requests_per_minute:
            return False, f"Rate limit exceeded: {self.requests_per_minute} requests per minute"
        
        # Count requests in last hour
        hour_count = sum(count for _, count in self._hour_buckets[ip])
        if hour_count >= self.requests_per_hour:
            return False, f"Rate limit exceeded: {self.requests_per_hour} requests per hour"
        
        # Add this request
        self._minute_buckets[ip].append((now, 1))
        self._hour_buckets[ip].append((now, 1))
        
        return True, ""
    
    async def __call__(self, request: Request, call_next):
        """Middleware function."""
        # Get client IP
        client_ip = request.client.host
        
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/"]:
            return await call_next(request)
        
        # Skip rate limiting for test client (localhost)
        if client_ip in ["testclient", "127.0.0.1", "localhost"]:
            response = await call_next(request)
            response.headers["X-RateLimit-Disabled"] = "test-mode"
            return response
        
        # Check rate limit
        allowed, error_msg = self.check_rate_limit(client_ip)
        
        if not allowed:
            logger.warning(f"Rate limit exceeded for {client_ip}: {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        
        return response


# Global rate limiter instance
rate_limiter = RateLimiter(
    requests_per_minute=60,
    requests_per_hour=1000
)

