from django.contrib.auth import authenticate, login, logout
from funcs import *

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
