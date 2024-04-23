# -*- coding: utf-8 -*-
"""
Created on Tue Apr 02 15:05:42 2024

@author: Hadley.Nanayakkara
"""

import pytest
import pandas as pd
from validation import metadata_cols, ci_col, check_cis, format_args, check_arguments, validate_data

class Test_metadata_cols:

    df = pd.DataFrame({'area': [1, 2]*6,
                    'area2': ['Area7', 'Area2','Area1']*4,
                    'num': [None, 82, 9, 48, 65, 8200, 10000, 10000, 8, 7, 750, 900],
                    'den': [10000, 10000, 10000, 10000] * 3})

    def test_cols(self):
        metadata_cols(self.df, "Percentage", confidence = None, method = "Wilsons")
        assert self.df.loc[0, "Statistic"] == "Percentage"
        assert "Method" not in self.df.columns # A method shoud not be provided if there are no CIs

    def test_single_confidence(self):
        metadata_cols(self.df, "Percentage", confidence = [0.95], method = "Wilsons")
        assert self.df.loc[0, "Method"] == "Wilsons"
        assert self.df.loc[0, "Confidence"] == "95%"

    def test_multi_confidence(self):
        metadata_cols(self.df, "Percentage", confidence = [0.9, 0.95, 0.998], method = None)
        assert self.df.loc[0, "Confidence"] == "90%, 95%, 99.8%"



# ci_col()
def test_ci_col_error():
    with pytest.raises(ValueError, match = "'ci_type' must be either 'upper', 'lower' or None"):
        ci_col(0.95, ci_type = "Invalid")

def test_ci_col_format():
        assert ci_col(0.95, ci_type = "lower") == "lower_95_ci"
        assert ci_col(0.998, ci_type = "upper") == "upper_99_8_ci"



# check_cis()
def test_ci_check_float():
    with pytest.raises(TypeError, match = "Confidence intervals must be of type: float"):
        check_cis([0.95, 1]) 

def test_ci_check_range():
    with pytest.raises(ValueError, match = "Confidence intervals must be between 0.9 and 1"):
        check_cis([0.89, 0.99]) 

def test_ci_check_round_er():
    with pytest.raises(ValueError, match = 'There are duplicate confidence intervals (when rounded to 4dp)*'): # regex doesn't like :
        check_cis([0.96741, 0.96742])

def test_ci_check_rounding():
    check_cis([0.95999, 0.99899, 0.96741]) == [0.96, 0.999, 0.9674]



# format_args()
def test_format_args():
    format_args(0.95, "col1") == ([0.95], ['col1'])



# check_arguments()
def test_check_arguments_df():
    data = [('area1', 30, 40), ('area1', 25, 50)]
    with pytest.raises(ValueError, match = "'df' argument must be a Pandas DataFrame"):
        check_arguments(data, "num", None)

class check_args: 

    df = pd.DataFrame({'area': [1, 2]*6,
                'area2': ['Area7', 'Area2','Area1']*4,
                'num': [None, 82, 9, 48, 65, 8200, 10000, 10000, 8, 7, 750, 900],
                'den': [10000, 10000, 10000, 10000] * 3})

    def test_check_arguments_quotes(self):
        with pytest.raises(TypeError, match = "Column names must be a quoted string"):
            check_arguments(self.df, ["num", 50], metadata = None)

    def test_check_arguments_header(self):
        with pytest.raises(ValueError, match = "denom_col is not a column header"):
            check_arguments(self.df, ["num", "denom_col"], metadata = None)

    def test_check_arguments_metadata(self):
        with pytest.raises(TypeError, match = "'metadata' must be either True or False"):
            check_arguments(self.df, ["num"], metadata = "Invalid")

# validate_data
    def test_validate_data_group_cols(self):
        with pytest.raises(TypeError, match = "Pass 'group_cols' as a list"):
            validate_data(self.df, "num", "area", True, denom_col = "den")

# validate_data
def test_validate_data_dtype():
    df = pd.DataFrame({'area': [1, 2], 'num': ["1", "82"], 'den': [10000, 10000]})
    with pytest.raises(TypeError, match = "'num' column must be a numeric data type"):
        validate_data(df, "num", ["area"], True, denom_col = "den")

def test_validate_data_neg():
    df = pd.DataFrame({'area': [1, 2], 'num': [-1, 82], 'den': [10000, 10000]})
    with pytest.raises(ValueError, match = "No negative numbers can be used to calculate these statistics"):
        validate_data(df, "num", ["area"], True, denom_col = "den")

def test_validate_data_den0():
    df = pd.DataFrame({'area': [1, 2], 'num': [0, 82], 'den': [0, 10000]})
    with pytest.raises(ValueError, match = "Denominators must be greater than zero"):
        validate_data(df, "num", ["area"], True, denom_col = "den")

def test_validate_data_den0():
    df = pd.DataFrame({'area': [1, 2], 'num': [5, 82], 'den': [1, 10000]})
    with pytest.raises(ValueError, match = "Numerators must be less than or equal to the denominator"):
        validate_data(df, "num", ["area"], True, denom_col = "den")