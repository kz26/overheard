# Create your views here.
from models import *
from django.contrib.auth import *
from django.shortcuts import *
from django.http import *
import simplejson as json
from forms import *

def site_login(request):
    if 'token' in request.GET:
        u = authenticate(token=request.GET['token'])
        if u:
            login(request, u)
    return redirect('/')
            
#def logintest(request):
#    return HttpResponse(str(request.user.is_authenticated()))

def render_posts(request, school, latest=True):
    try:
        school_obj = School.objects.get(slug=school)
    except:
        raise Http404
    
    request.session['school'] = school_obj
    posts = Post.objects.filter(school=school_obj).order_by('-date')[:10]
    return render(request, 'index.html', dictionary={'posts': posts})

def post_comment(request, postid):
    if request.is_ajax() and request.method == 'POST' and request.user.is_authenticated():
        c = PostComment()
        try:
            c.post = Post.objects.get(pk=int(postid))
        except:
            resp = {'success': False, 'error_msg': 'Invalid post ID'}
            return HttpResponse(json.dumps(resp))
        c.author = request.user
        f = CommentForm(request.POST, instance=c)
        if f.is_valid():
            f.save()
            resp = {'success': True}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'success': False, 'error_msg': f.errors}
            return HttpResponse(json.dumps(resp))
    resp = {'success': False}
    return HttpResponse(json.dumps(resp))

