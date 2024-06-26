# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:22:46 2024

@author: Annabel.Westermann
"""
import pandas as pd

from pandas.testing import assert_frame_equal
from pathlib import Path

from ..means import ph_mean

class TestMean:
    path = Path(__file__).parent / 'test_data/testdata_Mean.xlsx'
    
    data = pd.read_excel(path, sheet_name = 'testdata_Mean')
    results = pd.read_excel(path, sheet_name = 'testdata_Mean_results')
    results_NA = pd.read_excel(path, sheet_name = 'testdata_Mean_results_NA', na_values = "NA")
    
    
    def test_default_group(self):
        df = ph_mean(self.data.iloc[:-1], 'values', 'area').drop(['Confidence'], axis=1)
        df2 = self.results.iloc[:2, :].drop(['lower_99_8_ci', 'upper_99_8_ci'], axis=1)
        assert_frame_equal(df, df2)
        
    def test_2ci(self):
        df = ph_mean(self.data.iloc[:-1], 'values', 'area', confidence = [0.95, 0.998]).drop('Confidence', axis=1)
        df2 = self.results.iloc[:2, :]
        assert_frame_equal(df, df2)
        
    def test_NAs(self):
        df = ph_mean(self.data, 'values', 'area').drop(['Confidence'], axis=1)
        df2 = self.results_NA.iloc[:2, :].drop(['lower_99_8_ci', 'upper_99_8_ci'], axis = 1)
        assert_frame_equal(df, df2)
