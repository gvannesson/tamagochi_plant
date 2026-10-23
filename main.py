# import random
# from plant import Plant


# # --- Simulation sur 7 jours avec météo aléatoire ---
# ma_monstera = Plant("Ma monstera")
# possibilites_meteo = ["Pluie", "Grand Soleil", "Nuageux"]

# #TO DO
# #+ Ajouter la possibilité de déplacer la plante à l'intérieur
# #+ Ajouter une température et humidité intérieure ?
# #+ Ajouter des attaques d'insectes/ravageurs ?


# for jour in range(1, 8):
#   meteo_du_jour = random.choice(possibilites_meteo)
#   ma_monstera.simulate_day(jour, meteo_du_jour)




##############################################################

import openalea.plantgl.all as pgl
from openalea.plantgl.all import *

from openalea.mtg import *

import numpy as np
from numpy import *

import pandas as pd
from pandas import *

import time

import mtg
import plant_parameters
import plant


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

# This function enables to record the properties of each element of the MTG:
def recording_MTG_properties(g, file_name):
    """This function records the properties of each node of the MTG "g" inside a csv file.
    
    Parameters
    ---------
    g: MTG 
        MTG where properties are recorded
    file_name: csv fil name (or xlsx)
        the name of the csv file where properties of each node will be recorded
    
    Returns
    ------
    [no return]

    Authors
    -------
    Frederic REES

    """
    # We define the list of all properties of the MTG:
    initial_list_of_properties = list(g.properties().keys())
    # We verify that the list does not contain any "None" property:
    list_of_properties = []
    for property in initial_list_of_properties:
        if property is None:
            print("WARNING: a None property was detected in the MTG!")
            continue
        else:
            list_of_properties.append(property)
    # We sort the list by alphabetical order
    list_of_properties.sort()

    # We create an empty list of node indices:
    node_index = []
    # We create an empty list that will contain the properties of each node:
    g_properties = []

    # We cover all the vertices in the MTG:
    max_scale = g.max_scale()

    for vid in g.vertices_iter(scale = max_scale):
        # Initializing an empty list of properties for the current node:
        node_properties = []
        # Adding the index at the beginning of the list:
        node_properties.append(vid)
        # n represents the vertex:
        n = g.node(vid)
        # For each possible property:
        for property in list_of_properties:
            # We add the value of this property to the list:
            node_properties.append(getattr(n, property, "NA"))
        # Finally, we add the new node's properties list as a new item in g_properties:
        g_properties.append(node_properties)
    # We create a list containing the headers of the dataframe:
    column_names = ['node_index']
    column_names.extend(list_of_properties)
    # We create the final dataframe:
    data_frame = pd.DataFrame(g_properties, columns=column_names)
    # We record the dataframe as a csv file:
    #data_frame.to_csv(file_name, na_rep='NA', index=False, header=True)
    # We record the dataframe as a excel file:
    data_frame.to_csv(file_name,  na_rep='NA', index=False, header=True)

    return

###################################################################################################



class Plant:
    """ Define a plant as an above and below ground MTG.

    Some usefull functions can be defined as proxies.

    Authors
    -------
    Arman GRUMEL and Laurène PERTHAME
        Colzette model

    """
    def __init__(self, name='Rapessed', above=None, below=None):
        self.name = name
        self.above = self.init_above_mtg() if above is None else above
        self.below = self.init_below_mtg() if below is None else below

    @staticmethod
    def init_above_mtg():
        """ Simple function to create a simple aerial MTG

        """
        g = MTG()
        
        # Add a plant (scale is 1)
        vid = g.add_component(g.root, label='Plant')
        vid = g.add_component(vid, label='Axis')
        vid = g.add_component(vid, label='Phytomer')
        
        # Last scale
        vid = g.add_component(vid, label='Internode')
        lid = g.add_child(vid, edge_type='+', label='Leaf')
        bid = g.add_component(vid, edge_type='<', label='Bud')

        fat_mtg(g)

        return g

    @staticmethod
    def init_below_mtg():
        """ Simple function to create a simple belowground MTG or RootSystem Architecture

        Authors
        -------

        """
        g = MTG()
        
        # Add a plant (scale is 1)
        vid = g.add_component(g.root, label='RSA')
        vid = g.add_component(vid, label='Root')
        
        # Last scale
        vid = g.add_component(vid, label='Segment')
    
        fat_mtg(g)

        return g

