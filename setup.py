from setuptools import setup, find_packages
from os.path import join

version = '1.0b5'
readme = open(join('README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

setup(name = 'plone.app.folder',
      version = version,
      description = 'Integration package for `plone.folder` into Plone',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords = 'folder btree order plone archetypes atcontenttypes',
      author = 'Plone Foundation',
      author_email = 'plone-developers@lists.sourceforge.net',
      url = 'http://pypi.python.org/pypi/plone.app.folder/',
      license = 'LGPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['plone', 'plone.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires = [
          'setuptools',
          'plone.folder',
      ],
      tests_require = [
          'zope.testing',
      ],
      entry_points = '',
)
