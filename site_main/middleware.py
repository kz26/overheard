from models import UserProfile
from django.contrib.auth import authenticate, login, logout

class BanMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated():
            if UserProfile.objects.filter(user=request.user).exists() and request.user.profile.banned:
                logout(request)
        return None
