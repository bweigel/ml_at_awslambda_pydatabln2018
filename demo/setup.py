#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


setup(
    author="Benjamin Weigel",
    author_email='benjamin.weigel@europace.de',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    description="Demo project to illustrate deployment of ML-models to AWS lambdas",
    install_requires=[],
    license="MIT license",
    include_package_data=True,
    keywords='tutorial',
    name='tutorial',
    packages=find_packages(exclude=['*.test']),
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    version='0.1.0',
    zip_safe=False,
)
