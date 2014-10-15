from codecs import open
from setuptools import setup

setup(
    name='Appengine-Fixture-Loader',
    version='0.1',
    url='http://github.com/rbanffy/appengine-fixture-loader/',
    license='Apache',
    author='Ricardo Bánffy',
    author_email='appengine-fixture-loader@autonomic.com.br',
    description='Appengine fixture loader',
    long_description=open('README.md', 'r', 'utf8').read(),
    keywords=['appengine', 'loader', 'fixture'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=[
        'appengine_fixture_loader',
    ],
    package_data={},
    install_requires=[],
    extras_require={}
)
