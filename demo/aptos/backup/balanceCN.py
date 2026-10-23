""" License Cecill-C
balanceCN.py is part of caracol model
A module that 
    (1) Check available N: store, acquired, remobilized
    (2) Distribute N among organs according to rules and hypothesis
        (H1) lux --> N --> dS
        (H2) dvt --> dS --> N
    (3) Check available C : store, acquired, remobilized
    (4) Distribute C among organs according to rules
"""

"H1 : Hypothesis of N repartition according to amount of intercepted light"

import numpy as np
from openalea.mtg import mtg
from demo.aptos.backup.soilN import *
from demo.aptos.backup.morpho import *
from demo.aptos.backup.environment import *
from openalea.lpy import *

""" List of all organs and their attributes. 
For above-ground organs, phytomers are constitued of 
stem, leaf, axillary bud and apical bud. 
Surfaces are in cm2 and C,N quantities in mg or mg/cm2.  """

###############################################################################
# N
def destock_N(stock_N):
    """ Remobilize N stored the previous time step """
    a = 0.99
    return(a*stock_N)

def remobilized_N(organs, Coeff_remob):
    for org in organs : 
        N += N * Coeff_remob
    return(N)

def root_N_need():
    return()

def N_disp_aer():
    """ should be the difference between destockN, remobilized and root need """
    return(0.1)
    
def CN_organ(irr, N_disp_aer = 0.13, what = True):
    """ distributes N between organs according to intercepted light = Leight weight = wi"""
    if sum(irr['Ei']) !=0 : 
        irr.loc[:,'wi'] = irr['Ei']/sum(irr['Ei'])
    else : 
        irr['wi'] = 0
    # attribution of N
    irr.loc[:,'N_attr'] = irr['wi']*N_disp_aer
    
    if what : 
        return irr
    else : 
        return sum(irr['Ei']) * sum(irr['area'])*RUE()
# 1 # 
#N_disp_aer = destock_N(stock_N) + remobilizedN(organs, Coeff_remob) + soilN.N_acquisition() - root_N_need

# Zoom 1 : Balance CN for shoots # 
def balance(lstring, N_disp_aer = 0.13):
    l = Lsystem('plant4.lpy')
    scene = l.sceneInterpretation(lstring)
    cscene, raw, agg = illuminate(scene)
    #_, _ = cscene.plot(raw, maxval = 1.01)
    irr = PS_irradiance(agg, lstring, ['Internode','Petiole','Leaf', 'Apex'])
    # N repartition according to light 
    irr = CN_organ(irr, N_disp_aer) # we get the N attributed to the organ
    return(irr)

# total BM obtained
#BM =  CN_organ(agg, lstring, 'Leaf', False) + CN_organ(agg, lstring, 'Internode', False)

def destock_C(stock_C):
    """ Remobilize C stored the previous time step """
    a=0.99
    return(a*stock_C)
    
def acquis_C(X):
    """ Give C acquired by aerial part according to light interception and
    radiation use efficiency """

    RUE = 6 # mg of Fresh Weight / mole
    PPFDi_tot = sum_organs(X,"leaf","PPFD")
    C_acquis = PPFDi_tot * RUE 
    return(C_acquis) #PPFDi in micromole

######### TIME STEP #########
def time(root, aer, C_stock, N_stock): 
    """ Balance C and N offer and demand. 
    Allocate C and N among organs """
    # Calculating the variables : 
    C_destock = destock_C(C_stock)
    N_destock = destock_N(N_stock)

    # N acquisition and root growth 
    N_acquis = acquis_N(root)
    N_offer = N_destock + N_acquis
    Nr_pot = N_offer 
    dVr_pot = growth_root(root, 1)[1]
    Nr_demand = dVr_pot * cost.root_N
    Cr_demand = dVr_pot * cost.root_C

    # Aer growth and C acquisition
    Na_pot = N_offer - Nr_demand
    aer = light_model(aer)
    aer = light_weight(aer)
    aer = demand_N_aer(aer,Na_pot)
    dSa_pot = growth_aer(aer, 1)[1]
    Ca_demand = dSa_pot * cost.aer_C

    C_acquis = acquis_C(aer)
    C_offer = C_destock + C_acquis
    Ca_pot = C_offer  

    if Ca_demand <= Ca_pot:
        #aerial
        Ca = Ca_demand ; Na = Na_pot
        aer = growth_aer(aer,1)[0]
        #roots
        Cr_pot = Ca_pot - Ca
        if  Cr_demand <= Cr_pot:
            Cr = Cr_demand ; Nr = Nr_pot
            root = growth_root(root,1)[0]
            
            C_stock = C_stock + Cr_pot - Cr
            N_stock = N_stock 

        else :  
            red_r = Cr_pot / Cr_demand
            dVr = growth_root(root, red_r)[1]
            Cr = Cr_pot ; Nr = dVr * cost.root_N
            root = growth_root(root, red)[0]

            C_stock = C_stock 
            N_stock = N_stock + Nr_pot - Nr 

    else : 
        red_a = Ca_pot / Ca_demand
        aer = growth_aer(aer, red_a)[0]
        dSa = growth_aer(aer, red_a)[1]
        Ca = Ca_pot
        Na = dSa / sfqn_tot
        if Na < Na_pot : 
            N_stock = N_stock + Na_pot - Na
        elif Na == Na_pot :
            C_stock = C_stock
            N_stock = N_stock
    
    return(root, aer, C_stock, N_stock)

def new_phyt(aer):
    """ Create new phytomer """
    n = len(aer)
    aer_new = aer[0:n-1] + [aer[n-1][0:2]]
    AP_old = aer[n-1][2]

    S = stem ; L = leaf ; AP = apbud
    [S.area, L.area, AP.area] = [0.47*AP_old.area, 0.47* AP_old.area, 0.06 * AP_old.area ]

    aer_new = aer_new + [[S,L,AP]]

    return(aer_new)