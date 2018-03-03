# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from plone.app.folder.utils import findObjects
from plone.app.folder.testing import PLONE_APP_FOLDER_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UtilsTests(unittest.TestCase):

    layer = PLONE_APP_FOLDER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        self.portal.manage_addFolder(id='root', title='Root')
        self.portal.root.manage_addFolder(id='foo', title='Foo')
        self.portal.root.foo.manage_addFolder(id='bar', title='Bar')
        self.portal.root.foo.bar.manage_addDocument(id='doc1', title='a document')
        self.portal.root.foo.bar.manage_addDocument(id='file1', title='a file')
        self.portal.root.manage_addFolder(id='bar', title='Bar')
        self.portal.root.bar.manage_addFolder(id='foo', title='Foo')
        self.portal.root.bar.foo.manage_addDocument(id='doc2', title='a document')
        self.portal.root.bar.foo.manage_addDocument(id='file2', title='a file')
        self.good = (
            'bar', 'bar/foo', 'bar/foo/doc2', 'bar/foo/file2',
            'foo', 'foo/bar', 'foo/bar/doc1', 'foo/bar/file1'
        )

    def ids(self, results):
        return tuple(sorted([r[0] for r in results]))

    def testZopeFindAndApply(self):
        found = self.portal.root.ZopeFindAndApply(self.portal.root, search_sub=True)
        self.assertEqual(self.ids(found), self.good)

    def testFindObjects(self):
        found = list(findObjects(self.portal.root))
        # the starting point itself is returned
        self.assertEqual(found[0], ('', self.portal.root))
        # but the rest should be the same...
        self.assertEqual(self.ids(found[1:]), self.good)
