from logging import getLogger
from inspect import currentframe
from Acquisition import aq_parent


logger = getLogger(__name__)


class GopipIndex(object):
    """ fake index for sorting against `getObjPositionInParent` """

    keyForDocument = 42

    def __init__(self, catalog):
        self.catalog = catalog

    def __len__(self):
        # with python 2.4 returning `sys.maxint` gives:
        # OverflowError: __len__() should return 0 <= outcome < 2**31
        # so...
        return 2**31 - 1

    def documentToKeyMap(self):
        # we need to get the containers in order to get the respective
        # positions of the search results, but before that we need those
        # results themselves.  luckily this is only ever called from
        # `sortResults`, so we can get it form there.  oh, and lurker
        # says this won't work in jython, though! :)
        rs = currentframe(1).f_locals['rs']
        pos = {}
        containers = {}
        getpath = self.catalog.paths.get
        traverse = aq_parent(self.catalog).unrestrictedTraverse
        for rid in rs:
            path = getpath(rid)
            parent, id = path.rsplit('/', 1)
            container = containers.get(parent, None)
            if container is None:
                container = containers[parent] = traverse(parent)
            pos[rid] = container.getObjectPosition(id)
        return pos


def _getSortIndex(self, args):
    """ returns the special fake index for "gopip" or a real one """
    sort_index_name = self._get_sort_attr('on', args)
    if sort_index_name == 'getObjPositionInParent':
        return GopipIndex(catalog=self)
    return self.__nogopip_old_getSortIndex(args)


def reindexOnReorder(self, parent):
    """ reindexing of "gopip" isn't needed any longer :) """
    pass


def applyPatches():
    from Products.ZCatalog.Catalog import Catalog
    Catalog.__nogopip_old_getSortIndex = Catalog._getSortIndex
    Catalog._getSortIndex = _getSortIndex
    from Products.CMFPlone.PloneTool import PloneTool
    PloneTool.reindexOnReorder = reindexOnReorder
