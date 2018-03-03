# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting

import doctest


class PloneAppFolderLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import plone.app.folder
        self.loadZCML(package=plone.app.folder)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')


PLONE_APP_FOLDER_FIXTURE = PloneAppFolderLayer()

PLONE_APP_FOLDER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_FOLDER_FIXTURE, ),
    name='PloneAppFolderLayer:Integration',
)

PLONE_APP_FOLDER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_FOLDER_FIXTURE, ),
    name='PloneAppFolderLayer:Functional',
)

optionflags = (
    doctest.REPORT_ONLY_FIRST_FAILURE
    | doctest.ELLIPSIS
    | doctest.NORMALIZE_WHITESPACE
)
