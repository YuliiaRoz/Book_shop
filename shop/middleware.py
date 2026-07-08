import time
import logging

logger = logging.getLogger(__name__)

class PerformanceTrackingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
            logger.info(f"[ШВИДКІСТЬ] Сторінка {request.path} відпрацювала за {duration:.4} сек")
        return response
