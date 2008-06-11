1. PlainTopology:
Draw a topology from a series of commands.
	1.1. Console2Topology.py
	The commands are input from python console.
	*Usage: Console2Topology.py
	or python Console2Topology.py
	1.2. File2Topology.py
	The commands are input from a file.
	*Usage: File2Topology.py yourFile
	or python File2Topology.py yourFile
	1.3. AnyInput2Topology.py
	The commands are input either from python console or from a file.
	*Usage: AnyInput2Topology.py or AnyInput2Topology.py yourFile
	or python AnyInput2Topology.py or python AnyInput2Topology.py yourFile
	
2. RelationTopology
Draw a topology from relations.
	2.1. RelationTopologyViewer.py
	It can show entities and their relations.
		** Usage: RelationTopologyViewer.py yourFile
		or python RelationTopologyViewer.py yourFile
		** Example file: Files/Relation.re
	1.2. RelationColorTopologyViewer.py
	It can also represent male as blue color and female as pink color besides 
	the function of RelationTopologyViewer.py.
		** Usage: RelationColorTopologyViewer.py yourFile
		or python RelationColorTopologyViewer.py yourFile
		** Example file: Files/RelationGender.re
	1.3. RelationAttributeTopologyViewer.py
	1.) It can choose different shapes, colors, pictures, sizes, labels for entities.
	2.) It has link label to show relations and has the link arrow to show the direction of relation. 
	3.) The shapes, colors, pictures, sizes and labels of entities are updatable.
	3.) It can receive inputs from python console or from a file or from both.
		** Usage: RelationAttributeTopologyViewer.py or RelationAttributeTopologyViewer.py yourFile
		or python RelationAttributeTopologyViewer.py or python RelationAttributeTopologyViewer.py yourFile
		** Example file: Files/RelationAttribute.re
