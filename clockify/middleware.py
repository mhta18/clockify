import logging
import time
import json

logger = logging.getLogger("api_logger")


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()


        path = request.path
        method = request.method
        user = request.user if request.user.is_authenticated else "Anonymous"


        body = {}
        if path.startswith("/api/") and method in ["POST", "PUT", "PATCH","GET"]:
            try:
                if "multipart/form-data" not in request.content_type:
                    if request.content_type == "application/json" and request.body:
                        body_data = json.loads(request.body.decode("utf-8"))
                    else:
                        body_data = dict(request.POST.items())

                    if "password" in body_data:
                        body_data["password"] = "********"
                        
            except Exception:
                body_data = {"error": "<Invalid JSON or Binary Data>"}

        response = self.get_response(request)

        duration = time.time() - start_time

        log_message = (
            f"User: {user} | Method: {method} | Path: {path} | "
            f"Status: {response.status_code} | Duration: {duration:.2f}s | Payload: {body}"
        )

        if response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        return response
