""" Integration of C,N disponibility and
thermal time
* modification of organs properties
    (1) size
    (2) growth rate
    (3) senescence state
* modification of the number of organs 
    (1) apical growth
    (2) branching ??
* modification of organs relations : 
    (1) rosette -> 
    (2) bolting
    (3) flourishing
    (4) fructification
"""
from openalea import *
from openalea.lpy import *
from openalea.plantgl.all import *
from demo.aptos.backup.morpho import *
from demo.aptos.backup.soilN import *
from demo.aptos.backup.environment import *
from demo.aptos.backup.balanceCN import *
from copy import deepcopy

# Development (derivation) if resources and thermaltime #
"""derive(lstring, corresponding iteration number, nb of iterations to apply) """

###################################################################################################
""" Define first plant"""
#### Phenological parameters ####
transition1 = 50 #rosette -> bolting (degree days) Jullien et al. 2011
transition2 = 300#bolting -> flower (days)
transition3 = 345 #flower -> fruits (days)
l = Lsystem('interpret.lpy')
# Define Axiom :
pI = ParameterSet(radius = 0.03, height = 0.06)
pP = ParameterSet(length = 0.01)
pL = ParameterSet(area = 1)
pA = ParameterSet(age = 0)
lstring = Lsystem('plant3.lpy', {'pI':pI, 'pP':pP, 'pL':pL, 'alpha':0}).axiom +Lsystem('Bud.lpy', {'pA':pA}).axiom
tt,i = 1,0
plant = balance(lstring, 0)
plant = plant.loc[:, ['area','rank', 'Organ']]   
plant.loc[:,'Ntot'] = [0.5, 0.5, 0.1]

###################################################################################################
biblio = []
init = False
for k in range(1,60):
    # balance N
    N_disp_aer = 0.1
    step = balance(lstring, 0.1)
    step = step.loc[:, ['rank','Organ', 'N_attr']]
    plant = pandas.merge(plant, step, on=['rank', 'Organ'])
    plant.loc[:,'Ntot'] = plant.loc[:,'Ntot'] + plant['N_attr']
    plant = plant.loc[:, ['area', 'rank', 'Organ', 'Ntot']]

    # phytomere initiation
    N4bud = plant[plant['Organ']=='Apex'].iloc[0]['Ntot']
    if N4bud >= BT() : 
        # create new lines in df with increase
        newI = dict(zip(plant.columns,[0, max(plant['rank'])+1, 'Internode', IoL()*N4bud]))
        newL = dict(zip(plant.columns,[0, max(plant['rank'])+1, 'Leaf',(1-IoL())*N4bud]))
        newA = dict(zip(plant.columns,[0, 1, 'Apex',0]))
        plant = plant.loc[plant['Organ']!='Apex', :]
        plant = plant.append(newI, ignore_index = True)
        plant = plant.append(newL, ignore_index = True)
        plant = plant.append(newA, ignore_index = True) 
        init = True
    
    # surface growth
    """ Hypothesis : a part NgNt of allocated N is dedicated to growth. 
    For the moment, we consider C never limiting """
    plant.loc[:,'N4S'] = plant.loc[:,'Ntot'] * NgNt()
    plant.loc[:,'dS'] = plant.loc[:,'N4S']/sfqn()
    plant.loc[plant['Organ']=='Apex']['N4S']=0 # apex correction 
    plant.loc[:,'Ntot'] = plant.loc[:,'Ntot'] - plant.loc[:,'N4S']

    # lstring actualisation
    j= Lsystem().axiom #empty AxialTree 
    alpha =0
    for rank in pandas.unique(plant['rank']): 
        P=[]
        for org in ['Internode', 'Leaf']:
        #for org in plant[plant['Organ']!='Apex'][plant['rank']==i]['Organ']:
            former_S = plant[plant['Organ']=='Leaf'][plant['rank']==rank]['area'].iloc[0]
            dS = plant[plant['Organ']== org][plant['rank']==rank]['dS'].iloc[0]
            if org == 'Internode':
                R,H = RoH(former_S*1e4)
                r,h  = RoH(dS)
                P+=[ParameterSet(radius = R+r, height = H+h)]
            else : 
                a =  dS + former_S*1e4
                P += [ParameterSet(area = a)]
        if alpha <360 : alpha+=90
        else : alpha =0
        pI, pL = P
        j += Lsystem('plant3.lpy', {'pI':pI, 'pP':pP, 'pL':pL, 'alpha':alpha}).axiom 
    # adding apex # 
    dS = plant[plant['Organ']=='Apex']['dS'].iloc[0]
    a =  dS + plant[plant['Organ']=='Apex']['area'].iloc[0] *1e4
    pA = ParameterSet(area =a) 
    j+= Lsystem('Bud.lpy', {'pA':pA}).axiom
    lstring = j
    biblio +=[j]
