from openalea.mtg import *
from openalea.mtg import traversal
from openalea.plantgl.all import Scene

from openalea.caribu.CaribuScene import CaribuScene
from oawidgets.plantgl import *

from numpy import *
import numpy as np
from pandas import *
import pandas as pd

import mtg_visualization

###################################

def update_MTG(g, outputs):
    """Update the MTG after run methods.

    Parameters
    ----------
    g: MTG 
        MTG where properties are recorded

    outputs: dict
        New properties values after run methods
    
    Returns
    -------
    g: MTG 
        MTG where properties are recorded

    Examples
    --------
    >>> outputs = {'Param1': { vid1: , vid2, ...}, 'Param2': { vid1: , vid2, ...}}

    Authors
    -------
    Armand Grumel and Laurène Perthame
        Colzette model

    """
    print("Update the MTG...")

    # add the missing property
    for param in outputs.keys():
        if param not in g.properties():
            g.add_property(param)

        # update the MTG
        g.property(param).update(outputs[param])

########################################################################################
        
def total(list):
    """Calculation the organ MTG properties aggregation.

    Parameters
    ----------
    list: list
        list of all organs property values
    
    Returns
    -------
    _total: float 
        pool of all organs property values

    Authors
    -------
    Solen Farra

    """
    print("Calcul the pool...")
       
    _total = 0
    for i in list:
        _total = _total + i
    
    return _total

########################################################################################



##Caribu is computed to obtain the Eii for each leaf of the mtg
class Photosynthesis:
    """Photosynthesis methods.

    Authors
    -------
    Solen Farra

    """
    def __init__(self, g, parcelle,
                  caribu, photosynthesis) :

        self.g = g
        self.caribu = self.caribu(g, parcelle) if caribu is None else caribu
        self.photosynthesis = self.leaf_photosynthesis(g) if photosynthesis is None else photosynthesis

        return
    
    def caribu(g, parcelle):
       """ Light radiation model
       
       Parameters
       ----------
        g: MTG 
            MTG where properties are recorded
            
        Returns
        -------
        Ei : MTG properties
            Intercepted radiation  umol/m2

        References
        ----------
        Chelle et al. (2004)

        Authors
        -------
        Christophe Pradal
        Laurène Perthame
        Solen Farra

       """
       outputs=dict()
       
       zenith=[(30,(0,0,-1))]
       
       can = mtg_visualization.scene3d(g)
       
       #energy, emission, direction, elevation, azimuth = turtle.turtle(sectors='46', energy=100.)
       #sources = list(zip(energy, direction))

       cs = CaribuScene(scene=can,light=zenith,pattern=parcelle[2])
        
       raw,agg=cs.run(infinite=True,simplify=False,direct=False)
       #cs.plot(raw['Ei'],display=True)

       Eabs = agg['default_band']['Eabs']
       Ei = agg['default_band']['Ei']
       area = agg['default_band']['area']

       alive = [k for k, v in g.properties()['Fall'].items() if v == False]
    
       outputs['Eabs']= dict(zip(alive,Eabs.values()))
       outputs['Ei']= dict(zip(alive,Ei.values()))
       outputs['area']= dict(zip(alive,area.values()))

       return update_MTG(g,outputs)


    def leaf_photosynthesis(g, alpha = 0.026) :
        """Calculation of the actual quantity of carbon produced of each organ.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
        
        alpha: MTG properties
            quantical yield (slope coefficient) from the light response-curve of photosynthesis
            cf Wuhan poster methods

        Ei: MTG proporties
            Incident light on the organ (umol/m2)
        
        Respiration: MTG properties
            Carbon quantity spend for respiration activity (g)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        Photosynthesis: MTG proporties
            Net quantity of carbon produced (molCO2/m2/sec)

        References
        ----------
        Drouet (1998)

        Authors
        -------
        Solen FARRA

        ______________________________________________________________________________________________________
        #TODO : From PARi for each leaf, why don't we use Monteith here ? We use it for the potential growth ?
        -- Calculation of the real photosynthesis with an empirical approach at the leaf scale 
        (quantic yield by N content)
        -- Add alpha calcul in the model (cf Wuhan ppt)
        
        #NOTE : Convert Photosynthesis into g of C to obtain C quantity (use molar mass) :
        --  C_flux <- CO2_flux * constants$umol2mol * constants$Cmol * constants$kg2g * constants$days2seconds
        -- C_flux (g C m-2 d-1) <- CO2_flux (umol CO2 m-2 s-1) * umol2mol = 1e-06 *  Cmol = 0.012011 * kg2g = 1000 * days2seconds = 86400

        """
        print("Run the actual photosynthesis...")

        outputs=dict()

        alive = [k for k, v in g.properties()['Fall'].items() if v == False]
        Ei = [v for k, v in g.properties()['Ei'].items()]
        respiration = [v for k, v in g.properties()['Respiration'].items()]

        outputs['Photosynthesis']= dict(zip(alive,[(((((alpha*a)-b)*1e-06)*0.012011)*1000)*86400 for a, b in zip(Ei, respiration)]))
        
        return update_MTG(g,outputs)

