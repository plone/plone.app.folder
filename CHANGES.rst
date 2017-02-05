Changelog
=========

1.2.2 (2017-02-05)
------------------

Bug fixes:

- Support ZODB5
  [pbauer]


1.2.1 (2016-12-19)
------------------

Fixes:

- Remove unused tests/bbb.py file which is not used by plone.app.folder itself.
  [gforcada]

1.2.0 (2015-10-27)
------------------

Fixes:

- Rerelease 1.1.1 as 1.2.0, because this is for Plone 5.0 and higher.
  [maurits]


1.1.1 (2015-10-27)
------------------

New:

- Use registry lookup for types_use_view_action_in_listings.
  [esteele]

Fixes:

- Fixed test in combination with Products.BTreeFolder2 2.13.4 and
  higher.
  [maurits]


1.1.0 (2015-03-11)
------------------

- Reduced dependencies and declared them explicit.
  Do not depend on ``Products.CMFPlone`` any more.
  Pep8fied et al.
  ATCT is now an extra require.
  Skip Zope2 old style interfaces.
  Stop Plone 3 support in 1.1 series (remove bbb+patches).
  Get rid of old outdated interface fallbacks.
  [jensens]

- Remove profile, since Plone 4+ was no longer used anyway.
  [gforcada]


1.0.6 (2014-01-27)
------------------

- Fix test for Plone 4, so we really only apply the reindexOnReorder
  patch when we are on Plone 3.
  [maurits]


1.0.5 (2013-01-13)
------------------

- Only set up the folder content type if Archetypes is present.
  [davisagli]

1.0.4 - 2011-01-03
------------------

- Depend on ``Products.CMFPlone`` instead of ``Plone``.
  [elro]


1.0.3 - 2010-11-06
------------------

- Next/previous folder adapter should not return non-contentish objects,
  such as local workflow policies as example.
  This fixes http://dev.plone.org/plone/ticket/11234.
  [thomasdesvenain]


1.0.2 - 2010-08-08
------------------

- Adjust tests to work with Zope 2.13 and avoid deprecation warnings.
  [hannosch]

- Show the next **viewable** item in next/previous
  viewlet/link, as the behaviour was in Plone 3.
  This fixes http://dev.plone.org/plone/ticket/10309.
  [mr_savage]


1.0.1 - 2010-07-18
------------------

- Update license to GPL version 2 only.
  [hannosch]


1.0 - 2010-07-07
----------------

- Moved migration logic into the BTreeMigrationView to allow subclasses to
  override part of the logic.
  [hannosch]

- Remove the overly noisy migration report per folder.
  [hannosch]


1.0b7 - 2010-06-03
------------------

- Updated tests to not rely on the existence of the Large Plone Folder type,
  which was removed for Plone 4.
  [davisagli]


1.0b6 - 2010-05-02
------------------

- Nogopip vs. Acquisition take two - not all folders have a getOrdering
  method, so we need to avoid acquiring it.
  [hannosch]


1.0b5 - 2010-04-06
------------------

- Match ``getObjectPositionInParent`` behavior and handle unordered folders
  inside ordered folders shown in the navigation tree at the same time.
  [hannosch]


1.0b4 - 2010-03-06
------------------

- Don't try to store an acquisition-wrapped catalog on the positional index.
  [hannosch]


1.0b3 - 2010-02-18
------------------

- Only apply monkey patch for `reindexOnReorder` on Plone 3.x & shortcut
  indexing completely if the fake index has been installed.
  [witsch]

- Replace monkey patch for `Catalog._getSortIndex` with a fake index that
  can sort search results according to their position in the container.
  [witsch]

- Add optimization for sorting results by folder position for the usual
  "all results in one folder" case.
  [witsch]

- Add adapter for previous/next support that doesn't need the catalog.
  [witsch]

- Remove `getObjPositionInParent` catalog index and use a sort index based
  on the folder's order information instead.
  [witsch]


1.0b2 - 2010-01-28
------------------

- Add `IATBTreeFolder` to `implements` list of `ATFolder` replacement.
  [thet]


1.0b1 - 2009-11-15
------------------

- Copy the `index_html` method from `ATContentTypes` to better support WebDAV.
  [davisagli]

- Add in-place migration code.
  [witsch]

- Work around imports no longer present in Plone 4.0.
  [witsch]

- Briefly document the `plone.app.folder.tests.bbb` usage.
  [wichert]


1.0a1 - 2009-05-07
------------------

- Initial release as factored out from `plone.folder`.
  [witsch]
