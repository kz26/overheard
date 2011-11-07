# Create your views here.
from models import *
from django.contrib.auth import *
from django.shortcuts import *
from django.http import *
import simplejson as json
from forms import *
from django.db.models import Count
from django.core.paginator import Paginator
from django.conf import settings
from django_magic import funcs

def site_login(request):
    if 'token' in request.GET:
        u = authenticate(token=request.GET['token'])
        if u:
            login(request, u)
            request.session.set_expiry(604800)
    return redirect('/')
            
def render_posts(request, school, latest=True):
    try:
        school_obj = School.objects.get(slug=school)
    except:
        raise Http404
    request.session['school'] = school_obj
    errors = False
    f = NewPostForm()
    if request.method == 'POST' and request.user.is_authenticated():
         p = Post()
         p.author = request.user
         p.school = school_obj
         f = NewPostForm(request.POST, request.FILES, instance=p)
         if f.is_valid():
             f.save()
             return redirect('/')
         else: errors = f.errors
    request.session['school'] = school_obj
    if latest:
        posts = Post.objects.filter(school=school_obj).order_by('-date')[:settings.POSTS_PER_PAGE]
    else:
        posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-date')[:settings.POSTS_PER_PAGE]
    return render(request, 'index.html', dictionary={'posts': posts, 'latest': latest, 'f': f})

def render_single_post(request, school, postid):
    try:
        school_obj = School.objects.get(slug=school)
    except:
        raise Http404
    request.session['school'] = school_obj
    
    post = Post.objects.filter(school=school_obj, pk=int(postid))
    if post.exists():
        return render(request, 'index.html', dictionary={'posts': post, 'single': True, 'hide_permalink': True})
    else:    
        raise Http404
        
def render_user_posts(request, school, userid):
    try:
        school_obj = School.objects.get(slug=school)
    except:
        raise Http404
    request.session['school'] = school_obj
    
    try:
        user_obj = User.objects.get(pk=int(userid))
    except:
        raise Http404
    posts = Post.objects.filter(school=school_obj, author=user_obj)
    return render(request, 'index.html', dictionary={'posts': posts, 'single': True})

def render_posts_popular(request, school):
    return render_posts(request, school, latest=False)

def index_view(request):
    return render_posts(request, 'uchicago')

def more_posts(request, school, latest=True):
    if request.is_ajax() and request.method == 'GET':
        page = 1
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])
            except:
                return HttpResponse(status=400)
        try:
            school_obj = School.objects.get(slug=school)
        except:
            raise Http404
        if latest:
            posts = Post.objects.filter(school=school_obj).order_by('-date')
        else:
            posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-date')
        pgn = Paginator(posts, settings.POSTS_PER_PAGE)
        try:
            posts = pgn.page(page).object_list
        except:
            resp = []
            return HttpResponse(json.dumps(resp))
        if len(posts):
            posts_s = Post.serialize_posts_json(posts)
            return HttpResponse(posts_s)
        else:
            resp = []
            return HttpResponse(json.dumps(resp))
    return HttpResponse(status=400)

def more_posts_popular(request, school):
    return more_posts(request, school, latest=False)

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
            resp = {'success': True, 'comment': c.simplify()}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'success': False, 'error_msg': f.errors}
            return HttpResponse(json.dumps(resp))
    resp = {'success': False}
    return HttpResponse(json.dumps(resp))

def site_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')
