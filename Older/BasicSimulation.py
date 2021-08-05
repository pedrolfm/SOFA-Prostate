
import sys
import os

from stlib.scene import MainHeader, ContactHeader
from stlib.physics.rigid import Cube
from stlib.physics.rigid import Floor
# A prefab that implements an ElasticMaterialObject
from stlib.physics.deformable import ElasticMaterialObject
import stlib.physics.collision
from stlib.physics.constraints import FixedBox

#Basic example

def createScene(rootNode):
    """Setting up a simple scene"""
    
    MainHeader(rootNode, gravity = [0.0, -981.0, 0.0])
    ContactHeader(rootNode, alarmDistance = 15, contactDistance = 5)
     
    Cube(rootNode, translation = [0.0,60.0,10.0], rotation = [0.0,60.0,10.0], uniformScale = 20.0)
    
    Floor(rootNode, translation = [0.0,-160.0,0.0], isAStaticObject = True)


    return rootNode

