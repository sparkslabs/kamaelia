---
pagename: Components
last-modified-date: 2009-01-06
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Components]{style="font-size: 24pt; font-weight: 600;"}

[Parts: See a need, fill a need]{style="font-size: 18pt;"}

This section is a reference to all the Kamaelia components currently in
the repositor. Whilst it is largely a component reference, it also
contains the documentation from other files in Kamaelia.\* . In
Kamaelia.Support this is primarily supporting code rather than
components, where as Kamaelia.Apps contains application specific docs
from (mainly) components used in Kamaelia Applications. This page is
generated largely automatically (manually initiated process) from the
source files, and the documentation linked to from here is also
generated automatically from the source files

::: {.container}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}
===================================

All of these components are implemented using Axon - Kamaelia\'s core.
You probably want to have a look over at the [Axon
documentation](/Docs/Axon/Axon.html) if you\'re writing new components.
:::

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference} Components
==================================================================

Application specific components are now at the end of the file, preceded
by support code.
:::

::: {.section}
::: {.container}
:::

-   **[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}**
    -   **[Codec](/Components/pydoc/Kamaelia.Audio.Codec.html){.reference}**
        -   **[PyMedia](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.html){.reference}**
            -   **[Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.html){.reference}**
                (
                [Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.Decoder.html){.reference}
                )
            -   **[Encoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Encoder.html){.reference}**
                (
                [Encoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Encoder.Encoder.html){.reference}
                )
    -   **[Filtering](/Components/pydoc/Kamaelia.Audio.Filtering.html){.reference}**
        (
        [LPF](/Components/pydoc/Kamaelia.Audio.Filtering.LPF.html){.reference}
        )
    -   **[Input](/Components/pydoc/Kamaelia.Audio.Input.html){.reference}**
    -   **[Output](/Components/pydoc/Kamaelia.Audio.Output.html){.reference}**
    -   **[PyMedia](/Components/pydoc/Kamaelia.Audio.PyMedia.html){.reference}**
        -   **[Input](/Components/pydoc/Kamaelia.Audio.PyMedia.Input.html){.reference}**
            (
            [Input](/Components/pydoc/Kamaelia.Audio.PyMedia.Input.Input.html){.reference}
            )
        -   **[Output](/Components/pydoc/Kamaelia.Audio.PyMedia.Output.html){.reference}**
            (
            [Output](/Components/pydoc/Kamaelia.Audio.PyMedia.Output.Output.html){.reference}
            )
        -   **[Resample](/Components/pydoc/Kamaelia.Audio.PyMedia.Resample.html){.reference}**
            (
            [Resample](/Components/pydoc/Kamaelia.Audio.PyMedia.Resample.Resample.html){.reference}
            )
    -   **[RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.html){.reference}**
        (
        [RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.RawAudioMixer.html){.reference}
        )
-   **[Automata](/Components/pydoc/Kamaelia.Automata.html){.reference}**
    -   **[Behaviours](/Components/pydoc/Kamaelia.Automata.Behaviours.html){.reference}**
        (
        [bouncingFloat](/Components/pydoc/Kamaelia.Automata.Behaviours.bouncingFloat.html){.reference},
        [cartesianPingPong](/Components/pydoc/Kamaelia.Automata.Behaviours.cartesianPingPong.html){.reference},
        [continuousIdentity](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousIdentity.html){.reference},
        [continuousOne](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousOne.html){.reference},
        [continuousZero](/Components/pydoc/Kamaelia.Automata.Behaviours.continuousZero.html){.reference},
        [loopingCounter](/Components/pydoc/Kamaelia.Automata.Behaviours.loopingCounter.html){.reference}
        )
-   **[BaseIPC](/Components/pydoc/Kamaelia.BaseIPC.html){.reference}**
-   **[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}**
    -   **[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}**
        (
        [Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.Carousel.html){.reference}
        )
    -   **[ConnectedServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.html){.reference}**
        (
        [ServerCore](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.ServerCore.html){.reference},
        [SimpleServer](/Components/pydoc/Kamaelia.Chassis.ConnectedServer.SimpleServer.html){.reference}
        )
    -   **[Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.html){.reference}**
        (
        [Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.Graphline.html){.reference}
        )
    -   **[Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.html){.reference}**
        (
        [Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.Pipeline.html){.reference}
        )
    -   **[Prefab](/Components/pydoc/Kamaelia.Chassis.Prefab.html){.reference}**
        (
        [JoinChooserToCarousel](/Components/pydoc/Kamaelia.Chassis.Prefab.JoinChooserToCarousel.html){.reference}
        )
    -   **[Seq](/Components/pydoc/Kamaelia.Chassis.Seq.html){.reference}**
        (
        [Seq](/Components/pydoc/Kamaelia.Chassis.Seq.Seq.html){.reference}
        )
-   **[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}**
    -   **[Dirac](/Components/pydoc/Kamaelia.Codec.Dirac.html){.reference}**
        (
        [DiracDecoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracDecoder.html){.reference},
        [DiracEncoder](/Components/pydoc/Kamaelia.Codec.Dirac.DiracEncoder.html){.reference}
        )
    -   **[RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.html){.reference}**
        (
        [RawYUVFramer](/Components/pydoc/Kamaelia.Codec.RawYUVFramer.RawYUVFramer.html){.reference}
        )
    -   **[Speex](/Components/pydoc/Kamaelia.Codec.Speex.html){.reference}**
        (
        [SpeexDecode](/Components/pydoc/Kamaelia.Codec.Speex.SpeexDecode.html){.reference},
        [SpeexEncode](/Components/pydoc/Kamaelia.Codec.Speex.SpeexEncode.html){.reference}
        )
    -   **[Vorbis](/Components/pydoc/Kamaelia.Codec.Vorbis.html){.reference}**
        (
        [AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.Codec.Vorbis.AOAudioPlaybackAdaptor.html){.reference},
        [VorbisDecode](/Components/pydoc/Kamaelia.Codec.Vorbis.VorbisDecode.html){.reference}
        )
    -   **[WAV](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}**
        (
        [WAVParser](/Components/pydoc/Kamaelia.Codec.WAV.WAVParser.html){.reference},
        [WAVWriter](/Components/pydoc/Kamaelia.Codec.WAV.WAVWriter.html){.reference}
        )
    -   **[YUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.html){.reference}**
        (
        [FrameToYUV4MPEG](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.FrameToYUV4MPEG.html){.reference},
        [YUV4MPEGToFrame](/Components/pydoc/Kamaelia.Codec.YUV4MPEG.YUV4MPEGToFrame.html){.reference}
        )
