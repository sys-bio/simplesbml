# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 16:19:07 2015

@author: carolc24
"""

from setuptools import setup

setup(name='simplesbml',
      version='1.1',
      description='A simplified interface for constructing SBML docs',
      author='Caroline Cannistra',
      author_email='carolc24@uw.edu',
      packages=['simplesbml'],
      zip_safe=False)

f = open('simplesbml/__init__.py', 'r');
init = f.read();
f.close();
g = open('__init__.py', 'w');
g.write(init);
g.close();