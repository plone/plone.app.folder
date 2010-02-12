from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.app.folder.tests.base import IntegrationTestCase
from plone.app.folder.tests.layer import IntegrationLayer


class TestNextPrevious(IntegrationTestCase):
    """ basic use cases and tests for next/previous navigation, essentially
        borrowed from `Products.CMFPlone.tests.testNextPrevious.py` """

    layer = IntegrationLayer

    def afterSetUp(self):
        self.populateSite()

    #set up a lot of content - can be reused in each (sub)test
    def populateSite(self):
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
        self.failUnless(INextPreviousProvider(self.folder.case, None) is not None)

    def testNextPreviousEnablingOnCreation(self):
        self.folder.invokeFactory('Folder', 'case')
        
        #first the field on the atfolder direct, to get sure the field is there
        enabled = self.folder.case.getNextPreviousEnabled()
        self.failIf(enabled)
        
        #secoundly we test if the adapter provides the isNextPreviousEnabled()
        adapter = INextPreviousProvider(self.folder.case)
        self.failIf(adapter.enabled)

    def testNextPreviousViewDisabled(self):
        view = self.portal.folder1.doc11.restrictedTraverse('@@plone_nextprevious_view', None)
        self.failIf(view is None)
        
        #is it enabled (default is false)
        self.failIf(view.enabled())

    def testNextPreviousViewEnabled(self):
        #set the parent folder "getNextPreviousEnabled" to true
        self.portal.folder1.setNextPreviousEnabled(True)
        
        # clear request memos
        view = self.portal.folder1.doc12.restrictedTraverse('@@plone_nextprevious_view', None)
        self.failUnless(view.enabled())

        # test the next method
        next = view.next()
        self.assertEquals(next['url'], self.portal.folder1.doc13.absolute_url())
        
        # test the previous method
        previous = view.previous()
        self.assertEquals(previous['url'], self.portal.folder1.doc11.absolute_url())

    def testAdapterOnPortal(self):
        view = self.portal.doc1.restrictedTraverse('@@plone_nextprevious_view', None)
        self.failUnless(view)
        self.failIf(view.enabled())
        self.assertEquals(None, view.next())
        self.assertEquals(None, view.previous())

    def testNextPreviousItems(self):
        self.folder.invokeFactory('Folder', 'case3')
        
        for documentCounter in range(1, 6):
            self.folder.case3.invokeFactory('Document', 'subDoc%d' % documentCounter)
    
        container  = self.folder.case3
        testedItem = container.subDoc2
        
        #set up the adapter for the folder
        adapter = INextPreviousProvider(container)

        #test the next item of subDoc2
        next = adapter.getNextItem(self.folder.case3.subDoc2)
        self.failUnlessEqual(next["id"], 'subDoc3')

        #test that the contenttype is defined correct
        self.failUnlessEqual(next["portal_type"], 'Document')
        
        #test the previous item of subDoc2
        previous = adapter.getPreviousItem(self.folder.case3.subDoc2)
        self.failUnlessEqual(previous["id"], 'subDoc1')
        
        #first item should not have a previous item
        previous = adapter.getPreviousItem(self.folder.case3.subDoc1)
        self.failUnlessEqual(previous, None)

        #last item should not have a next item
        next = adapter.getNextItem(self.folder.case3.subDoc5)
        self.failUnlessEqual(next, None)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNextPrevious))
    return suite
