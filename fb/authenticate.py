# custom Facebook authentication backend
from django.contrib.auth.models import User
from fb import facebook

class FBAuthBackend:
    def authenticate(self, token=None):
        graph = facebook.GraphAPI(token)
        try:
            profile = graph.get_object("me") # will throw an exception if token is invalid
        except:
            return None
        uid = profile['id']

        user_obj = User.objects.get_or_create(username=uid)
        user = user_obj[0]
        if user_obj[1]:
            user.set_unusable_password()
            user.first_name = profile['first_name']
            user.last_name = profile['last_name'] 
            user.email = profile['email']
            user.save()
        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except:
            return None

