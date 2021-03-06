#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from django.http import Http404, HttpResponse
from django.views.generic.base import TemplateResponseMixin

from .callable_queryset import CallableQuerysetMixin
from ...models import Entry

logger = logging.getLogger('online')


class EntryTimeConfMixin(object):
    """
    Mixin centralizing the time configuration of entry.
    """
    date_field = 'create_time'
    month_format = '%m'
    week_format = '%W'


class EntryConfMixin(EntryTimeConfMixin):
    """
    Mixin centralizing the configuration.
    """
    context_object_name = 'entry'
    template_name = 'blog/entry.html'


class EntryVisibleMixin(object):
    """
    Mixin validating the entry's visibility.
    """

    def get_object(self, queryset=None):
        """
        [Override] Validate visibility.
        """
        obj = super(EntryVisibleMixin, self).get_object(queryset)
        if obj.is_visible:
            return obj
        raise Http404('No such entry')


class EntryDetailMixin(EntryConfMixin, EntryVisibleMixin, CallableQuerysetMixin, TemplateResponseMixin):
    """
    Mixin of entry detail.
    """
    queryset = Entry.published.all

    def get_context_data(self, **kwargs):
        """
        [Override] Update context data when rendering.
        """
        context = super(EntryDetailMixin, self).get_context_data(**kwargs)
        # context['entry'] = self.object
        self.request.entry = self.object
        context.update(getattr(self, 'private_context_data', {}))
        return context
