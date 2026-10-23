from openalea.mtg import *
from openalea.mtg.turtle import *
from openalea.mtg import turtle as turt
from openalea.mtg.plantframe import color
from openalea.plantgl.all import *
from openalea.plantgl import all as pgl
from openalea.plantgl.all import Vector3, Color3, Scaled, Color4

import openalea.plantgl.all as pgl

from numpy import *
from pandas import *
import pandas as pd
import math
import numpy as np

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


#leaf shape 
def unileaflet(length=1., width=1.):
    """Generates a unileaflet shape (circle leaf) made with 8 triangles.
    
    Parameters
    ---------
    length: float
        length of the shape defaults to 1.
    width: float
        width of the shape, defaults to 1.
    
    Returns
    ------
    shape : pgl.Group

    AUTHORS
    -------
    Armand GRUMEL and Laurène PERTHAME
        Colzette model

    """
    disc = pgl.Translated((-0.5,0,0), pgl.Disc())
    disc = pgl.Scaled((length, width,1), disc)
    disc = pgl.AxisRotated(axis=(0,1,0), angle=radians(90.), geometry=disc)
    d3 = pgl.AxisRotated(axis=(1,0,0), angle=0., geometry=disc)

    shape = pgl.Group([d3])

    return shape

def species_faba_bean_solo(g):
    "bricolage..."
    
    outputs = dict()

    f = [k for k, v in g.properties()['label'].items()]
    l = [k for k, v in g.properties()['label'].items() if v == 'Leaf']
    
    outputs['Species']= dict(zip(f,['Faba bean']*len(f)))
    outputs['label']= dict(zip(l,['FababeanLeaf']*len(l)))

    return update_MTG(g, outputs)




###3D scene generation    
#Visitors
def ColzetteVisitor(
    g, 
    v,
    turtle,
    ):
    """
    Visitor that can handle an MTG file with multiple plants 
    This function is called by the scene3D() function when creating the 3D scene
    
    g is an MTG tree. In contains all the geometrical information needed by the visitor 
    v is the ID of the vertex being generated (int)
    turtle is the turtle used to create the 3D space
    """

    #retrieve the node and its label 
    v = v 
    nid = g.node(v)
    label = g.label(v)

    if nid.parent() is None :#this is a new plant base
        p = nid.complex_at_scale(scale=1)
        #print('plant no',p)
        if 'PlantPosition' in p.properties():
            #print (p.label, 'moving to ', p.position)
            turtle.move(list(map(float,p.PlantPosition)))
        else:
            print('standing still')
            turtle.move(0,0,0)

        if 'azimuth' in p.properties():
            turtle.rollR(p.azimuth)
    
    turtle.rollL(137.5)

    if g.edge_type(v) == '+':
        
        turtle.setWidth(2.0)


        if label == 'Leaf':
            
            leafscale = Vector3(1, nid.LeafWidth, nid.LeafLength)
        
            turtle.down(nid.InsertionAngle)
            
            turtle.setColor(2)

            turtle.F(nid.PetioleLength)

            turtle.setColor(3)
            
            turtle.down(nid.LeafAngle-nid.InsertionAngle)
            leafshape = unileaflet()
            my_leaf = Scaled(leafscale, leafshape)
            turtle.customGeometry(my_leaf)

            
        if label == 'DeadLeaf' :

            leafscale = Vector3(1, nid.LeafWidth, nid.LeafLength)
    
            turtle.down(nid.InsertionAngle)
            
            turtle.setColor(4)

            turtle.F(nid.PetioleLength)

            turtle.setColor(4)
            
            turtle.down(nid.LeafAngle-nid.InsertionAngle)
            leafshape = unileaflet()

            my_leaf = Scaled(leafscale, leafshape)
            turtle.customGeometry(my_leaf)

            turtle.setColor(4)

        if label == 'FababeanLeaf' :

            leafscale = Vector3(1, 0, 0)
        
            turtle.down(7.0)
            
            turtle.setColor(2)

            turtle.F(3.0)

            turtle.setColor(5)
            
            turtle.down(5.0-2.0)
            leafshape = unileaflet()
            my_leaf = Scaled(leafscale, leafshape)
            turtle.customGeometry(my_leaf)


    if label == 'Internode':
        turtle.setWidth(nid.StemDiam)
        turtle.setColor(1)
        turtle.F(nid.NodeLength)


    turtle.setId(v)