def vegetative(
    DJ,
    phyllochrone,
    coord,
    name,
    species):
    """ Build a plant with n_nodes internodes
    """

    n_nodes=round(DJ*phyllochrone)
    
    #print('plantes à',n_nodes,'entrenoeuds')
    above = g = MTG()

    for pl in coord:
        if pl == (-71.42857142857142, -10.0, 0.0) :
       
            #print(pl)
            vid = g.add_component(g.root, label='Plant',edge_type='/', PlantPosition=pl) #vid = vertex_id
            vid = g.add_component(vid, label='Axis')

            pid = g.add_component(vid, label='Phytomer') #pid= phytomer_id
            vid = g.add_component(pid, label='Internode') 
            #○g.node(vid).NodeLength = node_length
            g.node(vid).Species = species
            #g.node(vid).short = True
            #leaf_id = g.add_child(vid, Edge_type='+', Label='Leaf')
            
            for i in range(int(n_nodes)-1):
                pid = g.add_child(pid, EdgeType='<', label='Phytomer')
                vid, pid = g.add_child_and_complex(vid, complex=pid, edge_type='<', label='Internode')

                j = i + 1
                lid = g.add_child(vid, edge_type='+', label='Leaf', LeafPosition = j)
                
                #g.node(vid).NodeLength = node_length
                g.node(vid).Species = species
                #g.node(vid).Fall = False
                #g.node(vid).short = True

              
    return Plant(name=name, above = above) 


def species(g): 
    """ Build an mtg of associated plant.
    """
    
    outputs = dict()
    
    species = dict()

    values = [v[1] for k, v in g.properties()['PlantPosition'].items()]
    keys = [k for k, v in g.properties()['PlantPosition'].items()]

    position = dict(zip(keys, values))

    for k, v in position.items() : 
        if v < 0 :
            species[k] = 'Rapeseed'
            
        elif v > 0 :
           species[k] = 'Rapeseed'

        else :
            species[k] = 'Faba bean'
            
    outputs['Species']= species

    return update_MTG(g,outputs)
    

def species_faba_bean_solo(g):
    "bricolage..."
    
    outputs = dict()

    f = [k for k, v in g.properties()['label'].items()]
    l = [k for k, v in g.properties()['label'].items() if v == 'Leaf']
    
    outputs['Species']= dict(zip(f,['Faba bean']*len(f)))
    outputs['label']= dict(zip(l,['FababeanLeaf']*len(l)))

    return update_MTG(g, outputs)


def leaf_species(g):
    "bricolage..."
    
    faba = dict()
    rapeseed = dict()
    l = dict()
    outputs = dict()

    r = [k for k, v in g.properties()['Species'].items() if v == 'Faba bean']
    n = [k for k, v in g.properties()['label'].items()]

    min_r = min(r)
    max_r = max(r)
    
    intervalle = [i for i in range(min_r, max_r+44)]

    listSub = [k for k in n if k not in intervalle]
    vv = [v for k, v in g.properties()['label'].items()]

    list_r = dict(zip(listSub, vv))
    list_f = dict(zip(intervalle, vv))

    d = dict(g.properties()['Species'].items())
    dl = dict(g.properties()['label'].items())

    for k, v in list_r.items() :
        if not v == 'Plant' :
            rapeseed[k] = 'Rapeseed'

            for i in intervalle :
                faba[i] = 'Faba bean'
                
                for k,v in list_f.items():
                    if v == 'Leaf':
                        l[k] = 'FababeanLeaf'

    leaf_species = d | rapeseed | faba
    leaf_label = dl | l

    outputs['Species']= leaf_species
    outputs['label']= leaf_label

    return update_MTG(g,outputs)

