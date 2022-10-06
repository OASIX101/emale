"""
ASGI config for home_vote project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from django.core.asgi import get_asgi_application

configuration = os.getenv('ENVIRONMENT').lower()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'home_vote.settings.{configuration}')
application = get_asgi_application()
