#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Author, Category, Entry, Image, Site

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Entry)
admin.site.register(Image)
admin.site.register(Site)
