import logging
import time

logger = logging.getLogger("api_logger")


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()


        path = request.path
        method = request.method
        user = request.user if request.user.is_authenticated else "Anonymous"


        body = ""
        if path.startswith("/api/") and method in ["POST", "PUT", "PATCH","GET"]:
            try:

                if "multipart/form-data" not in request.content_type:
                    form_data = dict(request.POST.items())
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
