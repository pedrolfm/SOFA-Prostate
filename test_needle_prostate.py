import Sofa.Core

USE_GUI = True


def main():
    import SofaRuntime
    import Sofa.Gui
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")

    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.createGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()

def createScene(root):

    root.gravity=[0, 0, 0]
    root.dt=0.2

    root.addObject('DefaultVisualManagerLoop')
    root.addObject('FreeMotionAnimationLoop')

    root.addObject('VisualStyle', displayFlags="showCollisionModels")
    root.addObject('RequiredPlugin', pluginName="SofaOpenglVisual SofaBoundaryCondition SofaGeneralLoader SofaGeneralSimpleFem SofaMiscCollision CImgPlugin")
    root.addObject('DefaultPipeline', name="CollisionPipeline")
    root.addObject('BruteForceDetection', name="N2") #TODO: use the new implementation.
    root.addObject("LocalMinDistance", name="Intersection", alarmDistance="3", contactDistance="1")
    #root.addObject("LocalMinDistance", name="Intersection", alarmDistance="3", contactDistance="2", useLMDFilters="0")
    root.addObject('RuleBasedContactManager', name="CollisionResponse", response="FrictionContact", responseParams="mu=0.3")
    root.addObject('DiscreteIntersection')
    root.addObject('GenericConstraintSolver',maxIterations = 1000, tolerance = 1e-07)


    #mesh was generated using Gmesh and a vtk model from a prostate MR mage in 3D Slicer
    meshName = "./Data/Prosta_2_2.msh"
    

# Prostate model:

    prostate = root.addChild('prostate')
    prostate.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness="0.1", rayleighMass="0.1")
    prostate.addObject('CGLinearSolver', name="linear_solver", iterations="25", tolerance="1e-09", threshold="1e-09")
    #prostate.addObject('MeshSTLLoader', name="meshLoader1", filename=meshName)
    prostate.addObject('MeshGmshLoader', name="meshLoader1", filename=meshName)
    prostate.addObject('TetrahedronSetTopologyContainer', name="topo", src="@meshLoader1") 
    prostate.addObject('MechanicalObject', name="mech", template="Vec3d", dx="0", dy="0", dz="0", rx="0", ry="0", rz="0" )
    prostate.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
    prostate.addObject('DiagonalMass', name="Mass", massDensity="1.0")
    prostate.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio="0.49", youngModulus="3000", computeGlobalMatrix="0")
    #prostate.addObject('TetrahedronFEMForceField', template="Vec3d", name="FEM", youngModulus="5000", poissonRatio = "0.49")
        #prostate.addObject('RegularGridSpringForceField', template="Vec3d", name="FEM", stiffness="5000", damping = "100")
    prostate.addObject('UncoupledConstraintCorrection')
    

    #vizualization
    visu = prostate.addChild('Visu')
    #visu.addObject('MeshSTLLoader',name="meshLoader",filename=meshName)
    visu.addObject('MeshGmshLoader',name="meshLoader",filename=meshName)
    visu.addObject('OglModel', name="VisualModel", color="#ecc854", src="@meshLoader")
    visu.addObject('BarycentricMapping', name="VisualMapping", output="@VisualModel")


    #collision model
    surf = prostate.addChild('Surf')
    surf.addObject('MeshGmshLoader', name="MeshLoader", filename=meshName)
    #surf.addObject('MeshSTLLoader', name="MeshLoader", filename=meshName)
    surf.addObject("MeshTopology", src="@MeshLoader")
    surf.addObject('MechanicalObject', name="CollisionObject", template="Vec3d", src="@MeshLoader")
    surf.addObject('TriangleCollisionModel', template="Vec3d")#name="CollisionModel", listRadius="@sphereLoader.listRadius")
    surf.addObject('LineCollisionModel')
    surf.addObject('PointCollisionModel')
    surf.addObject('BarycentricMapping', name="CollisionMapping") #, input="@../dofs", output="@spheres")



