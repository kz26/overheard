from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from uuid import uuid1
from os.path import splitext

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
    date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School)
    location = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, related_name="post_author")
    likes = models.ManyToManyField(User, related_name="post_likes", null=True, blank=True)
    image = models.ImageField(upload_to=gen_filename, null=True, blank=True)
    image_thumb = models.ImageField(upload_to=gen_filename, null=True, blank=True)

class PostComment(models.Model):
    class Meta:
        ordering = ['date']
        unique_together = ('post', 'author', 'content')
    post = models.ForeignKey(Post)
    author =  models.ForeignKey(User)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True) 
