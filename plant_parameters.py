from openalea.mtg import *
from openalea.mtg.turtle import *

from numpy import *
import numpy as np
from pandas import *

#######################################

def update_MTG(g, outputs):
    """
    Update the MTG 
    :Param dict outputs: {'Param1': { vid1: , vid2, ...}, 'Param2': { vid1: , vid2, ...}}
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

###########################################

def monstera_phenotype(g,
                       node_length: float = 0.2,
                       leaf_max: float=0.6587057,
                       sd: float= 0.246378,
                       amp: float=0.1188,
                       phyllot : float = 137.5,
                       ins_angle : float = 40,
                       leaf_angle : float = 80, #à mesurer expérimentallement
                       total_surface: float=300, 
                       coeff_width: float =0.831562, 
                       coeff_petiole: float =0.51017, #limb length to petiole length , 0.31017 length/whole leag length
                       stem_d: float=0.1,
                       coeff_petiole_d : float=0.5
                        ): 
    """
    applies phenotypical attributes to an MTG based on Parameters. 
        leaf_max : [float between 0 and 1] Expectation of the bell curve => Position of the biggest leaf along the stem.
        sd: [float] Standard deviation of the bell curve => repartition of the leaf surface
        amp: [float] amplitude of the bell curve 
        phyllot: [float, degrees] phyllotaxy angle 
        ins_angle: [float, degrees] insertion angle of the petiole
        leaf_angle: [float, degrees] angle of the flat of the leaf
        total_surface: [int, cm2] surface to be shared following the bell proportion
        coeff_width: [float] Leaf Width / Leaf Length ratio (limb only)
        coeff_petiole: [float] Petiole Length / Leaf Length 
        stem_d: [float, cm] stem diameter
        coeff_petiole_d : [float] petiole diameter / stem diameter ration 
    """
    outputs=dict()
        
    leaves=[k for k, v in g.properties()['label'].items()  if v =='Leaf']
    nodes = [k for k, v in g.properties()['label'].items()]
    plants=[k for k, v in g.properties()['label'].items()  if v=='Plant']
    internodes=[k for k, v in g.properties()['label'].items()  if v=='Internode']

    surface=generate_normalized_bell_curve_points(mean=leaf_max,std_dev=sd,amplitude=amp,N=int(len(leaves)/len(plants)))
    outputs['SurfaceRepartition']=dict(zip(leaves,surface*len(leaves)))
    outputs['LeafSurface']=dict(zip(leaves,[element * total_surface for element in surface]*len(leaves)))

    outputs['LeafLength']= dict(zip(leaves,
            [2*(element/(coeff_width*pi))**(0.5) for element in outputs['LeafSurface'].values()]*len(leaves)))

    outputs['LeafWidth']=dict(zip(leaves,
                    [element *coeff_width for element in outputs['LeafLength'].values()]*len(leaves)))
    
    outputs['SurfTheo']=dict(zip(leaves,[pi*(element/2)*(coeff_width*element/2) for element in outputs['LeafLength'].values()]*len(leaves)))

    outputs['PetioleLength']=dict(zip(leaves,[element * coeff_petiole for element in outputs['LeafLength'].values()]*len(leaves)))
    
    outputs['InsertionAngle']=dict(zip(leaves,[ins_angle]*len(leaves)))
    outputs['LeafAngle']=dict(zip(leaves,[leaf_angle]*len(leaves)))
    outputs['Phyllotaxy']=dict(zip(leaves,[phyllot]*len(leaves)))

    outputs['StemDiam']=dict(zip(internodes,[stem_d]*len(internodes)))
    outputs['PetioleDiam']=dict(zip(leaves,[stem_d*coeff_petiole_d]*len(leaves)))

    outputs['NodeLength']=dict(zip(nodes,[node_length]*len(nodes)))

    return update_MTG(g,outputs)
          
#TO DO: 
# + add elongation coefficient = node_length, petiole length
# + add growth coefficient = leaf length, leaf width, leaf surface
# + add diameter coefficient = stem diam, petiole diam
# + add limb curve angle = curve

def monstera_metabolism(g,
    fall : bool = False,
    growth : bool = True,
    photosynthesis : float = None,
    Ei : float = 380,
    respiration : float = 0.,
    potential_photosynthesis : float = 0.,
    potential_area : float = 0.01 ,
    potential_nitrogen_content : float = 0.,
    nitrogen_source : bool = True,
    nitrogen_sink : bool = True,
    nitrogen_content : float = 10,
    nitrogen_demand : float = 0.,
    nitrogen_storage : float = 0.,
    nitrogen_import : float = 0.,
    nitrogen_export : float = 0.,
    nrue : float = 0.10,
    sfqn : float = 0.3,
    weight_import : float = 0.,
    weight_export : float = 0.,
    carbon_content : float = 0.,
    carbon_demand : float = 0.,
    carbon_deficit : float = 0.,
    carbon_import : float = 0.,
    carbon_export : float = 0.,
    carbon_spend : float = 0.,
    carbon_growth : float = 0.,
    carbon_storage : float = 0.,
    carbon_nitrogen_ratio : float = 0.,
    nitrogen_fall_threshold_empirical : float= 0.,
    Ei_fall_threshold_empirical : float = 0.,
    carbon_fall_threshold_mecanism : float = 0.,
    nitrogen_fall_threshold_mecanism : float = 0.): 
    """
    """
    outputs=dict()

    for k, v in g.properties()['Species'].items() :
        if v == 'Rapeseed': 
                
            leaves=[k for k, v in g.properties()['label'].items()  if v =='Leaf']

            outputs['Growth']=dict(zip(leaves,[growth]*len(leaves)))

            outputs['Ei']=dict(zip(leaves,[Ei]*len(leaves)))
            outputs['Photosynthesis']=dict(zip(leaves,[photosynthesis]*len(leaves)))
            outputs['Respiration']=dict(zip(leaves,[respiration]*len(leaves)))

            outputs['PotentialPhotosynthesis']=dict(zip(leaves,[potential_photosynthesis]*len(leaves)))
            outputs['PotentialArea']=dict(zip(leaves, [potential_area]*len(leaves)))
            outputs['PotentialNitrogenContent']=dict(zip(leaves, [potential_nitrogen_content]*len(leaves)))

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
            outputs['FallEmpirical']= dict(zip(leaves,[fall]*len(leaves)))
            outputs['NirogenFallThresholdEmpirical']=dict(zip(leaves,[nitrogen_fall_threshold_empirical]*len(leaves)))
            outputs['NirogenFallThresholdMecanism']=dict(zip(leaves,[nitrogen_fall_threshold_mecanism]*len(leaves)))
            outputs['CarbonFallThresholdMecanism']=dict(zip(leaves,[carbon_fall_threshold_mecanism]*len(leaves)))
            outputs['EiFallThresholdEmpirical']=dict(zip(leaves,[Ei_fall_threshold_empirical]*len(leaves)))

            return update_MTG(g,outputs)
        
        