#====== Needle =====================

    meshFile = "./Data/syrette2.obj"
    scale=10
        
    needleNode = root.addChild("Needle")

    needleNode.addObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="1.0")
    needleNode.addObject('CGLinearSolver', name="linear solver", iterations="25", tolerance="1e-10", threshold="10e-10")
    needleNode.addObject('MechanicalObject', name="mechObject", template="Rigid3d",  dx = 20, dy = 130, dz = 20, rx = 0, ry = 0, rz = -90.0,  scale3d=[scale, scale, scale])
    needleNode.addObject('UniformMass', name="mass", totalMass="5")
    needleNode.addObject('UncoupledConstraintCorrection')
   # Visual node
    needleVisNode = needleNode.addChild("VisualModel")
    needleVisNode.addObject('MeshObjLoader', name='instrumentMeshLoader', filename=meshFile)
    needleVisNode.addObject('OglModel', name="InstrumentVisualModel", src='@instrumentMeshLoader', dy = -2*scale,  scale3d=[scale, scale, scale])
 
    needleVisNode.addObject('RigidMapping', name="MM-VM mapping", input="@../mechObject", output="@InstrumentVisualModel")
    # Collision node
    needleColNode = needleNode.addChild("CollisionModel")
    needleColNode.addObject('MeshObjLoader', filename=meshFile, name="loader")
    needleColNode.addObject('MeshTopology', src="@loader", name="InstrumentCollisionModel")
    needleColNode.addObject('MechanicalObject', src="@InstrumentCollisionModel", name="instrumentCollisionState", dy = -2*scale, scale3d=[scale, scale, scale])
    needleColNode.addObject('TriangleCollisionModel', name="instrumentTrinagle", contactStiffness="5000", contactFriction="0.0")
    needleColNode.addObject('LineCollisionModel', name="instrumentLine", contactStiffness="5000", contactFriction="0.0")
    needleColNode.addObject('PointCollisionModel', name="instrumentPoint",
    contactStiffness="5000", contactFriction="0.0")
    needleColNode.addObject('RigidMapping', name="MM-CM mapping", input="@../mechObject", output="@instrumentCollisionState")
        
    # add needle movement
    needleNode.addObject('LinearMovementConstraint', template="Rigid3d",
                             indices = 0,
                             keyTimes=[0, 1.8, 2.6, 3.7],
                             movements= [[0, 0, 0, 0, 0, 0],
                                         [0, -8, 0, 0, 0, 0],
                                         [0, -25, 0, 0, 0, 0],
                                         [0, -35, 0, 0, 0, 0]])



    # Instantiate floor
    totalMass = 1.0
    volume = 1.0
    inertiaMatrix=[1., 0., 0., 0., 1., 0., 0., 0., 1.]
    floor = root.addChild("floor")
    floor.addObject('MechanicalObject', name="mstate", template="Rigid3", translation2=[0.0,-20.0,0.0], rotation2=[0., 0., 0.], showObjectScale=5.0)
    floor.addObject('UniformMass', name="mass", vertexMass=[totalMass, volume, inertiaMatrix[:]])
    floorCollis = floor.addChild('collision')
    floorCollis.addObject('MeshObjLoader', name="loader", filename="mesh/floor.obj", triangulate="true", scale=5.0)
    floorCollis.addObject('MeshTopology', src="@loader")
    floorCollis.addObject('MechanicalObject')
    floorCollis.addObject('TriangleCollisionModel', moving=False, simulated=False)
    floorCollis.addObject('LineCollisionModel', moving=False, simulated=False)
    floorCollis.addObject('PointCollisionModel', moving=False, simulated=False)

    floorCollis.addObject('RigidMapping')

    #### visualization
    floorVisu = floor.addChild("VisualModel")
    floorVisu.loader = floorVisu.addObject('MeshObjLoader', name="loader", filename="mesh/floor.obj")
    floorVisu.addObject('OglModel', name="model", src="@loader", scale3d=[5.0]*3, color=[1., 1., 0.], updateNormals=False)
    floorVisu.addObject('RigidMapping')
    

    return root
    
    
    

if __name__ == '__main__':
    main()
