# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 16:19:07 2015

@author: carolc24, Kyle Medley
"""

from setuptools import setup

setup(name='simplesbml',
      version='1.2.2',
      description='A simplified interface for constructing SBML docs.',
      author='Caroline Cannistra, Kyle Medley',
      author_email='tellurium-discuss@googlegroups.com',
      url='http://simplesbml.readthedocs.io/en/latest/',
      install_requires=[],
      packages=['simplesbml'],
      extras_require={
          ':python_version=="3.7"': ['python-libsbml>=5.18.0'],
          ':python_version<"3.7"': ['tesbml>=5.15.0']
      }
)
