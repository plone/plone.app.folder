from unittest import defaultTestLoader
from plone.app.folder.tests.base import IntegrationTestCase
from plone.app.folder.tests.layer import IntegrationLayer


class FolderReplacementTests(IntegrationTestCase):

    layer = IntegrationLayer

    def afterSetUp(self):
        self.setRoles(['Manager'])

    def testCreateFolder(self):
        self.folder.invokeFactory('Folder', 'foo')
        self.failUnless(self.folder['foo'])
        self.assertEqual(self.folder['foo'].getPortalTypeName(), 'Folder')
        from plone.app.folder.base import BaseBTreeFolder
        self.failUnless(isinstance(self.folder['foo'], BaseBTreeFolder))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
