import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_booking.settings')

application = get_wsgi_application()

import django
from django.conf import settings

staticfiles_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
if not os.path.exists(staticfiles_dir):
    from django.core.management import call_command
    call_command('collectstatic', '--noinput', verbosity=0)

app = application