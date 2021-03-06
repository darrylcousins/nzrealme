#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'M2Crypto==0.22.3',
    'dm.xmlsec.binding==1.3.1',
    'isodate==0.5.0',
    'defusedxml==0.4.1',
    'python-saml',
]

test_requirements = [
    'pytest',
    'flake8',
    'sphinx'
]

setup(
    name='nzrealme',
    version='0.1.0',
    description='NZ RealMe python package',
    long_description=readme + '\n\n' + history,
    author='Darryl Cousins',
    author_email='darryljcousins@gmail.com',
    url='https://github.com/darrylcousins/nzrealme',
    packages=[
        'nzrealme',
    ],
    package_dir={'nzrealme':
                 'nzrealme'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    keywords='saml saml2 xmlsec realme nzrealme',
)
