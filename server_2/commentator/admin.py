# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from commentator.models import *
# Register your models here.
admin.site.register(Commentator)
admin.site.register(Commentary)
