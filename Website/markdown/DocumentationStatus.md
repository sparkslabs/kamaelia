---
pagename: DocumentationStatus
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Documentation Notes]{style="font-size:24pt;font-weight:600"}

[A check list]{style="font-size:18pt"}

The purpose of this page is to act as an index (think index of a book)
to the documentation that\'s been written. It also allows us to see what
documentation still needs writing. This is \*ALOT\* of documentation.
I\'ll produce a template for component/module documentation shortly.

In the spirit of [NaNoWriMo](http://www.nanowrimo.org/), we\'re spending
November getting the documentation up to date for the RELEASE trees.

[Axon/]{style="font-size:18pt;font-weight:600"}

sss

[Axon/Axon]{style="font-size:16pt"}

\_\_init\_\_.py \-- UNCHECKED \--

AdaptiveCommsComponent.py \-- UNCHECKED \--

-   AdaptiveCommsComponent

AxonExceptions.py \-- UNCHECKED \--

-   AxonException
-   normalShutdown
-   invalidComponentInterface
-   noSpaceInBox
-   BadParentTracker
-   ServiceAlreadyExists
-   BadComponent
-   BadInbox
-   MultipleServiceDeletion
-   NamespaceClash
-   AccessToUndeclaredTrackedVariable
-   ArgumentsClash

Axon.py \-- UNCHECKED \--

-   AxonObject

Component.py \-- UNCHECKED \--

-   component

CoordinatingAssistantTracker.py \-- UNCHECKED \--

-   coordinatingassistanttracker

debugConfigDefaults.py \-- UNCHECKED \--

debugConfigFile.py \-- UNCHECKED \--

debug.py \-- UNCHECKED \--

-   debug

idGen.py \-- UNCHECKED \--

-   idGen

Ipc.py \-- UNCHECKED \--

-   ipc
-   WaitComplete
-   reactivate
-   newComponent
-   shutdownMicroprocess
-   notify
-   status
-   wouldblock
-   producerFinished
-   errorInformation

Linkage.py \-- UNCHECKED \--

-   linkage

Microprocess.py \-- UNCHECKED \--

-   microprocess

Postman.py \-- UNCHECKED \--

-   postman

Scheduler.py \-- UNCHECKED \--

-   scheduler

ThreadedComponent.py \-- UNCHECKED \--

-   threadedcomponent

util.py \-- UNCHECKED \--

-   Finality

[Axon/Axon/test]{style="font-size:15pt"}

AxonTest.py \-- UNCHECKED \--

-   VerboseTestResults
-   suite
-   FixedTestProgram
-   AddNameToVerboseTextString

TemplateTestModule.py \-- UNCHECKED \--

-   classWeAreTesting\_Test

test\_AdaptiveCommsComponent.py \-- UNCHECKED \--

-   AdaptiveCommsComponent\_Test

test\_Axon.py \-- UNCHECKED \--

-   Axon\_Test

test\_Component.py \-- UNCHECKED \--

-   TComponent
-   TComponentAsync
-   TestMainLoopComponent
-   closeDownCompTestException
-   TestMainLoopComponentClosedown
-   dummylinkage
-   testpostman
-   testpostman2
-   Component\_Test

test\_CoordinatingAssistantTracker.py \-- UNCHECKED \--

-   dummyComponent
-   CoordinatingAssistantTracker\_Test

test\_debugConfigFile.py \-- UNCHECKED \--

-   classWeAreTesting\_Test

test\_debug.py \-- UNCHECKED \--

-   classWeAreTesting\_Test

test\_idGen.py \-- UNCHECKED \--

-   classWeAreTesting\_Test

test\_Ipc.py \-- UNCHECKED \--

-   ipc\_Test
-   newComponent\_Test
-   shutdownMicroprocess\_Test
-   notify\_Test
-   status\_Test
-   wouldblock\_Test
-   producerFinished\_Test
-   errorInformation\_Test

test\_Linkage.py \-- UNCHECKED \--

-   DummyPostman
-   TestComponent
-   linkage\_Test

test\_Microprocess.py \-- UNCHECKED \--

-   MicroProcess\_Test

test\_Postman.py \-- UNCHECKED \--

-   named
-   AdvancedMockLinkage
-   AdvancedMockLinkage2
-   postman\_Test

test\_Scheduler.py \-- UNCHECKED \--

-   scheduler\_Test

test\_\_\_str\_\_.py \-- UNCHECKED \--

-   str\_Test

test\_util.py \-- UNCHECKED \--

-   util\_Test

[Kamaelia/]{style="font-size:18pt;font-weight:600"}

afortune.pl

\_\_init\_\_.py

KamaeliaExceptions.py

-   socketSendFailure
-   connectionClosedown
-   connectionDied
-   connectionDiedSending
-   connectionDiedReceiving
-   connectionServerShutdown
-   BadRequest

KamaeliaIPC.py

-   socketShutdown
-   newCSA
-   shutdownCSA
-   newServer

MimeRequestComponent.py

-   MimeRequestComponent

ReadFileAdaptor.py

-   ReadFileAdaptor

SampleTemplateComponent.py

-   myComponent

SimpleServerComponent.py

SingleServer.py

vorbisDecodeComponent.py

[Kamaelia/Tools]{style="font-size:15pt"}

-   axonshell.py \-- UNCHECKED \--
-   AxonVisualiser.py \-- UNCHECKED \--
-   VisualPipeBuilder.py \-- UNCHECKED \--

[Kamaelia/Tools/PipeBuilder]{style="font-size:15pt"}

BuildViewer.py

-   ComponentParticle

GUI.py

-   ArgumentsPanel
-   BuilderControlsGUI
-   TextOutputGUI

PipeBuild.py

-   PipeBuild

PipelineWriter.py

-   PipelineWriter

[Kamaelia/Kamaelia/Data]{style="font-size:15pt"}

-   README
-   \_\_init\_\_.py
-   Escape.py
-   MimeDict.py
-   MimeObject.py
-   Rationals.py
-   requestLine.py

[Kamaelia/Kamaelia/Data/Tests]{style="font-size:15pt"}

-   test\_Escape.py
-   test\_MimeDict.py
-   test\_Rationals.py

[Kamaelia/Kamaelia/Chassis]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   Prefab.py
-   ConnectedServer.py
-   Carousel.py

[Kamaelia/Kamaelia/Chassis/test]{style="font-size:15pt"}

-   test\_Carousel.py

[Kamaelia/Kamaelia/Codec]{style="font-size:15pt"}

-   Dirac.py
-   \_\_init\_\_.py
-   RawYUVFramer.py

[Kamaelia/Kamaelia/File]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   Reading.py
-   Writing.py

[Kamaelia/Kamaelia/Internet]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   ConnectedSocketAdapter.py
-   Multicast\_receiver.py
-   Multicast\_sender.py
-   Multicast\_transceiver.py
-   Selector.py
-   TCPClient.py
-   TCPServer.py
-   ThreadedTCPClient.py

[Kamaelia/Kamaelia/Internet/test]{style="font-size:15pt"}

-   test\_BasicMulticastSystem.py
-   test\_MulticastTransceiverSystem.py
-   test\_TCPServerClientSystem.py

[Kamaelia/Kamaelia/Internet/Simulate]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   BrokenNetwork.py

[Kamaelia/Kamaelia/Physics]{style="font-size:15pt"}

-   Behaviours.py
-   \_\_init\_\_.py

[Kamaelia/Kamaelia/Physics/Simple]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   MultipleLaws.py
-   Particle.py
-   ParticleSystem.py
-   SimpleLaws.py
-   SpatialIndexer.py

[Kamaelia/Kamaelia/Protocol]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   SpatialIndexer.py

[Kamaelia/Kamaelia/Sketch]{style="font-size:15pt"}

Empty on release tree, candidate for deletion in practice

[Kamaelia/Kamaelia/Support]{style="font-size:15pt"}

Candidate for being moved to somewhere else

[Kamaelia/Kamaelia/test]{style="font-size:15pt"}

Needs a revamp (BADLY - probably also moving out of this directory -
probably up )

-   README
-   debug.conf
-   SynchronousLinks\_SystemTest.py
-   test\_ConsoleEcho.py
-   test\_MimeRequestComponent.py
-   test\_Selector.py

[Kamaelia/Kamaelia/UI]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   PygameDisplay.py

[Kamaelia/Kamaelia/UI/Pygame]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   BasicSprite.py
-   Button.py
-   EventHandler.py
-   Image.py
-   KeyEvent.py
-   Multiclick.py
-   SpriteScheduler.py
-   Ticker.py
-   VideoOverlay.py

[Kamaelia/Kamaelia/UI/Tk]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   TkWindow.py

[Kamaelia/Kamaelia/UI/MH]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   DragHandler.py
-   PyGameApp.py

[Kamaelia/Kamaelia/Util]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   Chargen.py
-   Chooser.py
-   Comparator.py
-   ConsoleEcho.py
-   Fanout.py
-   FilterComponent.py
-   Graphline.py
-   Introspector.py
-   LossyConnector.py
-   MarshallComponent.py
-   Marshalling.py
-   NullSinkComponent.py
-   passThrough.py
-   PipelineComponent.py
-   RateFilter.py
-   Splitter.py
-   TestResultComponent.py
-   ToStringComponent.py

[Kamaelia/Kamaelia/Util/test]{style="font-size:15pt"}

-   test\_Chooser.py
-   test\_Comparator.py
-   test\_ForwardIteratingChooser.py
-   test\_LossyConnector.py
-   test\_Marshalling.py
-   test\_RateControl.py
-   test\_Splitter.py
-   test\_TestResultComponent.py
-   test\_VariableRateControl.py

[Kamaelia/Kamaelia/Visualisation]{style="font-size:15pt"}

-   \_\_init\_\_.py

[Kamaelia/Kamaelia/Visualisation/Axon]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   AxonLaws.py
-   AxonVisualiserServer.py
-   ExtraWindowFurniture.py
-   PComponent.py
-   PPostbox.py

[Kamaelia/Kamaelia/Visualisation/PhysicsGraph]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   chunks\_to\_lines.py
-   GridRenderer.py
-   lines\_to\_tokenlists.py
-   ParticleDragger.py
-   RenderingParticle.py
-   TopologyViewerComponent.py
-   TopologyViewerServer.py

[Kamaelia/Examples]{style="font-size:15pt"}

\...

[Kamaelia/Examples/example1]{style="font-size:15pt"}

-   README
-   FortuneCookie\_ServerClient.py

[Kamaelia/Examples/example2]{style="font-size:15pt"}

-   README
-   SimpleStreamingSystem.py

[Kamaelia/Examples/example3]{style="font-size:15pt"}

-   README
-   SimpleStreamer.py
-   SimpleStreamingClient.py

[Kamaelia/Examples/example4]{style="font-size:15pt"}

-   README
-   MulticastStreamingClient.py
-   MulticastStreamingServer.py
-   MulticastStreamingSystem.py
-   MulticastStreamingSystem\_SRM.py

[Kamaelia/Examples/example5]{style="font-size:15pt"}

-   README
-   IntrospectingSimpleStreamingSystem.py

[Kamaelia/Examples/example6]{style="font-size:15pt"}

-   TopologyVisualiser.py

[Kamaelia/Examples/example7]{style="font-size:15pt"}

-   BasicGraphVisualisation.py

[Kamaelia/Examples/example7/BasicGraphVisualisation]{style="font-size:15pt"}

-   \_\_init\_\_.py
-   ParticleDragger.py
-   PhysApp1.py
-   VisibleParticle.py

[Kamaelia/Examples/example8]{style="font-size:15pt"}

README

Slides/

-   Collection of 6 pictures 800x600

slideshow.py

topology.py

topology\_slideshow.py

[Kamaelia/Examples/example9]{style="font-size:15pt"}

pictures/

-   Collection of small pictures

banner.gif

cat.gif

Simplegame.py

hold.wav

KDE\_Beep\_Bottles.wav

[Kamaelia/Examples/example10]{style="font-size:15pt"}

-   snowboard-jum-352x288x75.dirac.drc
-   SimpleDiracEncodeDecode.py
-   SimpleDiracPlayer.py

[Kamaelia/Examples/example11]{style="font-size:15pt"}

-   Ulysses
-   Ticker.py

[Kamaelia/Examples/example12]{style="font-size:15pt"}

-   SimpleMultiFileStreamer.py
-   ClientStreamToFile.py
