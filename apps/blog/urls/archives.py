#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from ..views.archives import EntryIndex, EntryYear, EntryMonth

urlpatterns = [
    # Index archive
    url(r'^page/(?P<page>\d+)/$',
        EntryIndex.as_view(),
        name='index_paginated'),
    url(r'^$', EntryIndex.as_view(), name='index'),

    # Year archives
    url(r'^(?P<year>\d{4})/page/(?P<page>\d+)/$',
        EntryYear.as_view(),
        name='year_paginated'),
    url(r'^(?P<year>\d{4})/$', EntryYear.as_view(), name='year'),

    # Month archives
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d+)/$',
        EntryMonth.as_view(),
        name='month_paginated'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', EntryMonth.as_view(), name='month'),
]
