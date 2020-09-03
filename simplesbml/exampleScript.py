# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 19:59:46 2020

@author: hsauro
"""

# Example script, uses simplesbml to create a stoichiometry matrix 

import tellurium as te, simplesbml, numpy as np

r = te.loada("""
S0 + S3 -> S2; k0*S0*S3;
S3 + S2 -> S0; k1*S3*S2;
S5 -> S2 + S4; k2*S5;
S0 + S1 -> S3; k3*S0*S1;
S5 -> S0 + S4; k4*S5;
S0 -> S5; k5*S0;
S1 + S1 -> S5; k6*S1*S1;
S3 + S5 -> S1; k7*S3*S5;
S1 -> $S4 + S4; k8*S1;

S0 = 0; S1 = 0; S2 = 0; S3 = 0; S4 = 0; S5 = 0;
k0 = 0; k1 = 0; k2 = 0; k3 = 0; k4 = 0
k5 = 0; k6 = 0; k7 = 0; k8 = 0
""")

model = simplesbml.loadSBMLStr(r.getSBML())

# Allocate space for the stoichiometry matrix
stoich = np.zeros((model.getNumFloatingSpecies(), model.getNumReactions()))
for i in range (model.getNumFloatingSpecies()):
    floatingSpeciesId = model.getNthFloatingSpeciesId (i)
    
    for j in range (model.getNumReactions()):
        productStoichiometry = 0; reactantStoichiometry = 0

        numProducts = model.getNumProducts (j)
        for k1 in range (numProducts):
            productId = model.getProduct (j, k1)

            if (floatingSpeciesId == productId):
               productStoichiometry += model.getProductStoichiometry (j, k1)

        numReactants = model.getNumReactants(j)
        for k1 in range (numReactants):
            reactantId = model.getReactant (j, k1)
            if (floatingSpeciesId == reactantId):
               reactantStoichiometry += model.getReactantStoichiometry (j, k1)

        st = int(productStoichiometry - reactantStoichiometry)
        stoich[i,j] = st
    
print (stoich)

