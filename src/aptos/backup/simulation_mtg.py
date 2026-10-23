
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
from morpho import *
from soilN import *
from environment import *
from balanceCN import *
from copy import deepcopy
from openalea.mtg import *
from openalea.mtg.io import lpy2mtg, mtg2lpy

###################################################################################################
""" Define first plant"""
#### plant, lstring, mtg ####
l = Lsystem('plant4.lpy')
lstring = l.axiom
#g = lpy2mtg(lstring, l)

lstring = ite(lstring)
l.plot(lstring)

for i in range(30):
    lstring = ite(lstring)
###################################################################################################
def ite(lstring):
    g = lpy2mtg(lstring, l)
    # get N available for shoots : 
    N4shoot = N_disp_aer()
    # allocate N between organs according hypothesis : 
    step = balance(lstring, N4shoot)
    # see the potential growth of organs according to newly attributed N 
    N4growth_tot = 0
    for vid in g.VtxList()[1:] : 
        N_attr = step.loc[ g.property('_axial_id')[vid] , 'N_attr']
        P = g.property('parameters')[vid] # change ParameterSet
        P.Nmob += N_attr
        P.N4growth = P.Nmob * NgNt()
        # sum 
        N4growth_tot +=P.N4growth
    # total surface growth : potential new surface
    dS_pot_tot = N4growth_tot / sfqn()
    # BM or C need : 
    C_need_tot = dS_pot_tot * CostC()
    # C available from photosynthesis : 
    C4shoot = step.sum()['Ei']*step.sum()['area']*1e4 * RUE()
    # checking C demand and C offer : satisfaction coefficient growth : 
    if C_need_tot ==0 : 
        satC = -1 # should not occur 
    elif C_need_tot <= C4shoot : 
        satC = 1 # C demand is met, actual growth --> pot growth
    elif C_need_tot > C4shoot : satC = C4shoot/C_need_tot # C demand is not met. growth at the satisfaction ratio
    # actual growth : mtg actualisation of area and N content  
    if satC>=0 : 
        for vid in g.VtxList()[1:-1] : 
            P = g.property('parameters')[vid]
            try: # internode 
                P.height += (satC * P.N4growth * sfqn()) / 2*np.pi* P.radius
                P.Nmob -= satC * P.N4growth 
            except AttributeError : 
                try : # petiole
                    P.length += 0
                    P.Nmob += 0
                except AttributeError: #leaf
                    P.area += satC * P.N4growth / sfqn()
                    P.Nmob -= satC * P.N4growth 

        # new phytomere initiation :     
        if g.property('parameters')[g._id].N4growth >= BT():
            # Add a new metamer with a bud
            P = g.property('parameters')[g._id]
            if P.alpha <360: alpha = P.alpha +90
            else : alpha = 0
            id_li = g._parent[g._id] # id of the last internode
            g.remove_vertex(g._id) # removing the apical bud --> internode + leaf
            id_ni = g.add_child(id_li, label='Internode', edge_type='<', parameters = ParameterSet(Nmob = P.N4growth * IoL(), radius = 0.03, height = 0.01) )
            id_ni = g.add_child(id_ni, label = 'Petiole', edge_type='+', parameters = ParameterSet(Nmob = 0, length=0.1, alpha = P.alpha))
            id_ni = g.add_child(id_ni, label = 'Leaf', edge_type='<', parameters = ParameterSet(Nmob = P.N4growth * (1-IoL()), area = 0.1) )
            g.add_child(id_li, label = 'Apex', edge_type = '<', parameters = ParameterSet(Nmob = P.Nmob - P.N4growth, age = P.age, alpha = alpha))
            
    else : pass
    # mtg to lstring 
    lstring = mtg2lpy(g, l)
    return(lstring)
