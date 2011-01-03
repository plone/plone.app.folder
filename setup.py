from setuptools import setup, find_packages

version = '1.0.5'

readme = open('README.txt').read()
history = open('CHANGES.txt').read()

setup(name = 'plone.app.folder',
      version = version,
      description = 'Integration package for `plone.folder` into Plone',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Other Audience',
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='folder btree order plone archetypes atcontenttypes',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.folder/',
      license='GPL version 2',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['plone', 'plone.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires = [
          'Products.CMFPlone',
          'setuptools',
          'plone.folder',
      ],
)
