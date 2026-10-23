from dataclasses import dataclass
import genericmodel
from genericmodel.component import Model, declare
from genericmodel.component_factory import *

@dataclass
class LeafCarbon(Model) :

    PotentialPhotosynthesis : float = declare(default = 1.3, 
                                               unit = "umol/m2", 
                                               unit_comment = "of CO2", 
                                               destriction = " ",
                                               min_value = " ",
                                               max_value=" ",
                                               value_comment = " ",
                                               references = "Greenlab model",
                                               DOI = " ",
                                               variable_type = "input",
                                               by = "Photosynthesis model",
                                               state_variable_type=" ",
                                               edit_by="user")
    carbon_demand : float = declare()

    def __init__(g, self, **scenario) :
        self.g=g
        self.prop = self.g.properties()
        self.choregrapher.add_data(data = self.prop)
        self.apply_scenario(**scenario)
        self.link_self_to_mtg()

   
    @priorbalance
    @state
    def _carbon_growth(self):
        return
    
    @selfbalance
    @rate
    @potential
    
    def _carbon_demand(self, CarbonContent, label, PotentialPhotosynthesis) :
        
        if label == 'Leaf' : 
            CarbonDemand = CarbonContent - PotentialPhotosynthesis
        else :
            CarbonDemand = 0.
        
        return CarbonDemand
    
    @selfbalance
    @rate
    @allocation
    def _carbon_storage():
        return
    
    @selfbalance
    @rate
    @allocation
    def _carbon_exported():
        return
    
    @selfbalance
    @rate
    @allocation
    def _carbon_import():
        return
    
    @selfbalance
    @state
    def _carbon_content():
        return
    

       