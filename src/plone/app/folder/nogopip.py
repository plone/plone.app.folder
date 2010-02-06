from os import environ
from sys import maxint
from inspect import currentframe
from Globals import DevelopmentMode
from Acquisition import aq_parent


paranoid = DevelopmentMode or 'ZOPETESTCASE' in environ


class GopipIndex(object):
    """ fake index for sorting against `getObjPositionInParent` """

    keyForDocument = 42

    def __init__(self, catalog):
        self.catalog = catalog

    def __len__(self):
        return maxint

    def documentToKeyMap(self):
        # we need to figure out the container in order to get
        # the order of its objects;  luckily this is only ever
        # called from `sortResults`, so we can get it form there
        # lurker says this won't work in jython, though! :)
        rs = currentframe(1).f_locals['rs']
        if not rs:
            return {}
        rids = iter(rs)
        first = rids.next()         # first rid in result set
        path = self.catalog.paths[first]
        path = path[:path.rindex('/')]
        traverse = aq_parent(self.catalog).unrestrictedTraverse
        container = traverse(path)

        # make sure the path is the same for all results, but only
        # in debug-mode or during test runs...
        if paranoid:
            for rid in rids:
                p = self.catalog.paths[rid]
                assert path == p[:p.rindex('/')]

        pos = {}
        getrid = self.catalog.uids.get
        if hasattr(container, 'idsInOrder'):
            ids = container.idsInOrder
        else:
            ids = container.objectIds
        for idx, id in enumerate(ids()):
            rid = getrid(path + '/' + id)
            if rid is not None and rid in rs:
                pos[rid] = idx
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
