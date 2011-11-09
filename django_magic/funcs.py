from django.conf import settings
import re
from subprocess import Popen, PIPE
import os

pat = re.compile(r': (.*)$')

def is_valid_file(fn):
    if settings.MAGICFILE_PATH:
        p = settings.MAGICFILE_PATH
    else:
        p = 'file'
    args = [p, '--mime-type', fn]
    p = Popen(args, stdout=PIPE).communicate()[0].rstrip()
    m = pat.findall(p)
    if m[0] in settings.VALID_MIME_TYPES:
        return True
    return False