class PotentialGrowth:
    """Growth methods. 

    Authors
    -------
    Solen FARRA

    """
    def __init__(self, g, potential_area = None, potential_photosynthesis = None, area = None) :
        
        self.g = g
        self.potential_area = self.leaf_potential_area(g) if potential_area is None else potential_area
        self.potential_photosynthesis = self.leaf_potential_photosynthesis(g) if potential_photosynthesis is None else potential_photosynthesis

        return 

    def leaf_potential_area(self, g) :
        """Estimation of the potential leaf area based on a radiation use efficiency of each organ.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        NRUE: MTG proporties
            Nitrogen Use Efficiency by radiation unit coefficient
            The leaf nitrogen content per unit of incident light (input from the past time step)

        Ei : MTG proporties
            Incident light on the organ (W/m2)
        
        SFQN : MTG proporties
            Nitrogen quantity by surface unit coefficient
            Thus we calculate Ei --> TN --> SF and we obtain a leaf area at the end
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA

        """
        print("Run a potential area...")

        outputs=dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        nrue = [v for k, v in g.properties()['NRUE'].items() if k in alive] 
        Ei = [v for k, v in g.properties()['Ei'].items() if k in alive]
        sfqn = [v for k, v in g.properties()['SFQN'].items() if k in alive]

        outputs['PotentialArea']= dict(zip(alive,[(a*b)/c for a, b, c in zip(nrue, Ei, sfqn)])) 
       
        return update_MTG(g,outputs)
    

    def leaf_potential_photosynthesis(self, g,
                                      epsilon_a : float = 0.1, 
                                      epsilon_b : float = 0.2 ):
        """Calculation of a potential (optimum) quantity of carbon produced of each organ.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
        
        alpha: MTG proporties
            quantical yield (slope coefficient) from the light response-curve of photosynthesis

        Ei: MTG proporties
            Incident light on the organ (W/m2)
        
        epsilon_b: float
            Biological efficiency coefficient (g/MJ)

        epsilon_a: float
            Absorption efficiency coefficient

        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA

        References
        ----------
        Monteith (1981)
            Penman-Monteith equation

        ______________________________________________________________________________
        #TODO : Add potential_photosynthesis with Solen experimental method to compare
         Should we remove respiration ? Monteith is not net photosynthesis ?
         --- No need, if its just an estimation of optimum carbon produced without takin account carbon cost

        """
        print("Run a potential photosynthesis...")

        outputs=dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        Ei = [v for k, v in g.properties()['Ei'].items() if k in alive]

        outputs['PotentialPhotosynthesis']= dict(zip(alive,[((a*epsilon_a)*epsilon_b) for a in Ei]))

        return update_MTG(g,outputs)

        
class Competition:
    """Nutrient competition status methods. 

    Authors
    -------
    Solen FARRA

    """
    def __init__(self, g, 
                 carbon_deficit = None, source_N = None, sink_N = None) :
    
        self.g = g
        self.carbon_deficit = self.leaf_carbon_deficit(g) if carbon_deficit is None else carbon_deficit
        self.source_N = self.leaf_nitrogen_source(g) if source_N is None else source_N
        self.sink_N = self.leaf_nitrogen_sink(g) if sink_N is None else sink_N
    
        return 
    
    def leaf_carbon_deficit(self, g):
        """Calculation of the carbon deficit according to the actual photosynthesis and the carbon stress for each organ.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        CarbonDemand: MTG properties
            Actual quantity of carbon produced by photosynthesis (g)
        
        PotentialArea: MTG properties
            Carbon quantity spend for nitrogen redistribution among organs (g)

        Area: MTG properties
            Actual leaf area 
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA

        _______________________________________________________________________
        #TODO : Carbon_demand is a value calculated from the previous time step
        # --- We can develop the same model but with a Nitrogen_Demand input (with a potential nitrogen demand and a nitrogen deficit ?)

        """
        print("Run the actual carbon deficit...")

        outputs=dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        photosynthesis = [v for k, v in g.properties()['Photosynthesis'].items()]
        carbon_demand = [v for k, v in g.properties()['CarbonDemand'].items()]

        outputs['CarbonDeficit']= dict(zip(alive,[a-b for a, b in zip(photosynthesis, carbon_demand)]))

        return update_MTG(g,outputs)
    
    def leaf_nitrogen_source(self, g):
        """Evaluation of the nitrogen source-sink relationship between organs.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        CarbonDemand: MTG properties
            Actual quantity of carbon produced by photosynthesis (g)
        
        PotentialArea: MTG properties
            Carbon quantity spend for nitrogen redistribution among organs (g)

        Area: MTG properties
            Actual leaf area 
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA

        """
        print("Run the actual nitrogen competition status of each organ...") 

        outputs=dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        nitrogen =[v for k, v in g.properties()['NitrogenContent'].items() if k in alive]

        pool_N = total(nitrogen)
       
        for k,v in g.properties()['NitrogenContent'].items() :
            if k in alive :
                if v < pool_N : 

                    source = [k]
                    outputs['NitrogenSource']= dict(zip(source,[True]))
                    
                    update_MTG(g,outputs)
                
                else :

                    sink = [k]
                    outputs['NitrogenSource']= dict(zip(sink,[False]))

                    update_MTG(g,outputs)
               
        return update_MTG(g,outputs)
    
    
    def leaf_nitrogen_sink(self, g):
        """Evaluation of the nitrogen source-sink relationship between organs.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        CarbonDemand: MTG properties
            Actual quantity of carbon produced by photosynthesis (g)
        
        PotentialArea: MTG properties
            Carbon quantity spend for nitrogen redistribution among organs (g)

        Area: MTG properties
            Actual leaf area 
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA

        """
        print("Run the actual nitrogen competition status of each organ...") 

        outputs=dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        
        for k,v in g.properties()['CarbonDeficit'].items():
            if k in alive :
                if v < 0 : 
                
                    sink = [k] 
                    outputs['NitrogenSink']= dict(zip(sink,[True]))
                    
                    update_MTG(g,outputs)

                
                else :
                    
                    source = [k]
                    outputs['NitrogenSink']= dict(zip(source,[False]))  

                    update_MTG(g,outputs)

        return update_MTG(g,outputs)

