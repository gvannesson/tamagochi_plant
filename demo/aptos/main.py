import openalea.plantgl.all as pgl
from openalea.plantgl.all import *

from openalea.mtg import *

import numpy as np
from numpy import *

import pandas as pd
from pandas import *

import time

from aptos import mtg_main as mtg
 
from aptos import parameters_rapeseed
from aptos import parameters_faba_bean 
from aptos import mtg_visualization 
from aptos import model
from aptos import tools as files

from openalea.caribu.CaribuScene import CaribuScene

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
    Armand GRUMEL and Laurène PERTHAME
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

class PlotMTG:
    """Run MTG methods.

    Authors
    -------
    Solen FARRA

    """
    print("Choose a method to create the MTG...")
    
    def __init__(self, csv_filename, plant_dataframe, field_dataframe = None) :
        
        self.csv_filename = self.create_MTG_from_csv_file() if csv_filename is None else None
        self.plant_dataframe = self.create_plant_MTG_from_scratch() if plant_dataframe is None else field_dataframe
        self.field_dataframe = self.create_field_MTG_from_scratch() if field_dataframe is None else plant_dataframe

        return 

    @staticmethod
    def create_faba_bean_field_MTG_from_scratch(numofseeds,
                                      nplants,
                                      length,
                                      width,
                                      sowing_density,
                                      inter_row,
                                      nrow,
                                      plant_density,
                                      DJ,
                                      phyllochrone,
                                      name,
                                      species):
        """Creation of the MTG from zero with a generic MTG pipeline and properties functions.
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Frederic REES

        """
        print("Create the MTG from scratch...")
        
        #We plot the MTG:
        parcelle = mtg.agronomicplot(numofseeds,
                                      nplants,
                                      length,
                                      width,
                                      sowing_density,
                                      inter_row,
                                      nrow,
                                      plant_density)
        coord=parcelle[1]

        g = mtg.vegetative_field( DJ,
                                phyllochrone,
                                coord,
                                name,
                                species
                                ).above

        mtg.species_faba_bean_solo(g)

        parameters_faba_bean.faba_bean_phenotype(g)
        parameters_faba_bean.faba_bean_metabolism(g)

        #files.recording_MTG_properties(g, file_name = 'MTG_0000.csv')

        return g, parcelle
    
    def create_faba_bean_plant_MTG_from_scratch(numofseeds,
                                      nplants,
                                      length,
                                      width,
                                      sowing_density,
                                      inter_row,
                                      nrow,
                                      plant_density,
                                      DJ,
                                      phyllochrone,
                                      name,
                                      species):
        """Creation of the MTG from zero with a generic MTG pipeline and properties functions.
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Frederic REES

        """
        print("Create the MTG from scratch...")
        # We read the environemental/initial conditions:
        #input_dataframe = pd.read_excel(r'C:\Users\FARRA\AppData\Local\GitHubDesktop\app-3.2.3\src\caracol\src\caracol\APTOS_input_1.xlsx', header=0, sheet_name="scenario")

        #We plot the MTG:
        parcelle = mtg.agronomicplot(numofseeds,
                                      nplants,
                                      length,
                                      width,
                                      sowing_density,
                                      inter_row,
                                      nrow,
                                      plant_density)
        coord=parcelle[1]

        g = mtg.vegetative( DJ,
                                phyllochrone,
                                coord,
                                name,
                                species
                                ).above

        mtg.species_faba_bean_solo(g)

        parameters_faba_bean.faba_bean_phenotype(g)
        parameters_faba_bean.faba_bean_metabolism(g)

        #files.recording_MTG_properties(g, file_name = 'MTG_0000.csv')

        return g, parcelle
    
    @staticmethod
    def create_field_MTG_from_scratch(numofseeds,
                                      nplants,
                                      length,
                                      width,
                                      sowing_density,
                                      inter_row,
                                      nrow,
                                      plant_density,
                                      DJ,
                                      phyllochrone,
                                      name,
                                      species
                                      ):
        """Creation of the MTG from zero with a generic MTG pipeline and properties functions.
        
        Returns
        ------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Frederic REES

        """
        print("Create the field MTG from scratch...")
        # We read the environemental/initial conditions:
        #input_dataframe = pd.read_excel(r'C:\Users\FARRA\AppData\Local\GitHubDesktop\app-3.2.3\src\caracol\src\caracol\APTOS_input_1.xlsx', header=0, sheet_name="scenario")

        #We plot the MTG:
        parcelle = mtg.agronomicplot(numofseeds,
                                      nplants,
                                      length,
                                      width,
                                      sowing_density,
                                      inter_row,
                                      nrow,
                                      plant_density)
        coord=parcelle[1]

        g = mtg.vegetative_field( DJ,
                                phyllochrone,
                                coord,
                                name,
                                species
                                ).above

        mtg.species(g)
        mtg.leaf_species(g)

        parameters_rapeseed.rapeseed_phenotype(g)
        parameters_rapeseed.rapeseed_metabolism(g)

        parameters_faba_bean.faba_bean_phenotype(g)
        parameters_faba_bean.faba_bean_metabolism(g)

        #files.recording_MTG_properties(g, file_name = 'MTG_0000.csv')

        return g, parcelle
    

    @staticmethod
    def create_MTG_from_Colzette(PlantAge,
                                  phylloc,
                                  numofseeds,
                                  pattern,
                                  inter_row,
                                  plant_density) :
        """Creation of the MTG base on Colzette model (dynamical simulation)
        
        Authors
        -------
        Arman GRUMEL & Laurène PERTHAME
            Colzette model
        
        """

        #PlantAge plant age in DD 
        #phylloc plant phyllochrone Leaf/DD
        #numofseeds number of plants to simulate
        #pattern  pattern can be 'Rows' or 'Homogeneous'   /!\ if numofseeds=1, 'Rows' is applied by default

        outputfilename ='Results_'+str(round(PlantAge*phylloc))+'L_'+str(numofseeds)+pattern[0]

        data = pd.read_csv("Valeursparam.csv",sep=";")

        Results = pd.DataFrame()
        """
        Results['SurfProp']=list() #Surface proportion repartition
        Results['LeafS']=list()
        Results['LeafL']=list()
        Results['LeafW']=list()
        Results['RealLeafS']=list()
        Results['Ei']=list()
        Results['Eabs']=list()
        Results['TheoLeafS']=list()
        Results['RatiosWL']=list()
        """
        progress = 0 

        print(len(data),"combinations to run. Let's get started !")

        for index,row in data.iterrows() :

            Temporary_Res = dict()

            progress += 1
            print('Progress : ' , progress, '/', len(data))
            
            #1 create an MTG for a plant at a certain age (DD), for a given phyllochron (n_leaves/DD)
            if pattern=='Rows' or numofseeds==1:
                parcelle = parameters_rapeseed.agronomicplot(nplants = numofseeds,
                                                    length=1,
                                                    width=1,
                                                    sowing_density = plant_density,
                                                    inter_row = inter_row,
                                                    plant_density = plant_density)
                #parcelle[0] : nb de plantes, 
                #parcelle[1] : coordonnées, 
                #parcelle[2] : limites du domaine (-x,-y,x,y),
                #parcelle[3] : surface en m2 du domaine, 
                #parcelle[4] : coefficient de conversion de mètre à l'unitée utilisée dans la scène
                    
                    
                g = parameters_rapeseed.vegetative_rapeseed_field(PlantAge,
                                                        phyllochrone = phylloc,
                                                        coord=parcelle[1]).above 

            elif pattern == 'Homogeneous': 
                parcelle = mtg_visualization.generate_centered_diagonal_mesh_points(numofseeds)
                g = parameters_rapeseed.vegetative_rapeseed_field(PlantAge,
                                                           phyllochrone = phylloc,
                                                           coord = multiply(parcelle[1],100)).above 
                

            #2 attribute architectural properties to the MTG 
            parameters_rapeseed.phenotype(g,
                                   skew = 5,
                                   phyllot = 137.5,
                                   leaf_angle = 80,
                                   coeff_petiole = 0.51017, #limb length to petiole length , 0.31017 length/whole leag length
                                   stem_d = 0.1,
                                   coeff_petiole_d = 0.5,
                                   total_surface=300,
                                   leaf_max = row["LargLeafPos"],
                                   sd = row["LS_spread"],
                                   amp = row['Bell_amp'],
                                   ins_angle = row["Ins_angle"],
                                   coeff_width = row["coefLenWid"]
                                   )

            Temporary_Res = Temporary_Res | g.properties()
        
            #TO DO (optional) : generate 3D archi and save picture 

            #3 CARIBU
            can = mtg_visualization.scene3d(g)
            zenith=[(100,(0,0,-1))]
            #opts = list(map(str, [data_path('par.opt'), data_path('nir.opt')]))

            cs = CaribuScene(scene=can,light=zenith,pattern=parcelle[2])
            raw,agg=cs.run(infinite=True,simplify=True,direct=False)

            Temporary_Res = Temporary_Res | agg

            Temporary_Res=pd.DataFrame.from_dict(Temporary_Res,orient='columns')

            Results=pd.concat([Results,Temporary_Res])
            filtered_results = Results[Results['label']=='Leaf']
            
            Results.to_csv('Colzetteresults2.csv')
            filtered_results.to_csv(outputfilename+'.csv')

            return g

