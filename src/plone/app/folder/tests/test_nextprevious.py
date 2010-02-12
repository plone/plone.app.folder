from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.app.folder.tests.base import IntegrationTestCase
from plone.app.folder.tests.layer import IntegrationLayer


class NextPreviousSupportTests(IntegrationTestCase):
    """ basic use cases and tests for next/previous navigation, essentially
        borrowed from `Products.CMFPlone.tests.testNextPrevious.py` """

    layer = IntegrationLayer

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        self.portal.invokeFactory('Document', 'doc2')
        self.portal.invokeFactory('Document', 'doc3')
        self.portal.invokeFactory('Folder', 'folder1')
        self.portal.invokeFactory('Link', 'link1')
        self.portal.link1.setRemoteUrl('http://plone.org')
        self.portal.link1.reindexObject()
        folder1 = getattr(self.portal, 'folder1')
        folder1.invokeFactory('Document', 'doc11')
        folder1.invokeFactory('Document', 'doc12')
        folder1.invokeFactory('Document', 'doc13')
        self.portal.invokeFactory('Folder', 'folder2')
        folder2 = getattr(self.portal, 'folder2')
        folder2.invokeFactory('Document', 'doc21')
        folder2.invokeFactory('Document', 'doc22')
        folder2.invokeFactory('Document', 'doc23')
        folder2.invokeFactory('File', 'file21')
        self.setRoles(['Member'])

    def testIfFolderImplementsPreviousNext(self):
        self.folder.invokeFactory('Folder', 'case')
        self.failUnless(INextPreviousProvider(self.folder.case, None))

    def testNextPreviousEnablingOnCreation(self):
        self.folder.invokeFactory('Folder', 'case')
        # first ensure the field on the atfolder is there
        self.failIf(self.folder.case.getNextPreviousEnabled())
        # then check if the adapter provides the attribute
        self.failIf(INextPreviousProvider(self.folder.case).enabled)

    def testNextPreviousViewDisabled(self):
        doc = self.portal.folder1.doc11
        view = doc.restrictedTraverse('@@plone_nextprevious_view')
        self.failIf(view is None)
        self.failIf(view.enabled())

    def testNextPreviousViewEnabled(self):
        self.portal.folder1.setNextPreviousEnabled(True)
        doc = self.portal.folder1.doc11
        view = doc.restrictedTraverse('@@plone_nextprevious_view')
        self.failIf(view is None)
        self.failUnless(view.enabled())

    def testAdapterOnPortal(self):
        doc = self.portal.doc1
        view = doc.restrictedTraverse('@@plone_nextprevious_view')
        self.failUnless(view)
        self.failIf(view.enabled())
        self.assertEqual(None, view.next())
        self.assertEqual(None, view.previous())

    def testNextPreviousItems(self):
        container = self.folder[self.folder.invokeFactory('Folder', 'case3')]
        for id in range(1, 6):
            container.invokeFactory('Document', 'subDoc%d' % id)
        adapter = INextPreviousProvider(container)
        # text data for next/previous items
        next = adapter.getNextItem(container.subDoc2)
        self.assertEqual(next['id'], 'subDoc3')
        self.assertEqual(next['portal_type'], 'Document')
        self.assertEqual(next['url'], container.subDoc3.absolute_url())
        previous = adapter.getPreviousItem(container.subDoc2)
        self.assertEqual(previous['id'], 'subDoc1')
        self.assertEqual(previous['portal_type'], 'Document')
        self.assertEqual(previous['url'], container.subDoc1.absolute_url())
        # first item should not have a previous item
        previous = adapter.getPreviousItem(container.subDoc1)
        self.assertEqual(previous, None)
        # last item should not have a next item
        next = adapter.getNextItem(container.subDoc5)
        self.assertEqual(next, None)


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
