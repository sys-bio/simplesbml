# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 15:26:54 2015

@author: carolc24
"""

import simplesbml

enzyme = simplesbml.sbmlModel(); #Create new model
enzyme.addSpecies('Glucose', 3.4); #Add 3.4 moles of species 'Glucose' 
enzyme.addSpecies('[ATP]', 1.0); #Add 1.0 M of species 'ATP' (in concentration instead of amount)
enzyme.addSpecies('[G6P]', 0.0); 
enzyme.addSpecies('[ADP]', 0.0);
enzyme.addParameter('k1', 0.1); #Default units are 1/s
enzyme.addParameter('fracATP', 1.0, units='dimensionless'); #For assignment rule later
enzyme.addReaction(['Glucose', 'ATP'], ['2 G6P', 'ADP'], 'kp*Glucose*ATP', local_params={'kp':0.1}); #Glucose+ATP -> 2G6P+ADP
enzyme.addEvent('G6P == 1', {'k1':'0.3'}); #When [G6P] = 1 mol/L, k1 is reassigned as 0.3
enzyme.addAssignmentRule('fracATP', 'ATP/(ATP+ADP)'); #Parameter fracATP is equal to ATP/(ATP+ADP)

code1 = simplesbml.writeCode(enzyme.document); #Produces code to create model 'enzyme' in string format
