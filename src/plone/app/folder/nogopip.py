# -*- coding: utf-8 -*-
from zope.deferredimport import deprecated


deprecated(
    "Please import from plone.folder.nogopip",
    GopipIndex='plone.folder.nogopip:GopipIndex',
    manage_addGopipForm='plone.folder.nogopip:manage_addGopipForm',
    manage_addGopipIndex='plone.folder.nogopip:manage_addGopipIndex',
)