-   **[Community](/Components/pydoc/Kamaelia.Community.html){.reference}**
-   **[Device](/Components/pydoc/Kamaelia.Device.html){.reference}**
    -   **[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}**
        -   **[Core](/Components/pydoc/Kamaelia.Device.DVB.Core.html){.reference}**
            (
            [DVB\_Demuxer](/Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Demuxer.html){.reference},
            [DVB\_Multiplex](/Components/pydoc/Kamaelia.Device.DVB.Core.DVB_Multiplex.html){.reference}
            )
        -   **[DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.html){.reference}**
            (
            [DemuxerService](/Components/pydoc/Kamaelia.Device.DVB.DemuxerService.DemuxerService.html){.reference}
            )
        -   **[EIT](/Components/pydoc/Kamaelia.Device.DVB.EIT.html){.reference}**
            (
            [EITPacketParser](/Components/pydoc/Kamaelia.Device.DVB.EIT.EITPacketParser.html){.reference},
            [NowNextChanges](/Components/pydoc/Kamaelia.Device.DVB.EIT.NowNextChanges.html){.reference},
            [NowNextServiceFilter](/Components/pydoc/Kamaelia.Device.DVB.EIT.NowNextServiceFilter.html){.reference},
            [PSIPacketReconstructor](/Components/pydoc/Kamaelia.Device.DVB.EIT.PSIPacketReconstructor.html){.reference},
            [TimeAndDatePacketParser](/Components/pydoc/Kamaelia.Device.DVB.EIT.TimeAndDatePacketParser.html){.reference}
            )
        -   **[NowNext](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}**
            (
            [NowNextProgrammeJunctionDetect](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextProgrammeJunctionDetect.html){.reference},
            [NowNextServiceFilter](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextServiceFilter.html){.reference}
            )
        -   **[PSITables](/Components/pydoc/Kamaelia.Device.DVB.PSITables.html){.reference}**
            (
            [FilterOutNotCurrent](/Components/pydoc/Kamaelia.Device.DVB.PSITables.FilterOutNotCurrent.html){.reference}
            )
        -   **[Parse](/Components/pydoc/Kamaelia.Device.DVB.Parse.html){.reference}**
            -   **[ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.html){.reference}**
                (
                [ParseEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable.html){.reference},
                [ParseEventInformationTable\_Subset](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.ParseEventInformationTable_Subset.html){.reference},
                [SimplifyEIT](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseEventInformationTable.SimplifyEIT.html){.reference}
                )
            -   **[ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.html){.reference}**
                (
                [ParseNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable.html){.reference},
                [ParseNetworkInformationTable\_ActualAndOtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualAndOtherNetwork.html){.reference},
                [ParseNetworkInformationTable\_ActualNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_ActualNetwork.html){.reference},
                [ParseNetworkInformationTable\_OtherNetwork](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseNetworkInformationTable.ParseNetworkInformationTable_OtherNetwork.html){.reference}
                )
            -   **[ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.html){.reference}**
                (
                [ParseProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable.ParseProgramAssociationTable.html){.reference}
                )
            -   **[ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.html){.reference}**
                (
                [ParseProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseProgramMapTable.ParseProgramMapTable.html){.reference}
                )
            -   **[ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.html){.reference}**
                (
                [ParseServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable.html){.reference},
                [ParseServiceDescriptionTable\_ActualAndOtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualAndOtherTS.html){.reference},
                [ParseServiceDescriptionTable\_ActualTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_ActualTS.html){.reference},
                [ParseServiceDescriptionTable\_OtherTS](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.ParseServiceDescriptionTable_OtherTS.html){.reference},
                [SDT\_to\_SimpleServiceList](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable.SDT_to_SimpleServiceList.html){.reference}
                )
            -   **[ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.html){.reference}**
                (
                [ParseTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeAndDateTable.ParseTimeAndDateTable.html){.reference}
                )
            -   **[ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.html){.reference}**
                (
                [ParseTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.ParseTimeOffsetTable.ParseTimeOffsetTable.html){.reference}
                )
            -   **[PrettifyTables](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.html){.reference}**
                (
                [PrettifyEventInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyEventInformationTable.html){.reference},
                [PrettifyNetworkInformationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyNetworkInformationTable.html){.reference},
                [PrettifyProgramAssociationTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramAssociationTable.html){.reference},
                [PrettifyProgramMapTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyProgramMapTable.html){.reference},
                [PrettifyServiceDescriptionTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyServiceDescriptionTable.html){.reference},
                [PrettifyTimeAndDateTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeAndDateTable.html){.reference},
                [PrettifyTimeOffsetTable](/Components/pydoc/Kamaelia.Device.DVB.Parse.PrettifyTables.PrettifyTimeOffsetTable.html){.reference}
                )
            -   **[ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.html){.reference}**
                (
                [ReassemblePSITables](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITables.html){.reference},
                [ReassemblePSITablesService](/Components/pydoc/Kamaelia.Device.DVB.Parse.ReassemblePSITables.ReassemblePSITablesService.html){.reference}
                )
        -   **[Receiver](/Components/pydoc/Kamaelia.Device.DVB.Receiver.html){.reference}**
            (
            [Receiver](/Components/pydoc/Kamaelia.Device.DVB.Receiver.Receiver.html){.reference}
            )
        -   **[SoftDemux](/Components/pydoc/Kamaelia.Device.DVB.SoftDemux.html){.reference}**
            (
            [DVB\_SoftDemuxer](/Components/pydoc/Kamaelia.Device.DVB.SoftDemux.DVB_SoftDemuxer.html){.reference}
            )
        -   **[Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.html){.reference}**
            (
            [Tuner](/Components/pydoc/Kamaelia.Device.DVB.Tuner.Tuner.html){.reference}
            )
-   **[Exceptions](/Components/pydoc/Kamaelia.Exceptions.html){.reference}**
-   **[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}**
    -   **[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}**
        (
        [Carousel](/Components/pydoc/Kamaelia.Experimental.Chassis.Carousel.html){.reference},
        [Graphline](/Components/pydoc/Kamaelia.Experimental.Chassis.Graphline.html){.reference},
        [InboxControlledCarousel](/Components/pydoc/Kamaelia.Experimental.Chassis.InboxControlledCarousel.html){.reference},
        [Pipeline](/Components/pydoc/Kamaelia.Experimental.Chassis.Pipeline.html){.reference}
        )
    -   **[ERParsing](/Components/pydoc/Kamaelia.Experimental.ERParsing.html){.reference}**
        (
        [ERModel2Visualiser](/Components/pydoc/Kamaelia.Experimental.ERParsing.ERModel2Visualiser.html){.reference},
        [ERParser](/Components/pydoc/Kamaelia.Experimental.ERParsing.ERParser.html){.reference}
        )
    -   **[Services](/Components/pydoc/Kamaelia.Experimental.Services.html){.reference}**
        (
        [RegisterService](/Components/pydoc/Kamaelia.Experimental.Services.RegisterService.html){.reference},
        [Subscribe](/Components/pydoc/Kamaelia.Experimental.Services.Subscribe.html){.reference},
        [ToService](/Components/pydoc/Kamaelia.Experimental.Services.ToService.html){.reference}
        )
-   **[File](/Components/pydoc/Kamaelia.File.html){.reference}**
    -   **[Append](/Components/pydoc/Kamaelia.File.Append.html){.reference}**
        (
        [Append](/Components/pydoc/Kamaelia.File.Append.Append.html){.reference}
        )
    -   **[BetterReading](/Components/pydoc/Kamaelia.File.BetterReading.html){.reference}**
        (
        [IntelligentFileReader](/Components/pydoc/Kamaelia.File.BetterReading.IntelligentFileReader.html){.reference}
        )
    -   **[MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.html){.reference}**
        (
        [MaxSpeedFileReader](/Components/pydoc/Kamaelia.File.MaxSpeedFileReader.MaxSpeedFileReader.html){.reference}
        )
    -   **[ReadFileAdaptor](/Components/pydoc/Kamaelia.File.ReadFileAdaptor.html){.reference}**
        (
        [ReadFileAdaptor](/Components/pydoc/Kamaelia.File.ReadFileAdaptor.ReadFileAdaptor.html){.reference}
        )
    -   **[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}**
        (
        [FixedRateControlledReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.FixedRateControlledReusableFileReader.html){.reference},
        [PromptedFileReader](/Components/pydoc/Kamaelia.File.Reading.PromptedFileReader.html){.reference},
        [RateControlledFileReader](/Components/pydoc/Kamaelia.File.Reading.RateControlledFileReader.html){.reference},
        [RateControlledReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.RateControlledReusableFileReader.html){.reference},
        [ReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.ReusableFileReader.html){.reference},
        [SimpleReader](/Components/pydoc/Kamaelia.File.Reading.SimpleReader.html){.reference}
        )
    -   **[TriggeredFileReader](/Components/pydoc/Kamaelia.File.TriggeredFileReader.html){.reference}**
        (
        [TriggeredFileReader](/Components/pydoc/Kamaelia.File.TriggeredFileReader.TriggeredFileReader.html){.reference}
        )
    -   **[UnixPipe](/Components/pydoc/Kamaelia.File.UnixPipe.html){.reference}**
    -   **[UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.html){.reference}**
        (
        [UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.UnixProcess.html){.reference}
        )
    -   **[UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.html){.reference}**
        (
        [UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.UnixProcess2.html){.reference}
        )
    -   **[WholeFileWriter](/Components/pydoc/Kamaelia.File.WholeFileWriter.html){.reference}**
        (
        [WholeFileWriter](/Components/pydoc/Kamaelia.File.WholeFileWriter.WholeFileWriter.html){.reference}
        )
    -   **[Writing](/Components/pydoc/Kamaelia.File.Writing.html){.reference}**
        (
        [SimpleFileWriter](/Components/pydoc/Kamaelia.File.Writing.SimpleFileWriter.html){.reference}
        )