class Nitrogen:
    """Nitrogen exchange methods. 

    Authors
    -------
    Solen FARRA

    """
    def __init__(self, g,
                 potential_nitrogen_content = None,
                 nitrogen_demand = None,
                 weight_export = None,
                 weight_import = None,
                 nitrogen_import = None,
                 nitrogen_export = None,
                 nitrogen_storage = None,
                 NRUE = None,
                 carbon_expend = None,
                 nitrogen_content = None,
                 carbon_nitrogen_ratio = None) :
    
        self.g = g
        self.potential_nitrogen_content = self.leaf_potential_nitrogen_content(g) if potential_nitrogen_content is None else potential_nitrogen_content
        self.nitrogen_demand = self.leaf_nitrogen_demand(g) if nitrogen_demand is None else nitrogen_demand
        self.NRUE = self.leaf_NRUE(g) if NRUE is None else NRUE
        self.weight_export = self.leaf_nitrogen_export_ponderation(g) if weight_export is None else weight_export
        self.weight_import = self.leaf_nitrogen_import_ponderation(g) if weight_import is None else weight_import
        self.nitrogen_import = self.leaf_nitrogen_import(g) if nitrogen_import is None else nitrogen_import
        self.nitrogen_export = self.leaf_nitrogen_export(g) if nitrogen_export is None else nitrogen_export
        self.nitrogen_storage = self.leaf_nitrogen_storage(g) if nitrogen_storage is None else nitrogen_storage
        self.carbon_expend = self.leaf_senescence_carbon_cost(g) if carbon_expend is None else carbon_expend
        self.nitrogen_content = self.leaf_nitrogen_content(g) if nitrogen_content is None else nitrogen_content
        self.carbon_nitrogen_ratio = self.leaf_carbon_nitrogen_ratio(g) if carbon_nitrogen_ratio is None else carbon_nitrogen_ratio
    
        return 

    # This function calculates the leaf nitrogen demand according to the potential leaf area:
    def leaf_potential_nitrogen_content(self, g):#### leaf nitrogen demand used in import export function to calcule the N quantity to move
        """Calculation of the potential nitrogen content of each organ.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded

        PotentialArea : MTG proporties
            Potential leaf area (m2)
        
        SFQN : MTG proporties
            Nitrogen quantity by surface unit coefficient
            Thus we calculate Ei --> TN --> SF and we obtain a leaf area at the end
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        PotentialNitrogenContent : MTG proporties
            Potential nitrogen content of the organ (g)

        Authors
        -------
        Solen FARRA

        """
        print("Run the potential nitrogen content...")

        outputs=dict()

        alive=[k for k, v in g.properties()['Fall'].items()  if v == False]
        potential_area = [v for k, v in g.properties()['PotentialArea'].items() if k in alive]
        sfqn = [v for k, v in g.properties()['SFQN'].items() if k in alive]

        outputs['PotentialNitrogenContent']= dict(zip(alive,[a*b for a, b in zip(sfqn, potential_area)]))
        
        return update_MTG(g,outputs)

        
    def leaf_nitrogen_demand(self, g):
        """Calculation of the nitrogen demand of each organ.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
        
        POtentialArea: MTG proporties
            Potential organ area according to the RUE (m2)

        NitrogenContent : MTG proporties
            Actual nitrogen content of the organ (g)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        NitrogenDemand: MTG properties
            Nitrogen demand of each organ according to a potential

        Authors
        -------
        Solen FARRA

        ___________________________________________
        #NOTE : # The nitrogen demand cannot be > 0 

        """
        print("Run the actual nitrogen demand...")

        outputs=dict()

        alive=[k for k, v in g.properties()['Fall'].items()  if v == False]
        potential_nitrogen_content = [v for k, v in g.properties()['PotentialNitrogenContent'].items()]
        nitrogen_content = [v for k, v in g.properties()['NitrogenContent'].items()] 
        
        outputs['NitrogenDemand']= dict(zip(alive,[a-b for a, b in zip(potential_nitrogen_content, nitrogen_content)]))

        return update_MTG(g,outputs)

    def leaf_nitrogen_export_ponderation(self, g,
                                 Ei_max: float = 100) :
        """Leaf export mecanism drive by ponderation 
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        Ei : MTG properties
            Incident light on the organ (umol/m2)
            
        Returns
        -------
        g : MTG
            the above part of the plant
        
        PonderationExport : MTG properties
            Proportion of participation of the organ to the export pool according to his Ei

        References
        ----------
        Lemaire et al. (2008)

        Authors
        -------
        Solen Farra

        """
        print("Run the nitrogen export ponderation...")

        outputs=dict()

        senescent = [k for k, v in g.properties()['Ei'].items() if v < 20.0]
        Ei = [v for k, v in g.properties()['Ei'].items() if k in senescent]
               
        for  k, v in g.properties()['Fall'].items() :
            if v == False :
                    
                outputs['PonderationExport']= dict(zip(senescent,[a/Ei_max for a in Ei]))
                        
            else : 
                
                pass

        return update_MTG(g,outputs)

                    
    def leaf_nitrogen_import_ponderation(self,g,
                        Ei_max: float = 100) :
        """Leaf nitrogen import mecanism drive by ponderation
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        Ei : MTG properties
            Incident light on the organ (umol/m2)
            
        Returns
        -------
        g : MTG
            the above part of the plant
        
        PonderationImport : MTG properties
            Proportion of participation of the organ to the export pool according to his Ei

        References
        ----------
        Lemaire et al. (2008)

        Authors
        -------
        Solen Farra

        #TODO : Determine if NitrogenImport > NitrogenDemand --> nitrogen storage = import - demand and NitrogenContent = nitrogen_demand ; 
        else nitrogenContent = nitrogen import 
        cf leaf_nitrogen_content method : needs to be updated

        """
        print("Run the nitrogen import ponderation...")

        outputs=dict()
        
        sink = [k for k, v in g.properties()['Ei'].items() if v > 20.0]
        Ei = [v for k, v in g.properties()['Ei'].items() if k in sink]
    
        outputs['PonderationImport']= dict(zip(sink,[1/(a/Ei_max) for a in Ei]))
        
        return update_MTG(g,outputs)


    def leaf_nitrogen_export(self, g):
        """Leaf nitrogen import mecanism drive by ponderation
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        NitrogenContent : MTG properties
            actual nitrogen content (g/g)

        WeightExport : MTG properties
            exportation ponderation coefficient
            
        Returns
        -------
        g : MTG
            the above part of the plant
        
        NitrogenExport : MTG properties
            Nitrogen export quantity (g)

        References
        ----------
        Lemaire et al. (2008)

        Authors
        -------
        Solen Farra

        """
        print("Run the actual nitrogen export...")

        outputs=dict()

        senescent = [k for k, v in g.properties()['Ei'].items() if v < 20.0]
        nitrogen_content =[v for k, v in g.properties()['NitrogenContent'].items()]
        weight_export = [v for k, v in g.properties()['PonderationExport'].items()]
       
        outputs['NitrogenExport']= dict(zip(senescent,[a*b for a, b in zip(nitrogen_content,weight_export)]))

        return update_MTG(g,outputs)

                    
    def leaf_nitrogen_import(self, g) :
        """Leaf nitrogen import mecanism drive by ponderation
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        NitrogenContent : MTG properties
            actual nitrogen content (g/g)

        WeightImport : MTG properties
            importation ponderation coefficient
            
        Returns
        -------
        g : MTG
            the above part of the plant
        
        NitrogenImport : MTG properties
            Nitrogen import quantity (g)

        References
        ----------
        Lemaire et al. (2008)

        Authors
        -------
        Solen Farra

        __________________________________________________________________________________________________________________________________
        #TODO : Determine if NitrogenImport > NitrogenDemand --> nitrogen storage = import - demand and NitrogenContent = nitrogen_demand ; 
        else nitrogenContent = nitrogen import 
        cf leaf_nitrogen_content method : needs to be updated

        -- NitrogenDemand > 0 == NitrogenStorage

        """
        print("Run the actual nitrogen import...")

        outputs=dict()

        sink =[k for k, v in g.properties()['Ei'].items() if v > 20.0]
        nitrogen_content =[v for k, v in g.properties()['NitrogenContent'].items()]
        weight_import =[v for k, v in g.properties()['PonderationImport'].items()]
        weight_import = [v for k, v in g.properties()['PonderationImport'].items()]
        
        outputs['NitrogenImport']= dict(zip(sink,[a*b for a, b in zip(nitrogen_content, weight_import)]))

        return update_MTG(g,outputs)
                

    def leaf_NRUE(self, g):
        """Calculation of the radiation use efficiency for each organs.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        Ei : MTG proporties
            Incident light on the organ (W/m2)
            
        NitrogenContent : MTG proporties
            Nitrogen content of each organs (g/g) 
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        NRUE: MTG
            Nitrogen Use Efficiency by Radiation unit coefficient

        Authors
        -------
        Solen FARRA

        References
        ----------
        Luquet et al. (2006)
            EcoMeristem model

        """
        print("Run the actual light use by nitrogen unit...")

        outputs=dict()

        alive=[k for k, v in g.properties()['Fall'].items()  if v == False]
        Ei = [v for k, v in g.properties()['Ei'].items() if k in alive]
        nitrogen_content = [v for k, v in g.properties()['NitrogenContent'].items() if k in alive]

        outputs['NRUE']= dict(zip(alive,[a/b for a, b in zip(nitrogen_content, Ei)]))

        return update_MTG(g,outputs)
    

    def leaf_senescence_carbon_cost(self, g,
                                     kr : float = 0.08):
        """Calculation of the carbon cost of nitrogen exchange among organs.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
            
        NitrogenImport : MTG proporties
            Nitrogen quantity import of each organs (g) 
        
        NitrogenContent : MTG proporties
            Actual nitrogen content of each organs (g)
        
        kr : float
            Carbon cost coefficient of nitrogen resorption for each organs (kg/C/m2)
        
        Returns
        -------
        g: MTG 
            MTG where properties are recorded
        
        CarbonSpend : MTG properties
            final carbon cost of the nitrogen balance (g)

        Authors
        -------
        Solen FARRA

        References
        ----------
        Fisher et al. (2010)
        Brzostek et al. (2014)
            FUN 2.0 model

        """
        print("Run the carbon cost of nitrogen re-allocation...")

        outputs = dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        nitrogen_import = [v for k, v in g.properties()['NitrogenImport'].items()]
        nitrogen_content = [v for k, v in g.properties()['NitrogenContent'].items()]

        outputs['CarbonSpend']= dict(zip(alive,[(kr/a)*b for a, b in zip(nitrogen_content, nitrogen_import)]))

        return update_MTG(g,outputs)
    
    def leaf_nitrogen_content(self, g):
        """Calculation of the final nitrogen content after exchange among organs.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
            
        NitrogenImport : MTG properties
            Nitrogen quantity import of each organs (g) 
        
        NitrogenExport : MTG properties
            Nitrogen quantity export of each organs (g) 
        
        NitrogenContent : MTG properties
            final nitrogen content (g)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        NitrogenContent : MTG properties
            final nitrogen content (g)

        Authors
        -------
        Solen FARRA

        References
        ----------
        Fisher et al. (2010)
        Brzostek et al. (2014)
            FUN 2.0 model

        """
        print("Run the nitrogen content...")

        outputs = dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        senescent = [k for k, v in g.properties()['Ei'].items()  if v < 20.0]
        sink = [k for k, v in g.properties()['Ei'].items()  if v > 20.0]
        nitrogen_import = [v for k, v in g.properties()['NitrogenImport'].items() if k in sink]
        nitrogen_export = [v for k, v in g.properties()['NitrogenExport'].items() if k in senescent]
        nitrogen_content = [v for k, v in g.properties()['NitrogenContent'].items()]
         
        outputs['NitrogenContent']= dict(zip(alive,[(a+b)-c for a, b, c in zip(nitrogen_content, nitrogen_import, nitrogen_export)]))

        return update_MTG(g,outputs)

    
    def leaf_carbon_nitrogen_ratio(self, g):
        """Evaluation of the C:N ratio of each organ for growth regulation and shoot:root balance.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
            
        NitrogenContent : MTG proporties
           Final nitrogen content of each organs (g)

        CarbonGrowth : MTG properties
            Carbon quantity left to growth after nitrogen exchange among organs.
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        CarbonNitrogenRatio : MTG properties
            actual carbon and nitrogen quantities ratio

        Authors
        -------
        Solen FARRA

        References
        ----------
        Fisher et al. (2010)
        Brzostek et al. (2014)
            FUN 2.0 model

        """
        print("Run the C:N ratio...")

        outputs = dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        carbon_growth = [v for k, v in g.properties()['CarbonGrowth'].items() if k in alive]
        nitrogen_import = [v for k, v in g.properties()['NitrogenImport'].items() if k in alive]

        for a, b in zip(carbon_growth, nitrogen_import) :
            if b == 0.:
                print("Cannot divide by zero")
            
            else : 
                outputs['CarbonNitrogenRatio']= dict(zip(alive,[a/b]))

        return update_MTG(g,outputs)
    
    
    def leaf_nitrogen_storage(self, g) :
        """Evaluation of the stored nitrogen after balance.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
            
        NitrogenDemand : MTG proporties
           nitrogen needs of each organs (g)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        NitrogenStorage : MTG properties
            nitrogen quantity left after carbon balance (g)

        Authors
        -------
        Solen FARRA

        """
        print("Run the nitrogen storage...")

        outputs = dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        nitrogen_demand = [v for k, v in g.properties()['NitrogenDemand'].items()]
               
        for v in nitrogen_demand :
            if v > 0 :
                    
                outputs['NitrogenStorage']= dict(zip(alive,[a for a in nitrogen_demand]))
                        
            else : 
                
                pass

        return update_MTG(g,outputs)

