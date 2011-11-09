from django.core.management.base import BaseCommand, CommandError
from site_main.models import School
import sys

class Command(BaseCommand):
    args = '<filename>'
    help = 'Imports a list of schools from the specified tab-separated text file'

    def handle(self, *args, **options):
        try:
            f = open(args[0], 'r')
            for line in f:
                l = line.rstrip().split('\t')
                s = School(name=l[0], short_name=l[1])
                s.save()
                self.stdout.write("%s (%s)\n" % (l[0], l[1]))
        except:
            print sys.exc_info()[1]
