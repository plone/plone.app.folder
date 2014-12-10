# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing.bbb import PTC_FUNCTIONAL_TESTING
from Testing.ZopeTestCase import app
from Testing.ZopeTestCase import close
from Testing.ZopeTestCase import installPackage
from plone.folder.partial import PartialOrdering
from transaction import commit
from zope.component import provideAdapter

# BBB Zope 2.12
try:
    from Zope2.App.zcml import load_config
    load_config  # pyflakes
    from OFS import metaconfigure
    metaconfigure  # pyflakes
except ImportError:
    from Products.Five.zcml import load_config
    from Products.Five import fiveconfigure as metaconfigure


class IntegrationLayer(PloneSandboxLayer):
    """ layer for integration tests using the folder replacement type """

    defaultBases = (PTC_FUNCTIONAL_TESTING,)

    def setUpZope(self, app, configurationContext):
        from plone.app.folder import tests
        self.loadZCML('testing.zcml', tests)
        z2.installProduct(app, 'plone.app.blob')


    def setUpPloneSite(self, portal):
        # restore default workflow
        applyProfile(portal, 'profile-plone.app.folder:default')

        types = getToolByName(portal, 'portal_types')
        assert types.getTypeInfo('Folder').product == 'plone.app.folder'


class PartialOrderingIntegrationLayer(IntegrationLayer):
    """ layer for integration tests using the partial ordering adapter """

    def setUpZope(self, app, configurationContext):
        IntegrationLayer.setUpZope(self, app, configurationContext)
        provideAdapter(PartialOrdering)
