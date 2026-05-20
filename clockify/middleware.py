import logging
import time
import json

logger = logging.getLogger("api_logger")


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Capture request start time
        start_time = time.time()

        # 2. Extract request details safely
        path = request.path
        method = request.method
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Only log payloads for API paths
        body = ""
        if path.startswith("/api/") and method in ["POST", "PUT", "PATCH","GET"]:
            try:
                # Be careful: reading request.body can sometimes disrupt file uploads.
                # If content_type is multipart, it's safer to skip raw body logging.
                if "multipart/form-data" not in request.content_type:
                    form_data = dict(request.POST.items())
                    # 🔒 Security Best Practice: Mask sensitive data like passwords
                    if "password" in form_data:
                        body["password"] = "********"
            except Exception:
                body = "<Invalid JSON or Binary Data>"

        # 3. Process the request and get the response
        response = self.get_response(request)

        # 4. Calculate execution duration
        duration = time.time() - start_time

        # 5. Log the combined metrics
        log_message = (
            f"User: {user} | Method: {method} | Path: {path} | "
            f"Status: {response.status_code} | Duration: {duration:.2f}s | Payload: {body}"
        )

        if response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        return response
