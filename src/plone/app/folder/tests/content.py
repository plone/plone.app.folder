from zope.interface import implements
from AccessControl import ClassSecurityInfo
from OFS.interfaces import IOrderedContainer
from Products.ATContentTypes.config import PROJECTNAME
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.interfaces import IATFolder
from Products.ATContentTypes.permission import permissions
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.CMFPlone.utils import _createObjectByType
from plone.folder.interfaces import IOrderable
from plone.app.folder.base import BaseBTreeFolder


ATFolderSchema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema
finalizeATCTSchema(ATFolderSchema, folderish=True, moveDiscussion=False)


class OrderableFolder(BaseBTreeFolder):
    """ sample ordered btree-based folder (needing the interface) """
    implements(IOrderable)


class NonBTreeFolder(ATCTOrderedFolder):
    """ an old-style folder much like `ATFolder` before Plone 4;  this is
        a reduced version of `ATContentTypes.content.folder.ATFolder` """
    implements(IATFolder, IOrderedContainer)

    schema = ATFolderSchema
    portal_type = 'NonBTreeFolder'
    archetype_name = 'NonBTreeFolder'
    security = ClassSecurityInfo()


permissions['NonBTreeFolder'] = PROJECTNAME + ': ATFolder'
registerATCT(NonBTreeFolder, PROJECTNAME)


def create(ctype, container, id, *args, **kw):
    """ helper to create old-style folders as their regular type/factory has
        been replaced in plone 4 and isn't available anymore for testing """
    if ctype == 'Folder':
        dispatcher = container.manage_addProduct['ATContentTypes']
        factory = dispatcher.addNonBTreeFolder(id, *args, **kw)
        obj = container._getOb(id)
        obj._setPortalTypeName(ctype)
        return obj
    else:
        return _createObjectByType(ctype, container, id, *args, **kw)
