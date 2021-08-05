
import sys
import os

from stlib.scene import MainHeader, ContactHeader
from stlib.physics.rigid import Cube
from stlib.physics.rigid import Floor
# A prefab that implements an ElasticMaterialObject
from stlib.physics.deformable import ElasticMaterialObject
import stlib.physics.collision
from stlib.physics.constraints import FixedBox

# This function includes the whole mechanical model of the silicone piece, as written in the previous step, except that the prefab ElasticMaterialObject is used, instead of creating each component.
def ElasticBody(parent):
    """Create an object with an elastic deformation law"""
    body = parent.createChild("ElasticBody")

    # Prefab ElasticMaterialObject implementing the whole mechanical model of the silicone piece
    e = ElasticMaterialObject(body,
                              volumeMeshFileName="data/mesh/tripod_mid.gidmsh",
                              poissonRatio=0.45,
                              youngModulus=800,
                              totalMass=0.032,
                              rotation=[90, 0, 0])

    # Visual model
    visual = e.createChild("Visual")
    visual.createObject("MeshSTLLoader",
                        name="loader",
                        filename="/Users/pedro/Downloads/mac/SOFA_v19.06.99_custom_MacOS_v11/plugins/SoftRobots/docs/tutorials/Tripod/mesh/tripod_mid.stl",
                        rotation=[90, 0, 0])
    visual.createObject("OglModel",
                        name="renderer",
                        src="@loader",
                        color=[1.0, 1.0, 1.0, 0.5])
    visual.createObject("BarycentricMapping",
                        input=e.dofs.getLinkPath(),
                        output=visual.renderer.getLinkPath())
    return body

def createScene(rootNode):
    """Setting up a simple scene"""
    
    MainHeader(rootNode, gravity = [0.0, -981.0, 0.0])
    ContactHeader(rootNode, alarmDistance = 5, contactDistance = 1)
     
    Cube(rootNode, translation = [0.0,60.0,10.0], uniformScale = 2.0)
    
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
    
    # Bulbo = ElasticMaterialObject(rootNode, name="Bulbo",
    #                 volumeMeshFileName="/Users/pedro/Downloads/mac/Data/Prosta_16_16.msh",
    #                 surfaceMeshFileName="/Users/pedro/Downloads/mac/Data/Prosta_16_16.stl",                     
    #                 collisionMesh =	"/Users/pedro/Downloads/mac/Data/Prosta_16_16.stl",
    #                 withConstrain=True,
    #                 surfaceColor=[0.2, 0.9, 0.0],
    #                 scale=[0.9, 0.9, 0.9],
    #                 poissonRatio=0.49,
    #                 youngModulus=90000,
    #                 translation=[0.0,60.0,35.0])
    
    fixingBox=[0.0,0.0,0.0]
    BoxROICoordinates=[-5, 0, -5,  5, 1, 5]
    FixedBox(Prostate, atPositions=[-10.0,-1.0,-20.0,60.0,60.0,5.0], doVisualization=True)
    
    
    # scene = Scene(rootNode, gravity=[0.0, -981.0, 0.0])
    # scene.dt = 0.025
    # scene.VisualStyle.displayFlags = "showBehavior"
    # 
    # scene.Config.createObject("MeshSTLLoader", name="loader", filename="/Users/pedro/Downloads/mac/SOFA_v19.06.99_custom_MacOS_v11/plugins/SoftRobots/docs/tutorials/Tripod/details/data/mesh/blueprint.stl")
    # scene.Config.createObject("OglModel", src="@loader")
    # body = ElasticBody(scene.Modelling)
    # fix = FixingBox(scene.Modelling,
    #             body.ElasticMaterialObject,
    #             eulerRotation=[0,0,0],
    #             translation=[0.0, .0, 0.0],
    #             scale=[30., 30., 30.])
    # 
    # # Changing the property of the Box ROI so that the constraint area appears on screen.
    # fix.BoxROI.drawBoxes = True
    # 
    return rootNode

