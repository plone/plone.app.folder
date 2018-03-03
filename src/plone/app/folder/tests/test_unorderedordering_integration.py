# -*- coding: utf-8 -*-
from plone.app.folder.testing import PLONE_APP_FOLDER_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UnorderedOrderingTests(unittest.TestCase):
    """ tests regarding order-support for folders with unordered ordering """

    layer = PLONE_APP_FOLDER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])

    def create(self):
        container = self.portal[self.portal.invokeFactory('Folder', 'foo')]
        container.setOrdering('unordered')
        container.invokeFactory('Document', id='o1')
        container.invokeFactory('Document', id='o2')
        return container

    def testNotifyAdded(self):
        container = self.create()
        self.assertEqual(set(container.objectIds()), set(['o1', 'o2']))
        container.invokeFactory('Document', id='o3')
        self.assertEqual(set(container.objectIds()), set(['o1', 'o2', 'o3']))

    def testNotifyRemoved(self):
        container = self.create()
        self.assertEqual(set(container.objectIds()), set(['o1', 'o2']))
        container.manage_delObjects('o2')
        self.assertEqual(set(container.objectIds()), set(['o1']))

    def testGetObjectPosition(self):
        container = self.create()
        self.assertEqual(container.getObjectPosition('o1'), None)
        self.assertEqual(container.getObjectPosition('o2'), None)