-   **[IPC](/Components/pydoc/Kamaelia.IPC.html){.reference}**
-   **[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}**
    -   **[ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter.html){.reference}**
        (
        [ConnectedSocketAdapter](/Components/pydoc/Kamaelia.Internet.ConnectedSocketAdapter.ConnectedSocketAdapter.html){.reference}
        )
    -   **[Multicast\_receiver](/Components/pydoc/Kamaelia.Internet.Multicast_receiver.html){.reference}**
        (
        [Multicast\_receiver](/Components/pydoc/Kamaelia.Internet.Multicast_receiver.Multicast_receiver.html){.reference}
        )
    -   **[Multicast\_sender](/Components/pydoc/Kamaelia.Internet.Multicast_sender.html){.reference}**
        (
        [Multicast\_sender](/Components/pydoc/Kamaelia.Internet.Multicast_sender.Multicast_sender.html){.reference}
        )
    -   **[Multicast\_transceiver](/Components/pydoc/Kamaelia.Internet.Multicast_transceiver.html){.reference}**
        (
        [Multicast\_transceiver](/Components/pydoc/Kamaelia.Internet.Multicast_transceiver.Multicast_transceiver.html){.reference}
        )
    -   **[Selector](/Components/pydoc/Kamaelia.Internet.Selector.html){.reference}**
        (
        [Selector](/Components/pydoc/Kamaelia.Internet.Selector.Selector.html){.reference}
        )
    -   **[Simulate](/Components/pydoc/Kamaelia.Internet.Simulate.html){.reference}**
        -   **[BrokenNetwork](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.html){.reference}**
            (
            [Duplicate](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Duplicate.html){.reference},
            [Reorder](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Reorder.html){.reference},
            [Throwaway](/Components/pydoc/Kamaelia.Internet.Simulate.BrokenNetwork.Throwaway.html){.reference}
            )
    -   **[SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.html){.reference}**
        (
        [SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.SingleServer.html){.reference},
        [echo](/Components/pydoc/Kamaelia.Internet.SingleServer.echo.html){.reference}
        )
    -   **[TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.html){.reference}**
        (
        [TCPClient](/Components/pydoc/Kamaelia.Internet.TCPClient.TCPClient.html){.reference}
        )
    -   **[TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.html){.reference}**
        (
        [TCPServer](/Components/pydoc/Kamaelia.Internet.TCPServer.TCPServer.html){.reference}
        )
    -   **[ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.html){.reference}**
        (
        [ThreadedTCPClient](/Components/pydoc/Kamaelia.Internet.ThreadedTCPClient.ThreadedTCPClient.html){.reference}
        )
    -   **[TimeOutCSA](/Components/pydoc/Kamaelia.Internet.TimeOutCSA.html){.reference}**
    -   **[UDP](/Components/pydoc/Kamaelia.Internet.UDP.html){.reference}**
        (
        [PostboxPeer](/Components/pydoc/Kamaelia.Internet.UDP.PostboxPeer.html){.reference},
        [SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP.SimplePeer.html){.reference},
        [TargettedPeer](/Components/pydoc/Kamaelia.Internet.UDP.TargettedPeer.html){.reference}
        )
    -   **[UDP\_ng](/Components/pydoc/Kamaelia.Internet.UDP_ng.html){.reference}**
        (
        [PostboxPeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.PostboxPeer.html){.reference},
        [SimplePeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.SimplePeer.html){.reference},
        [TargettedPeer](/Components/pydoc/Kamaelia.Internet.UDP_ng.TargettedPeer.html){.reference},
        [UDPReceiver](/Components/pydoc/Kamaelia.Internet.UDP_ng.UDPReceiver.html){.reference},
        [UDPSender](/Components/pydoc/Kamaelia.Internet.UDP_ng.UDPSender.html){.reference}
        )
