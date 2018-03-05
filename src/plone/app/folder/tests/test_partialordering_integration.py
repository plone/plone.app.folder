# -*- coding: utf-8 -*-
from plone.app.folder.testing import PLONE_APP_FOLDER_AT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.folder.interfaces import IOrderable
from Products.ATContentTypes.content.document import ATDocument
from zope.interface import classImplements

import unittest


class PartialOrderingTests(unittest.TestCase):
    """ tests regarding order-support for only items marked orderable """

    layer = PLONE_APP_FOLDER_AT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])

        self.folder = self.portal[
            self.portal.invokeFactory('Folder', 'folder')
        ]
        classImplements(ATDocument, IOrderable)

    def testGetObjectPositionForNonOrderableContent(self):
        oid = self.folder.invokeFactory('Event', id='foo')
        obj = self.folder._getOb(oid)
        # a non-orderable object should return "no position"
        self.assertFalse(IOrderable.providedBy(obj), 'orderable events?')
        self.assertIsNone(self.folder.getObjectPosition(oid))
        # a non-existant object should raise an error, though
        self.assertRaises(ValueError, self.folder.getObjectPosition, 'bar')

    def testRemoveNonOrderableContent(self):
        self.folder.invokeFactory('Event', id='foo')
        self.folder.manage_delObjects('foo')
        self.assertFalse(self.folder.hasObject('foo'), 'foo?')

    def testCreateOrderableContent(self):
        # create orderable content
        oid = self.folder.invokeFactory('Document', id='foo')
        self.assertEqual(oid, 'foo')
        self.assertTrue(self.folder.hasObject('foo'), 'foo?')
        self.assertEqual(self.folder.getObjectPosition(oid), 0)
        # and some more...
        self.folder.invokeFactory('Document', id='bar')
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.folder.invokeFactory('Event', id='party')
        self.assertEqual(self.folder.getObjectPosition('party'), None)
