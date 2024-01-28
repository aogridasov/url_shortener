import logging

from django.utils import timezone


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def _get_user_ip(request):
        user_ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if user_ip:
            return user_ip.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def __call__(self, request):
        response = self.get_response(request)
        user_ip = self._get_user_ip(request)
        logging.info(
            (
                f"{timezone.now()} | {request.method} | {request.path}| "
                f"{user_ip} | {response.status_code}"
            )
        )
        return response
