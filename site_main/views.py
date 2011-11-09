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
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django_magic import funcs
from fb.funcs import *
from fbhooks import *
from django.core.mail import mail_admins
from django.template.loader import render_to_string

def select_school(request):
    schools = School.objects.all().order_by('name')
    return render(request, 'select-school.html', dictionary={'schools': schools})

def index_view(request):
    if 'school' in request.session.keys():
        return redirect(reverse('site_main.views.render_posts', args=[request.session['school'].slug]))
    return select_school(request)

def site_login(request):
    if 'code' in request.GET:
        token = get_access_token("http://" + Site.objects.get_current().domain + request.path, request.GET['code'])
        if token:
            u = authenticate(token=token)
            if u:
                UserProfile.objects.get_or_create(user=u)
                login(request, u)
    return redirect('/')
   
def fb_post_callback(request, postid):
    if 'code' in request.GET:
        try:
            post_obj = Post.objects.get(pk=int(postid))
        except:
            return HttpResponse(status=400)
        token = get_access_token("http://" + Site.objects.get_current().domain + request.path, request.GET['code'])
        if token:
            new_wall_post(token, post_obj)
        return redirect(reverse('site_main.views.render_posts', args=[post_obj.school.slug]))
    return HttpResponse(status=400)

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
            p.likes.add(request.user)
            p.save()
            return redirect(generate_auth_link(reverse('site_main.views.fb_post_callback', args=[p.pk])))
        else: 
            errors = f.errors
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
        return render(request, 'index.html', dictionary={'posts': post, 'hideExtra': True, 'hide_permalink': True, 'own_meta': post[0]})
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
    return render(request, 'index.html', dictionary={'posts': posts, 'hideExtra': True})

def render_posts_popular(request, school):
    return render_posts(request, school, latest=False)

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
            posts_s = Post.serialize_posts_json(posts, request.user.is_authenticated())
            return HttpResponse(posts_s)
        else:
            resp = []
            return HttpResponse(json.dumps(resp))
    return HttpResponse(status=400)

def more_posts_popular(request, school):
    return more_posts(request, school, latest=False)

def like_post(request, postid):
    if request.is_ajax() and request.method == 'GET' and request.user.is_authenticated():
        try:
            post = Post.objects.get(pk=int(postid))
        except:
            resp = {'success': False, 'error_msg': 'Invalid post ID'}
            return HttpResponse(json.dumps(resp))
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            resp = {'success': True}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'success': False, 'error_msg': 'You already like this post.'}
            return HttpResponse(json.dumps(resp))
    resp = {'success': False, 'error_msg': 'You need to be logged in to like a post.'}
    return HttpResponse(json.dumps(resp))

def report_post(request, postid):
    if request.is_ajax() and request.method == 'GET' and request.user.is_authenticated():
        try:
            post = Post.objects.get(pk=int(postid))
        except:
            return HttpResponse(status=400)
        message = render_to_string('admin-report-post.txt', {'reporter': request.user, 'post': post})
        mail_admins("Post reported", message)
        return HttpResponse()
    return HttpResponse(status=400)

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
            resp = {'success': False, 'error_msg': 'Input is invalid.'}
            return HttpResponse(json.dumps(resp))
    resp = {'success': False, 'error_msg': 'You need to be logged in to comment.'}
    return HttpResponse(json.dumps(resp))

def site_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')
