# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:35:23 2020

@author: hsauro
"""

import pytest
import unittest
import os
from   simplesbml import *
import tellurium as te
import json


testFile = 'testModel1'
data = json.load (open (testFile + '.json'))

getNumCompartments = data['getNumCompartments']
getNumSpecies = data['getNumSpecies']
numFloatingSpecies = data['numFloatingSpecies']
numBoundarySpecies = data['numBoundarySpecies']
listOfAllSpecies = data['listOfAllSpecies']
getNthFloatingSpeciesId = data['getNthFloatingSpeciesId']
isSpeciesValueSet = data['isSpeciesValueSet']
isFloatingSpecies = data['isFloatingSpecies']
isBoundarySpecies = data['isBoundarySpecies']
getSpeciesInitialConcentration = data['getSpeciesInitialConcentration']
listOfFloatingSpecies = data['listOfFloatingSpecies']
listOfBoundarySpecies = data['listOfBoundarySpecies']
isConcentration = data['isConcentration']
getNumParameters = data['getNumParameters']
getListOfParameters = data['getListOfParameters']
getParameterId = data['getParameterId']
isParameterValueSet = data['isParameterValueSet']
getParameterValue = data['getParameterValue']
getNumReactions = data['getNumReactions']
getNumRules = data['getNumRules']
getNumEvents = data['getNumEvents']
getNthReactionId = data['getNthReactionId']
getNumReactants = data['getNumReactants']
getNumProducts = data['getNumProducts']
getRateLaw = data['getRateLaw']
getReactant = data['getReactant']
getProduct = data['getProduct']
getReactantStoichiometry = data['getReactantStoichiometry']
getProductStoichiometry = data['getProductStoichiometry']

antModel = open(testFile + '.ant').read()
print ('\n' + antModel)
r = te.loada (antModel)
sbmlStr = r.getSBML()
model = SbmlModel (sbmlStr=sbmlStr)

# Compartments
#=============

@pytest.mark.parametrize("input,expected", [
    (getNumCompartments['argument'], getNumCompartments['results'])])
def testCompartment(input, expected):
    assert model.getNumCompartments() == expected

# Species
#========

@pytest.mark.parametrize("input,expected", [
    (getNumSpecies['argument'], getNumSpecies['results']),])
def test_getNumSpecies(input, expected):
    assert model.getNumSpecies() == expected                      

@pytest.mark.parametrize("input,expected", [
    (numFloatingSpecies['argument'], numFloatingSpecies['results'])])
def testSpecies_2(input, expected):
    assert model.getNumFloatingSpecies() == expected

@pytest.mark.parametrize("input,expected", [
    (numBoundarySpecies['argument'], numBoundarySpecies['results'])])      
def testSpecies_3(input, expected):
    assert model.getNumBoundarySpecies() == expected
      
@pytest.mark.parametrize("input,expected", [
    (listOfAllSpecies['argument'], listOfAllSpecies['results'])])      
def testSpecies_4(input, expected):
    assert model.getListOfAllSpecies() == expected

@pytest.mark.parametrize("input,expected", [
    (getNthFloatingSpeciesId['argument'], getNthFloatingSpeciesId['results'])])   
def testSpecies_5(input, expected):
    for index, sp in enumerate (input):
        assert model.getNthFloatingSpeciesId(sp) == expected[index]
                         
@pytest.mark.parametrize("input,expected", [
    (isSpeciesValueSet['argument'], isSpeciesValueSet['results'])])   
def testSpecies_7(input, expected):
    for index, sp in enumerate (input):
        assert model.isSpeciesValueSet (sp) == expected[index]

@pytest.mark.parametrize("input,expected", [
    (isFloatingSpecies['argument'], isFloatingSpecies['results'])])   
def testSpecies_9(input, expected):
    for index, sp in enumerate (input):
        assert model.isFloatingSpecies (sp) == expected[index]
 
@pytest.mark.parametrize("input,expected", [
    (isBoundarySpecies['argument'], isBoundarySpecies['results'])]) 
def testSpecies_11(input, expected):
    for index, sp in enumerate (input):
        assert model.isBoundarySpecies (sp) == expected[index]

@pytest.mark.parametrize("input,expected", [
    (getSpeciesInitialConcentration['argument'], getSpeciesInitialConcentration['results'])])  
def test_getSpeciesInitialConcentration(input, expected):
    for index, sp in enumerate (input):
        assert model.getSpeciesInitialConcentration (sp) == expected[index]

@pytest.mark.parametrize("input,expected", [
    (listOfFloatingSpecies['argument'], listOfFloatingSpecies['results'])])      
def testSpecies_14(input, expected):
    assert model.getListOfFloatingSpecies () == expected 

@pytest.mark.parametrize("input,expected", [
    (listOfBoundarySpecies['argument'], listOfBoundarySpecies['results'])])      
def testSpecies_15(input, expected):
    assert model.getListOfBoundarySpecies () == expected

@pytest.mark.parametrize("input,expected", [
    (isConcentration['argument'], isConcentration['results'])])      
def test_isConcentration(input, expected):
    assert model.isConcentration (input) == expected

# ==========================================================================================


# Parameters
#===========

@pytest.mark.parametrize("input,expected", [
    (getNumParameters['argument'], getNumParameters['results'])])      
def test_getNumParameters(input, expected):
    assert model.getNumParameters() == expected

@pytest.mark.parametrize("input,expected", [
    (getListOfParameters['argument'], getListOfParameters['results'])])      
def test_getListOfParameters(input, expected):
    assert model.getListOfParameters() == expected

@pytest.mark.parametrize("input,expected", [
    (getParameterId['argument'], getParameterId['results'])])      
def test_getParameterId(input, expected):
    for index, sp in enumerate (input):    
         assert model.getParameterId(sp) == expected[index]

@pytest.mark.parametrize("input,expected", [
    (isParameterValueSet['argument'], isParameterValueSet['results'])])      
def test_isParameterValueSet(input, expected):
    assert model.isParameterValueSet(input) == expected

@pytest.mark.parametrize("input,expected", [
    (getParameterValue['argument'], getParameterValue['results'])])      
def test_getParameterValue(input, expected):
    for index, sp in enumerate (input):
        assert model.getParameterValue(sp) == expected[index]

# ==========================================================================================


# Reactions
# =========

@pytest.mark.parametrize("input,expected", [
    (getNumReactions['argument'], getNumReactions['results'])])      
def test_getNumReactions(input, expected):
    assert model.getNumReactions() == expected

@pytest.mark.parametrize("input,expected", [
    (getNthReactionId['argument'], getNthReactionId['results'])])      
def test_getNthReactionId(input, expected):
    for index, sp in enumerate (input):
        assert model.getNthReactionId (sp) == expected[index]   

@pytest.mark.parametrize("input,expected", [
    (getNumReactants['argument'], getNumReactants['results'])])      
def test_getNumReactants(input, expected):
    for index, sp in enumerate (input):
        assert model.getNumReactants (sp) == expected[index]
        
@pytest.mark.parametrize("input,expected", [
    (getNumProducts['argument'], getNumProducts['results'])])      
def test_getNumProducts(input, expected):
    for index, sp in enumerate (input):
        assert model.getNumProducts (sp) == expected[index]
        
@pytest.mark.parametrize("input,expected", [
    (getRateLaw['argument'], getRateLaw['results'])])      
def test_getRateLaw(input, expected):
    for index, sp in enumerate (input):
        assert model.getRateLaw (sp).replace (' ', '') == expected[index]

# Requires two arguments, reaction Id and reactant index
@pytest.mark.parametrize("input,expected", [
    (getReactant['argument'], getReactant['results'])])      
def test_getReactant(input, expected):
    for index, sp in enumerate (input):
        assert model.getReactant (sp[0], sp[1]) == expected[index][0]

# Requires two arguments, reaction Id and reactant index
@pytest.mark.parametrize("input,expected", [
    (getProduct['argument'], getProduct['results'])])      
def test_getProduct(input, expected):
    for index, sp in enumerate (input):
        assert model.getProduct (sp[0], sp[1]) == expected[index][0]

# Requires two arguments, reaction Id and reactant index
@pytest.mark.parametrize("input,expected", [
    (getReactantStoichiometry['argument'], getReactantStoichiometry['results'])])      
def test_getReactantStoichiometry(input, expected):
    for index, sp in enumerate (input):
        assert model.getReactantStoichiometry (sp[0], sp[1]) == expected[index][0]

# Requires two arguments, reaction Id and reactant index
@pytest.mark.parametrize("input,expected", [
    (getProductStoichiometry['argument'], getProductStoichiometry['results'])])      
def test_getProductStoichiometry(input, expected):
    for index, sp in enumerate (input):
        assert model.getProductStoichiometry (sp[0], sp[1]) == expected[index][0]
        
# ==========================================================================================

# Events
# ======

@pytest.mark.parametrize("input,expected", [
    (getNumEvents['argument'], getNumEvents['results'])])      
def test_getNumEvents(input, expected):
    assert model.getNumEvents() == expected


# ==========================================================================================


# Rules
#======

@pytest.mark.parametrize("input,expected", [
    (getNumRules['argument'], getNumRules['results'])])      
def test_getNumRules (input, expected):
    assert model.getNumRules() == expected


pytest.main()