from openalea.mtg import *
from openalea.mtg.turtle import *

from numpy import *
import numpy as np
from pandas import *

#######################################

def update_MTG(g, outputs):
    """
    Update the MTG 
    :param dict outputs: {'param1': { vid1: , vid2, ...}, 'param2': { vid1: , vid2, ...}}
    """
     # add the missing property
    for param in outputs.keys():
        if param not in g.properties():
            g.add_property(param)
        # update the MTG
        g.property(param).update(outputs[param])

###########################################
        
def generate_normalized_bell_curve_points(mean, std_dev, amplitude, N):
    """ returns the leaf area of individual leaves along a bell shaped model, as a proportion of the total leaf area """
    x_values = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, N)
    y_values = amplitude * np.exp(-0.5 * ((x_values - mean) / std_dev)**2)
    
    # Normalize y values to ensure the sum is 1
    normalized_y_values = y_values / np.sum(y_values)
    
    points = list(normalized_y_values)
    return points

############################################

def faba_bean_phenotype(g,
                        node_length: float = 1.5,
                        leaf_max: float=0.444,
                        sd: float= 0.223, 
                        amp: float=0.297,
                        phyllot : float = 150,
                        ins_angle : float = 17.3,
                        leaf_angle : float = 60, #?
                        total_surface: float=149.7932, 
                        coeff_width: float =0.65861731722, 
                        coeff_petiole: float =0.51017, #limb length to petiole length , 0.31017 length/whole leag length
                        stem_d: float=0.15850526,#?
                        coeff_petiole_d : float=0.5):

    outputs = dict()

    l = [k for k, v in g.properties()['label'].items()  if v =='FababeanLeaf']
    p = [k for k, v in g.properties()['label'].items()  if v =='Plant']
    i = [k for k, v in g.properties()['label'].items()  if v=='Internode']

    keys = [k for k, v in g.properties()['Species'].items() if v =='Faba bean']

    leaves = [k for k in keys if k in l]
    plants = [k for k in keys if k in p]
    internodes  = [k for k in keys if k in i]

    surface =generate_normalized_bell_curve_points(mean=leaf_max,std_dev=sd,amplitude=amp,N=int(len(leaves)/len(plants)))

    outputs['SurfaceRepartition']=dict(zip(leaves,surface*len(leaves)))
    outputs['LeafSurface']=dict(zip(leaves,[element * total_surface for element in surface]*len(leaves)))

    outputs['LeafLength']= dict(zip(leaves,
            [2*(element/(coeff_width*pi))**(0.5) for element in outputs['LeafSurface'].values()]*len(leaves)))

    outputs['LeafWidth']=dict(zip(leaves,
                    [element *coeff_width for element in outputs['LeafLength'].values()]*len(leaves)))
    
    outputs['SurfTheo']=dict(zip(leaves,[pi*(element/2)*(coeff_width*element/2) for element in outputs['LeafLength'].values()]*len(leaves)))

    outputs['PetioleLength']=dict(zip(leaves,[element * coeff_petiole for element in outputs['LeafLength'].values()]*len(leaves)))

    outputs['PetioleLength']=dict(zip(leaves,[1]*len(leaves)))
    
    outputs['InsertionAngle']=dict(zip(leaves,[ins_angle]*len(leaves)))
    outputs['LeafAngle']=dict(zip(leaves,[leaf_angle]*len(leaves)))
    outputs['Phyllotaxy']=dict(zip(leaves,[phyllot]*len(leaves)))

    outputs['StemDiam']=dict(zip(internodes,[stem_d]*len(internodes)))
    outputs['PetioleDiam']=dict(zip(leaves,[stem_d*coeff_petiole_d]*len(leaves)))

    outputs['NodeLength']=dict(zip(keys,[node_length]*len(keys)))

    return update_MTG(g,outputs)

