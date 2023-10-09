import numpy as np
import statsmodels.api as sm
from scipy.optimize import curve_fit
import pandas as pd
from statsmodels.tools.eval_measures import rmse
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

def sigmoid(t, K ,tau, b, c):
    '''Sigmoid function of the form K/(1+exp(-b*(t-tau))) + c'''
    y = K / (1 + np.exp(-b*(t-tau))) + c
    return (y)


def sigmoid_fit(col):
    '''Fit a sigmoid to a column of data'''
    try:
        col=col.dropna().truncate(after=col.idxmax())
        if len(col)<=4:
            raise "Not enough data points to fit sigmoid"
        K_temp=col.max()
        p0 = [max(col.values), col.index[np.searchsorted(col,K_temp/2)],0.2,min(col.values)]
        popt, pcov = curve_fit(sigmoid, col.index, col.values.flatten(),p0, method='dogbox')
        K,tau,beta,c=list(popt)
        fitted_values=sigmoid(col.index,K,tau,beta,c)
        rmse_=rmse(col.values.flatten(),fitted_values)
        r_squared=r2_score(col.values.flatten(),fitted_values)
        r_squared_adj=1-(1-r_squared)*(len(col)-1)/(len(col)-len(popt)-1)
        return pd.Series({
        'c':c, 
        'K':K,
        'beta':beta,
        'tau':tau,
        "r_squared":r_squared,
        "r_squared_adj":r_squared_adj,
        "rmse":rmse_,
        })
    except:
        return  pd.Series({
        'c':np.nan, 
        'K':np.nan,
        'beta':np.nan,
        'tau':np.nan,
        "r_squared":np.nan,
        "r_squared_adj":np.nan,
        "rmse":np.nan,
        })


def exp_func(t, a, b):
    '''Exponential function of the form a*exp(b*t)'''
    return a * np.exp(b * t)

def exponential_fit(col):
    '''Fit an exponential to a column of data'''
    col=col.dropna()
    t=col.index
    y=col.values.flatten()
    p0 = [y[0], np.log(y[-1]/y[0]) / (t[-1]-t[0])]
    try:
        popt, _ = curve_fit(exp_func, t, y, p0)
        r_squared=r2_score(y,exp_func(t,*popt))
        r_squared_adj=1-(1-r_squared)*(len(col)-1)/(len(col)-len(popt)-1)
        a=popt[0]
        b=popt[1]
    except:
        a=np.nan
        b=np.nan
        r_squared=np.nan
        r_squared_adj=np.nan
    return pd.Series({
        "starting_GII":a,
        "growth_rate":b,
        'r_squared':r_squared,
        'r_squared_adj':r_squared_adj,
    })

def viability_linear_fit(col):
    col=col.dropna()
    X = col.index.values.reshape(-1, 1)
    y = col.values
    reg=LinearRegression().fit(X,col.dropna())
    return pd.Series({'initial_conf':reg.intercept_,'growth_rate':reg.coef_[0]})

