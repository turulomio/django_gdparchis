from django.utils import timezone
from gdparchis.routes4 import routes4
from gdparchis.squares4 import squares4

class GdParchisMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        self.squares4=squares4
        self.routes4=routes4
        
        
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.start=timezone.now()
        request.squares4=self.squares4
        request.routes4=self.routes4

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
