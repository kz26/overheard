from django.conf import settings

def app_id(request):
    return {'fb_app_id': settings.FB_APP_ID}
