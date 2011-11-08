from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from uuid import uuid1
from os.path import splitext
import simplejson as json
from cStringIO import StringIO
from django.conf import settings
from django.core.files.base import ContentFile
#from django.contrib.auth.signals import *
from imagehelper import *
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from prettydate import pretty_date

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    banned = models.BooleanField(default=False)
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)

User.profile = property(lambda u: UserProfile.objects.get(user=u))
User.firstl = property(lambda u: u.first_name + " " + u.last_name[0])

class School(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='short_name', unique=True)
    def __unicode__(self):
        return self.name

def gen_filename(instance, filename):
    return str(uuid1()) + splitext(filename)[1].lower()

class Post(models.Model):
    class Meta:
        unique_together = ('school', 'location', 'content', 'author')

    date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School)
    location = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, related_name="post_author")
    likes = models.ManyToManyField(User, related_name="post_likes", null=True, blank=True)
    image = models.ImageField(upload_to=gen_filename, null=True, blank=True)
    image_thumb = models.ImageField(upload_to=gen_filename, null=True, blank=True)

    def __unicode__(self):
        return self.location

    def date_pretty(self):
        return pretty_date(self.date)

    def has_images(self):
        return self.image and self.image_thumb

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.image and not self.image_thumb:
            try:
                tf = makeThumbnail(self.image.path) 
                if tf:
                    self.image_thumb.save(self.image.name, ContentFile(tf.read()))
                    tf.close()
            except:
                pass
    
    @staticmethod
    def serialize_posts_json(pqueryset, logged_in=False):
        data = []
        for q in pqueryset:
            p = {}
            p['id'] = q.pk
            p['date'] = pretty_date(q.date)
            p['location'] = q.location
            p['school'] = q.school.name
            p['content'] = q.content.replace('\n', '<br />')
            p['author'] = q.author.firstl
            p['author_url'] = "http://" + Site.objects.get_current().domain + reverse('site_main.views.render_user_posts', args=[q.school.slug, q.author.pk])
            p['likes'] = q.likes.count()
            p['liked'] = logged_in and (q.author in q.likes.all())
            p['image'] = False
            p['url'] = "http://" + Site.objects.get_current().domain + reverse('site_main.views.render_single_post', args=[q.school.slug, q.pk])
            if q.image and q.image_thumb:
                i = {}
                i['full'] = q.image.url
                i['thumb'] = q.image_thumb.url
                p['image'] = i
            comments = q.postcomment_set.all().order_by('date')
            cl = []
            for c in comments:
                cd = {}
                cd['author'] = c.author.firstl
                cd['author_url'] = "http://" + Site.objects.get_current().domain + reverse('site_main.views.render_user_posts', args=[q.school.slug, c.author.pk])
                cd['date'] = pretty_date(c.date)
                cd['content'] = c.content
                cl.append(cd)
            p['comment_count'] = len(cl)
            p['comments'] = cl
            p['comment_post_url'] = reverse('site_main.views.post_comment', args=[q.pk])
            data.append(p)
        return json.dumps(data)


class PostComment(models.Model):
    class Meta:
        ordering = ['date']
        unique_together = ('post', 'author', 'content')
    post = models.ForeignKey(Post)
    author =  models.ForeignKey(User)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def date_pretty(self):
        return pretty_date(self.date)

    def simplify(self):
        d = {}
        d['author'] = self.author.firstl
        d['author_url'] = reverse('site_main.views.render_user_posts', args=[self.post.school.slug, self.author.pk])
        d['content'] = self.content
        d['date'] = self.date_pretty()
        d['post'] = self.post.pk
        return d
        
