# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:52:06 2020

@author: hsauro
"""

import tellurium as te
import simplesbml

r = te.loada("""
             
    k1 := 3.4
    x' = k1*x
    
    J1: S1 -> S2; k1*S1;
    J2: $S3 -> S3; (k2+k3)*S3
    
    at time > 10: k2 = 200;
    at S1 > S2: k2 = 200/3, k3 = 1.02
    
    k2 = 1.2345; k3 = 0.98776;
    S1 = 10.6; S2 = 0
    S3 = 99.76; x = 0.345
""")

s = simplesbml.sbmlModel (sbmlStr=r.getSBML())

print ('Num compartments = ', s.getNumCompartments())
print ('Num parameters =', s.getNumParameters())
print ('Num species =', s.getNumSpecies())
print ('Num floating species = ', s.getNumFloatingSpecies())
print ('Num floating species = ', s.getNumBoundarySpecies())
print ('Num reactions = ', s.getNumReactions())
print ('List of compartments: ', s.getListOfCompartments())
print ('List of ALL species: ', s.getListOfAllSpecies())
print ('list of floating species = ', s.getListOfFloatingSpecies())
print ('list of boundary species = ', s.getListOfBoundarySpecies())
print ('List of reactions = ', s.getListOfReactions())
print ('List of rules = ', s.getListOfRules())

print ('Compartment values:')
p = s.getListOfCompartments()
for v in p:
    print (v, ': ', s.getCompartmentVolume (v))
    
print ('Parameter values:')
p = s.getListOfParameters()
for v in p:
    print (v, ': ', s.getParameterValue (v))
    
print ('Species values:')
p = s.getListOfAllSpecies()
for v in p:
    print (v, ': ', s.getSpeciesInitialConcentration (v))
 
print ('Rate laws:')
reactions = s.getListOfReactions()
for v in reactions:
    print (v, ': ', s.getRateLaw (v))
    
print ('-------------------------------------------------')
print ('Reaction Details:')
rs = s.getListOfReactions()
for rId in rs:
    print ('Reaction:', rId)
    print ('Number of reactants: ', s.getNumReactants (rId))
    print ('Number of products: ', s.getNumProducts (rId))
    for i in range (s.getNumReactants(rId)):
        print ('Name and stoichiometry of Reactant:', s.getReactant(rId, i), s.getReactantStoichiometry (rId, i))
    for i in range (s.getNumProducts(rId)):
        print ('Name and stoichiometry of Product:', s.getProduct(rId, i), s.getProductStoichiometry (rId, i))
    print ('-------------------------------') 
    
if s.getNumRules() > 0:
    #print ('-------------------------------------------------')
    print ('Rule Details:')
    for i in range (s.getNumRules()):
        ruleType = s.getRuleType (i)  # note argument could also be a Id string
        Id = s.getRuleId(i)
        print ('Rule: ', Id, '(' + ruleType + '), Right-hand side = ', s.getRuleRightSide(i))
           
if s.getNumEvents() > 0:
    print ('-------------------------------------------------')
    print ('Event Details:')
    for i in range (s.getNumEvents()):
        Id = s.getEventId(i) # note argument could also be a Id string
        numAssignments = s.getNumEventAssignments(i)
        print ('Event: ', Id, ', Number of assignments in the event = ', numAssignments)
        print ('Event trigger: ', s.getEventTrigger (i))
        for j in range (numAssignments):
            assignment = s.getEventAssignment (i, j)
            print ("Assignment:", str (j) + ', Formula =', assignment)
        if i != s.getNumEvents() - 1:
           print ('--------------------------------')
    