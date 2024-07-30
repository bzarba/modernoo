from .models import Setting

class SettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings = Setting.objects.filter(active=True).first()

        request.settings = settings

        response = self.get_response(request)
        return response
