#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from codecs import open

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='Appengine-Fixture-Loader',
    version='0.1.9',
    description='Appengine fixture loader',
    long_description=readme + '\n\n' + history,
    author='Ricardo Bánffy',
    author_email='appengine-fixture-loader@autonomic.com.br',
    url='http://github.com/rbanffy/appengine-fixture-loader/',
    packages=[
        'appengine_fixture_loader',
    ],
    package_dir={'appengine_fixture_loader':
                 'appengine_fixture_loader'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache",
    zip_safe=False,
    keywords=['appengine', 'loader', 'fixture'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
