# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 22:50:46 2020

@author: hsauro
"""

import tellurium as te
import roadrunner
import simplesbml

testCount = 0
failedTests = []
    
def initializeTests(title, modelStr):
    global testCount
    global failedTests
    testCount = 0
    failedTests = []
    r = te.loada (modelStr)
    sbmlStr = r.getSBML()
    print ('\nBegin Report: ' + title)
    return simplesbml.SbmlModel (sbmlStr=sbmlStr)

def printReport():
    global testCount
    global failedTests
    print()
    print (testCount, 'tests pass') 
    print (len (failedTests), 'tests fail')   

    if len (failedTests) > 0:
       print ('Failed Tests:' ) 
    for i in failedTests:
        print (i, ' ')
    print ('End Report')
       
def assertEqual (func, arguments, result):
    global testCount
    testCount += 1
    input = None
    if arguments != None:
       if type (arguments) == list:
          input = func (arguments[0], arguments[1])
       else:
          input = func (arguments)
    else:
       input = func ()
        
    if input == result:
       print ('.',end='')
    else:
       print ('F',end='')
       failedTests.append ([testCount, func.__name__])

       
model = """
  S1 -> S2; k1*S1;
  k1 = 0.1; S1 = 10; S2 = 2.5
"""

model = initializeTests('Test 1', model)

assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumFloatingSpecies, None, 2)
assertEqual (model.getNumBoundarySpecies, None, 0)
assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumSpecies, None, 2)
assertEqual (model.getNumReactions, None, 1)
assertEqual (model.getNumEvents, None, 0)
assertEqual (model.getNumRules, None, 0)

assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2'])  
assertEqual (model.getNthFloatingSpeciesId, 0, 'S1')
assertEqual (model.getNthFloatingSpeciesId, 1, 'S2')
assertEqual (model.isSpeciesValueSet, 'S1', True)
assertEqual (model.isSpeciesValueSet, 'S2', True)
assertEqual (model.isFloatingSpecies, 'S1', True)
assertEqual (model.isFloatingSpecies, 'S2', True)
assertEqual (model.isBoundarySpecies, 'S1', False)
assertEqual (model.isBoundarySpecies, 'S2', False)            
assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
assertEqual (model.getListOfFloatingSpecies, None,  ['S1', 'S2'])
assertEqual (model.getListOfBoundarySpecies, None, [])

assertEqual (model.isConcentration, 'S1', True)
assertEqual (model.getNumParameters, None, 1)
assertEqual (model.getListOfParameterIds, None, ['k1'])
assertEqual (model.getParameterId, 0, 'k1')
assertEqual (model.isParameterValueSet, 'k1', True)
assertEqual (model.getParameterValue, 'k1', 0.1)

assertEqual (model.getListOfReactionIds, None, ['_J0'])
assertEqual (model.getNthReactionId, 0, '_J0')
assertEqual (model.getNumReactants, 0, 1)
assertEqual (model.getNumProducts, 0, 1)
assertEqual (model.getRateLaw, 0, 'k1 * S1')
assertEqual (model.getReactant,  ['_J0', 0], 'S1')
assertEqual (model.getProduct, ['_J0', 0], 'S2')
assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)

printReport()

# ==================================================================
   
modelStr = """
       $S1 -> S2; k1*S1;
        S2 -> S3; k2*S2-k3*S3
        k1 = 0.1; k2 = 0.2; k3 = 0.3
        S1 = 10; S2 = 2.5; S3 = 3.4