class Carbon:
    """Carbon balance methods. 

    Authors
    -------
    Solen FARRA

    """
    def __init__(self, g, carbon_growth = None, carbon_demand = None, carbon_export = None, 
               carbon_import = None, growth = None, carbon_storage = None, carbon_content = None) :

        self.g = g
        self.carbon_growth = self.leaf_carbon_growth(g) if carbon_growth is None else carbon_growth
        self.carbon_demand = self.leaf_carbon_demand(g) if carbon_demand is None else carbon_demand
        self.carbon_export = self.leaf_carbon_export(g) if carbon_export is None else carbon_export
        self.carbon_import = self.leaf_carbon_import(g) if carbon_import is None else carbon_import
        self.carbon_storage = self.leaf_carbon_storage(g) if carbon_storage is None else carbon_storage
        self.carbon_content = self.leaf_carbon_content(g) if carbon_content is None else carbon_content
        self.growth = self.leaf_carbon_growth(g) if growth is None else growth
            
        return 
    
    # This function calculates the carbon finally available for growth after nutrient redistribution:
    def leaf_carbon_growth(self, g) :
        """Calculation of the carbon left after nitrogen balance.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        Photosynthesis: MTG properties
            Actual quantity of carbon produced by photosynthesis (g)
        
        CarbonSpend: MTG properties
            Carbon quantity spend for nitrogen redistribution among organs (g)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        CarbonGrowth : MTG properties
            carbon quantity left after nitrogen balance

        Authors
        -------
        Solen FARRA

        """
        print("Run the carbon available for growth...")

        outputs = dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        photosynthesis = [v for k, v in g.properties()['Photosynthesis'].items()]
        carbon_spend = [v for k, v in g.properties()['CarbonSpend'].items()]

        outputs['CarbonGrowth']= dict(zip(alive,[a-b for a, b in zip(photosynthesis, carbon_spend)]))

        return update_MTG(g,outputs)

    def leaf_carbon_demand(self, g) :
        """Calculation of a carbon need for each organ.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
        
        PotentialPhotosynthesis: MTG properties
            Potential (optimum) quantity of carbon produced by photosynthesis according to a potential leaf area (g)
        
        CarbonGrowth: MTG properties
            Carbon quantity left for growth of each organs (g)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        CarbonDemand : MTG properties
            carbon needs accordint to photosyntehsis potential 
        
        References
        ----------
        Optimization theory

        Authors
        -------
        Solen FARRA

        """
        print("Run the carbon demand...")

        outputs = dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        potential_photosynthesis = [v for k, v in g.properties()['PotentialPhotosynthesis'].items()]
        carbon_growth = [v for k, v in g.properties()['CarbonGrowth'].items()]

        outputs['CarbonDemand'] = dict(zip(alive,[a-b for a, b in zip(carbon_growth, potential_photosynthesis)]))

        return update_MTG(g,outputs)
    
    def leaf_carbon_storage(self, g) :
        """Evaluation of the stored carbon after turnover mecanism.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
                
        CarbonDemand: MTG properties
            carbon needs accordint to photosyntehsis potential  (g)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        CarbonStorage : MTG properties
            carbon quantity left after carbon balance (g)

        Authors
        -------
        Solen FARRA

        """
        print("Run the carbon storage...")

        outputs = dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        carbon_demand = [v for k, v in g.properties()['CarbonDemand'].items()]
               
        for v in carbon_demand :
            if v > 0 :
                    
                outputs['CarbonStorage']= dict(zip(alive,[a for a in carbon_demand]))
                        
            else : 
                
                pass

        return update_MTG(g,outputs)


    def leaf_carbon_export(self, g) :
        """Carbon export according to ponderation.
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        CarbonStorage: MTG properties
            Carbon quantity storage after carbon balance
        
        WeightExport: MTG properties
            Ponderation coefficient of each organs for nutrient pool export

        Returns
        -------
        g : MTG
            the above part of the plant
        
        CarbonExport: MTG properties
            export carbon quantity (g)

        References
        ----------
        Lemaire et al. (2008)

        """
        print("Run the actual carbon export...")

        outputs=dict()

        source =[k for k, v in g.properties()['Ei'].items() if v > 80.0]
        carbon_storage =[v for k, v in g.properties()['CarbonStorage'].items() if k in source]
        weight_export =[v for k, v in g.properties()['PonderationExport'].items() if k in source]

        for  k, v in g.properties()['Fall'].items() :
            if v == False :

                outputs['CarbonExport']= dict(zip(source,[a*b for a, b in zip(carbon_storage, weight_export)]))

            else :

                pass

        return update_MTG(g,outputs)
    

    def leaf_carbon_import(self, g) :
        """Carbon import according to ponderation.
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        CarbonStorage: MTG properties
            Carbon quantity storage after carbon balance
        
        WeightImport: MTG properties
            Ponderation coefficient of each organs for nutrient pool export

        Returns
        -------
        g : MTG
            the above part of the plant
        
        CarbonImport: MTG properties
            import carbon quantity (g)

        References
        ----------
        Lemaire et al. (2008)

        """      
        print("Run the actual carbon import...")
        
        outputs=dict()

        sink =[k for k, v in g.properties()['Ei'].items() if v < 80.0]
        weight_import =[v for k, v in g.properties()['PonderationImport'].items() if k in sink]
        carbon_storage =[v for k, v in g.properties()['CarbonStorage'].items() if k in sink]
    
        for  k, v in g.properties()['Fall'].items() :
            if v == False :
                        
                outputs['CarbonImport']= dict(zip(sink,[a*b for a,b in zip(carbon_storage, weight_import)]))
            
            else :

                pass

        return update_MTG(g,outputs)
    

    def leaf_carbon_content(self, g) :
        """Final carbon content after carbon balance.
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        CarbonGrowth: MTG properties
            Carbon quantity storage after carbon balance
        
        CarbonImport: MTG properties
            import carbon quantity
        
        CarbonExport: MTG properties
            export carbon quantity

        CarbonContent: MTG properties
            actual carbon content (g/g)

        Returns
        -------
        g : MTG
            the above part of the plant
        
        CarbonContent: MTG properties
            final carbon content (g/g)

        """       
        print("Run the actual carbon content...")
        
        outputs=dict()

        alive = [k for k, v in g.properties()['Fall'].items()  if v == False]
        sink = [k for k, v in g.properties()['Ei'].items() if v < 80.0]
        carbon_content = [v for k, v in g.properties()['CarbonContent'].items()]
        carbon_growth = [v for k, v in g.properties()['CarbonGrowth'].items()]
        carbon_import = [v for k, v in g.properties()['CarbonImport'].items() if k in sink]
        source = [k for k, v in g.properties()['Ei'].items() if v > 80.0]    
        carbon_export = [v for k, v in g.properties()['CarbonExport'].items() if k in source]      

        outputs['CarbonContent']= dict(zip(alive,[a+b+c-d for a, b, c, d in zip(carbon_content, carbon_growth, carbon_import, carbon_export)]))

        return update_MTG(g,outputs)
    
