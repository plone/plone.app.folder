# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from plone.folder.partial import PartialOrdering
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
from zope.component import provideAdapter

import doctest


class PloneAppFolderLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import plone.app.folder
        self.loadZCML(package=plone.app.folder)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')
#
#        acl_users = getToolByName(portal, 'acl_users')
#
#        acl_users.userFolderAddUser('manager', 'secret', ['Manager', ], [])


class PloneAppFolderATLayer(PloneAppFolderLayer):

    def setUpZope(self, app, configurationContext):
        super(PloneAppFolderATLayer, self).setUpZope(app, configurationContext)
        import Products.ATContentTypes
        self.loadZCML(package=Products.ATContentTypes)
        z2.installProduct(app, 'Products.ATContentTypes')
        provideAdapter(PartialOrdering)

    def setUpPloneSite(self, portal):
        super(PloneAppFolderATLayer, self).setUpPloneSite(portal)
        self.applyProfile(portal, 'Products.ATContentTypes:default')


PLONE_APP_FOLDER_FIXTURE = PloneAppFolderLayer()

PLONE_APP_FOLDER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_FOLDER_FIXTURE, ),
    name='PloneAppFolderLayer:Integration',
)

PLONE_APP_FOLDER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_FOLDER_FIXTURE, ),
    name='PloneAppFolderLayer:Functional',
)

PLONE_APP_FOLDER_AT_FIXTURE = PloneAppFolderATLayer()

PLONE_APP_FOLDER_AT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_FOLDER_AT_FIXTURE, ),
    name='PloneAppFolderATLayer:Integration',
)

PLONE_APP_FOLDER_AT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_FOLDER_AT_FIXTURE, ),
    name='PloneAppFolderATLayer:Functional',
)

optionflags = (
    doctest.REPORT_ONLY_FIRST_FAILURE
    | doctest.ELLIPSIS
    | doctest.NORMALIZE_WHITESPACE
)
