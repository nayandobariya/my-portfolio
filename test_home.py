import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from portfolio.views import home
from django.test import RequestFactory

rf = RequestFactory()
request = rf.get('/')
try:
    response = home(request)
    print('OK')
except Exception as e:
    print(e)
