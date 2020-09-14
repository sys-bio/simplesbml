# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 16:19:07 2015, 2020

@author: carolc24, Kyle Medley, Hebrert Sauro
"""

from setuptools import setup
import os.path, codecs

with open("README.md", "r") as fh:
    long_description = fh.read()

# The following two methods were copied from
# https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            print (line)
            delim = '"' if '"' in line else "'"
            print ('delim = ', delim)
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(name='simplesbml',
      version=get_version("simplesbml/_version.py"),   # Update the version number for new releases
      description='A simplified interface for constructing and accessing SBML docs. Version 2.0',
      author='Caroline Cannistra, Kyle Medley, Hebrert Sauro',
      author_email='tellurium-discuss@googlegroups.com',
      url='http://simplesbml.readthedocs.io/en/latest/',
      long_description=long_description,
      long_description_content_type='text/markdown',     
      install_requires=['tesbml>=5.15.0'],
      license='MIT',
      packages=['simplesbml'],
      include_package_data=True,
      classifiers=[
       'License :: OSI Approved :: MIT License',
       'Programming Language :: Python :: 3.7',
       'Programming Language :: Python :: 3.8',
       'Operating System :: OS Independent',
      ],
      python_requires='>=3.7',)
