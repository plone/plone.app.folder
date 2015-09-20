# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.utils import getToolByName
from plone.app.folder.folder import IATUnifiedFolder
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.registry.interfaces import IRegistry
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer


@implementer(INextPreviousProvider)
@adapter(IATUnifiedFolder)
class NextPrevious(object):
    """ adapter for acting as a next/previous provider """

    def __init__(self, context):
        self.context = context
        registry = getUtility(IRegistry)
        self.vat = registry.get('plone.types_use_view_action_in_listings', [])
        self.security = getSecurityManager()
        order = context.getOrdering()
        if not isinstance(order, list):
            order = order.idsInOrder()
        if not isinstance(order, list):
            order = None
        self.order = order

    @property
    def enabled(self):
        return self.context.getNextPreviousEnabled()

    def getNextItem(self, obj):
        """ return info about the next item in the container """
        if not self.order:
            return None
        pos = self.context.getObjectPosition(obj.getId())
        for oid in self.order[pos+1:]:
            data = self.getData(self.context[oid])
            if data:
                return data

    def getPreviousItem(self, obj):
        """ return info about the previous item in the container """
        if not self.order:
            return None
        order_reversed = list(reversed(self.order))
        pos = order_reversed.index(obj.getId())
        for oid in order_reversed[pos+1:]:
            data = self.getData(self.context[oid])
            if data:
                return data

    def getData(self, obj):
        """ return the expected mapping, see `INextPreviousProvider` """
        if not self.security.checkPermission('View', obj):
            return None
        elif not IContentish.providedBy(obj):
            # do not return a not contentish object
            # such as a local workflow policy for example (#11234)
            return None

        ptype = obj.portal_type
        url = obj.absolute_url()
        if ptype in self.vat:       # "use view action in listings"
            url += '/view'
        return dict(
            id=obj.getId(),
            url=url,
            title=obj.Title(),
            description=obj.Description(),
            portal_type=ptype
        )
