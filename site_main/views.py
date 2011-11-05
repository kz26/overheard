# Create your views here.
from models import *
from django.contrib.auth import *
from django.shortcuts import *
from django.http import *

def site_login(request):
    if 'token' in request.GET:
        u = authenticate(token=request.GET['token'])
        if u:
            login(request, u)
    return redirect('/')
            
def logintest(request):
    return HttpResponse(str(request.user.is_authenticated()))
