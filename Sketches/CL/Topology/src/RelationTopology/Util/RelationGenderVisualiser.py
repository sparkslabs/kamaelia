from RelationParticles import BlueParticle
from Kamaelia.Visualisation.PhysicsGraph.RenderingParticle import RenderingParticle
from Kamaelia.Visualisation.PhysicsGraph.TopologyViewer import TopologyViewer

def RelationGenderVisualiser( **dictArgs):
    """\
Create a customised TopologyViewer, different genders with different colors 
    """

    args = dict(dictArgs)
    particleTypes = { "Male"      : BlueParticle,
                      "Female"    : RenderingParticle,
                    }

    args["particleTypes"] = particleTypes
    args.pop("laws", None)
    return TopologyViewer( **args
                          )