# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(Recipe)
admin.site.register(Picture)
admin.site.register(Tag)

# Register your models here.
