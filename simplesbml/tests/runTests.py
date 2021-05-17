# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 22:50:46 2020

@author: hsauro
"""

try:
   import tellurium as _te
except:
   print("You will need to install tellurium if you want to run the tests")
   print ("We use tellurium to define the test models")
   import sys
   sys.exit()

import simplesbml as _simplesbml

_testCount = 0
_failedTest = []
    
def _initializeTests(title, modelStr):
    global _testCount
    global _failedTest
    _testCount = 0
    _failedTest = []
    r = _te.loada (modelStr)
    sbmlStr = r.getSBML()
    print ('\nBegin Report: ' + title)
    return _simplesbml.loadSBMLStr (sbmlStr)

def _printReport():
    global _testCount
    global _failedTest
    print()
    print (_testCount, 'tests pass') 
    print (len (_failedTest), 'tests fail')   

    if len (_failedTest) > 0:
       print ('Failed Tests:' ) 
    for i in _failedTest:
        print (i, ' ')
    print ('End Report')
       
def _assertEqual (func, arguments, result):
    global _testCount
    _testCount += 1
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
       _failedTest.append ([_testCount, func.__name__])

 
def run():      
  model = """
    S1 -> S2; k1*S1;
    k1 = 0.1; S1 = 10; S2 = 2.5
  """

  model = _initializeTests('Test 1', model)

  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumFloatingSpecies, None, 2)
  _assertEqual (model.getNumBoundarySpecies, None, 0)
  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumSpecies, None, 2)
  _assertEqual (model.getNumReactions, None, 1)
  _assertEqual (model.getNumEvents, None, 0)
  _assertEqual (model.getNumRules, None, 0)

  _assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2'])  
  _assertEqual (model.getNthFloatingSpeciesId, 0, 'S1')
  _assertEqual (model.getNthFloatingSpeciesId, 1, 'S2')
  _assertEqual (model.isSpeciesValueSet, 'S1', True)
  _assertEqual (model.isSpeciesValueSet, 'S2', True)
  _assertEqual (model.isFloatingSpecies, 'S1', True)
  _assertEqual (model.isFloatingSpecies, 'S2', True)
  _assertEqual (model.isBoundarySpecies, 'S1', False)
  _assertEqual (model.isBoundarySpecies, 'S2', False)            
  _assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
  _assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
  _assertEqual (model.getListOfFloatingSpecies, None,  ['S1', 'S2'])
  _assertEqual (model.getListOfBoundarySpecies, None, [])

  _assertEqual (model.isConcentration, 'S1', True)
  _assertEqual (model.getNumParameters, None, 1)
  _assertEqual (model.getListOfParameterIds, None, ['k1'])
  _assertEqual (model.getParameterId, 0, 'k1')
  _assertEqual (model.isParameterValueSet, 'k1', True)
  _assertEqual (model.getParameterValue, 'k1', 0.1)

  _assertEqual (model.getListOfReactionIds, None, ['_J0'])
  _assertEqual (model.getNthReactionId, 0, '_J0')
  _assertEqual (model.getNumReactants, 0, 1)
  _assertEqual (model.getNumProducts, 0, 1)
  _assertEqual (model.getRateLaw, 0, 'k1 * S1')
  _assertEqual (model.getReactant,  ['_J0', 0], 'S1')
  _assertEqual (model.getProduct, ['_J0', 0], 'S2')
  _assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
  _assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)

  _printReport()

  # ==================================================================
     
  modelStr = """
         $S1 -> S2; k1*S1;
          S2 -> S3; k2*S2-k3*S3
          k1 = 0.1; k2 = 0.2; k3 = 0.3
          S1 = 10; S2 = 2.5; S3 = 3.4
  """

  model = _initializeTests('Test 2', modelStr)

  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumFloatingSpecies, None, 2)
  _assertEqual (model.getNumBoundarySpecies, None, 1)
  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumSpecies, None, 3)
  _assertEqual (model.getNumReactions, None, 2)
  _assertEqual (model.getNumEvents, None, 0)
  _assertEqual (model.getNumRules, None, 0)
  _assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2', 'S3'])
     
  _assertEqual (model.getNthFloatingSpeciesId, 0, 'S2')
  _assertEqual (model.getNthFloatingSpeciesId, 1, 'S3')
  _assertEqual (model.isSpeciesValueSet, 'S1', True)
  _assertEqual (model.isSpeciesValueSet, 'S2', True)
  _assertEqual (model.isFloatingSpecies, 'S1', False)
  _assertEqual (model.isFloatingSpecies, 'S2', True)
  _assertEqual (model.isBoundarySpecies, 'S1', True)
  _assertEqual (model.isBoundarySpecies, 'S2', False)            
  _assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
  _assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
  _assertEqual (model.getListOfFloatingSpecies, None,  ['S2', 'S3'])
  _assertEqual (model.getListOfBoundarySpecies, None, ['S1'])

  _assertEqual (model.isConcentration, 'S1', True)
  _assertEqual (model.getNumParameters, None, 3)
  _assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3'])
  _assertEqual (model.getParameterId, 0, 'k1')
  _assertEqual (model.isParameterValueSet, 'k1', True)
  _assertEqual (model.getParameterValue, 'k1', 0.1)

  _assertEqual (model.getListOfReactionIds, None, ['_J0', '_J1'])
  _assertEqual (model.getNthReactionId, 0, '_J0')
  _assertEqual (model.getNumReactants, 0, 1)
  _assertEqual (model.getNumProducts, 0, 1)
  _assertEqual (model.getRateLaw, 0, 'k1 * S1')
  _assertEqual (model.getReactant,  ['_J0', 0], 'S1')
  _assertEqual (model.getProduct, ['_J0', 0], 'S2')
  _assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
  _assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)
   
  _printReport()   

  # ==================================================================

  modelStr = """
         $S1 + S2 -> S3; k1*S1*S2;
          S3 -> 2 S4; k2*S3-k3*S4
          k1 = 0.1; k2 = 0.2; k3 = 0.3
          S1 = 10; S2 = 2.5; S3 = 3.4; S4 = 0
          """
          
  model = _initializeTests('Test 3', modelStr)            

  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumFloatingSpecies, None, 3)
  _assertEqual (model.getNumBoundarySpecies, None, 1)
  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumSpecies, None, 4)
  _assertEqual (model.getNumReactions, None, 2)
  _assertEqual (model.getNumEvents, None, 0)
  _assertEqual (model.getNumRules, None, 0)
  _assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2', 'S3', 'S4'])
     
  _assertEqual (model.getNthFloatingSpeciesId, 0, 'S2')
  _assertEqual (model.getNthFloatingSpeciesId, 1, 'S3')
  _assertEqual (model.isSpeciesValueSet, 'S1', True)
  _assertEqual (model.isSpeciesValueSet, 'S2', True)
  _assertEqual (model.isFloatingSpecies, 'S1', False)
  _assertEqual (model.isFloatingSpecies, 'S2', True)
  _assertEqual (model.isBoundarySpecies, 'S1', True)
  _assertEqual (model.isBoundarySpecies, 'S2', False)            
  _assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
  _assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
  _assertEqual (model.getListOfFloatingSpecies, None,  ['S2', 'S3', 'S4'])
  _assertEqual (model.getListOfBoundarySpecies, None, ['S1'])

  _assertEqual (model.isConcentration, 'S1', True)
  _assertEqual (model.getNumParameters, None, 3)
  _assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3'])
  _assertEqual (model.getParameterId, 0, 'k1')
  _assertEqual (model.isParameterValueSet, 'k1', True)
  _assertEqual (model.getParameterValue, 'k1', 0.1)

  _assertEqual (model.getListOfReactionIds, None, ['_J0', '_J1'])
  _assertEqual (model.getNthReactionId, 0, '_J0')
  _assertEqual (model.getNumReactants, 0, 2)
  _assertEqual (model.getNumProducts, 0, 1)
  _assertEqual (model.getRateLaw, 0, 'k1 * S1 * S2')
  _assertEqual (model.getReactant,  ['_J0', 0], 'S1')
  _assertEqual (model.getProduct, ['_J0', 0], 'S3')
  _assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
  _assertEqual (model.getReactantStoichiometry, ['_J0', 1], 1)
  _assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)

  _assertEqual (model.getNthReactionId, 1, '_J1')
  _assertEqual (model.getNumReactants, 1, 1)
  _assertEqual (model.getNumProducts, 1, 1)
  _assertEqual (model.getRateLaw, 1, 'k2 * S3 - k3 * S4')
  _assertEqual (model.getReactant,  ['_J1', 0], 'S3')
  _assertEqual (model.getProduct, ['_J1', 0], 'S4')
  _assertEqual (model.getReactantStoichiometry, ['_J1', 0], 1)
  _assertEqual (model.getProductStoichiometry, ['_J1', 0], 2)

  _printReport()

  # ==================================================================

  modelStr = """
          J1: 2 S1 + 3 S2 -> 5 S3 + 7 S4; v
          v = 0
          S1 = 10; S2 = 2.5; S3 = 3.4; S4 = 0
          """
   
  model = _initializeTests('Test 4', modelStr)            

  _assertEqual (model.getListOfReactionIds, None, ['J1'])
  _assertEqual (model.getNthReactionId, 0, 'J1')
  _assertEqual (model.getNumReactants, 0, 2)
  _assertEqual (model.getNumProducts, 0, 2)
  _assertEqual (model.getRateLaw, 0, 'v')
  _assertEqual (model.getReactant, ['J1', 0], 'S1')
  _assertEqual (model.getReactant, ['J1', 1], 'S2')
  _assertEqual (model.getProduct, ['J1', 0], 'S3')
  _assertEqual (model.getProduct, ['J1', 1], 'S4')
  _assertEqual (model.getReactantStoichiometry, ['J1', 0], 2)
  _assertEqual (model.getReactantStoichiometry, ['J1', 1], 3)
  _assertEqual (model.getProductStoichiometry, ['J1', 0], 5)
  _assertEqual (model.getProductStoichiometry, ['J1', 1], 7)

  _printReport()

  # ==================================================================

  modelStr = """
          k1 := 7.8
          $S1 + S2 -> S3; k1*S1*S2;
          S3 -> 2 S4; k2*S3-k3*S4
          k2 = 0.2; k3 = 0.3
          S1 = 10; S2 = 2.5; S3 = 3.4; S4 = 0
          """
   
  model = _initializeTests('Test 5', modelStr)            

  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumFloatingSpecies, None, 3)
  _assertEqual (model.getNumBoundarySpecies, None, 1)
  _assertEqual (model.getNumCompartments, None, 1)
  _assertEqual (model.getNumSpecies, None, 4)
  _assertEqual (model.getNumReactions, None, 2)
  _assertEqual (model.getNumEvents, None, 0)
  _assertEqual (model.getNumRules, None, 1)
  _assertEqual (model.getListOfAllSpecies, None, ['S1', 'S2', 'S3', 'S4'])
     
  _assertEqual (model.getNthFloatingSpeciesId, 0, 'S2')
  _assertEqual (model.getNthFloatingSpeciesId, 1, 'S3')
  _assertEqual (model.isSpeciesValueSet, 'S1', True)
  _assertEqual (model.isSpeciesValueSet, 'S2', True)
  _assertEqual (model.isFloatingSpecies, 'S1', False)
  _assertEqual (model.isFloatingSpecies, 'S2', True)
  _assertEqual (model.isBoundarySpecies, 'S1', True)
  _assertEqual (model.isBoundarySpecies, 'S2', False)            
  _assertEqual (model.getSpeciesInitialConcentration, 'S1', 10)
  _assertEqual (model.getSpeciesInitialConcentration, 'S2', 2.5)          
  _assertEqual (model.getListOfFloatingSpecies, None,  ['S2', 'S3', 'S4'])
  _assertEqual (model.getListOfBoundarySpecies, None, ['S1'])

  _assertEqual (model.isConcentration, 'S1', True)
  _assertEqual (model.getNumParameters, None, 3)
  _assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3'])
  _assertEqual (model.getParameterId, 0, 'k1')
  _assertEqual (model.isParameterValueSet, 'k1', True)
  _assertEqual (model.getParameterValue, 'k2', 0.2)
  _assertEqual (model.getParameterValue, 'k3', 0.3)

  _assertEqual (model.getListOfReactionIds, None, ['_J0', '_J1'])
  _assertEqual (model.getNthReactionId, 0, '_J0')
  _assertEqual (model.getNumReactants, 0, 2)
  _assertEqual (model.getNumProducts, 0, 1)
  _assertEqual (model.getRateLaw, 0, 'k1 * S1 * S2')
  _assertEqual (model.getReactant,  ['_J0', 0], 'S1')
  _assertEqual (model.getProduct, ['_J0', 0], 'S3')
  _assertEqual (model.getReactantStoichiometry, ['_J0', 0], 1)
  _assertEqual (model.getReactantStoichiometry, ['_J0', 1], 1)
  _assertEqual (model.getProductStoichiometry, ['_J0', 0], 1)

  _assertEqual (model.getNthReactionId, 1, '_J1')
  _assertEqual (model.getNumReactants, 1, 1)
  _assertEqual (model.getNumProducts, 1, 1)
  _assertEqual (model.getRateLaw, 1, 'k2 * S3 - k3 * S4')
  _assertEqual (model.getReactant,  ['_J1', 0], 'S3')
  _assertEqual (model.getProduct, ['_J1', 0], 'S4')
  _assertEqual (model.getReactantStoichiometry, ['_J1', 0], 1)
  _assertEqual (model.getProductStoichiometry, ['_J1', 0], 2)
        
  _assertEqual (model.getListOfRuleIds, None, ['k1'])
  _assertEqual (model.getRuleId, 0, 'k1')
  _assertEqual (model.getRuleRightSide, 0, '7.8')
  _assertEqual (model.getRuleType, 0, 'Assignment rule')
  _assertEqual (model.isRuleType_Assignment, 0, True)

  _printReport()

  # ==================================================================

  modelStr = """
             k1 := sin (time)
             k2 := k1 + 3.14
             
             S1 -> S2; v
             S1 = 1; S2 = 0; v = 0
          """
   
  model = _initializeTests('Test 6', modelStr)            

  _assertEqual (model.getNumRules, None, 2)

  _assertEqual (model.getRuleId, 0, 'k1')
  _assertEqual (model.getRuleRightSide, 0, 'sin(time)')
  _assertEqual (model.getRuleType, 0, 'Assignment rule')
  _assertEqual (model.isRuleType_Assignment, 0, True)

  _assertEqual (model.getRuleId, 1, 'k2')
  _assertEqual (model.getRuleRightSide, 1, 'k1 + 3.14')
  _assertEqual (model.getRuleType, 1, 'Assignment rule')
  _assertEqual (model.isRuleType_Assignment, 1, True)

  _printReport()

  # ==================================================================

  modelStr = """ 
             model rabbit()         

             k1 = 1.1; k2 = 2.2; k3 = 3.3; k4 = 4.4
             k5 = 5.5; k6 = 6.6; k7 = 7.7; k8 = 8.8
             end
          """
   
  model = _initializeTests('Test 7', modelStr)            

  _assertEqual (model.getModelId, None, 'rabbit')
  _assertEqual (model.getNumParameters, None, 8)
  _assertEqual (model.getListOfParameterIds, None, ['k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8'])
  _assertEqual (model.getParameterValue, 'k1', 1.1)
  _assertEqual (model.getParameterValue, 1, 2.2)
  _assertEqual (model.getParameterValue, 'k3', 3.3)

  _printReport()

  # ==================================================================

  modelStr = """  
             compartment c1, c2, c3, c4;
             
             c1 = 1.1; c2 = 2.2; c3 = 3.3; c4 = 4.4
             """
   
  model = _initializeTests('Test 8', modelStr)            

  _assertEqual (model.getNumCompartments, None, 4)
  _assertEqual (model.getListOfCompartmentIds, None, ['c1', 'c2', 'c3', 'c4'])
  _assertEqual (model.getCompartmentVolume, 'c1', 1.1)
  _assertEqual (model.getCompartmentVolume, 'c2', 2.2)
  _assertEqual (model.getCompartmentVolume, 2, 3.3)
  _assertEqual (model.getCompartmentVolume, 'c4', 4.4)
  _assertEqual (model.getCompartmentId, 0, 'c1')
  _assertEqual (model.getCompartmentId, 2, 'c3')
  _assertEqual (model.getNumInitialAssignments, None, 0)
  _assertEqual (model.getNumFunctionDefinitions, None, 0)

  _printReport()

  # ==================================================================

  modelStr = """  
              S1 -> S2; k1*S3;
              S2 -> S3; v;
              
              E0: at time > 10: k1 = k1/2
             
              k1 = 0.1; S1 = 10; S2 = 0; S3 = 0; v = 0        
              """
   
  model = _initializeTests('Test 9', modelStr)            

  _assertEqual (model.getNumEvents, None, 1)
  _assertEqual (model.getEventId, 0, 'E0')
  _assertEqual (model.getEventTrigger, 0, 'time > 10')
  _assertEqual (model.getNumEventAssignments, 0, 1)
  _assertEqual (model.getEventVariable, [0, 0], 'k1')
  _assertEqual (model.getEventAssignment, [0,0], 'k1 / 2')
  _assertEqual (model.getEventString, 0, 'at time > 10 then { k1 = k1 / 2 }')

  _printReport()

  # ==================================================================

  modelStr = """  
              S1 -> S2; k1*S3;
              S2 -> S3; v;
                       
              k1 = 0.1; S1 = 10; S2 = 0; S3 = 0; v = 0        
              """
   
  model = _initializeTests('Test 10', modelStr)            

  _assertEqual (model.getNumModifiers, 0, 1)
  _assertEqual (model.getListOfModifiers, 0, ['S3'])

  _printReport()

  # ==================================================================

  modelStr = """  
              function Hill (x, y)
                  x*2 + y
              end
              
              S1 -> S2; k1*S3;
              S2 -> S3; Hill (S2, S3)
                       
              k1 = 0.1; S1 = 10; S2 = 0; S3 = 0; v = 0        
              """
   
  model = _initializeTests('Test 10', modelStr)            

  _assertEqual (model.getNumModifiers, 0, 1)
  _assertEqual (model.getListOfModifiers, 0, ['S3'])

  _assertEqual (model.getNumFunctionDefinitions, None, 1)
  _assertEqual (model.getListOfFunctionIds, None, ['Hill'])
  _assertEqual (model.getFunctionId, 0, 'Hill')
  _assertEqual (model.getFunctionBody, 0, 'x * 2 + y')
  _assertEqual (model.getNumArgumentsInUserFunction, 0, 2)
  _assertEqual (model. getListOfArgumentsInUserFunction, 0, ['x', 'y'])

  _printReport()

  print ("\nAll Tests Complete")
  # getCompartmentIdSpeciesIsIn
  # getSpeciesInitialConcentration




