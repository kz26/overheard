from django.conf import settings
from urlparse import parse_qs
import hashlib
import hmac
import base64
import simplejson as json

def get_access_token(redirect_uri, auth_code):
    qstring = (("client_id", settings.FB_APP_ID),
        ("redirect_uri", redirect_uri),
        ("client_secret", settings.FB_APP_SECRET),
        ("code", auth_code))
    try:
        d = urllib2.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(qstring))
    except urllib2.HTTPError, e:
        return None
    return parse_qs(d.read())

def check_access_token(token): # checks if the access token is valid
    qstring = {'access_token': token}
    try:
        urllib2.urlopen("https://graph.facebook.com/me?" + urllib.urlencode(qstring))
    except urllib2.HTTPError, e:
        return False
    return True

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(request, secret=settings.FB_APP_SECRET):
    encoded_sig, payload = request.split(".")
    
    # decode data
    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data['algorithm'].upper() != 'HMAC-SHA256':
        return None

    # check sig
    hasher = hmac.new(secret, payload, digestmod=hashlib.sha256)
    if hasher.digest() != sig:
        return None

    return data

def getSignedRequestCookieName():
    return 'fbsr_' + settings.FB_APP_ID

def parse_signed_request_cookie(cookies):
    if getSignedRequestCookieName() in cookies.keys():
        return parse_signed_request(cookies[getSignedRequestCookieName()])
    return None

