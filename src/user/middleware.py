from .models import Visitor

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the visitor's IP address
        ip_address = request.META.get('REMOTE_ADDR')
        
        # Check if the IP address is not already in the database to avoid duplicate entries
        if ip_address and not Visitor.objects.filter(ip_address=ip_address).exists():
            Visitor.objects.create(ip_address=ip_address)
        
        response = self.get_response(request)
        return response
