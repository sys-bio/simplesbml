# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:27:57 2020

@author: hsauro
"""

import json

model = """
        S1 -> S2; k1*S1;
        k1 = 0.1; S1 = 10; S2 = 2.5
        """
with open ('testModel1.ant', 'w') as f:
     f.write (model)
    
data = {'modeFileName': 'testModel1.ant', 
        'getNumCompartments': {'argument': None, 'results': 1},
        'getNumSpecies': {'argument': None, 'results': 2},
        'numFloatingSpecies': {'argument': None, 'results': 2},
        'numBoundarySpecies': {'argument': None, 'results': 0},
        'listOfAllSpecies': {'argument': None, 'results': ['S1', 'S2']},
        'getNthFloatingSpeciesId': {'argument': [0, 1], 'results': ['S1', 'S2']},
        'isSpeciesValueSet': {'argument': ['S1','S2'], 'results': [True, True]},
        'isFloatingSpecies': {'argument': ['S1', 'S2'], 'results': [True, True]},
        'isBoundarySpecies': {'argument': ['S1', 'S2'], 'results': [False,False]},
        'getSpeciesInitialConcentration': {'argument': ['S1','S2'], 'results': [10,2.5]},
        'listOfFloatingSpecies': {'argument': None, 'results': ['S1', 'S2']},
        'listOfBoundarySpecies': {'argument': None, 'results': []},
        'isConcentration': {'argument': 'S1', 'results': True},
        'getNumParameters': {'argument': None, 'results': 1},
        'getListOfParameters': {'argument': None, 'results': ['k1']},
        'getParameterId': {'argument': [0], 'results': ['k1']},
        'isParameterValueSet': {'argument': 'k1', 'results': True},
        'getParameterValue': {'argument': ['k1'], 'results': [0.1]},
        'getNumReactions': {'argument': None, 'results': 1},
        'getNumRules': {'argument': None, 'results': 0},
        'getNumEvents': {'argument': None, 'results': 0},
        'getNthReactionId': {'argument': [0], 'results': ['_J0']},
        'getNumReactants': {'argument': [0], 'results': [1]},
        'getNumProducts': {'argument': [0], 'results': [1]},
        'getRateLaw': {'argument': [0], 'results': ['k1*S1']},
        'getReactant': {'argument': [['_J0', 0]], 'results': [['S1']]},
        'getProduct': {'argument': [['_J0', 0]], 'results': [['S2']]},
        'getReactantStoichiometry': {'argument': [['_J0', 0]], 'results': [[1]]},
        'getProductStoichiometry': {'argument': [['_J0', 0]], 'results': [[1]]}
        }
 
with open ('testModel1.json', 'w') as json_file:
    json.dump (data, json_file)
    
# ================================================================================
    
model = """
       $S1 -> S2; k1*S1;
        S2 -> S3; k2*S2-k3*S3
        k1 = 0.1; k2 = 0.2; k3 = 0.3
        S1 = 10; S2 = 2.5; S3 = 3.4
        """
with open ('testModel2.ant', 'w') as f:
     f.write (model)
    
data = {'modeFileName': 'testModel2.ant', 
        'getNumCompartments': {'argument': None, 'results': 1},
        'getNumSpecies': {'argument': None, 'results': 3},
        'numFloatingSpecies': {'argument': None, 'results': 2},
        'numBoundarySpecies': {'argument': None, 'results': 1},
        'listOfAllSpecies': {'argument': None, 'results': ['S1', 'S2', 'S3']},
        'getNthFloatingSpeciesId': {'argument': [0, 1], 'results': ['S2', 'S3']},
        'isSpeciesValueSet': {'argument': ['S1', 'S2', 'S3'], 'results': [True, True, True]},
        'isFloatingSpecies': {'argument': ['S1', 'S2', 'S3'], 'results': [False, True, True]},
        'isBoundarySpecies': {'argument': ['S1', 'S2', 'S3'], 'results': [True, False, False]},
        'getSpeciesInitialConcentration': {'argument': ['S1','S2'], 'results': [10, 2.5]},
        'listOfFloatingSpecies': {'argument': None, 'results': ['S2', 'S3']},
        'listOfBoundarySpecies': {'argument': None, 'results': ['S1']},
        'isConcentration': {'argument': 'S1', 'results': True},
        'getNumParameters': {'argument': None, 'results': 3},
        'getListOfParameters': {'argument': None, 'results': ['k1', 'k2', 'k3']},
        'getParameterId': {'argument': [0, 1, 2], 'results': ['k1', 'k2', 'k3']},
        'isParameterValueSet': {'argument': 'k1', 'results': True},
        'getParameterValue': {'argument': ['k1','k2', 'k3'], 'results': [0.1, 0.2, 0.3]},
        'getNumReactions': {'argument': None, 'results': 2},
        'getNumRules': {'argument': None, 'results': 0},
        'getNumEvents': {'argument': None, 'results': 0},
        'getNthReactionId': {'argument': [0, 1], 'results': ['_J0', '_J1']},
        'getNumReactants': {'argument': [0, 1], 'results': [1, 1]},
        'getNumProducts': {'argument': [0, 1], 'results': [1, 1]},
        'getRateLaw': {'argument': [0], 'results': ['k1*S1']},
        'getReactant': {'argument': [['_J0', 0]], 'results': [['S1']]},
        'getProduct': {'argument': [['_J0', 0]], 'results': [['S2']]},
        'getReactantStoichiometry': {'argument': [['_J0', 0]], 'results': [[1]]},
        'getProductStoichiometry': {'argument': [['_J0', 0]], 'results': [[1]]}
        }
 
with open ('testModel2.json', 'w') as json_file:
    json.dump (data, json_file)
    