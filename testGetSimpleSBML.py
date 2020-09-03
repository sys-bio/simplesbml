# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:52:06 2020

@author: hsauro
"""

import tellurium as te
import simplesbml

r = te.loada("""
 
    function Hill(S, Vm, K, n)
      S^n*Vm/(K + S^n);
    end
            
    k1 := 3.4
    x' = k1*x
    
    J1: S1 -> S2; k1*S1;
    J2: $S3 -> S3; (k2+k3)*S3
    
    at time > 10: k2 = 200;
    at S1 > S2: k2 = 200/3, k3 = 1.02
    
    k2 = 1.2345; k3 = 0.976;
    S1 = 10.6; S2 = 0.234
    S3 = 99.76; x = 0.345
""")

model = simplesbml.SbmlModel (sbmlStr=r.getSBML())
# or you can load from a file:
# model = simplesbml.sbmlModel (sbmlFile='mymodel.xml')

print ('Number of compartments = ', model.getNumCompartments())
print ('Number of parameters =', model.getNumParameters())
print ('Number of species =', model.getNumSpecies())
print ('Number of floating species = ', model.getNumFloatingSpecies())
print ('Number of floating species = ', model.getNumBoundarySpecies())
print ('Number of reactions = ', model.getNumReactions())
print ('Number of of function definitions = ', model.getNumFunctionDefinitions())
print ('List of compartments: ', model.getListOfCompartmentIds())
print ('List of ALL species: ', model.getListOfAllSpecies())
print ('list of floating species = ', model.getListOfFloatingSpecies())
print ('list of boundary species = ', model.getListOfBoundarySpecies())
print ('List of reactions = ', model.getListOfReactionIds())
print ('List of rules = ', model.getListOfRules())
print ('List of function definitions = ', model.getListOfFunctionIds())

print ('Compartment values:')
p = model.getListOfCompartmentIds()
for v in p:
    print (v, ': ', model.getCompartmentVolume (v))
    
print ('Parameter values:')
p = model.getListOfParameterIds()
for v in p:
    print (v, ': ', model.getParameterValue (v))
    
print ('Species values:')
p = model.getListOfAllSpecies()
for v in p:
    if model.isSpeciesValueSet (v):
       print (v, ': ', model.getSpeciesInitialConcentration (v))
    else:
       print (v, ': species value not set') 
 
print ('Rate laws:')
reactions = model.getListOfReactionIds()
for v in reactions:
    print (v, ': ', model.getRateLaw (v))
    
print ('-------------------------------------------------')
print ('Reaction Details:')
rs = model.getListOfReactionIds()
for rId in rs:
    print ('Reaction:', rId)
    print ('Number of reactants: ', model.getNumReactants (rId))
    print ('Number of products: ', model.getNumProducts (rId))
    for i in range (model.getNumReactants(rId)):
        print ('Name and stoichiometry of Reactant:', model.getReactant(rId, i), model.getReactantStoichiometry (rId, i))
    for i in range (model.getNumProducts(rId)):
        print ('Name and stoichiometry of Product:', model.getProduct(rId, i), model.getProductStoichiometry (rId, i))
    print ('-------------------------------') 
    
if model.getNumRules() > 0:
    #print ('-------------------------------------------------')
    print ('Rule Details:')
    for i in range (model.getNumRules()):
        ruleType = model.getRuleType (i)  # note argument could also be a Id string
        Id = model.getRuleId(i)
        print ('Rule: ', Id, '(' + ruleType + ') = ', model.getRuleRightSide(i))
           
if model.getNumEvents() > 0:
    print ('-------------------------------------------------')
    print ('Event Details:')
    for i in range (model.getNumEvents()):
        Id = model.getEventId(i) # note argument could also be a Id string
        numAssignments = model.getNumEventAssignments(i)
        print ('Event: ', Id, ', Number of assignments in the event = ', numAssignments)
        print ('Event trigger: ', model.getEventTrigger (i))
        print (model.getEventString (i))
        if i != model.getNumEvents() - 1:
           print ('--------------------------------')

if model.getNumFunctionDefinitions() > 0:
    print ('-------------------------------------------------')
    print ('User Function Details:')
    for i in range (model.getNumFunctionDefinitions()):
        Id = model.getFunctionId(i) # note argument could also be an Id string
        print ('Function: ', Id)
        print ('Arguments: ', model.getListOfArgumentsInUserFunction (i))
        print ('Function body: ', model.getFunctionBody(i))
        print ('--------------------------------')
           