##Mtg builder with mutliple plants
# functions from Adel used in vegetative_rapeseed_field()
def adel_regular(nb_plants, nb_rank, dx, dy, nx=None):
    
    if nx is None:
        nx = int(nb_plants/nb_rank)
    ny = nb_rank
    domain = ((0,0),(nx*dx, ny*dy))
    return [(i*dx+dx/2., j*dy+dy/2., 0.) for j in range(ny) for i in range(nx)], domain



def agronomicplot(nplants, 
                  length, 
                  width, 
                  sowing_density, 
                  plant_density, 
                  inter_row,
                  nrow, 
                  noise=0, 
                  convunit=100, 
                  center_scene=True
                  ):
    """ Returns the number of plants, the positions, the domain (scene units), the domain area (square meter) and the conversion coefficient for meter to scene unit (1/convunit) of a micro-plot specified with agronomical variables
    nplants is the number of plants of the micro-plot (mandatory if length or width is None)
    length (m) is plot dimension along row direction (mandatory if nplants is None)
    width (m) is plot dimension perpendicular to row direction (mandatory if nplants is None)
    sowing density is the density of seeds sawn (mandatory) #surfacic density ?
    plant_density is the density of plants that are present (after loss due to bad emergence, early death...) (mandatory)
    inter_row (m) is for the  distance between rows (mandatory)
    noise (%), indicates the precision of the sowing for the inter plant spacing
    convunit is the conversion factor from meter to scene unit
    center_scene allows to center the position around origin. If False, the scene is in the x+,y+ sector, the origin being at the lower left corner of the domain
    
    Rows are Eiallel to x-axis
    Length and Width are adjusted to produce a canopy centered in its domain and compliant with infinitisation
    """
    from operator import itemgetter
    import random

    sowing_density = plant_density

    inter_plant = 1. / inter_row / sowing_density
    
    if nplants is None: # length and width are NOT None
        nrow = max(1, int(float(width) / inter_row))
        plant_per_row = max(1, int(float(length) / inter_plant))
        nplants = nrow * plant_per_row
        
    else: # nplants is NOT None ; length and width are None 
        #import math
        #nrow = max(1, int(math.sqrt(nplants)))
        nrow = nrow
        
    dx = inter_plant * convunit
    dy = inter_row * convunit
    positions, domain = adel_regular(nplants, nrow, dx, dy)
    n_emerged = int(nplants * plant_density / sowing_density)
    positions = random.sample(positions, n_emerged)
    # sorting by ranks
    positions = sorted(positions, key= itemgetter(1,0))
    domain_area = abs(domain[1][0] - domain[0][0]) / convunit * abs(domain[1][1] - domain[0][1]) / convunit
    if center_scene:
        xc = float(domain[1][0] + domain[0][0]) / 2
        yc = float(domain[1][1] + domain[0][1]) / 2
        positions = [(x - xc, y - yc, z) for x, y, z in positions]
        domain = ((domain[0][0] - xc, domain[0][1] - yc), (domain[1][0] - xc, domain[1][1] - yc))
    
    return n_emerged, positions, domain, domain_area, 1. / convunit

