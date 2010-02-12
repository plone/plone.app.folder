from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.app.folder.folder import IATUnifiedFolder


class NextPrevious(object):
    """ adapter for acting as a next/previous provider """
    implements(INextPreviousProvider)
    adapts(IATUnifiedFolder)

    def __init__(self, context):
        self.context = context
        props = getToolByName(context, 'portal_properties').site_properties
        self.vat = props.getProperty('typesUseViewActionInListings', ())

    @property
    def enabled(self):
        return self.context.getNextPreviousEnabled()

    def getNextItem(self, obj):
        """ return info about the next item in the container """
        pos = self.context.getObjectPosition(obj.getId())
        ordering = self.context.getOrdering()
        try:
            try:                # first try `__getitem__`
                next = ordering[pos + 1]
            except TypeError:
                next = ordering.idsInOrder()[pos + 1]
            return self.getData(self.context[next])
        except IndexError:      # in case next > len(folder)
            return None

    def getPreviousItem(self, obj):
        """ return info about the previous item in the container """
        pos = self.context.getObjectPosition(obj.getId())
        ordering = self.context.getOrdering()
        if pos > 0:
            try:                # first try `__getitem__`
                prev = ordering[pos - 1]
            except TypeError:
                prev = ordering.idsInOrder()[pos - 1]
            return self.getData(self.context[prev])
        return None

    def getData(self, obj):
        """ return the expected mapping, see `INextPreviousProvider` """
        ptype = obj.portal_type
        url = obj.absolute_url()
        if ptype in self.vat:       # "use view action in listings"
            url += '/view'
        return dict(id=obj.getId(), url=url, title=obj.Title(),
            description=obj.Description(), portal_type=ptype)
