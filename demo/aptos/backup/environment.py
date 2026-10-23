"""
environment.py is part of caracol model
An above-ground environment module 
* spatial light model distribution
* temperature
* spatialized light acquisition
* degree day cumulation
"""
import pandas
import numpy as np
from openalea.plantscan3d import *
from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.light import light_source

""" copié collé de light_it.py """
def illuminate(scene, light = None, pattern = None, scene_unit = 'cm'):
    infinite = False
    if pattern is not None:
        infinite = True
    cs = CaribuScene(scene, light = light, scene_unit = scene_unit, pattern=pattern)
    raw, agg = cs.run(direct = True, simplify = True, infinite = infinite)
    return(cs, raw['Ei'], pandas.DataFrame(agg))

# light received by the leaves ##
def PS_irradiance(df, lstring, org_list, aggregate = False):
    f = pandas.DataFrame([])
    for name in org_list : 
        organs = [pid for pid,m in enumerate(lstring) if m.name ==name]
        if len(organs) > 0:
            temp = df.loc[df.index.isin(organs),:].copy()
            temp.loc[:, 'rank'] = range(1, len(organs)+1)
            temp.loc[:, 'Organ'] = name
        f = pandas.concat([f, temp])
    if aggregate : 
        f = f.apply(numpy.mean)
    return f

