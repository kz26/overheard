from models import UserProfile
from django.contrib.auth import authenticate, login, logout
from fb.funcs import *

class FBCookieAuthMiddleware:
    def process_request(self, request):
        sr = parse_signed_request_cookie(request.COOKIES)
        if request.user.is_authenticated():
            if not sr:
                logout(request)
        else:
            if sr and 'oauth_token' in sr.keys():
                u = authenticate(sr['oauth_token'])
                login(request, u)
        return None
            
class BanMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated():
            if UserProfile.objects.filter(user=request.user).exists() and request.user.profile.banned:
                logout(request)
        return None
