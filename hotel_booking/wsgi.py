import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_booking.settings')

from django.conf import settings
if not os.path.exists(os.path.join(settings.BASE_DIR, 'staticfiles')):
    from django.core.management import call_command
    call_command('collectstatic', '--noinput')

app = get_wsgi_application()
application = app