#Scene creation
def prepareScene(scene, width=1200, height=1200, scale=1, x_center=-1.47168e-10, y_center=-0.296039, z_center=7.92478,
                 x_cam=32.619, y_cam=19.5995, z_cam=43.7766, grid=False):
    """
    This function returns the scene that will be used in PlantGL to display the MTG.
    :param scene: the scene to start with
    :param width: the width of the graph (in pixels)
    :param height: the height of the graph (in pixels)
    :param scale: a dimensionless factor for zooming in or out
    :param x_center: the x-coordinate of the center of the graph
    :param y_center: the y-coordinate of the center of the graph
    :param z_center: the z-coordinate of the center of the graph
    :param x_cam: the x-coordinate of the camera looking at the center of the graph
    :param y_cam: the y-coordinate of the camera looking at the center of the graph
    :param z_cam: the z-coordinate of the camera looking at the center of the graph
    :param grid: a Boolean describing whether grids should be displayed on the graph
    :return: scene
    """
    #32.619,19.5995,43.7766
    #-0.333657,0.111502,7.92478
    #-1.47168e-10,-0.296039,7.92478
    # We define the coordinates of the point cam_target that will be the center of the graph:
    cam_target = pgl.Vector3(x_center * scale,
                             y_center * scale + 0.7,
                             z_center * scale)
    # We define the coordinates of the point cam_pos that represents the position of the camera:
    cam_pos = pgl.Vector3(x_cam * scale,
                          y_cam * scale,
                          z_cam * scale)
    # We position the camera in the scene relatively to the center of the scene:
    pgl.Viewer.camera.lookAt(cam_pos, cam_target)
    # We define the dimensions of the graph:
    pgl.Viewer.frameGL.setSize(width, height)
    # We define whether grids are displayed or not:
    pgl.Viewer.grids.set(grid, grid, grid, grid)

    return scene


def scene3d(g, select_visitor=ColzetteVisitor):
    """
    calls a PlantGL turtle to generate a 3D scene
    g is an MTG file
    """
    #color dict of the 3D elements
    colors = dict()
    colors['Internode'] = (100, 100, 80)
    colors['Petiole'] = (100, 100, 80)
    colors['Leaf'] = (9, 82, 40)
    colors['DeadLeaf'] = (255, 255, 0)

    colors['FababeanLeaf'] = (85, 107, 47)

    t = pgl.PglTurtle()
    # set colors 
    color = Color3(*colors['Internode'])
    t.setColorAt(1, color)
    color = Color3(*colors['Petiole'])
    t.setColorAt(2, color)
    color = Color3(*colors['Leaf'])
    t.setColorAt(3, color)
    color = Color3(*colors['DeadLeaf'])
    t.setColorAt(4, color)

    color = Color3(*colors['FababeanLeaf'])
    t.setColorAt(5, color)

    # We compute the colors of the graph:
    #my_colormap(g, property_name, cmap=cmap, vmin=vmin, vmax=vmax, lognorm=lognorm)
    
    # We initialize the scene with the MTG g:
    scene = turt.TurtleFrame(g, visitor=select_visitor, turtle=t, gc=False, all_roots=True)
    # We get a list of all shapes in the scene:
    scene = prepareScene(scene)
    #shapes = dict((sh.id, sh) for sh in scene)

    # We use the property 'color' of the MTG calculated by the function 'my_colormap':
    #colors = g.properties()['color']
    
    # We cover each node of the MTG:
    #for vid in colors:
        #if vid in shapes:
            #n = g.node(vid)
            #key = n._vid
            # If the element is not dead:
            #fall = [v for k, v in g.properties()['Fall'].items() if k == key]
            #for v in fall :
                #if v == True:
                    # We color it according to the property cmap defined by the user:
                    #shapes[vid].appearance = pgl.Material([255,255,0])
                #else:

                    #shapes[vid].appearance = pgl.Material(colors[vid])
                    
                    # Otherwise, we print it in black:
                    #shapes[vid].appearance = pgl.Material([0, 0, 0])
                # property=g.property(prop_cmap)
                # if n.property <=0:
                #     shapes[vid].appearance = pgl.Material([0, 0, 200])
        #else :
            #pass
    
    return scene

def generate_centered_mesh_points(n):
    side_length = int(math.sqrt(n))
    if side_length * side_length < n:
        side_length += 1
    
    points = []
    for i in range(side_length):
        for j in range(side_length):
            if len(points) < n:
                x = (i - (side_length - 1) / 2) / (side_length - 1)
                y = (j - (side_length - 1) / 2) / (side_length - 1)
                z = 0
                points.append((x, y, z))
            else:
                break
    
    return points


def generate_centered_diagonal_mesh_points(n):
    side_length = int(math.sqrt(n))
    if side_length * side_length < n:
        side_length += 1
    
    points = []
    for i in range(side_length):
        for j in range(side_length):
            if len(points) < n:
                x = (i - (side_length - 1) / 2) / (side_length - 1)
                y = (j - (side_length - 1) / 2) / (side_length - 1)
                z = 0
                if i % 2 == 1:  # Shift every other row
                    y += 0.5 / side_length
                points.append((x, y, z))
            else:
                break
    limits= ((-75,-75),(75,75))
    return n,points,limits