def faba_bean_metabolism(g,
    fall : bool = False,
    growth : bool = True,
    photosynthesis : float = None,
    Ei = 380,
    respiration = 0.,
    potential_photosynthesis= 0.,
    potential_area= 0.,
    nitrogen_source : bool = True,
    nitrogen_sink : bool = True,
    nitrogen_content = 20,
    nitrogen_demand = 0.,
    nitrogen_storage= 0.,
    nitrogen_import= 0.,
    nitrogen_export= 0.,
    nrue = 0.2,
    sfqn = 0.3,
    weight_import= 0.,
    weight_export= 0.,
    carbon_content= 0.,
    carbon_demand = 0.,
    carbon_deficit = 0.,
    carbon_import= 0.,
    carbon_export= 0.,
    carbon_spend= 0.,
    carbon_growth = 0.5,
    carbon_storage = 0.,
    carbon_nitrogen_ratio= 0.,
    nitrogen_fall_threshold_empirical= 0.,
    PAR_fall_threshold_empirical= 0.,
    carbon_fall_threshold_mecanism= 0.,
    nitrogen_fall_threshold_mecanism = 0.): 
    """
    """
    outputs=dict()

    for k, v in g.properties()['Species'].items() :
        if v == 'Faba bean': 
    
            leaves=[k for k, v in g.properties()['label'].items()  if v=='FababeanLeaf']

            outputs['Growth']=dict(zip(leaves,[growth]*len(leaves)))

            outputs['Ei']=dict(zip(leaves,[Ei]*len(leaves)))
            outputs['Photosynthesis']=dict(zip(leaves,[photosynthesis]*len(leaves)))
            outputs['Respiration']=dict(zip(leaves,[respiration]*len(leaves)))

            outputs['PotentialPhotosynthesis']=dict(zip(leaves,[potential_photosynthesis]*len(leaves)))
            outputs['PotentialArea']=dict(zip(leaves, [potential_area]*len(leaves)))

            outputs['NitrogenSource']=dict(zip(leaves,[nitrogen_source]*len(leaves)))
            outputs['NitrogenSink']=dict(zip(leaves,[nitrogen_sink]*len(leaves)))
            
            outputs['NitrogenContent']=dict(zip(leaves,[nitrogen_content]*len(leaves)))
            outputs['NitrogenDemand']=dict(zip(leaves,[nitrogen_demand]*len(leaves)))
            outputs['NitrogenImport']=dict(zip(leaves,[nitrogen_import]*len(leaves)))
            outputs['NitrogenExport']=dict(zip(leaves,[nitrogen_export]*len(leaves)))
            outputs['NitrogenStorage']=dict(zip(leaves,[nitrogen_storage]*len(leaves)))
            outputs['NRUE']=dict(zip(leaves,[nrue]*len(leaves)))
            outputs['SFQN']=dict(zip(leaves,[sfqn]*len(leaves)))


            outputs['PonderationExport']=dict(zip(leaves,[weight_export]*len(leaves)))
            outputs['PonderationImport']=dict(zip(leaves,[weight_import]*len(leaves)))
            
            outputs['CarbonContent']=dict(zip(leaves,[carbon_content]*len(leaves)))
            outputs['CarbonDemand']=dict(zip(leaves,[carbon_demand]*len(leaves)))
            outputs['CarbonDeficit']=dict(zip(leaves,[carbon_deficit]*len(leaves)))
            outputs['CarbonImport']=dict(zip(leaves,[carbon_import]*len(leaves)))
            outputs['CarbonExport']=dict(zip(leaves,[carbon_export]*len(leaves)))
            outputs['CarbonSpend']=dict(zip(leaves,[carbon_spend]*len(leaves)))
            outputs['CarbonGrowth']=dict(zip(leaves,[carbon_growth]*len(leaves)))
            outputs['CarbonStorage']=dict(zip(leaves,[carbon_storage]*len(leaves)))
            outputs['CarbonNitrogenRatio']=dict(zip(leaves,[carbon_nitrogen_ratio]*len(leaves)))

            outputs['Fall']= dict(zip(leaves,[fall]*len(leaves)))
            outputs['NirogenFallThresholdEmpirical']=dict(zip(leaves,[nitrogen_fall_threshold_empirical]*len(leaves)))
            outputs['NirogenFallThresholdMecanism']=dict(zip(leaves,[nitrogen_fall_threshold_mecanism]*len(leaves)))
            outputs['CarbonFallThresholdMecanism']=dict(zip(leaves,[carbon_fall_threshold_mecanism]*len(leaves)))
            outputs['PARFallThresholdEmpirical']=dict(zip(leaves,[PAR_fall_threshold_empirical]*len(leaves)))

            return update_MTG(g,outputs)
        
       