-   **[KamaeliaExceptions](/Components/pydoc/Kamaelia.KamaeliaExceptions.html){.reference}**
-   **[KamaeliaIPC](/Components/pydoc/Kamaelia.KamaeliaIPC.html){.reference}**
-   **[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}**
    -   **[AIM](/Components/pydoc/Kamaelia.Protocol.AIM.html){.reference}**
        -   **[AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.html){.reference}**
            (
            [AIMHarness](/Components/pydoc/Kamaelia.Protocol.AIM.AIMHarness.AIMHarness.html){.reference}
            )
        -   **[ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.html){.reference}**
            (
            [ChatManager](/Components/pydoc/Kamaelia.Protocol.AIM.ChatManager.ChatManager.html){.reference}
            )
        -   **[LoginHandler](/Components/pydoc/Kamaelia.Protocol.AIM.LoginHandler.html){.reference}**
            (
            [LoginHandler](/Components/pydoc/Kamaelia.Protocol.AIM.LoginHandler.LoginHandler.html){.reference}
            )
        -   **[OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.html){.reference}**
            (
            [OSCARClient](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARClient.html){.reference},
            [OSCARProtocol](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.OSCARProtocol.html){.reference},
            [SNACExchanger](/Components/pydoc/Kamaelia.Protocol.AIM.OSCARClient.SNACExchanger.html){.reference}
            )
    -   **[AudioCookieProtocol](/Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol.html){.reference}**
        (
        [AudioCookieProtocol](/Components/pydoc/Kamaelia.Protocol.AudioCookieProtocol.AudioCookieProtocol.html){.reference}
        )
    -   **[EchoProtocol](/Components/pydoc/Kamaelia.Protocol.EchoProtocol.html){.reference}**
        (
        [EchoProtocol](/Components/pydoc/Kamaelia.Protocol.EchoProtocol.EchoProtocol.html){.reference}
        )
    -   **[EchoProtocolComponent](/Components/pydoc/Kamaelia.Protocol.EchoProtocolComponent.html){.reference}**
    -   **[FortuneCookieProtocol](/Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol.html){.reference}**
        (
        [FortuneCookieProtocol](/Components/pydoc/Kamaelia.Protocol.FortuneCookieProtocol.FortuneCookieProtocol.html){.reference}
        )
    -   **[Framing](/Components/pydoc/Kamaelia.Protocol.Framing.html){.reference}**
        (
        [DataChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataChunker.html){.reference},
        [DataDeChunker](/Components/pydoc/Kamaelia.Protocol.Framing.DataDeChunker.html){.reference},
        [DeFramer](/Components/pydoc/Kamaelia.Protocol.Framing.DeFramer.html){.reference},
        [Framer](/Components/pydoc/Kamaelia.Protocol.Framing.Framer.html){.reference}
        )
    -   **[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}**
        -   **[ErrorPages](/Components/pydoc/Kamaelia.Protocol.HTTP.ErrorPages.html){.reference}**
        -   **[HTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}**
            (
            [SimpleHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SimpleHTTPClient.html){.reference},
            [SingleShotHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SingleShotHTTPClient.html){.reference}
            )
        -   **[HTTPHelpers](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPHelpers.html){.reference}**
            (
            [HTTPMakePostRequest](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPHelpers.HTTPMakePostRequest.html){.reference}
            )
        -   **[HTTPParser](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPParser.html){.reference}**
            (
            [HTTPParser](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPParser.HTTPParser.html){.reference}
            )
        -   **[HTTPRequestHandler](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPRequestHandler.html){.reference}**
            (
            [HTTPRequestHandler](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPRequestHandler.HTTPRequestHandler.html){.reference}
            )
        -   **[HTTPResourceGlue](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPResourceGlue.html){.reference}**
        -   **[HTTPServer](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer.html){.reference}**
            (
            [HTTPServer](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer.HTTPServer.html){.reference}
            )
        -   **[Handlers](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.html){.reference}**
            -   **[Minimal](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.Minimal.html){.reference}**
                (
                [Minimal](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.Minimal.Minimal.html){.reference}
                )
            -   **[SessionExample](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.SessionExample.html){.reference}**
                (
                [SessionExample](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.SessionExample.SessionExample.html){.reference}
                )
            -   **[UploadTorrents](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.UploadTorrents.html){.reference}**
                (
                [UploadTorrents](/Components/pydoc/Kamaelia.Protocol.HTTP.Handlers.UploadTorrents.UploadTorrents.html){.reference}
                )
        -   **[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}**
            (
            [IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastClient.html){.reference},
            [IcecastDemux](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastDemux.html){.reference},
            [IcecastStreamRemoveMetadata](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastStreamRemoveMetadata.html){.reference},
            [IcecastStreamWriter](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastStreamWriter.html){.reference}
            )
        -   **[MimeTypes](/Components/pydoc/Kamaelia.Protocol.HTTP.MimeTypes.html){.reference}**
    -   **[IRC](/Components/pydoc/Kamaelia.Protocol.IRC.html){.reference}**
        -   **[IRCClient](/Components/pydoc/Kamaelia.Protocol.IRC.IRCClient.html){.reference}**
    -   **[MimeRequestComponent](/Components/pydoc/Kamaelia.Protocol.MimeRequestComponent.html){.reference}**
        (
        [MimeRequestComponent](/Components/pydoc/Kamaelia.Protocol.MimeRequestComponent.MimeRequestComponent.html){.reference}
        )
    -   **[Packetise](/Components/pydoc/Kamaelia.Protocol.Packetise.html){.reference}**
        (
        [MaxSizePacketiser](/Components/pydoc/Kamaelia.Protocol.Packetise.MaxSizePacketiser.html){.reference}
        )
    -   **[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.html){.reference}**
        -   **[NullPayloadPreFramer](/Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadPreFramer.html){.reference}**
        -   **[NullPayloadRTP](/Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadRTP.html){.reference}**
            (
            [NullPayloadPreFramer](/Components/pydoc/Kamaelia.Protocol.RTP.NullPayloadRTP.NullPayloadPreFramer.html){.reference}
            )
        -   **[RTCPHeader](/Components/pydoc/Kamaelia.Protocol.RTP.RTCPHeader.html){.reference}**
        -   **[RTP](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.html){.reference}**
            (
            [RTPDeframer](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPDeframer.html){.reference},
            [RTPFramer](/Components/pydoc/Kamaelia.Protocol.RTP.RTP.RTPFramer.html){.reference}
            )
        -   **[RTPHeader](/Components/pydoc/Kamaelia.Protocol.RTP.RTPHeader.html){.reference}**
        -   **[RtpPacker](/Components/pydoc/Kamaelia.Protocol.RTP.RtpPacker.html){.reference}**
            (
            [RtpPacker](/Components/pydoc/Kamaelia.Protocol.RTP.RtpPacker.RtpPacker.html){.reference}
            )
    -   **[RecoverOrder](/Components/pydoc/Kamaelia.Protocol.RecoverOrder.html){.reference}**
    -   **[SDP](/Components/pydoc/Kamaelia.Protocol.SDP.html){.reference}**
        (
        [SDPParser](/Components/pydoc/Kamaelia.Protocol.SDP.SDPParser.html){.reference}
        )
    -   **[SimpleReliableMulticast](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.html){.reference}**
        (
        [Annotator](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.Annotator.html){.reference},
        [RecoverOrder](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.RecoverOrder.html){.reference},
        [SRM\_Receiver](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.SRM_Receiver.html){.reference},
        [SRM\_Sender](/Components/pydoc/Kamaelia.Protocol.SimpleReliableMulticast.SRM_Sender.html){.reference}
        )
    -   **[SimpleVideoCookieServer](/Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer.html){.reference}**
        (
        [HelloServer](/Components/pydoc/Kamaelia.Protocol.SimpleVideoCookieServer.HelloServer.html){.reference}
        )
    -   **[Torrent](/Components/pydoc/Kamaelia.Protocol.Torrent.html){.reference}**
        -   **[TorrentClient](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.html){.reference}**
            (
            [BasicTorrentExplainer](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.BasicTorrentExplainer.html){.reference},
            [TorrentClient](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentClient.TorrentClient.html){.reference}
            )
        -   **[TorrentIPC](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentIPC.html){.reference}**
        -   **[TorrentMaker](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentMaker.html){.reference}**
            (
            [TorrentMaker](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentMaker.TorrentMaker.html){.reference}
            )
        -   **[TorrentPatron](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentPatron.html){.reference}**
            (
            [TorrentPatron](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentPatron.TorrentPatron.html){.reference}
            )
        -   **[TorrentService](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentService.html){.reference}**
            (
            [TorrentService](/Components/pydoc/Kamaelia.Protocol.Torrent.TorrentService.TorrentService.html){.reference}
            )
-   **[ReadFileAdaptor](/Components/pydoc/Kamaelia.ReadFileAdaptor.html){.reference}**
-   **[SampleTemplateComponent](/Components/pydoc/Kamaelia.SampleTemplateComponent.html){.reference}**
    (
    [CallbackStyleComponent](/Components/pydoc/Kamaelia.SampleTemplateComponent.CallbackStyleComponent.html){.reference},
    [StandardStyleComponent](/Components/pydoc/Kamaelia.SampleTemplateComponent.StandardStyleComponent.html){.reference}
    )
