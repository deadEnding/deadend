#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from django.http import HttpResponse
from django.views.generic.dates import BaseDateDetailView

from lib.exceptions import InvalidRequestParamException, OperationTooFrequentException
from .mixins.entries import EntryDetailMixin
from .mixins.response import JSONResponseMixin
from ..utils import category_ancestors, entry_tags
from ..caches import EntryCounterCache, EntryActorIpCache
from ..breadcrumbs import Link
from ..settings import PTN_BLOG_ENTRY_FEEDBACK

logger = logging.getLogger('file')


class EntryDetail(EntryDetailMixin, BaseDateDetailView, JSONResponseMixin):
    """
    Entry detail view.
    TODO: entry login and password protections.
    """
    # session_key = 'entry_passwd_%s'

    @property
    def private_context_data(self):
        """
        Private context data: title, breadcrumbs, direct subdirectories.
        """
        ttl = self.object.title
        breadcrumbs = category_ancestors(self.object.category, disable_last_url=False)
        breadcrumbs.append(Link(self.object.title))
        return {'ttl': ttl, 'breadcrumbs': breadcrumbs, 'labels': entry_tags(self.object)}

    def post(self, request, *args, **kwargs):
        """
        Deal with feedback(useful or userless) of the entry.
        """
        try:
            type = int(request.POST.get('type', 1))
            if type not in [-1, 1]:
                raise InvalidRequestParamException('Param "type" is invalid, type="%s"' % str(type))

            entry = self.get_object()
            entry_actor = EntryActorIpCache(entry, PTN_BLOG_ENTRY_FEEDBACK)
            ip = request.META.get('REMOTE_ADDR', '')
            if not entry_actor.exists(ip):
                entry_counter = EntryCounterCache(entry)
                ctype = 'useful_num' if type == 1 else 'useless_num'
                entry_counter.incr(ctype)
                entry_actor.add(ip)
                status_json = {'status': 0, 'msg': 'success'}
            else:
                raise OperationTooFrequentException('Operation is too frequent')
        except Exception, e:
            if isinstance(e, InvalidRequestParamException):
                status_json = {'status': 3, 'msg': u'操作太频繁~'}
            else:
                status_json = {'status': 3, 'msg': u'已经反馈过~'}
            logger.error('[%s] deal with feedback except, err: %s' % (request.view_name, str(e)))
        finally:
            return self.response([status_json])


    # def get(self, request, *args, **kwargs):
    #     """
    #     Validate permission.
    #     """
    #     # if self.object.login_required and not request.user.is_authenticated():
    #     #     pass
    #     if self.object.password and self.object.password != \
    #         self.request.session.get(self.session_key % self.object):
    #         return render_to_response('', {})

    #     response = super(self.__class__, self).get(request, *args, **kwargs)
