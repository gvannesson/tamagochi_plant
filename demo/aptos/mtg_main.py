from openalea.mtg import *

import numpy as np

##########################


def update_MTG(g, outputs):
    """
    Update the MTG 
    :Param dict outputs: {'Eiam1': { vid1: , vid2, ...}, 'Eiam2': { vid1: , vid2, ...}}
    """
     # add the missing property
    for param in outputs.keys():
        if param not in g.properties():
            g.add_property(param)
        # update the MTG
        g.property(param).update(outputs[param])

###########################################

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

        Authors
        -------
        Arman GRUMEL and Laurène PERTHAME
            Colzette model

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
        Arman GRUMEL and Laurène PERTHAME
            Colzette model

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
            
            for i in range(n_nodes-1):
                pid = g.add_child(pid, EdgeType='<', label='Phytomer')
                vid, pid = g.add_child_and_complex(vid, complex=pid, edge_type='<', label='Internode')

                j = i + 1
                lid = g.add_child(vid, edge_type='+', label='Leaf', LeafPosition = j)
                
                #g.node(vid).NodeLength = node_length
                g.node(vid).Species = species
                #g.node(vid).Fall = False
                #g.node(vid).short = True

                


    return Plant(name=name, above = above) 

def vegetative_DJ(
    DJ: int = 950,
    node_length: float= 0.02,
    phyllochrone = 0.015,
    name = 'Rapeseed'

    ):
    """ Build an mtg of a single plant. The number of internodes is based on its age (DD) and phyllochrone 
    """
    n_nodes=round(DJ*phyllochrone)
    above = g = MTG()
    vid = g.add_component(g.root, label='Plant')
    vid = g.add_component(vid, label='Axis')

    pid = g.add_component(vid, label='Phytomer')
    vid = g.add_component(pid, label='Internode')
    g.node(vid).NodeLength = node_length
    #g.node(vid).short = True
    leaf_id = g.add_child(vid, edge_type='+', label='Leaf')
    
    for i in range(n_nodes-1):
        pid = g.add_child(pid, edge_type='<', label='Phytomer')
        vid, pid = g.add_child_and_complex(vid, complex=pid, edge_type='<', label='Internode')
        g.node(vid).NodeLength = node_length
        #g.node(vid).short = True

        leaf_id = g.add_child(vid, edge_type='+', label='Leaf')

    return Plant(name, above = above)


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
            #g.node(vid).Fall = False
            #g.node(vid).short = True

    return Plant(name=name, above = above) 