-   **[SimpleServerComponent](/Components/pydoc/Kamaelia.SimpleServerComponent.html){.reference}**
-   **[SingleServer](/Components/pydoc/Kamaelia.SingleServer.html){.reference}**
-   **[UI](/Components/pydoc/Kamaelia.UI.html){.reference}**
    -   **[GraphicDisplay](/Components/pydoc/Kamaelia.UI.GraphicDisplay.html){.reference}**
    -   **[MH](/Components/pydoc/Kamaelia.UI.MH.html){.reference}**
        -   **[DragHandler](/Components/pydoc/Kamaelia.UI.MH.DragHandler.html){.reference}**
        -   **[PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.html){.reference}**
            (
            [PyGameApp](/Components/pydoc/Kamaelia.UI.MH.PyGameApp.PyGameApp.html){.reference}
            )
        -   **[test](/Components/pydoc/Kamaelia.UI.MH.test.html){.reference}**
            -   **[test\_DragHandler](/Components/pydoc/Kamaelia.UI.MH.test.test_DragHandler.html){.reference}**
    -   **[OpenGL](/Components/pydoc/Kamaelia.UI.OpenGL.html){.reference}**
        -   **[ArrowButton](/Components/pydoc/Kamaelia.UI.OpenGL.ArrowButton.html){.reference}**
            (
            [ArrowButton](/Components/pydoc/Kamaelia.UI.OpenGL.ArrowButton.ArrowButton.html){.reference}
            )
        -   **[Button](/Components/pydoc/Kamaelia.UI.OpenGL.Button.html){.reference}**
            (
            [Button](/Components/pydoc/Kamaelia.UI.OpenGL.Button.Button.html){.reference}
            )
        -   **[Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.html){.reference}**
            (
            [Container](/Components/pydoc/Kamaelia.UI.OpenGL.Container.Container.html){.reference}
            )
        -   **[Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.html){.reference}**
            (
            [Interactor](/Components/pydoc/Kamaelia.UI.OpenGL.Interactor.Interactor.html){.reference}
            )
        -   **[Intersect](/Components/pydoc/Kamaelia.UI.OpenGL.Intersect.html){.reference}**
        -   **[Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.html){.reference}**
            (
            [Label](/Components/pydoc/Kamaelia.UI.OpenGL.Label.Label.html){.reference}
            )
        -   **[LiftTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.LiftTranslationInteractor.html){.reference}**
            (
            [LiftTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.LiftTranslationInteractor.LiftTranslationInteractor.html){.reference}
            )
        -   **[MatchedTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.MatchedTranslationInteractor.html){.reference}**
            (
            [MatchedTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.MatchedTranslationInteractor.MatchedTranslationInteractor.html){.reference}
            )
        -   **[Movement](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.html){.reference}**
            (
            [PathMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.PathMover.html){.reference},
            [SimpleBuzzer](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleBuzzer.html){.reference},
            [SimpleMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleMover.html){.reference},
            [SimpleRotator](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.SimpleRotator.html){.reference},
            [WheelMover](/Components/pydoc/Kamaelia.UI.OpenGL.Movement.WheelMover.html){.reference}
            )
        -   **[OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.html){.reference}**
            (
            [OpenGLComponent](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLComponent.OpenGLComponent.html){.reference}
            )
        -   **[OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.html){.reference}**
            (
            [OpenGLDisplay](/Components/pydoc/Kamaelia.UI.OpenGL.OpenGLDisplay.OpenGLDisplay.html){.reference}
            )
        -   **[ProgressBar](/Components/pydoc/Kamaelia.UI.OpenGL.ProgressBar.html){.reference}**
            (
            [ProgressBar](/Components/pydoc/Kamaelia.UI.OpenGL.ProgressBar.ProgressBar.html){.reference}
            )
        -   **[PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.html){.reference}**
            (
            [PygameWrapper](/Components/pydoc/Kamaelia.UI.OpenGL.PygameWrapper.PygameWrapper.html){.reference}
            )
        -   **[SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.html){.reference}**
            (
            [SimpleButton](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleButton.SimpleButton.html){.reference}
            )
        -   **[SimpleCube](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleCube.html){.reference}**
            (
            [SimpleCube](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleCube.SimpleCube.html){.reference}
            )
        -   **[SimpleRotationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleRotationInteractor.html){.reference}**
            (
            [SimpleRotationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleRotationInteractor.SimpleRotationInteractor.html){.reference}
            )
        -   **[SimpleTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleTranslationInteractor.html){.reference}**
            (
            [SimpleTranslationInteractor](/Components/pydoc/Kamaelia.UI.OpenGL.SimpleTranslationInteractor.SimpleTranslationInteractor.html){.reference}
            )
        -   **[SkyGrassBackground](/Components/pydoc/Kamaelia.UI.OpenGL.SkyGrassBackground.html){.reference}**
            (
            [SkyGrassBackground](/Components/pydoc/Kamaelia.UI.OpenGL.SkyGrassBackground.SkyGrassBackground.html){.reference}
            )
        -   **[TexPlane](/Components/pydoc/Kamaelia.UI.OpenGL.TexPlane.html){.reference}**
            (
            [TexPlane](/Components/pydoc/Kamaelia.UI.OpenGL.TexPlane.TexPlane.html){.reference}
            )
        -   **[Transform](/Components/pydoc/Kamaelia.UI.OpenGL.Transform.html){.reference}**
        -   **[Vector](/Components/pydoc/Kamaelia.UI.OpenGL.Vector.html){.reference}**
    -   **[Pygame](/Components/pydoc/Kamaelia.UI.Pygame.html){.reference}**
        -   **[Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.html){.reference}**
            (
            [Button](/Components/pydoc/Kamaelia.UI.Pygame.Button.Button.html){.reference}
            )
        -   **[Display](/Components/pydoc/Kamaelia.UI.Pygame.Display.html){.reference}**
            (
            [PygameDisplay](/Components/pydoc/Kamaelia.UI.Pygame.Display.PygameDisplay.html){.reference}
            )
        -   **[EventHandler](/Components/pydoc/Kamaelia.UI.Pygame.EventHandler.html){.reference}**
        -   **[Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.html){.reference}**
            (
            [Image](/Components/pydoc/Kamaelia.UI.Pygame.Image.Image.html){.reference}
            )
        -   **[KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.html){.reference}**
            (
            [KeyEvent](/Components/pydoc/Kamaelia.UI.Pygame.KeyEvent.KeyEvent.html){.reference}
            )
        -   **[MagnaDoodle](/Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle.html){.reference}**
            (
            [MagnaDoodle](/Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle.MagnaDoodle.html){.reference}
            )
        -   **[Multiclick](/Components/pydoc/Kamaelia.UI.Pygame.Multiclick.html){.reference}**
            (
            [Multiclick](/Components/pydoc/Kamaelia.UI.Pygame.Multiclick.Multiclick.html){.reference}
            )
        -   **[Text](/Components/pydoc/Kamaelia.UI.Pygame.Text.html){.reference}**
            (
            [TextDisplayer](/Components/pydoc/Kamaelia.UI.Pygame.Text.TextDisplayer.html){.reference},
            [Textbox](/Components/pydoc/Kamaelia.UI.Pygame.Text.Textbox.html){.reference}
            )
        -   **[Ticker](/Components/pydoc/Kamaelia.UI.Pygame.Ticker.html){.reference}**
            (
            [Ticker](/Components/pydoc/Kamaelia.UI.Pygame.Ticker.Ticker.html){.reference}
            )
        -   **[VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.html){.reference}**
            (
            [VideoOverlay](/Components/pydoc/Kamaelia.UI.Pygame.VideoOverlay.VideoOverlay.html){.reference}
            )
        -   **[VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.html){.reference}**
            (
            [VideoSurface](/Components/pydoc/Kamaelia.UI.Pygame.VideoSurface.VideoSurface.html){.reference}
            )
    -   **[PygameDisplay](/Components/pydoc/Kamaelia.UI.PygameDisplay.html){.reference}**
    -   **[Tk](/Components/pydoc/Kamaelia.UI.Tk.html){.reference}**
        -   **[TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.html){.reference}**
            (
            [TkWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.TkWindow.html){.reference},
            [tkInvisibleWindow](/Components/pydoc/Kamaelia.UI.Tk.TkWindow.tkInvisibleWindow.html){.reference}
            )
