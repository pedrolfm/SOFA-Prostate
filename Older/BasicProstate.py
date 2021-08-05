
import sys
import os

from stlib.scene import MainHeader, ContactHeader
from stlib.physics.rigid import Cube
from stlib.physics.rigid import Floor
from stlib.physics.rigid import Sphere
# A prefab that implements an ElasticMaterialObject
from stlib.physics.deformable import ElasticMaterialObject
import stlib.physics.collision
from stlib.physics.constraints import FixedBox

def createScene(rootNode):
    """Setting up a simple scene"""
    
    MainHeader(rootNode, gravity = [0.0, -981.0, 0.0])
    ContactHeader(rootNode, alarmDistance = 5, contactDistance = 1)
     
    #cube(rootNode, translation = [10.1,60.0,10.0], uniformScale = 1.0)
    
    Floor(rootNode, translation = [0.0,-160.0,0.0], isAStaticObject = True)
    
    
    Prostate = ElasticMaterialObject(rootNode, name="Prostate",
                        volumeMeshFileName="/Users/pedro/Downloads/mac/Data/Prosta_2_2.msh",
                        surfaceMeshFileName="/Users/pedro/Downloads/mac/Data/Prosta_2_2.stl",                     
                        collisionMesh =	"/Users/pedro/Downloads/mac/Data/Prosta_2_2.stl",
                        withConstrain=True,
                        surfaceColor=[0.0, 0.70, 1.0],
                        scale=[0.9, 0.9, 0.9],
                        poissonRatio=0.49,
                        youngModulus=500,
                        translation=[10.0,0.0,0.0])
    
    Bulbo = ElasticMaterialObject(rootNode, name="Bulbo",
                    volumeMeshFileName="/Users/pedro/Downloads/mac/Data/needle_s.msh",
                    surfaceMeshFileName="/Users/pedro/Downloads/mac/Data/needle_s.stl",                     
                    collisionMesh =	"/Users/pedro/Downloads/mac/Data/needle_s.stl",
                    withConstrain=True,
                    surfaceColor=[0.2, 0.9, 0.0],
                    scale=[0.9, 0.9, 0.9],
                    poissonRatio=0.33,
                    youngModulus=100000,
                    translation=[0.0,160.0,60.0],
                    rotation=[90.0,0.0,0.0])
    
    fixingBox=[0.0,0.0,0.0]
    BoxROICoordinates=[-5, 0, -5,  5, 1, 5]
    FixedBox(Prostate, atPositions=[-10.0,-1.0,-20.0,60.0,60.0,5.0], doVisualization=True)
    
    # fixingBox=[0.0,0.0,0.0]
    # BoxROICoordinates=[-5, 0, -5,  5, 1, 5]
    # PartiallyFixedBox(attachedTo=Bulbo, fixedAxis=[1, 0,1], box=[-10.0,140.0,-20.0,10.0,170.0,25.0], drawBoxes = True )
    
    return rootNode