#TODO : growth model (leaf, stem, petiol)
    #def leaf_growth_status(self, g) :
    #            
    #            print("Run the actual growth status...")
    #            
    #            outputs=dict()

    #            sink =[k for k, v in g.properties()['Ei'].items() if v > 80.0]
    #            growth =[v for k, v in g.properties()['Growth'].items() if k in sink]
    #            nitrogen =[v for k, v in g.properties()['NitrogenContent'].items()]

    #            pool_N = total(nitrogen)
                                               
    #            for k, v in nitrogen :
    #                if v < pool_N : 
                        
    #                    sink = [k]
    #                    outputs['Growth']= dict(zip(sink,[True]))
    #                        
    #                else :
    #                    
    #                    source = [k]
    #                    outputs['Growth']= dict(zip(source,[False for a in growth]))
    #          
    #            return update_MTG(g,outputs)
    

class Growth:
    """Growth methods. 

    Authors
    -------
    Solen FARRA

    """
    def __init__(self, g, area = None) :

        self.g = g
        self.area = self.leaf_area(g) if area is None else area
    
        return 

    def leaf_area(self, g) :
        """leaf area extend according to final carbon content.
        
        Parameters
        ----------
        g: MTG
            the above part of the plant

        carbon_demand : MTG proporties
            Nitrogen content of each organs (g)

        potential_area : MTG proporties
            Potential area of each organs according to a radiation use efficiency (m2)

        carbon_growth : MTG proporties
            Carbon quantity left to growth after nitrogen exchange among leaves (g)

        carbon_content : MTG proporties 
            Carbon content of each organs (g)

        Returns
        -------
        g : MTG
            the above part of the plant

        """
        print("Run the leaf area evolution...")

        outputs=dict()

        growing =[k for k, v in g.properties()['Growth'].items()  if v == True]
        potential_area =[v for k, v in g.properties()['PotentialArea'].items()]
        area =[v for k, v in g.properties()['LeafSurface'].items()]
        carbon_content =[v for k, v in g.properties()['CarbonContent'].items()]
        carbon_growth =[v for k, v in g.properties()['CarbonGrowth'].items()]

        for k, v in g.properties()['CarbonDemand'].items() :
            if v < 0 : 
                outputs['LeafSurface']= dict(zip(growing,[a for a in potential_area]))
            
            else :
                outputs['LeafSurface']= dict(zip(growing,[(a*b)/c for a, b, c in zip(carbon_growth, area, carbon_content)]))  ####From N content, use SFQN to obtain real leaf area, then convert C content (C unit by area depending on stress N)to obtain biomass

        return update_MTG(g,outputs)

        ###Implement carbon storage from C_demand and C_content
    

    
   # def plant_morphogenesis(self, g, initial_step, final_step) :
       # """leaf morphogenesis dynamic.
        
      #  Parameters
       # ----------
      #  g: MTG
      #      the above part of the plant

       # initial_step: int
       #     start time simulation

       # final_step: int
       #     end time simulation
            
       # N: MTG properties
       #     the number of plant

       # k: MTG properties
       #     the number of organs by plant
        
      #  Returns
       # -------
      #  g : MTG
      #      the above part of the plant
        
      #  References
       # ----------
      #  Oughou et al. (2022)

       # """
      #  print("Run the leaf morphogenesis dynamic...")

       # plants =[k for k, v in g.properties()['label'].items()  if v == 'Plant']
       # leaves =[k for k, v in g.properties()['label'].items()  if v == 'Leaf']

       # k = len(leaves)

       # alpha = 


       # for step in range(initial_step, final_step) :

       #   return update_MTG(g,outputs)
    