class Simulation:
    """Run a simulation according a configure scenario.

    Authors
    -------
    Solen FARRA

    """
    print("Choose and init a simulation scenario...")
    # We define an initial and final step for covering a certain period:
    def __init__(self,
                 g,
                 parcelle,
                 default,
                 initial_step, 
                 final_step) :
    
        self.parcelle = parcelle
        self.default = self.main(g, parcelle, default, initial_step, final_step) if default is None else default
       
    @staticmethod
    def main(g, parcelle, default, initial_step, final_step):
        """Run a default simulation.

        Parameters
        ----------
        g: MTG 
            MTG where properties are recorded

        initial_step : int
            first time step of the simulation
        
        finl_step : int
            end time step of the simulation
        
        Returns
        -------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA
        Frederic REES

        """
        print("")
        print("Start simulation...")

        tps1 = time.process_time()
       
        # For each time step covering the simulation period:
        for step in range(initial_step, final_step+1):
            print("")
            print("For step", step,":")

            outputs = dict()
            leaves = [k for k, v in g.properties()['label'].items()]
            outputs['Time']= dict(zip(leaves,[step]*len(leaves)))
            update_MTG(g,outputs)

            # We successively call the different class and methods:
            
            model.Photosynthesis.caribu(g = g, parcelle = parcelle)
            
            # We recording a snapshot a the MTG with caribu color legend:
           # plot_name = 'plot_caribu_%.5d.png' % step
            #pgl.Viewer.saveSnapshot(plot_name) 

            model.Photosynthesis.leaf_photosynthesis(g = g, alpha = 0.1)
            
            model.PotentialGrowth(g,
                            potential_photosynthesis = None,
                            potential_area = None, 
                            area = None)
            
            model.Competition(g, 
                        carbon_deficit = None,
                        source_N = None, 
                        sink_N = None)
            
            model.Nitrogen(g,
                     potential_nitrogen_content = None,
                     nitrogen_demand = None,
                     weight_import = None,
                     weight_export = None,
                     nitrogen_import = None,
                     nitrogen_export = None,
                     nitrogen_storage = None,
                     carbon_expend = None,
                     nitrogen_content = None,
                     NRUE = None,
                     carbon_nitrogen_ratio = None)
            
            model.Carbon(g, 
                   carbon_growth = None,
                   carbon_demand = None,
                   carbon_import = None,
                   carbon_export = None,
                   carbon_storage = None,
                   carbon_content = None)
            
            model.Growth(g, area = None)
            
            model.Fall(g, 
                 fall = None,
                 nitrogen_fall_threshold = None,
                 nitrogen_fall_threshold_empirical = False,
                 Ei_fall_threshold_empirical = False,
                 carbon_fall_threshold = None)
           
            # We view the plant MTG with PlantGL:
            #pgl.Viewer.display(mtg_visualization.scene3d(g, select_visitor = mtg_visualization.ColzetteVisitor))
           
            # We recording a snapshot of the MTG:
            #plot_name = 'plot.png' % step
            #pgl.Viewer.saveSnapshot(plot_name)

            # We record the main properties of the MTG:
            file_name = 'MTG.xlsx'
            files.recording_MTG_properties(g, file_name)

            #files.recording_MTG_df(g, file_name)

            #Results = pd.DataFrame()
            #Results = pd.concat([Results,results_df])
            
            #leaf_results = Results[Results['label']=='Leaf']
            #plant_results = Results[Results['label']=='Plant']

        print("")
        print("Simulation is done!")

        tps2 = time.process_time()
        print('Execution time: ', tps2 - tps1)

        return g
    
