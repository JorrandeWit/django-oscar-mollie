#!/usr/bin/env python
from setuptools import setup

setup(name='django-oscar-mollie',
      version='0.1',
      url='https://github.com/JorrandeWit/django-oscar-mollie',
      author="Jorran de Wit",
      author_email="jorrandewit@outlook.com",
      description="Mollie payment module for django-oscar",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4'],
      keywords="Payment, Mollie, iDeal",
      license='BSD',
      packages=[
        'mollie_oscar'
      ],
      install_requires=['mollie-api-python'])
