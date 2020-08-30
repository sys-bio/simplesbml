# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 16:19:07 2015, 2020

@author: carolc24, Kyle Medley, Hebrert Sauro
"""

from setuptools import setup
import os.path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='simplesbml',
      version='1.3.3',
      description='A simplified interface for constructing and accessing SBML docs.',
      author='Caroline Cannistra, Kyle Medley, Hebrert Sauro',
      author_email='tellurium-discuss@googlegroups.com',
      url='http://simplesbml.readthedocs.io/en/latest/',
      long_description=long_description,
      long_description_content_type='text/markdown',     
      install_requires=['tesbml>=5.15.0'],
      license='MIT',
      packages=['simplesbml'],
      classifiers=[
       'License :: OSI Approved :: MIT License',
       'Programming Language :: Python :: 3.7',
       'Programming Language :: Python :: 3.8',
       'Operating System :: OS Independent',
      ],
      python_requires='>=3.7',)
