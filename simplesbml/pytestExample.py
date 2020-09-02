# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:35:23 2020

@author: hsauro
"""

import pytest
import os
import json

testFile = '.\\testfiles\\testModel1'
testDataFileName = os.path.join(os.path.dirname(__file__), testFile + '.ant')
data = json.load (open (testFile + '.json'))

import pytest
@pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_eval(input, expected):
    assert eval(input) == expected
    
pytest.main()