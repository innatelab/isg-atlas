import numpy as np
import statsmodels.api as sm
from scipy.optimize import curve_fit
import pandas as pd
from statsmodels.tools.eval_measures import rmse
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

def sigmoid(t, K ,tau, b, c):
    y = K / (1 + np.exp(-b*(t-tau))) + c
    return (y)


def sigmoid_fit(col):
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
        #col=pd.Series(sigmoid(col.index,K,tau,beta,c),index=col.index)
        #return col
        return pd.Series({
        'c':c, 
        'K':K,
        'beta':beta,
        'tau':tau,
        "r_squared":r_squared,
        "r_squared_adj":r_squared_adj,
        "rmse":rmse_,
        # "fitted_values":pd.Series(fitted_values,index=col.index),
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
        # "fitted_values":np.nan,
        })


def exp_func(t, a, b):
    return a * np.exp(b * t)

def exponential_fit(col):
    col=col.dropna()
    t=col.index
    y=col.values.flatten()
    p0 = [y[0], np.log(y[-1]/y[0]) / (t[-1]-t[0])]
    try:
        popt, _ = curve_fit(exp_func, t, y, p0)
        r_squared=r2_score(y,exp_func(t,*popt))
        r_squared_adj=1-(1-r_squared)*(len(col)-1)/(len(col)-len(popt)-1)
        # fitted_values=pd.Series(exp_func(x,*popt),index=x)
        a=popt[0]
        b=popt[1]
        #fitted_values=pd.Series(exp_func(x,*popt),index=x)
    except:
        a=np.nan
        b=np.nan
        r_squared=np.nan
        r_squared_adj=np.nan
        #fitted_values=np.nan
    return pd.Series({
        "starting_GII":a,
        "growth_rate":b,
        'r_2':r_squared,
        'r_2_adj':r_squared_adj,
        #"fitted_values":fitted_values
    })

def viability_linear_fit(col):
    col=col.dropna()
    X = col.index.values.reshape(-1, 1)
    y = col.values
    reg=LinearRegression().fit(X,col.dropna())
    return pd.Series({'initial_conf':reg.intercept_,'growth_rate':reg.coef_[0]})