-   **[Util](/Components/pydoc/Kamaelia.Util.html){.reference}**
    -   **[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}**
        (
        [Backplane](/Components/pydoc/Kamaelia.Util.Backplane.Backplane.html){.reference},
        [PublishTo](/Components/pydoc/Kamaelia.Util.Backplane.PublishTo.html){.reference},
        [SubscribeTo](/Components/pydoc/Kamaelia.Util.Backplane.SubscribeTo.html){.reference}
        )
    -   **[Chargen](/Components/pydoc/Kamaelia.Util.Chargen.html){.reference}**
        (
        [Chargen](/Components/pydoc/Kamaelia.Util.Chargen.Chargen.html){.reference}
        )
    -   **[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.html){.reference}**
        (
        [Chooser](/Components/pydoc/Kamaelia.Util.Chooser.Chooser.html){.reference},
        [ForwardIteratingChooser](/Components/pydoc/Kamaelia.Util.Chooser.ForwardIteratingChooser.html){.reference}
        )
    -   **[ChunkNamer](/Components/pydoc/Kamaelia.Util.ChunkNamer.html){.reference}**
        (
        [ChunkNamer](/Components/pydoc/Kamaelia.Util.ChunkNamer.ChunkNamer.html){.reference}
        )
    -   **[Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.html){.reference}**
        (
        [Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.Chunkifier.html){.reference}
        )
    -   **[Clock](/Components/pydoc/Kamaelia.Util.Clock.html){.reference}**
        (
        [CheapAndCheerfulClock](/Components/pydoc/Kamaelia.Util.Clock.CheapAndCheerfulClock.html){.reference}
        )
    -   **[Collate](/Components/pydoc/Kamaelia.Util.Collate.html){.reference}**
        (
        [Collate](/Components/pydoc/Kamaelia.Util.Collate.Collate.html){.reference}
        )
    -   **[Comparator](/Components/pydoc/Kamaelia.Util.Comparator.html){.reference}**
        (
        [Comparator](/Components/pydoc/Kamaelia.Util.Comparator.Comparator.html){.reference}
        )
    -   **[Console](/Components/pydoc/Kamaelia.Util.Console.html){.reference}**
        (
        [ConsoleEchoer](/Components/pydoc/Kamaelia.Util.Console.ConsoleEchoer.html){.reference},
        [ConsoleReader](/Components/pydoc/Kamaelia.Util.Console.ConsoleReader.html){.reference}
        )
    -   **[ConsoleEcho](/Components/pydoc/Kamaelia.Util.ConsoleEcho.html){.reference}**
    -   **[DataSource](/Components/pydoc/Kamaelia.Util.DataSource.html){.reference}**
        (
        [DataSource](/Components/pydoc/Kamaelia.Util.DataSource.DataSource.html){.reference},
        [TriggeredSource](/Components/pydoc/Kamaelia.Util.DataSource.TriggeredSource.html){.reference}
        )
    -   **[Detuple](/Components/pydoc/Kamaelia.Util.Detuple.html){.reference}**
        (
        [SimpleDetupler](/Components/pydoc/Kamaelia.Util.Detuple.SimpleDetupler.html){.reference}
        )
    -   **[Fanout](/Components/pydoc/Kamaelia.Util.Fanout.html){.reference}**
        (
        [Fanout](/Components/pydoc/Kamaelia.Util.Fanout.Fanout.html){.reference}
        )
    -   **[Filter](/Components/pydoc/Kamaelia.Util.Filter.html){.reference}**
        (
        [Filter](/Components/pydoc/Kamaelia.Util.Filter.Filter.html){.reference}
        )
    -   **[FilterComponent](/Components/pydoc/Kamaelia.Util.FilterComponent.html){.reference}**
    -   **[FirstOnly](/Components/pydoc/Kamaelia.Util.FirstOnly.html){.reference}**
        (
        [FirstOnly](/Components/pydoc/Kamaelia.Util.FirstOnly.FirstOnly.html){.reference}
        )
    -   **[Graphline](/Components/pydoc/Kamaelia.Util.Graphline.html){.reference}**
    -   **[Introspector](/Components/pydoc/Kamaelia.Util.Introspector.html){.reference}**
        (
        [Introspector](/Components/pydoc/Kamaelia.Util.Introspector.Introspector.html){.reference}
        )
    -   **[LineSplit](/Components/pydoc/Kamaelia.Util.LineSplit.html){.reference}**
        (
        [LineSplit](/Components/pydoc/Kamaelia.Util.LineSplit.LineSplit.html){.reference}
        )
    -   **[LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.html){.reference}**
        (
        [LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector.LossyConnector.html){.reference}
        )
    -   **[MarshallComponent](/Components/pydoc/Kamaelia.Util.MarshallComponent.html){.reference}**
        (
        [BasicMarshallComponent](/Components/pydoc/Kamaelia.Util.MarshallComponent.BasicMarshallComponent.html){.reference}
        )
    -   **[Marshalling](/Components/pydoc/Kamaelia.Util.Marshalling.html){.reference}**
        (
        [DeMarshaller](/Components/pydoc/Kamaelia.Util.Marshalling.DeMarshaller.html){.reference},
        [Marshaller](/Components/pydoc/Kamaelia.Util.Marshalling.Marshaller.html){.reference}
        )
    -   **[Max](/Components/pydoc/Kamaelia.Util.Max.html){.reference}**
        (
        [Max](/Components/pydoc/Kamaelia.Util.Max.Max.html){.reference}
        )
    -   **[NullSink](/Components/pydoc/Kamaelia.Util.NullSink.html){.reference}**
        (
        [nullSinkComponent](/Components/pydoc/Kamaelia.Util.NullSink.nullSinkComponent.html){.reference}
        )
    -   **[NullSinkComponent](/Components/pydoc/Kamaelia.Util.NullSinkComponent.html){.reference}**
        (
        [nullSinkComponent](/Components/pydoc/Kamaelia.Util.NullSinkComponent.nullSinkComponent.html){.reference}
        )
    -   **[OneShot](/Components/pydoc/Kamaelia.Util.OneShot.html){.reference}**
        (
        [OneShot](/Components/pydoc/Kamaelia.Util.OneShot.OneShot.html){.reference},
        [TriggeredOneShot](/Components/pydoc/Kamaelia.Util.OneShot.TriggeredOneShot.html){.reference}
        )
    -   **[PassThrough](/Components/pydoc/Kamaelia.Util.PassThrough.html){.reference}**
        (
        [PassThrough](/Components/pydoc/Kamaelia.Util.PassThrough.PassThrough.html){.reference}
        )
    -   **[Pipeline](/Components/pydoc/Kamaelia.Util.Pipeline.html){.reference}**
    -   **[PipelineComponent](/Components/pydoc/Kamaelia.Util.PipelineComponent.html){.reference}**
    -   **[PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.html){.reference}**
        (
        [PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.PromptedTurnstile.html){.reference}
        )
    -   **[PureTransformer](/Components/pydoc/Kamaelia.Util.PureTransformer.html){.reference}**
        (
        [PureTransformer](/Components/pydoc/Kamaelia.Util.PureTransformer.PureTransformer.html){.reference}
        )
    -   **[RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.html){.reference}**
        (
        [RangeFilter](/Components/pydoc/Kamaelia.Util.RangeFilter.RangeFilter.html){.reference}
        )
    -   **[RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.html){.reference}**
        (
        [RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.RateChunker.html){.reference}
        )
    -   **[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}**
        (
        [ByteRate\_RequestControl](/Components/pydoc/Kamaelia.Util.RateFilter.ByteRate_RequestControl.html){.reference},
        [MessageRateLimit](/Components/pydoc/Kamaelia.Util.RateFilter.MessageRateLimit.html){.reference},
        [OnDemandLimit](/Components/pydoc/Kamaelia.Util.RateFilter.OnDemandLimit.html){.reference},
        [VariableByteRate\_RequestControl](/Components/pydoc/Kamaelia.Util.RateFilter.VariableByteRate_RequestControl.html){.reference}
        )
    -   **[SequentialTransformer](/Components/pydoc/Kamaelia.Util.SequentialTransformer.html){.reference}**
        (
        [SequentialTransformer](/Components/pydoc/Kamaelia.Util.SequentialTransformer.SequentialTransformer.html){.reference}
        )
    -   **[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}**
        (
        [Plug](/Components/pydoc/Kamaelia.Util.Splitter.Plug.html){.reference},
        [PlugSplitter](/Components/pydoc/Kamaelia.Util.Splitter.PlugSplitter.html){.reference},
        [Splitter](/Components/pydoc/Kamaelia.Util.Splitter.Splitter.html){.reference}
        )
    -   **[Stringify](/Components/pydoc/Kamaelia.Util.Stringify.html){.reference}**
        (
        [Stringify](/Components/pydoc/Kamaelia.Util.Stringify.Stringify.html){.reference}
        )
    -   **[Sync](/Components/pydoc/Kamaelia.Util.Sync.html){.reference}**
        (
        [Sync](/Components/pydoc/Kamaelia.Util.Sync.Sync.html){.reference}
        )
    -   **[TagWithSequenceNumber](/Components/pydoc/Kamaelia.Util.TagWithSequenceNumber.html){.reference}**
        (
        [TagWithSequenceNumber](/Components/pydoc/Kamaelia.Util.TagWithSequenceNumber.TagWithSequenceNumber.html){.reference}
        )
    -   **[TestResult](/Components/pydoc/Kamaelia.Util.TestResult.html){.reference}**
        (
        [TestResult](/Components/pydoc/Kamaelia.Util.TestResult.TestResult.html){.reference}
        )
    -   **[TestResultComponent](/Components/pydoc/Kamaelia.Util.TestResultComponent.html){.reference}**
    -   **[ToStringComponent](/Components/pydoc/Kamaelia.Util.ToStringComponent.html){.reference}**
    -   **[Tokenisation](/Components/pydoc/Kamaelia.Util.Tokenisation.html){.reference}**
        -   **[Simple](/Components/pydoc/Kamaelia.Util.Tokenisation.Simple.html){.reference}**
            (
            [lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Util.Tokenisation.Simple.lines_to_tokenlists.html){.reference},
            [tokenlists\_to\_lines](/Components/pydoc/Kamaelia.Util.Tokenisation.Simple.tokenlists_to_lines.html){.reference}
            )
    -   **[TwoWaySplitter](/Components/pydoc/Kamaelia.Util.TwoWaySplitter.html){.reference}**
        (
        [TwoWaySplitter](/Components/pydoc/Kamaelia.Util.TwoWaySplitter.TwoWaySplitter.html){.reference}
        )
    -   **[UnseenOnly](/Components/pydoc/Kamaelia.Util.UnseenOnly.html){.reference}**
        (
        [UnseenOnly](/Components/pydoc/Kamaelia.Util.UnseenOnly.UnseenOnly.html){.reference}
        )
