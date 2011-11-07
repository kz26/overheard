from django.conf import settings
from subprocess import Popen
from tempfile import *

def makeThumbnail(fn):
    temp = NamedTemporaryFile(delete=False)
    args = ['convert', fn, '-resize', '%sx%s' % (settings.MAX_THUMBNAIL_DIMENSION, settings.MAX_THUMBNAIL_DIMENSION), temp.name]
    Popen(args).communicate()
    return temp
