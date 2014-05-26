#!/usr/bin/env python
import sys,os
sys.path.append('/your/django/project/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from your_app.models import *
print your_table.objects.all()
