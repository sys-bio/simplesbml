# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:52:06 2020

@author: hsauro
"""

import tellurium as te
import simplesbml

r = te.loada("""
             
    k1 := 3.4
    
    S1 -> S2; k1*S1;
    $S3 -> S3; k2*S3
    
    k2 = 1.2345
    S1 = 10.6; S2 = 0
    S3 = 99.76
""")

s = simplesbml.sbmlModel (sbmlStr=r.getSBML())

print ('Num compartmetns = ', s.getNumCompartments())
print ('Num parameters =', s.getNumParameters())
print ('Num species =', s.getNumSpecies())
print ('Num floating species = ', s.getNumFloatingSpecies())
print ('Num floating species = ', s.getNumBoundarySpecies())
print ('Num reactions = ', s.getNumReactions())
print (s.getListOfCompartments())
print (s.getListOfAllSpecies())
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
    
print ('Reaction Details:')
rs = s.getListOfReactions()
for rId in rs:
    print ('Reaction:', rId)
    print ('Number of reactants: ', s.getNumReactants (rId))
    print ('Number of products: ', s.getNumProducts (rId))
    for i in range (s.getNumReactants(rId)):
        print ('Name and stoichiometry of Reactant:', s.getReactant(rId, i), s.getReactantStoichiometry (rId, i))
    for i in range (s.getNumProducts(rId)):
        print ('Name and stoichiometry of Reactant:', s.getProduct(rId, i), s.getProductStoichiometry (rId, i))
    
    
    