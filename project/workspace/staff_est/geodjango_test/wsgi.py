"""
WSGI config for geodjango_test project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

#sys.path.append('/home/lautaro/venvs/geodjango-app/lib/python2.7/site-packages')
#sys.path.append('/var/www/html/django-apps/geodjango_test')

sys.path.append('/home/centos/project/workspace/lib/python2.7/site-packages/')
sys.path.append('/home/centos/project/workspace/staff_est')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geodjango_test.settings-deploy")

application = get_wsgi_application()
