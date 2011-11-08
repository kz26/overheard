from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from fb.async import AsyncWallPost

def new_wall_post(access_token, post):
        message = "%s posted on OverheardBy.Me!" % (post.author.get_full_name())
        attachment = {'name': post.location,
            'link': "http://%s%s" % (Site.objects.get_current().domain, reverse('site_main.views.render_single_post', args=[post.school.slug, post.pk])),
            'caption': post.school.name,
            'description': post.content}
        AsyncWallPost(access_token, message, attachment).start()