-   **[Video](/Components/pydoc/Kamaelia.Video.html){.reference}**
    -   **[CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.html){.reference}**
        (
        [CropAndScale](/Components/pydoc/Kamaelia.Video.CropAndScale.CropAndScale.html){.reference}
        )
    -   **[DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.html){.reference}**
        (
        [DetectShotChanges](/Components/pydoc/Kamaelia.Video.DetectShotChanges.DetectShotChanges.html){.reference}
        )
    -   **[PixFormatConversion](/Components/pydoc/Kamaelia.Video.PixFormatConversion.html){.reference}**
        (
        [ToRGB\_interleaved](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToRGB_interleaved.html){.reference},
        [ToYUV420\_planar](/Components/pydoc/Kamaelia.Video.PixFormatConversion.ToYUV420_planar.html){.reference}
        )
-   **[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}**
    -   **[Axon](/Components/pydoc/Kamaelia.Visualisation.Axon.html){.reference}**
        -   **[AxonLaws](/Components/pydoc/Kamaelia.Visualisation.Axon.AxonLaws.html){.reference}**
        -   **[AxonVisualiserServer](/Components/pydoc/Kamaelia.Visualisation.Axon.AxonVisualiserServer.html){.reference}**
            (
            [AxonVisualiser](/Components/pydoc/Kamaelia.Visualisation.Axon.AxonVisualiserServer.AxonVisualiser.html){.reference},
            [AxonVisualiserServer](/Components/pydoc/Kamaelia.Visualisation.Axon.AxonVisualiserServer.AxonVisualiserServer.html){.reference}
            )
        -   **[ExtraWindowFurniture](/Components/pydoc/Kamaelia.Visualisation.Axon.ExtraWindowFurniture.html){.reference}**
        -   **[PComponent](/Components/pydoc/Kamaelia.Visualisation.Axon.PComponent.html){.reference}**
        -   **[PPostbox](/Components/pydoc/Kamaelia.Visualisation.Axon.PPostbox.html){.reference}**
    -   **[ER](/Components/pydoc/Kamaelia.Visualisation.ER.html){.reference}**
        -   **[ERLaws](/Components/pydoc/Kamaelia.Visualisation.ER.ERLaws.html){.reference}**
        -   **[ERVisualiserServer](/Components/pydoc/Kamaelia.Visualisation.ER.ERVisualiserServer.html){.reference}**
            (
            [ERVisualiser](/Components/pydoc/Kamaelia.Visualisation.ER.ERVisualiserServer.ERVisualiser.html){.reference},
            [ERVisualiserServer](/Components/pydoc/Kamaelia.Visualisation.ER.ERVisualiserServer.ERVisualiserServer.html){.reference}
            )
        -   **[ExtraWindowFurniture](/Components/pydoc/Kamaelia.Visualisation.ER.ExtraWindowFurniture.html){.reference}**
        -   **[PAttribute](/Components/pydoc/Kamaelia.Visualisation.ER.PAttribute.html){.reference}**
        -   **[PEntity](/Components/pydoc/Kamaelia.Visualisation.ER.PEntity.html){.reference}**
        -   **[PISA](/Components/pydoc/Kamaelia.Visualisation.ER.PISA.html){.reference}**
        -   **[PRelation](/Components/pydoc/Kamaelia.Visualisation.ER.PRelation.html){.reference}**
    -   **[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}**
        -   **[GridRenderer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.GridRenderer.html){.reference}**
        -   **[ParticleDragger](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.ParticleDragger.html){.reference}**
        -   **[RenderingParticle](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.RenderingParticle.html){.reference}**
        -   **[TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html){.reference}**
            (
            [TopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.TopologyViewer.html){.reference}
            )
        -   **[TopologyViewerComponent](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerComponent.html){.reference}**
        -   **[TopologyViewerServer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.html){.reference}**
            (
            [TextControlledTopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.TextControlledTopologyViewer.html){.reference},
            [TopologyViewerServer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.TopologyViewerServer.html){.reference}
            )
        -   **[chunks\_to\_lines](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.html){.reference}**
            (
            [chunks\_to\_lines](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines.chunks_to_lines.html){.reference}
            )
        -   **[lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.html){.reference}**
            (
            [lines\_to\_tokenlists](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists.lines_to_tokenlists.html){.reference}
            )
    -   **[PhysicsGraph3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.html){.reference}**
        -   **[Particles3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.Particles3D.html){.reference}**
        -   **[TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.html){.reference}**
            (
            [TopologyViewer3D](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3D.TopologyViewer3D.html){.reference}
            )
        -   **[TopologyViewer3DWithParams](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams.html){.reference}**
            (
            [TopologyViewer3DWithParams](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph3D.TopologyViewer3DWithParams.TopologyViewer3DWithParams.html){.reference}
            )
-   **[XML](/Components/pydoc/Kamaelia.XML.html){.reference}**
    -   **[SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.html){.reference}**
        (
        [SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.SimpleXMLParser.html){.reference}
        )
-   **[vorbisDecodeComponent](/Components/pydoc/Kamaelia.vorbisDecodeComponent.html){.reference}**

Support Code
============

These files do not contain Components, but are used with and useful for
components.

[**Kamaelia**](/Components/pydoc/Kamaelia.html)

-   **[Support](/Components/pydoc/Kamaelia.Support.html){.reference}**
    -   **[DVB](/Components/pydoc/Kamaelia.Support.DVB.html){.reference}**
        -   **[CRC](/Components/pydoc/Kamaelia.Support.DVB.CRC.html){.reference}**
        -   **[DateTime](/Components/pydoc/Kamaelia.Support.DVB.DateTime.html){.reference}**
        -   **[Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}**
    -   **[Data](/Components/pydoc/Kamaelia.Support.Data.html){.reference}**
        -   **[Escape](/Components/pydoc/Kamaelia.Support.Data.Escape.html){.reference}**
        -   **[Experimental](/Components/pydoc/Kamaelia.Support.Data.Experimental.html){.reference}**
            (
            [GraphSlideXMLComponent](/Components/pydoc/Kamaelia.Support.Data.Experimental.GraphSlideXMLComponent.html){.reference},
            [onDemandGraphFileParser\_Prefab](/Components/pydoc/Kamaelia.Support.Data.Experimental.onDemandGraphFileParser_Prefab.html){.reference}
            )
        -   **[ISO639\_2](/Components/pydoc/Kamaelia.Support.Data.ISO639_2.html){.reference}**
        -   **[MimeDict](/Components/pydoc/Kamaelia.Support.Data.MimeDict.html){.reference}**
        -   **[MimeObject](/Components/pydoc/Kamaelia.Support.Data.MimeObject.html){.reference}**
        -   **[Rationals](/Components/pydoc/Kamaelia.Support.Data.Rationals.html){.reference}**
        -   **[Repository](/Components/pydoc/Kamaelia.Support.Data.Repository.html){.reference}**
        -   **[bitfieldrec](/Components/pydoc/Kamaelia.Support.Data.bitfieldrec.html){.reference}**
        -   **[requestLine](/Components/pydoc/Kamaelia.Support.Data.requestLine.html){.reference}**
        -   **[tests](/Components/pydoc/Kamaelia.Support.Data.tests.html){.reference}**
            -   **[test\_Escape](/Components/pydoc/Kamaelia.Support.Data.tests.test_Escape.html){.reference}**
            -   **[test\_MimeDict](/Components/pydoc/Kamaelia.Support.Data.tests.test_MimeDict.html){.reference}**
            -   **[test\_Rationals](/Components/pydoc/Kamaelia.Support.Data.tests.test_Rationals.html){.reference}**
    -   **[Deprecate](/Components/pydoc/Kamaelia.Support.Deprecate.html){.reference}**
    -   **[OscarUtil](/Components/pydoc/Kamaelia.Support.OscarUtil.html){.reference}**
    -   **[OscarUtil2](/Components/pydoc/Kamaelia.Support.OscarUtil2.html){.reference}**
    -   **[Particles](/Components/pydoc/Kamaelia.Support.Particles.html){.reference}**
        -   **[MultipleLaws](/Components/pydoc/Kamaelia.Support.Particles.MultipleLaws.html){.reference}**
        -   **[Particle](/Components/pydoc/Kamaelia.Support.Particles.Particle.html){.reference}**
        -   **[ParticleSystem](/Components/pydoc/Kamaelia.Support.Particles.ParticleSystem.html){.reference}**
        -   **[SimpleLaws](/Components/pydoc/Kamaelia.Support.Particles.SimpleLaws.html){.reference}**
        -   **[SpatialIndexer](/Components/pydoc/Kamaelia.Support.Particles.SpatialIndexer.html){.reference}**
    -   **[Protocol](/Components/pydoc/Kamaelia.Support.Protocol.html){.reference}**
        -   **[IRC](/Components/pydoc/Kamaelia.Support.Protocol.IRC.html){.reference}**
    -   **[PyMedia](/Components/pydoc/Kamaelia.Support.PyMedia.html){.reference}**
        -   **[AudioFormats](/Components/pydoc/Kamaelia.Support.PyMedia.AudioFormats.html){.reference}**
    -   **[Tk](/Components/pydoc/Kamaelia.Support.Tk.html){.reference}**
        -   **[Scrolling](/Components/pydoc/Kamaelia.Support.Tk.Scrolling.html){.reference}**