def vegetative_field(
    DJ,
    phyllochrone,
    coord,
    name,
    species):
    """ Build a field with nrows(coord) plants that have n_nodes internodes

    """
    n_nodes=round(DJ*phyllochrone)
    
    #print('plantes à',n_nodes,'entrenoeuds')
    above = g = MTG()

    for pl in coord:
       
        #print(pl)
        vid = g.add_component(g.root, label='Plant',edge_type='/', PlantPosition=pl) #vid = vertex_id
        vid = g.add_component(vid, label='Axis')

        pid = g.add_component(vid, label='Phytomer') #pid= phytomer_id
        vid = g.add_component(pid, label='Internode') 
        #g.node(vid).NodeLength = node_length
        g.node(vid).Species = species
        #g.node(vid).short = True
        #leaf_id = g.add_child(vid, Edge_type='+', Label='Leaf')
        
        for i in range(n_nodes-1):
            pid = g.add_child(pid, EdgeType='<', label='Phytomer')
            vid, pid = g.add_child_and_complex(vid, complex=pid, edge_type='<', label='Internode')

            j = i + 1
            lid = g.add_child(vid, edge_type='+', label='Leaf', LeafPosition = j)
            
            g.node(vid).Node = j
            g.node(vid).Species = species
            g.node(vid).Fall = False
            g.node(vid).short = True

    return Plant(name=name, above = above) 

###################################################################""


class PlotMTG:
    """Run MTG methods.

    Authors
    -------
    Solen FARRA

    """
    print("Choose a method to create the MTG...")
    
    def __init__(self, csv_filename, plant_dataframe, field_dataframe = None) :
       
        self.plant_dataframe = self.create_plant_MTG_from_scratch() if plant_dataframe is None else field_dataframe
       

        return 

    
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
        parcelle = agronomicplot(numofseeds,
                                      nplants,
                                      length,
                                      width,
                                      sowing_density,
                                      inter_row,
                                      nrow,
                                      plant_density)
        coord=parcelle[1]

        g = vegetative( DJ,
                                phyllochrone,
                                coord,
                                name,
                                species
                                ).above

        mtg.species_faba_bean_solo(g)

        plant_parameters.monstera_phenotype(g)
        plant_parameters.monstera_metabolism(g)

        recording_MTG_properties(g, file_name = 'MTG_0000.csv')

        return g, parcelle
    
    



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
            
            plant.Photosynthesis.caribu(g = g, parcelle = parcelle)
            
            # We recording a snapshot a the MTG with caribu color legend:
            plot_name = 'plot_caribu_%.5d.png' % step
            pgl.Viewer.saveSnapshot(plot_name) 

            plant.Photosynthesis.leaf_photosynthesis(g = g, alpha = 0.1)
            
            plant.PotentialGrowth(g,
                            potential_photosynthesis = None,
                            potential_area = None, 
                            area = None)
            
            plant.Competition(g, 
                        carbon_deficit = None,
                        source_N = None, 
                        sink_N = None)
            
            plant.Nitrogen(g,
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
            
            plant.Carbon(g, 
                   carbon_growth = None,
                   carbon_demand = None,
                   carbon_import = None,
                   carbon_export = None,
                   carbon_storage = None,
                   carbon_content = None)
            
            plant.Growth(g, area = None)
            
            plant.Fall(g, 
                 fall = None,
                 nitrogen_fall_threshold = None,
                 nitrogen_fall_threshold_empirical = False,
                 Ei_fall_threshold_empirical = False,
                 carbon_fall_threshold = None)
           
            # We view the plant MTG with PlantGL:
            pgl.Viewer.display(mtg.scene3d(g, select_visitor = mtg.ColzetteVisitor))
           
            # We recording a snapshot of the MTG:
            plot_name = 'plot_%.5d.png' % step
            pgl.Viewer.saveSnapshot(plot_name)

            # We record the main properties of the MTG:
            file_name = 'MTG_%.5d.xlsx' % step
            recording_MTG_properties(g, file_name)

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
                                                    nplants = 1,
                                                    sowing_density = 35,
                                                    inter_row = 0.1,
                                                    nrow = 3,#raw by box (PHOCUS)
                                                    plant_density = 35,
                                                    DJ = 950,
                                                    phyllochrone = 0.015,
                                                    name = 'Solen',
                                                    species = 'Faba bean',
                                                    length = 1.0,
                                                    width = 1.0)

        Simulation.main(g, parcelle, default, initial_step, final_step)

        return g
    
    


######################################################################################################################################""

Run.faba_bean_plant_simulation(default = None, 
                     initial_step = 1, 
                     final_step = 1)