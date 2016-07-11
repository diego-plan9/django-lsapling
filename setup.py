#!/usr/bin/env python
from lsapling import __version__
from setuptools import setup, find_packages


setup(
    name='django-lsapling',
    description='''Utilities for working with tree structures in Django
        via the ltree postgresql extension.''',
    version=__version__,
    author='Diego M. Rodríguez',
    author_email='diego.plan9@gmail.com',
    url='https://github.com/diego-plan9/django-lsapling',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
        str('Development Status :: 4 - Beta'),
        str('Environment :: Web Environment'),
        str('Framework :: Django'),
        str('Intended Audience :: Developers'),
        str('License :: OSI Approved :: MIT License'),
        str('Operating System :: OS Independent'),
        str('Programming Language :: Python'),
        str("Programming Language :: Python :: 2.7"),
        str('Topic :: Utilities'),
    ],
    install_requires=[
        'Django>=1.8'
    ],
)
