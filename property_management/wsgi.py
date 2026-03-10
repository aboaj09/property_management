"""
WSGI config for property_management project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property_management.settings')

application = get_wsgi_application()

app = application