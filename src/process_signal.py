from scipy.signal import savgol_filter,medfilt
import pandas as pd
import numpy as np





def remove_initial_noise(col):
    #the min value is expected to be in the first few timepoints (until 9h?)
    try:
        col=col.dropna()
        col.loc[:col.loc[:9].idxmin()] = col.loc[:9].min()
        return col
    except:
        return np.nan


def smoothen(col,median_kernel=3):
    try:
        median_smoothed=medfilt(col.dropna(),kernel_size=median_kernel)
        savgol_smoothed=savgol_filter(median_smoothed, window_length=7, polyorder=4)
        savgol_smoothed[savgol_smoothed<0]=0
        return pd.Series(savgol_smoothed,index=col.dropna().index)
    except:
        return np.nan
