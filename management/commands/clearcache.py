from django.core.management.base import BaseCommand
from django.core.cache import cache

# http://stackoverflow.com/questions/5942759/best-place-to-clear-cache-when-restarting-django-server
class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        cache.clear()
        self.stdout.write('Cache cleared!\n')