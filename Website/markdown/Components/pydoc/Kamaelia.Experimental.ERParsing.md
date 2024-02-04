---
pagename: Components/pydoc/Kamaelia.Experimental.ERParsing
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[ERParsing](/Components/pydoc/Kamaelia.Experimental.ERParsing.html){.reference}
================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ERModel2Visualiser](/Components/pydoc/Kamaelia.Experimental.ERParsing.ERModel2Visualiser.html){.reference}**
-   **component
    [ERParser](/Components/pydoc/Kamaelia.Experimental.ERParsing.ERParser.html){.reference}**
:::

-   [Parser components for Entity-Relationship data](#566){.reference}
    -   [Example Usage:](#567){.reference}
    -   [ERParser Behaviour](#568){.reference}
    -   [ERModel2Visualiser Behaviour](#569){.reference}
    -   [Entity-Relationship textual description
        format](#570){.reference}
    -   [Parsed Entity-Relationship data](#571){.reference}
:::

::: {.section}
Parser components for Entity-Relationship data {#566}
==============================================

ERParser parses and buffers lines of text containing entity-relationship
data. Once a shutdown message is received, it emits the parsed data as a
list of entities and relationships.

ERModel2Visualiser transforms parsed entity-relationship data into
textual commands for the TopologyViewer component to produce a
visualisation. The TopologyViewer must be configured with suitable
particle types - such as
[Kamaelia.Visualisation.ER.ERVisualiserServer.ERVisualiser](/Components/pydoc/Kamaelia.Visualisation.ER.ERVisualiserServer.ERVisualiser.html){.reference}

See:
[Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer.html){.reference}

::: {.section}
[Example Usage:]{#example-usage} {#567}
--------------------------------

A simple pipeline that reads in entity-relationship data from a file and
writes out commands, suitable for a topology visualiser, to the console:

``` {.literal-block}
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Console import ConsoleEchoer

Pipeline(
    ReadFileAdaptor(entity_relationship_data_file),
    ERParser(),
    ERModel2Visualiser(),
    PureTransformer(lambda x: pprint.pformat(x)+"\n"),
    ConsoleEchoer(),
).run()
```

Provide the following file of entity relationship data:

``` {.literal-block}
#
# entity relationship data in this file!
#

entity Artist:
    simpleattributes artisticname genre

entity Manager:
    simpleattributes ID name1 telephone

entity ContractInfo:
    simpleattributes contractID data_from data_to duration1

entity MasterTrack:
    simpleattributes trackID working_title duration2

entity SoundEngineer:
    simpleattributes sound_eng_ID name2

entity FinishedTrack:
    simpleattributes version final_duration released_title

entity Album:
    simpleattributes album_ID title

relation ManagedBy(Artist,Manager)
relation HasContract(Artist,ContractInfo)
relation RecordedBy(MasterTrack,Artist)
relation EditedBy(SoundEngineer,MasterTrack)
relation OriginatesFrom(FinishedTrack,MasterTrack)
relation GroupedOn(FinishedTrack,Album)
relation CreatedBy(Album,Artist)
```

Once the ReadFileAdaptor component has finished reading and terminates,
the ERParser component sends a message, containing the following, out of
its \"outbox\" outbox:

``` {.literal-block}
[['entity', {'name': 'Artist', 'simpleattributes': ['artisticname', 'genre']}],
 ['entity',
  {'name': 'Manager', 'simpleattributes': ['ID', 'name1', 'telephone']}],
 ['entity',
  {'name': 'ContractInfo',
   'simpleattributes': ['contractID', 'data_from', 'data_to', 'duration1']}],
 ['entity',
  {'name': 'MasterTrack',
   'simpleattributes': ['trackID', 'working_title', 'duration2']}],
 ['entity',
  {'name': 'SoundEngineer', 'simpleattributes': ['sound_eng_ID', 'name2']}],
 ['entity',
  {'name': 'FinishedTrack',
   'simpleattributes': ['version', 'final_duration', 'released_title']}],
 ['entity', {'name': 'Album', 'simpleattributes': ['album_ID', 'title']}],
 ['relation', {'entities': ['Artist', 'Manager'], 'name': 'ManagedBy'}],
 ['relation', {'entities': ['Artist', 'ContractInfo'], 'name': 'HasContract'}],
 ['relation', {'entities': ['MasterTrack', 'Artist'], 'name': 'RecordedBy'}],
 ['relation',
  {'entities': ['SoundEngineer', 'MasterTrack'], 'name': 'EditedBy'}],
 ['relation',
  {'entities': ['FinishedTrack', 'MasterTrack'], 'name': 'OriginatesFrom'}],
 ['relation', {'entities': ['FinishedTrack', 'Album'], 'name': 'GroupedOn'}],
 ['relation', {'entities': ['Album', 'Artist'], 'name': 'CreatedBy'}]]
```

And the following is output from the console:

``` {.literal-block}
'ADD NODE Artist Artist auto entity'
'ADD NODE artisticname artisticname auto attribute'
'ADD NODE genre genre auto attribute'
'ADD NODE Manager Manager auto entity'
'ADD NODE ID ID auto attribute'
'ADD NODE name1 name1 auto attribute'
'ADD NODE telephone telephone auto attribute'
'ADD NODE ContractInfo ContractInfo auto entity'
'ADD NODE contractID contractID auto attribute'
'ADD NODE data_from data_from auto attribute'
'ADD NODE data_to data_to auto attribute'
'ADD NODE duration1 duration1 auto attribute'
'ADD NODE MasterTrack MasterTrack auto entity'
'ADD NODE trackID trackID auto attribute'
'ADD NODE working_title working_title auto attribute'
'ADD NODE duration2 duration2 auto attribute'
'ADD NODE SoundEngineer SoundEngineer auto entity'
'ADD NODE sound_eng_ID sound_eng_ID auto attribute'
'ADD NODE name2 name2 auto attribute'
'ADD NODE FinishedTrack FinishedTrack auto entity'
'ADD NODE version version auto attribute'
'ADD NODE final_duration final_duration auto attribute'
'ADD NODE released_title released_title auto attribute'
'ADD NODE Album Album auto entity'
'ADD NODE album_ID album_ID auto attribute'
'ADD NODE title title auto attribute'
'ADD NODE ManagedBy ManagedBy auto relation'
'ADD NODE HasContract HasContract auto relation'
'ADD NODE RecordedBy RecordedBy auto relation'
'ADD NODE EditedBy EditedBy auto relation'
'ADD NODE OriginatesFrom OriginatesFrom auto relation'
'ADD NODE GroupedOn GroupedOn auto relation'
'ADD NODE CreatedBy CreatedBy auto relation'
'ADD LINK Artist artisticname'
'ADD LINK Artist genre'
'ADD LINK Manager ID'
'ADD LINK Manager name1'
'ADD LINK Manager telephone'
'ADD LINK ContractInfo contractID'
'ADD LINK ContractInfo data_from'
'ADD LINK ContractInfo data_to'
'ADD LINK ContractInfo duration1'
'ADD LINK MasterTrack trackID'
'ADD LINK MasterTrack working_title'
'ADD LINK MasterTrack duration2'
'ADD LINK SoundEngineer sound_eng_ID'
'ADD LINK SoundEngineer name2'
'ADD LINK FinishedTrack version'
'ADD LINK FinishedTrack final_duration'
'ADD LINK FinishedTrack released_title'
'ADD LINK Album album_ID'
'ADD LINK Album title'
'ADD LINK Artist ManagedBy'
'ADD LINK Manager ManagedBy'
'ADD LINK Artist HasContract'
'ADD LINK ContractInfo HasContract'
'ADD LINK MasterTrack RecordedBy'
'ADD LINK Artist RecordedBy'
'ADD LINK SoundEngineer EditedBy'
'ADD LINK MasterTrack EditedBy'
'ADD LINK FinishedTrack OriginatesFrom'
'ADD LINK MasterTrack OriginatesFrom'
'ADD LINK FinishedTrack GroupedOn'
'ADD LINK Album GroupedOn'
'ADD LINK Album CreatedBy'
'ADD LINK Artist CreatedBy'
```
:::

::: {.section}
[ERParser Behaviour]{#erparser-behaviour} {#568}
-----------------------------------------

Send entity-relationship textual description data to the \"inbox\" inbox
as individual strings, one line per string.

When a producerFinished or shutdownMicroprocess is sent to the
\"control\" inbox this component sends out a single message containing,
as a list, the entities and relationships parsed from the data.

ERParser then immediately terminates and sends out the shudown message
it received out of its \"signal\" outbox.

See description of \"Entity-Relationship textual description format\"
and \"Parsed Entity-Relationship data\".
:::

::: {.section}
[ERModel2Visualiser Behaviour]{#ermodel2visualiser-behaviour} {#569}
-------------------------------------------------------------

Send parsed entity-relationship data to the \"inbox\" inbox.

When a producerFinished or shutdownMicroprocess is sent to the
\"control\" inbox this component transforms it into a set of textual
(string) commands suitable for a TopologyViewer component and sends it
out of its \"outbox\" outbox in two messages. The first contains the
commands to create the required nodes and the second contains the
commands to create the linkages between them.

ERModel2Visualiser then immediately terminates and sends out the shudown
message it received out of its \"signal\" outbox.

The TopologyViewer component that receives the commands must be
configured to know the following node types:

-   entity \-- represents an entity
-   relation \-- represents the mid-point and name label of a relation
-   attribute \-- represents an attribute of an entity
-   isa \-- represents the mid-point and label of a subtype-supertype
    relation

See description of \"Parsed Entity-Relationship data\".
:::

::: {.section}
[Entity-Relationship textual description format]{#entity-relationship-textual-description-format} {#570}
-------------------------------------------------------------------------------------------------

Entity relationship data is expressed as a text file. Blank lines or
lines beginning with a \'\#\' character are ignored.

Define entities by writing entity NAME: on its own line, without
indentation. To define attributes for an entity, write, indented, on the
next line, simpleattributes followed by a space separated list of
attributes.

To make an entity a subtype of another entity, begin the entity
declaration instead with entity NAME(SUPERTYPE):.

Example entities:

``` {.literal-block}
entity person:
    simpleattributes female name=sarah

# the following entities are subtypes of the 'person' entity

entity mum(person):

entity daughter(person):

entity son(person):
```

To define relations, write relation RELATION\_NAME(ENTITY,ENTITY,\...)
on its own line without indentation. A relation must involve two or more
entities. For example:

``` {.literal-block}
relation RelatedTo(mum,daughter,son)
relation siblings(son,daughter)
```
:::

::: {.section}
[Parsed Entity-Relationship data]{#parsed-entity-relationship-data} {#571}
-------------------------------------------------------------------

The parsed data takes the form of a list of entities and relations.

An entity is represented as a list beginning with the string \"entity\",
followed by a dictionary defining attributes. The key \"name\" maps to
the name of the entity:

> \[ \"entity\", { \"name\": \<name\>, \"simpleattributes\": \[
> \<attribute\>, \<attribute\>, \... \], \"subtype\": \<supertype-name\>
> \]

The key \"simpleattributes\", if present, maps to a list containing, as
strings each attribute.

Some may also contain a \"subtype\" key which maps to the name of the
entity that this one is a subtype of.

For example:

``` {.literal-block}
[ "entity",
  { "name"             : "person",
    "simpleattributes" : [ "female", "name=sarah" ]
  }
]

[ "entity",
  { "name" : "mum",
    "subtype" : "person"
  }
]
```

A relation is represented as a list beginning with the string
\"relation\", followed by a dictionary defining attributes:

> \[ \"relation\", { \"name\": \<name\>, \"entities\": \[
> \<entity-name\>, \<entity-name\>, \... \]

The key \"name\" maps to the name of the entity. The key \"entities\"
maps to a list containing, as strings, the names of the entities
involved in the relation. For example:

``` {.literal-block}
[ "relation",
  { "name"     : "IsA",
    "entities" : [ "mum", "person" ]
  }
]
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[ERParsing](/Components/pydoc/Kamaelia.Experimental.ERParsing.html){.reference}.[ERModel2Visualiser](/Components/pydoc/Kamaelia.Experimental.ERParsing.ERModel2Visualiser.html){.reference}
============================================================================================================================================================================================================================================================================================================================

::: {.section}
class ERModel2Visualiser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ERModel2Visualiser}
----------------------------------------------------------------------------------------------------------

ERModel2Visualiser() -\> new ERModel2Visualiser component.

Send parsed entity-relationship data as lists of entities and relations
to the \"inbox\" inbox. Once shutdown, sends out commands to drive a
TopologyViewer component to produce a visualisation of the described
entities and relations.

::: {.section}
### [Inboxes]{#symbol-ERModel2Visualiser.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-ERModel2Visualiser.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [main(self)]{#symbol-ERModel2Visualiser.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ERModel2Visualiser.shutdown}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[ERParsing](/Components/pydoc/Kamaelia.Experimental.ERParsing.html){.reference}.[ERParser](/Components/pydoc/Kamaelia.Experimental.ERParsing.ERParser.html){.reference}
========================================================================================================================================================================================================================================================================================================

::: {.section}
class ERParser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ERParser}
------------------------------------------------------------------------------------------------

ERParser() -\> new ERParser component.

Parses lines of Entity-Relationship data, send to the \"inbox\" inbox as
strings. Once shutdown, sends out a list of parsed entity and
relationship data.

::: {.section}
### [Inboxes]{#symbol-ERParser.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-ERParser.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [main(self)]{#symbol-ERParser.main}
:::

::: {.section}
#### [shutdown(self)]{#symbol-ERParser.shutdown}
:::
:::

::: {.section}
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
