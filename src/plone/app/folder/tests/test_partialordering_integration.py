# -*- coding: utf-8 -*-
from Products.ATContentTypes.content.document import ATDocument
from plone.app.folder.tests.base import IntegrationTestCase
from plone.app.folder.tests.layer import PartialOrderingIntegrationLayer
from plone.folder.interfaces import IOrderable
from zope.interface import classImplements


class PartialOrderingTests(IntegrationTestCase):
    """ tests regarding order-support for only items marked orderable """

    layer = PartialOrderingIntegrationLayer

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.folder = self.portal[
            self.portal.invokeFactory('Folder', 'folder')
        ]
        classImplements(ATDocument, IOrderable)

    def testGetObjectPositionForNonOrderableContent(self):
        oid = self.folder.invokeFactory('Event', id='foo')
        obj = self.folder._getOb(oid)
        # a non-orderable object should return "no position"
        self.assertFalse(IOrderable.providedBy(obj), 'orderable events?')
        self.assertEqual(self.folder.getObjectPosition(oid), None)
        # a non-existant object should raise an error, though
        self.assertRaises(ValueError, self.folder.getObjectPosition, 'bar')

    def testRemoveNonOrderableContent(self):
        self.setRoles(['Manager'])
        self.folder.invokeFactory('Event', id='foo')
        self.folder.manage_delObjects('foo')
        self.assertFalse(self.folder.hasObject('foo'), 'foo?')

    def testCreateOrderableContent(self):
        self.setRoles(['Manager'])
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
