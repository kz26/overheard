# custom Facebook authentication backend
from django.contrib.auth.models import User
from site_main.models import *
from fb import facebook

class FBAuthBackend:
    def authenticate(self, token=None):
        try:
            graph = facebook.GraphAPI(token)
            profile = graph.get_object("me") # will throw an exception if token is invalid
            uid = profile['id']

            # check for existing user
            try:
                user = User.objects.get(username=uid)
            except:
                user = None

            # otherwise create a new user
            if user == None:
                user = User(username=uid)
                #user.set_unusable_password()
                user.set_password(User.objects.make_random_password())
                user.save()
                uprofile = UserProfile(user=user)
                uprofile.save()
       
            user.first_name = profile['first_name']
            user.last_name = profile['last_name'] 
            user.save()
            return user
        except:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except:
            return None

