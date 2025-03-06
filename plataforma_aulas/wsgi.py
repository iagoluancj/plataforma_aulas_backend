"""
WSGI config for plataforma_aulas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma_aulas.settings')

try:
    from plataforma_aulas.seed import seed_database
    seed_database()
except Exception as e:
    print(f"Erro ao popular o banco: {e}")

application = get_wsgi_application()
