"""
WSGI config for core_settings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["LOCATION"] = "home/tony221b/inventory_management"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_settings.settings")

application = get_wsgi_application()
