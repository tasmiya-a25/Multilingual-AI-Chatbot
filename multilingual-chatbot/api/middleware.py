import time
import functools
from flask import request, jsonify

# Simple in-memory rate limiting
RATE_LIMIT_CACHE = {}

def rate_limit(limit=60, per=60):
    """
    Simple rate limiting decorator.
    Limits requests to `limit` per `per` seconds based on IP.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()
            
            if ip not in RATE_LIMIT_CACHE:
                RATE_LIMIT_CACHE[ip] = []
                
            # Clean up old requests
            RATE_LIMIT_CACHE[ip] = [t for t in RATE_LIMIT_CACHE[ip] if now - t < per]
            
            if len(RATE_LIMIT_CACHE[ip]) >= limit:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "message": "Too many requests. Please try again later."
                }), 429
                
            RATE_LIMIT_CACHE[ip].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator
