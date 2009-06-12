plone.app.folder
================

Overview
--------

This package provides base classes for folderish `Archetypes`_ /
`ATContentTypes`_ content types based on `B-trees`_, a.k.a. "large folders"
in Plone_.  Storing content in such folders provides significant
`performance benefits`_ over regular folders.

  .. _`Archetypes`: http://pypi.python.org/pypi/Products.Archetypes/
  .. _`ATContentTypes`: http://pypi.python.org/pypi/Products.ATContentTypes/
  .. _`B-trees`: http://en.wikipedia.org/wiki/B-tree
  .. _`Plone`: http://plone.org/
  .. _`performance benefits`: http://plone.org/products/plone/roadmap/191

The package only contains the integration layer for the base class provided
by `plone.folder`_, however.  Please see there for more detailed information.

  .. _`plone.folder`: http://pypi.python.org/pypi/plone.folder/

Caveats
-------

If you are using `plone.app.folder` in your product you may notice that
PloneTestCase will fail to setup a Plone site for your functional tests.
This can be resolved by adding this line to your functional test source::

    from plone.app.folder.tests import bbb