Application Specific Components
===============================

[**Kamaelia**](/Components/pydoc/Kamaelia.html)

-   **[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}**
    -   **[Compose](/Components/pydoc/Kamaelia.Apps.Compose.html){.reference}**
        -   **[BuildViewer](/Components/pydoc/Kamaelia.Apps.Compose.BuildViewer.html){.reference}**
        -   **[CodeGen](/Components/pydoc/Kamaelia.Apps.Compose.CodeGen.html){.reference}**
        -   **[GUI](/Components/pydoc/Kamaelia.Apps.Compose.GUI.html){.reference}**
        -   **[PipeBuild](/Components/pydoc/Kamaelia.Apps.Compose.PipeBuild.html){.reference}**
        -   **[PipelineWriter](/Components/pydoc/Kamaelia.Apps.Compose.PipelineWriter.html){.reference}**
    -   **[Games4Kids](/Components/pydoc/Kamaelia.Apps.Games4Kids.html){.reference}**
        -   **[BasicSprite](/Components/pydoc/Kamaelia.Apps.Games4Kids.BasicSprite.html){.reference}**
        -   **[MyGamesEventsComponent](/Components/pydoc/Kamaelia.Apps.Games4Kids.MyGamesEventsComponent.html){.reference}**
        -   **[SpriteScheduler](/Components/pydoc/Kamaelia.Apps.Games4Kids.SpriteScheduler.html){.reference}**
    -   **[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}**
        -   **[ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.html){.reference}**
            (
            [ConcreteMailHandler](/Components/pydoc/Kamaelia.Apps.Grey.ConcreteMailHandler.ConcreteMailHandler.html){.reference}
            )
        -   **[GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.html){.reference}**
            (
            [GreyListingPolicy](/Components/pydoc/Kamaelia.Apps.Grey.GreyListingPolicy.GreyListingPolicy.html){.reference}
            )
        -   **[MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.html){.reference}**
            (
            [MailHandler](/Components/pydoc/Kamaelia.Apps.Grey.MailHandler.MailHandler.html){.reference}
            )
        -   **[PeriodicWakeup](/Components/pydoc/Kamaelia.Apps.Grey.PeriodicWakeup.html){.reference}**
            (
            [PeriodicWakeup](/Components/pydoc/Kamaelia.Apps.Grey.PeriodicWakeup.PeriodicWakeup.html){.reference}
            )
        -   **[Support](/Components/pydoc/Kamaelia.Apps.Grey.Support.html){.reference}**
        -   **[WakeableIntrospector](/Components/pydoc/Kamaelia.Apps.Grey.WakeableIntrospector.html){.reference}**
            (
            [WakeableIntrospector](/Components/pydoc/Kamaelia.Apps.Grey.WakeableIntrospector.WakeableIntrospector.html){.reference}
            )
    -   **[IRCLogger](/Components/pydoc/Kamaelia.Apps.IRCLogger.html){.reference}**
        -   **[Support](/Components/pydoc/Kamaelia.Apps.IRCLogger.Support.html){.reference}**
    -   **[Show](/Components/pydoc/Kamaelia.Apps.Show.html){.reference}**
        -   **[GraphSlides](/Components/pydoc/Kamaelia.Apps.Show.GraphSlides.html){.reference}**
            (
            [GraphSlideXMLComponent](/Components/pydoc/Kamaelia.Apps.Show.GraphSlides.GraphSlideXMLComponent.html){.reference}
            )
    -   **[SpeakNWrite](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.html){.reference}**
        -   **[Gestures](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.html){.reference}**
            -   **[Analyser](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.Analyser.html){.reference}**
            -   **[Grammar](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.Grammar.html){.reference}**
            -   **[GrammarRules](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.GrammarRules.html){.reference}**
            -   **[Patterns](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.Patterns.html){.reference}**
            -   **[Pen](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.Pen.html){.reference}**
            -   **[PreProcessing](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.PreProcessing.html){.reference}**
            -   **[StrokeRecogniser](/Components/pydoc/Kamaelia.Apps.SpeakNWrite.Gestures.StrokeRecogniser.html){.reference}**
    -   **[Whiteboard](/Components/pydoc/Kamaelia.Apps.Whiteboard.html){.reference}**
        -   **[Audio](/Components/pydoc/Kamaelia.Apps.Whiteboard.Audio.html){.reference}**
        -   **[Canvas](/Components/pydoc/Kamaelia.Apps.Whiteboard.Canvas.html){.reference}**
        -   **[CheckpointSequencer](/Components/pydoc/Kamaelia.Apps.Whiteboard.CheckpointSequencer.html){.reference}**
        -   **[CommandConsole](/Components/pydoc/Kamaelia.Apps.Whiteboard.CommandConsole.html){.reference}**
        -   **[Entuple](/Components/pydoc/Kamaelia.Apps.Whiteboard.Entuple.html){.reference}**
        -   **[Options](/Components/pydoc/Kamaelia.Apps.Whiteboard.Options.html){.reference}**
        -   **[Painter](/Components/pydoc/Kamaelia.Apps.Whiteboard.Painter.html){.reference}**
        -   **[Palette](/Components/pydoc/Kamaelia.Apps.Whiteboard.Palette.html){.reference}**
        -   **[Router](/Components/pydoc/Kamaelia.Apps.Whiteboard.Router.html){.reference}**
        -   **[Routers](/Components/pydoc/Kamaelia.Apps.Whiteboard.Routers.html){.reference}**
        -   **[SingleShot](/Components/pydoc/Kamaelia.Apps.Whiteboard.SingleShot.html){.reference}**
        -   **[TagFiltering](/Components/pydoc/Kamaelia.Apps.Whiteboard.TagFiltering.html){.reference}**
        -   **[Tokenisation](/Components/pydoc/Kamaelia.Apps.Whiteboard.Tokenisation.html){.reference}**
        -   **[TwoWaySplitter](/Components/pydoc/Kamaelia.Apps.Whiteboard.TwoWaySplitter.html){.reference}**
        -   **[UI](/Components/pydoc/Kamaelia.Apps.Whiteboard.UI.html){.reference}**
:::

------------------------------------------------------------------------

::: {.section}
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
