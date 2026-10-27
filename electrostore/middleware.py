"""
Request Logging Middleware for ElectroStore
Logs all incoming requests with timestamp, method, path, and response status
"""
import logging
import time

logger = logging.getLogger('electrostore.requests')


class RequestLoggingMiddleware:
    """Middleware to log all HTTP requests"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log the request
        logger.info(
            f"[{request.method}] {request.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.3f}s | "
            f"IP: {self.get_client_ip(request)} | "
            f"User: {request.user if request.user.is_authenticated else 'Anonymous'}"
        )

        return response

    def get_client_ip(self, request):
        """Extract client IP from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