class Fall:
    """Leaves falling methods. 

    Authors
    -------
    Solen FARRA

    """
    def __init__(self, g, fall = None, nitrogen_fall_threshold = None, nitrogen_fall_threshold_empirical = False,
               Ei_fall_threshold_empirical = False, carbon_fall_threshold = None) :

        self.g = g
        self.mechanistic_fall = self.leaf_mechanistic_falling(g) if fall is None else fall
        self.empirical_fall = self.leaf_empirical_falling(g) if fall is None else fall
        self.nitrogen_fall_threshold_empirical = self.leaf_falling_empirical_nitrogen_threshold(g) if nitrogen_fall_threshold_empirical is None else nitrogen_fall_threshold
        self.nitrogen_fall_threshold = self.leaf_falling_mecanism_nitrogen_threshold(g) if nitrogen_fall_threshold is None else nitrogen_fall_threshold_empirical
        self.Ei_fall_threshold_empirical = self.leaf_falling_empirical_light_threshold(g) if Ei_fall_threshold_empirical is None else carbon_fall_threshold
        self.carbon_fall_threshold = self.leaf_falling_mecanism_carbon_threshold(g) if carbon_fall_threshold is None else Ei_fall_threshold_empirical
            
        return 

    # This function considers whether a leaf should fall or not:
    def leaf_mechanistic_falling(self, g):
        """Leaf fall mecanism.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        CarbonGrowth : MTG proporties
            Carbon left for growth after nitrogen exchange accoring to photosynthesis of each organs (g) 
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        Fall : MTG properties (bool)
            Death or alive state

        Authors
        -------
        Solen FARRA

        References
        ----------
        Field (1983)

        """
        print("Run organs fall...")

        outputs = dict()

        alive = rapeseed = [k for k, v in g.properties()['Fall'].items()  if v ==False]
        rapeseed = [k for k, v in g.properties()['Species'].items()  if v =='Rapeseed' and k in alive]
        senescent = [k for k, v in g.properties()['NitrogenSource'].items()  if v ==True and k in rapeseed]
        carbon_growth = [v for k, v in g.properties()['CarbonGrowth'].items()  if k in senescent]
        leaves = dict(zip(senescent, carbon_growth))

        for k, v in leaves.items() :
            if v < 0 :

                dead = [k]
                outputs['Fall']= dict(zip(dead,[True]))
                outputs['label']= dict(zip(dead,['DeadLeaf']))     
                
                update_MTG(g,outputs)

            else :

                alive = [k]
                outputs['Fall']= dict(zip(alive,[False]))

                update_MTG(g,outputs)


        return update_MTG(g,outputs)
    
    def leaf_empirical_falling(self, g):
        """Leaf fall mecanism.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        CarbonGrowth : MTG proporties
            Carbon left for growth after nitrogen exchange accoring to photosynthesis of each organs (g) 
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        FallEmpirical : MTG properties
            Death or alive state (empiric approach)

        Authors
        -------
        Solen FARRA

        References
        ----------
        Field (1983)

        """
        print("Run organs fall...")

        outputs = dict()

        alive = rapeseed = [k for k, v in g.properties()['Fall'].items()  if v ==False]
        rapeseed = [k for k, v in g.properties()['Species'].items()  if v =='Rapeseed' and k in alive]
        senescent = [k for k, v in g.properties()['NitrogenSource'].items()  if v ==True]
        nitrogen_content = [v for k, v in g.properties()['NitrogenContent'].items() if k in senescent]
        Eabs = [v for k, v in g.properties()['Eabs'].items() if k in senescent]

        for k in rapeseed :

            P = dict(zip(senescent,[(0.5724*a)+b for a, b in zip(nitrogen_content, Eabs)]))

            for k, v in P.items() :
                if v < 1.67879 :
                    
                    dead = [k]
                    outputs['FallEmpirical']= dict(zip(dead,[True]))
                    outputs['label']= dict(zip(dead,['DeadLeaf']))  

                    update_MTG(g,outputs) 
                
                else :

                    alive = [k]
                    outputs['FallEmpirical']= dict(zip(alive,[False]))

                    update_MTG(g,outputs)

        return update_MTG(g,outputs)
    
    # This function considers the final carbon and nitrogen mecanistical threshold for leaf fall:
   
    def leaf_falling_mecanism_carbon_threshold(self, g):
        """Leaf fall nutrient threshold estimation.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        NitrogenContent : MTG proporties
            Actual nitrogen content of each organs (g)
        
        CarbonContent : MTG propoerties
            Actual carbon content of each organs (g)

        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        CarbonFallThresholdMecanism: MTG properties
            fall carbon threshols (mecanist approach)

        Authors
        -------
        Solen FARRA

        References
        ----------
        Field (1983)

        """
        print("Run fall thresholds (mecanistical hypothesis)...")

        outputs = dict()

        fall = [v for k, v in g.properties()['Fall'].items() if v == True]
        carbon_content = [v for k, v in g.properties()['CarbonContent'].items() if k in fall]

        outputs['CarbonFallThresholdMecanism']= dict(zip(fall,[a for a in carbon_content]))
            
        
        return update_MTG(g,outputs)
    
    def leaf_falling_mecanism_nitrogen_threshold(self, g):
        """Leaf fall nutrient threshold estimation.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        NitrogenContent : MTG proporties
            Actual nitrogen content of each organs (g)
        
        CarbonContent : MTG propoerties
            Actual carbon content of each organs (g)

        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        NitrogenFallThresholdMecanism: MTG properties
            fall nitrogen threshols (mecanist approach)

        Authors
        -------
        Solen FARRA

        References
        ----------
        Field (1983)

        """
        print("Run fall thresholds (mecanistical hypothesis)...")

        outputs = dict()

        fall = [v for k, v in g.properties()['Fall'].items() if v == True]
        nitrogen_content = [v for k, v in g.properties()['NitrogenContent'].items() if k in fall]

        outputs['NitrogenFallThresholdMecanism']= dict(zip(fall,[a for a in nitrogen_content]))

        return update_MTG(g,outputs)
    
    # This function considers the final nitrogen and light empirical threshold for leaf fall:
    
    def leaf_falling_empirical_light_threshold(self, g):
        """Leaf fall empirical (light) threshold estimation.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        NitrogenContent : MTG proporties
            Actual nitrogen content of each organs (g)

        Ei : MTG proporties
            Incident light on the organ (W/m2)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded
        
        EiFallThresholdEmpirical

        Authors
        -------
        Solen FARRA

        References
        ----------
        Thomas (2013)

        """
        print("Run fall thresholds (empirical hypothesis)...")

        outputs = dict()

        fall = [v for k, v in g.properties()['Fall'].items() if v == True]
        Ei = [v for k, v in g.properties()['Ei'].items()]

        for k, v in g.properties()['Fall'].items() :
            if v == True :
                
                outputs['EiFallThresholdEmpirical']= dict(zip(fall,[a for a in Ei]))
            
            else :

                pass

        return update_MTG(g,outputs)
    
    def leaf_falling_empirical_nitrogen_threshold(self, g):
        """Leaf fall empirical (light) threshold estimation.
    
        Parameters
        ---------
        g: MTG 
            MTG where properties are recorded
    
        N_content : MTG proporties
            Actual nitrogen content of each organs (g)

        Ei : MTG proporties
            Incident light on the organ (W/m2)
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA

        References
        ----------
        Thomas (2013)

        """
        print("Run fall thresholds (empirical hypothesis)...")

        outputs = dict()

        fall = [v for k, v in g.properties()['Fall'].items() if v == True]
        nitrogen_content = [v for k, v in g.properties()['NitrogenContent'].items()]

        for k, v in g.properties()['Fall'].items() :
            if v == True :
                
                outputs['NitrogenFallThresholdEmpirical']= dict(zip(fall,[a for a in nitrogen_content]))
            
            else :

                pass

        return update_MTG(g,outputs)
    