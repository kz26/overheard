from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    banned = models.BooleanField(default=False)
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)

User.profile = property(lambda u: UserProfile.objects.get(user=u))

