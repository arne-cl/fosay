# -*- coding: utf-8 -*-
__author__="zoltan kochan"
__date__ ="$3 apr 2011 1:25:43$"

from setuptools import setup,find_packages

setup (
  name = 'fosay',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  #install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'Zoltan Kochan',
  author_email = 'ZoltanKochan@gmail.com',

  summary = 'An Interlingual Machine Translator',
  url = 'http://code.google.com/p/fosay/',
  license = 'GNU GPL v3',
  long_description=
        '''Fosay is an interlingual machine translator written in Python.
        Fosay allows adding new languages by simply describing their grammar
        with ATNL (Augmented Transition Network Language) and their dictionary
        with CWS (Cascading Word Sheets).''',

  # could also include long_description, download_url, classifiers, etc.


)