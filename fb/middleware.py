# Broken, do not use
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from funcs import *

class FBCookieAuthMiddleware:
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            return None
        sr = parse_signed_request_cookie(request.COOKIES)
        if sr:
            with open('/home/kzhang/sr.log', 'w') as f:
                f.write(str(sr))
        if request.user.is_authenticated():
            if not sr:
                logout(request)
            elif 'user_id' not in sr.keys() or sr['user_id'] != request.user.username:
                logout(request)
        elif sr:
            if 'oauth_token' in sr.keys():
                u = authenticate(token=sr['oauth_token'])
                if u:
                    login(request, u)
                    request.session['fb_access_token'] = sr['oauth_token']
            elif 'code' in sr.keys():
                token = get_access_token('', sr['code'])
                if token:
                    u = authenticate(token=token[0])
                    if u:
                        login(request, u)
                        request.session['fb_access_token'] = token[0]
            else:
                logout(request)
        return None
