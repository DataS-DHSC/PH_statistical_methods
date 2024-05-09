# -*- coding: utf-8 -*-

import re
import pandas as pd
from scipy.special import ndtri
from scipy.stats import chi2

def get_calc_variables(a):
    """
    Creates the cumulative normal distribution and z score for a given alpha

    :param a: alpha
    :return: cumulative normal distribution, z score
    """
    norm_cum_dist = ndtri((100 + (100 - (100 * (1-a)))) / 200)
    z = ndtri(1 - (1-a )/ 2)
    return norm_cum_dist, z


def euro_standard_pop():
    
    esp_age_bands = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34',
                  '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
                  '65-69', '70-74', '75-79', '80-84', '85-89', '90+']
    
    pops = [5000, 5500, 5500, 5500, 6000, 6000, 6500, 7000, 7000, 7000, 
            7000, 6500, 6000, 5500, 5000, 4000, 2500, 1500, 1000]
    
    data = pd.DataFrame({'age_group': age_groups,
                         'populations': pops})
    
    return data


def join_euro_standard_pops(df, age_col, group_cols = None):
    
    # Check number of rows
    if group_cols is not None:
        n_group_rows = df.groupby(group_cols).size().reset_index(name='counts')
    
        if n_group_rows.counts.nunique() > 1:
            raise ValueError('There must be the same number of rows per group')
            
        if n_group_rows.counts.unique() != 19:
            raise ValueError('There must be 19 rows of data per group')
            
    else:
        if len(df) != len(age_df):
            raise ValueError('Dataframe, if ungrouped, must have same number of rows as reference data')
    
    # Get euro standard pops and rank order
    esp = euro_standard_pop()
    esp['n1'] = esp['esp_age_bands'].rank()
    
    # Get first number of age and sort ascending
    df['n1'] = df.apply(lambda x: str(re.findall(r'(\d+)', x[col])[0]), axis=1)
    
    if df['n1'].nunique() == (len(df) if group_cols is None else n_group_rows.counts.unique()):
        raise ValueError('There are duplicate minimum ages, which is not accepted as the function orders by the first number in each age band.\
                         For example, <5 and 5-10 IS NOT accepted but <=4 and 5-10 IS accepted.')
    
    # order df values and assign over window
    df = df.sort_values(by='n1')
    if group_cols is not None:
        df['n1'] = df.groupby(group_cols)['n1'].rank()
    else:
        df['n1'] = df['n1'].rank()
    
    # join by columns
    df = df.merge(age_df, how='left', on='n1').drop('n1', axis=1)
    
    return df
    

