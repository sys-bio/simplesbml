# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 23:13:42 2015, 2020

@author: carolc24, Kyle Medley, hsauro
"""

from .simplesbml import SbmlModel
from .simplesbml import loadSBMLStr
from .simplesbml import loadSBMLFile

from simplesbml._version import __version__

try:
  import tellurium
  import simplesbml.tests.runTests as tests
except ImportError as error:
  print ("The tests rely on tellurium to construct the models")
  print ("Since tellurium is not installed the tests can't be run")
  print ("If you want to run the tests, pip install tellurium first")