class Run :
    """Run all.

    Authors
    -------
    Solen FARRA

    """
    print("Choose and init a mtg type simulation ...")

    def __init__():
        
        return
        
    

    @staticmethod
    def faba_bean_plant_simulation(default, initial_step, final_step):
        """Run with a single plant MTG.

        Parameters
        ----------
        g: MTG 
            MTG where properties are recorded

        initial_step : int
            first time step of the simulation
        
        finl_step : int
            end time step of the simulation
        
        Returns
        -------
        g: MTG 
            MTG where properties are recorded

        Authors
        -------
        Solen FARRA
        Frederic REES

        """
        g, parcelle = PlotMTG.create_faba_bean_plant_MTG_from_scratch(numofseeds = 18,
                                                    nplants = 18,
                                                    sowing_density = 35,
                                                    inter_row = 0.1,
                                                    nrow = 3,#raw by box (PHOCUS)
                                                    plant_density = 35,
                                                    DJ = 950,
                                                    phyllochrone = 0.015,
                                                    name = 'Solen',
                                                    species = 'Faba bean',
                                                    length = None,
                                                    width = None)

        Simulation.main(g, parcelle, default, initial_step, final_step)

        return g
    
    


######################################################################################################################################""

# #Run.faba_bean_plant_simulation(default = None, 
#                      initial_step = 1, 
#                      final_step = 2)



    