# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 16:19:07 2015

@author: carolc24, Kyle Medley
"""

from setuptools import setup

setup(name='simplesbml',
      version='1.2.1',
      description='A simplified interface for constructing SBML docs.',
      author='Caroline Cannistra, Kyle Medley',
      author_email='tellurium-discuss@googlegroups.com',
      url='http://simplesbml.readthedocs.io/en/latest/',
      install_requires=['tesbml>=5.15.0'],
      packages=['simplesbml'])
