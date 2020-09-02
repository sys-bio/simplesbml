# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:27:57 2020

@author: hsauro
"""

import json

model = """
        S1 -> S2; k1*S1;
        k1 = 0.1; S1 = 10; S2 = 0
        """

with open ('testModel1.ant', 'w') as f:
     f.write (model)
    
   
data = {'modeFileName': 'testModel1.ant', 
        'numCompartments': {'argument': 0, 'results': 1},
        'numSpecies': {'argument': 0, 'results': 2},
        'numFloatingSpecies': {'argument': 0, 'results': 2},
        'numBoundarySpecies': {'argument': 0, 'results': 0},
        'listOfAllSpecies': {'argument': 0, 'results': ['S1', 'S2']},
        'NthFloatingSpeciesId_0': {'argument': 0, 'results': 'S1'},
        'NthFloatingSpeciesId_1': {'argument': 1, 'results': 'S2'},
        'isSpeciesValueSet_0': {'argument': 'S1', 'results': True},
        'isSpeciesValueSet_1': {'argument': 'S2', 'results': True},
        'isFloatingSpecies_0': {'argument': 'S1', 'results': True},
        'isFloatingSpecies_1': {'argument': 'S2', 'results': True},
        'isBoundarySpecies_0': {'argument': 'S1', 'results': False},
        'isBoundarySpecies_1': {'argument': 'S2', 'results': False}}
        
with open ('testModel1.json', 'w') as json_file:
    json.dump (data, json_file)
    