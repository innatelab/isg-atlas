import pandas as pd
import numpy as np
import os
import re
from src.virus2mock import virus2mock

def read_incucyte_txt_file(txt_file_path):
    '''Reads the txt file exported from the Incucyte software and returns a dataframe'''
    df=pd.read_csv(txt_file_path, skiprows=6,decimal=',', sep='\t',).drop(['Date Time'], axis=1).set_index('Elapsed')
    
        #some of the columns are not numeric and escapes the decimal=',' option, also there are some spaces in the data
    df=df.replace(',','.',regex=True).replace(' ',np.nan).astype(float)
    return df

def read_flrsc_data(flrsc_path,id2virus):
    '''Reads the flrsc data and returns a dataframe'''
    flrsc_txt_files=os.listdir(flrsc_path)
    dfs=[]
    for flrsc_txt_file in flrsc_txt_files:
        virus_plate_id=flrsc_txt_file.strip('.txt')
        virus_id, set_, bio_rep = re.match('V(\d)_S(\d)_R(\d)', virus_plate_id).groups()
        virus=id2virus[virus_id]
        mock_plate_id = virus2mock.get(f'V{virus_id}_S{set_}_R{bio_rep}',np.nan)
        
        flrsc_df=read_incucyte_txt_file(flrsc_path / flrsc_txt_file)
    
        flrsc_df.columns=pd.MultiIndex.from_product([[virus], [set_], [bio_rep],[mock_plate_id],flrsc_df.columns],names=['virus','set','bio_rep','mock_plate_id','knockout'])
        dfs.append(flrsc_df)
    df=pd.concat(dfs, axis=1).sort_index(axis=1,ascending=True).sort_index()
    return df

def read_viability_data(viability_path):
    '''Reads the viability data and returns a dataframe'''
    txt_files=sorted(os.listdir(viability_path))
    dfs=[]
    for txt_file in txt_files:
        mock_plate_id = txt_file.strip('.txt')
        set_,bio_rep = re.match('V0_S(\d)_R(\d)', mock_plate_id).groups()
        virus="mock"
        df=pd.read_csv(viability_path / txt_file, skiprows=6,decimal=',', sep='\t',).drop(['Date Time'], axis=1).set_index('Elapsed')

        #some of the columns are not numeric and escapes the decimal=',' option, also there are some spaces in the data
        df=df.replace(',','.',regex=True).replace(' ',np.nan).astype(float)
        df.columns=pd.MultiIndex.from_product([[mock_plate_id],df.columns],names=['mock_plate_id','knockout'])
        dfs.append(df)
    
    df=pd.concat(dfs, axis=1).sort_index(axis=1,ascending=True)
    return df

def split_good_bad_runs(df,format="long"):
    '''Splits the dataframe into good and bad runs based on whether the entire row or column is NaN'''
    if format=="long":
        bad_runs=df.loc[df.isna().all(axis=1),:]
        good_runs=df.drop(bad_runs.index,axis=0)
    else:
        bad_runs=df.loc[:,df.isna().all(axis=0)]
        good_runs=df.drop(bad_runs.columns,axis=1)
    return good_runs,bad_runs
