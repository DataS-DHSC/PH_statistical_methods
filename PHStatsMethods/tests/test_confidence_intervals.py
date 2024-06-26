# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:19:46 2024

@author: Annabel.Westermann
"""

import pytest
from ..confidence_intervals import byars_lower, wilson_lower, wilson_upper

@pytest.mark.parametrize('value, confidence, result', [(100, 0.95, 81.36210549052788),
                                                       (200, 0.998, 159.11703750323326)])
def test_byars_lower(value, confidence, result):
    assert byars_lower(value, confidence) == result

def test_byars_upper():
    assert byars_lower(200, 0.998) == 159.11703750323326


@pytest.mark.parametrize('num, denom, confidence, result' , [(20, 360, 0.95, 0.036248204600072345),
                                                             (550, 2400, 0.998, 0.20375892211705743)])
def test_wilson_lower(num, denom, confidence, result):
    assert wilson_lower(num, denom, confidence) == result


@pytest.mark.parametrize('num1, denom1, conf, res', [(30, 400, 0.95, 0.10504770626130437),
                                                     (76, 238, 0.998, 0.418131030603369)])
def test_wilson_upper(num1, denom1, conf, res):
    assert wilson_upper(num1, denom1, conf) == res



