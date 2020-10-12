from setuptools import setup, find_packages

version = '1.3.2'

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

setup(
    name='plone.app.folder',
    version=version,
    description='Integration package for `plone.folder` into Plone',
    long_description=readme[readme.find('\n\n'):] + '\n' + history,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.2',
        'Framework :: Zope2',
        'Framework :: Zope :: 4',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='folder btree order plone archetypes atcontenttypes',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/plone.app.folder/',
    license='GPL version 2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    platforms='Any',
    zip_safe=False,
    install_requires=[
        'Products.CMFCore',
        'Products.GenericSetup',
        'Zope2',
        'plone.folder',
        'setuptools',
        'six',
        'plone.app.layout',
    ],
    extras_require={
        'atct': [
            'Products.ATContentTypes',
            'Products.Archetypes',
            'Products.BTreeFolder2',
        ],
        'test': [
            'plone.app.testing',
        ],
    },
)
