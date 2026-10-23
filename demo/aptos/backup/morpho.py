"""
part of caracol model
Logistic growth function of organs
Parameters of growth : Cost of surface in N, C ... + production of C / surface 
"""

from math import *
from math import exp
import numpy as np

def growth_logistic(ttime, finalsize, tip, b):
    """ A: size max, tip: time at inflexion point, b: slope parameter"""
    return finalsize / (1+exp(-(ttime-tip)/b ))

def growth_rate(ttime, finalsize, tip, b):
    g = exp(-(ttime-tip)/b)
    return(finalsize * g) / (b*pow((1+g), 2))

def sfqn(random = False):
    """ Quantity of N needed per surface unit in mg/cm2. Values between which sfqn is. To calibrate  """
    if random : 
        L = range(10, 25, 1)
        return np.random.choice(L)/100
    else : 
        return(0.18) 

def NgNt():
    """ Proportion of "easily mobilisable" N dedicated to growth """
    return(0.3)

def CostC():
    """ Cost C for cm² of photosynthetic surface. To calibrate"""
    return 0.4

def RUE():
    """ gBM produce per Energy intercepted by leaf. To calibrate """ 
    return(5)

def BT():
    """ Threshold of N storage in the apex to iniate a new leaf """
    return(0.05)

def IoL():
    """ (N for Internode / N for Leaf) repartition ratio """
    return 0.3

def RoH(area):
    """ return the height and radius of a cylinder of given area """
    #r_h = 0.3 #np.random.random()
    r = 0.03
    h = area / (2*np.pi * r)
    return r,h

def ST():
    """ Threshold of N easily remobilizable necessary in the leaf for it to grow """
    return (0.02)