"""

model = initializeTests('Test 2', modelStr)

assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumFloatingSpecies, None, 2)
assertEqual (model.getNumBoundarySpecies, None, 1)
assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumSpecies, None, 3)
assertEqual (model.getNumReactions, None, 2)
assertEqual (model.getNumEvents, None, 0)
assertEqual (model.getNumRules, None, 0)
assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2', 'S3'])
   
assertEqual (model.getNthFloatingSpeciesId, 0, 'S2')
assertEqual (model.getNthFloatingSpeciesId, 1, 'S3')
assertEqual (model.isSpeciesValueSet, 'S1', True)
assertEqual (model.isSpeciesValueSet, 'S2', True)
assertEqual (model.isFloatingSpecies, 'S1', False)
assertEqual (model.isFloatingSpecies, 'S2', True)
assertEqual (model.isBoundarySpecies, 'S1', True)
assertEqual (model.isBoundarySpecies, 'S2', False)            
assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
assertEqual (model.getListOfFloatingSpecies, None,  ['S2', 'S3'])
assertEqual (model.getListOfBoundarySpecies, None, ['S1'])

assertEqual (model.isConcentration, 'S1', True)
assertEqual (model.getNumParameters, None, 3)
assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3'])
assertEqual (model.getParameterId, 0, 'k1')
assertEqual (model.isParameterValueSet, 'k1', True)
assertEqual (model.getParameterValue, 'k1', 0.1)

assertEqual (model.getListOfReactionIds, None, ['_J0', '_J1'])
assertEqual (model.getNthReactionId, 0, '_J0')
assertEqual (model.getNumReactants, 0, 1)
assertEqual (model.getNumProducts, 0, 1)
assertEqual (model.getRateLaw, 0, 'k1 * S1')
assertEqual (model.getReactant,  ['_J0', 0], 'S1')
assertEqual (model.getProduct, ['_J0', 0], 'S2')
assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)
 
printReport()   

# ==================================================================

modelStr = """
       $S1 + S2 -> S3; k1*S1*S2;
        S3 -> 2 S4; k2*S3-k3*S4
        k1 = 0.1; k2 = 0.2; k3 = 0.3
        S1 = 10; S2 = 2.5; S3 = 3.4;
        """
        
model = initializeTests('Test 3', modelStr)            

assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumFloatingSpecies, None, 3)
assertEqual (model.getNumBoundarySpecies, None, 1)
assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumSpecies, None, 4)
assertEqual (model.getNumReactions, None, 2)
assertEqual (model.getNumEvents, None, 0)
assertEqual (model.getNumRules, None, 0)
assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2', 'S3', 'S4'])
   
assertEqual (model.getNthFloatingSpeciesId, 0, 'S2')
assertEqual (model.getNthFloatingSpeciesId, 1, 'S3')
assertEqual (model.isSpeciesValueSet, 'S1', True)
assertEqual (model.isSpeciesValueSet, 'S2', True)
assertEqual (model.isFloatingSpecies, 'S1', False)
assertEqual (model.isFloatingSpecies, 'S2', True)
assertEqual (model.isBoundarySpecies, 'S1', True)
assertEqual (model.isBoundarySpecies, 'S2', False)            
assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
assertEqual (model.getListOfFloatingSpecies, None,  ['S2', 'S3', 'S4'])
assertEqual (model.getListOfBoundarySpecies, None, ['S1'])

assertEqual (model.isConcentration, 'S1', True)
assertEqual (model.getNumParameters, None, 3)
assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3'])
assertEqual (model.getParameterId, 0, 'k1')
assertEqual (model.isParameterValueSet, 'k1', True)
assertEqual (model.getParameterValue, 'k1', 0.1)

assertEqual (model.getListOfReactionIds, None, ['_J0', '_J1'])
assertEqual (model.getNthReactionId, 0, '_J0')
assertEqual (model.getNumReactants, 0, 2)
assertEqual (model.getNumProducts, 0, 1)
assertEqual (model.getRateLaw, 0, 'k1 * S1 * S2')
assertEqual (model.getReactant,  ['_J0', 0], 'S1')
assertEqual (model.getProduct, ['_J0', 0], 'S3')
assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
assertEqual (model.getReactantStoichiometry, ['_J0', 1], 1)
assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)

assertEqual (model.getNthReactionId, 1, '_J1')
assertEqual (model.getNumReactants, 1, 1)
assertEqual (model.getNumProducts, 1, 1)
assertEqual (model.getRateLaw, 1, 'k2 * S3 - k3 * S4')
assertEqual (model.getReactant,  ['_J1', 0], 'S3')
assertEqual (model.getProduct, ['_J1', 0], 'S4')
assertEqual (model.getReactantStoichiometry, ['_J1', 0], 1)
assertEqual (model.getProductStoichiometry, ['_J1', 0], 2)

printReport()

# ==================================================================

modelStr = """
        J1: 2 S1 + 3 S2 -> 5 S3 + 7 S4; v
        v = 0
        S1 = 10; S2 = 2.5; S3 = 3.4; S4 = 0
        """
 
model = initializeTests('Test 4', modelStr)            

assertEqual (model.getListOfReactionIds, None, ['J1'])
assertEqual (model.getNthReactionId, 0, 'J1')
assertEqual (model.getNumReactants, 0, 2)
assertEqual (model.getNumProducts, 0, 2)
assertEqual (model.getRateLaw, 0, 'v')
assertEqual (model.getReactant, ['J1', 0], 'S1')
assertEqual (model.getReactant, ['J1', 1], 'S2')
assertEqual (model.getProduct, ['J1', 0], 'S3')
assertEqual (model.getProduct, ['J1', 1], 'S4')
assertEqual (model.getReactantStoichiometry, ['J1', 0], 2)
assertEqual (model.getReactantStoichiometry, ['J1', 1], 3)
assertEqual (model.getProductStoichiometry, ['J1', 0], 5)
assertEqual (model.getProductStoichiometry, ['J1', 1], 7)

printReport()

# ==================================================================

modelStr = """
        k1 := 7.8
        $S1 + S2 -> S3; k1*S1*S2;
        S3 -> 2 S4; k2*S3-k3*S4
        k2 = 0.2; k3 = 0.3
        S1 = 10; S2 = 2.5; S3 = 3.4;
        """
 
model = initializeTests('Test 5', modelStr)            

assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumFloatingSpecies, None, 3)
assertEqual (model.getNumBoundarySpecies, None, 1)
assertEqual (model.getNumCompartments, None, 1)
assertEqual (model.getNumSpecies, None, 4)
assertEqual (model.getNumReactions, None, 2)
assertEqual (model.getNumEvents, None, 0)
assertEqual (model.getNumRules, None, 1)
assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2', 'S3', 'S4'])
   
assertEqual (model.getNthFloatingSpeciesId, 0, 'S2')
assertEqual (model.getNthFloatingSpeciesId, 1, 'S3')
assertEqual (model.isSpeciesValueSet, 'S1', True)
assertEqual (model.isSpeciesValueSet, 'S2', True)
assertEqual (model.isFloatingSpecies, 'S1', False)
assertEqual (model.isFloatingSpecies, 'S2', True)
assertEqual (model.isBoundarySpecies, 'S1', True)
assertEqual (model.isBoundarySpecies, 'S2', False)            
assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
assertEqual (model.getListOfFloatingSpecies, None,  ['S2', 'S3', 'S4'])
assertEqual (model.getListOfBoundarySpecies, None, ['S1'])

assertEqual (model.isConcentration, 'S1', True)
assertEqual (model.getNumParameters, None, 3)
assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3'])
assertEqual (model.getParameterId, 0, 'k1')
assertEqual (model.isParameterValueSet, 'k1', True)
assertEqual (model.getParameterValue, 'k2', 0.2)
assertEqual (model.getParameterValue, 'k3', 0.3)

assertEqual (model.getListOfReactionIds, None, ['_J0', '_J1'])
assertEqual (model.getNthReactionId, 0, '_J0')
assertEqual (model.getNumReactants, 0, 2)
assertEqual (model.getNumProducts, 0, 1)
assertEqual (model.getRateLaw, 0, 'k1 * S1 * S2')
assertEqual (model.getReactant,  ['_J0', 0], 'S1')
assertEqual (model.getProduct, ['_J0', 0], 'S3')
assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
assertEqual (model.getReactantStoichiometry, ['_J0', 1], 1)
assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)

assertEqual (model.getNthReactionId, 1, '_J1')
assertEqual (model.getNumReactants, 1, 1)
assertEqual (model.getNumProducts, 1, 1)
assertEqual (model.getRateLaw, 1, 'k2 * S3 - k3 * S4')
assertEqual (model.getReactant,  ['_J1', 0], 'S3')
assertEqual (model.getProduct, ['_J1', 0], 'S4')
assertEqual (model.getReactantStoichiometry, ['_J1', 0], 1)
assertEqual (model.getProductStoichiometry, ['_J1', 0], 2)
      
assertEqual (model.getRuleId, 0, 'k1')
assertEqual (model.getRuleRightSide, 0, '7.8')
assertEqual (model.getRuleType, 0, 'Assignment rule')
assertEqual (model.isRuleType_Assignment, 0, True)

printReport()

# ==================================================================

modelStr = """
           k1 := sin (time)
           k2 := k1 + 3.14
           
           S1 -> S2; v
           S1 = 1; S2 = 0; v = 0
        """
 
model = initializeTests('Test 6', modelStr)            

assertEqual (model.getNumRules, None, 2)

assertEqual (model.getRuleId, 0, 'k1')
assertEqual (model.getRuleRightSide, 0, 'sin(time)')
assertEqual (model.getRuleType, 0, 'Assignment rule')
assertEqual (model.isRuleType_Assignment, 0, True)

assertEqual (model.getRuleId, 1, 'k2')
assertEqual (model.getRuleRightSide, 1, 'k1 + 3.14')
assertEqual (model.getRuleType, 1, 'Assignment rule')
assertEqual (model.isRuleType_Assignment, 1, True)

printReport()

# ==================================================================

modelStr = """ 
           model rabbit()         

           k1 = 1.1; k2 = 2.2; k3 = 3.3; k4 = 4.4
           k5 = 5.5; k6 = 6.6; k7 = 7.7; k8 = 8.8
           end
        """
 
model = initializeTests('Test 7', modelStr)            

assertEqual (model.getModelId, None, 'rabbit')
assertEqual (model.getNumParameters, None, 8)
assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8'])
assertEqual (model.getParameterValue, 'k1', 1.1)
assertEqual (model.getParameterValue, 1, 2.2)
assertEqual (model.getParameterValue, 'k3', 3.3)

printReport()

