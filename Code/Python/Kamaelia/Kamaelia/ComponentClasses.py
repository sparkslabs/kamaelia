# Component Heirarchy
#
# Overview
#	RtspRtpServer
#		SourceMedia
#		MetaInfoDB
#		RTPNetworkPlayer
#			Network Player
#			PreFramer
#			RTP_Handler
#				RTCPHandler
#				DataPump
#			Net Player Factory
#		RTSPNetworkPlayerControl
#		InternetConnectionAbstractionLayer
#
#	Dia	Doc
#	Y		RtspRtpServer
#	 			SourceMedia
#				MetaInfoDB
#	Y			RTPNetworkPlayer
#					Net Player Factory
#					Network Player
#						SourceControl
#						PlayerManagement
#						PlayerStateManagement
#						TransmissionControl
#						PlayerInformationBroker
#	Y	Y			PreFramer
#						FileReader
#						FormatDecoder
#						DataReframing
#						FileSelector
#						CommandInterpreter
#	Y				RTP_Handler
#						TimeStamping
#						RTPPackaging
#						PacketParser
#						PacketIdent
#						RTPControl
#						JitterCompensation
#	Y				RTCPHandler
#						LocalFeedbackHandler
#						ClientFeedbackHandler
#						ConnectionMonitoring]
#						ConnectionControl
#	Y				DataPump
#						DataPassthrough
#						BlockAcceptance
#						ConstantBitRateSender
#						CommandHandler
#						ConnCreate
#				RTSPNetworkPlayerControl
#					NetPlayerController
#					RTSPHandler
#					SDPFormatter
#				InternetConnectionAbstractionLayer
#					InetConnFactory
#					InetConn

#	Y		RtspRtpServer
#	 			SourceMedia
#				MetaInfoDB

from Axon.Component import component, scheduler

class RTPNetworkPlayer(component):   ### XXXX Code,Docs Needed
   """Contains logical subcomponents:
      PreFramer, RTPHandler, RTCPHandler, DataPump, 
      NetPlayerFactory, NetworkPlayer
   """
   Inboxes=["data", "feedback", "conninfo", "createplayer", "control"]
   Outboxes=["select", "stream", "getconn", "playerinfo"]
   Usescomponents=[PreFramer, RTPHandler, RTCPHandler, DataPump, 
                  NetPlayerFactory, NetworkPlayer]

   def __init__(self):
      #
      # Inbound passthrough linkages
      #
      self.link((self,"data"),         (PreFramer,"RecvSrc"),       passthrough=IN)
      self.link((self,"feedback"),     (DataPump,"source"),         passthrough=IN)
      self.link((self,"conninfo"),     (DataPump,"conninfo"),       passthrough=IN)
      self.link((self,"createplayer"), (NetPlayerFactory,"create"), passthrough=IN)
      self.link((self,"control"),      (NetworkPlayer,"control"),   passthrough=IN)
      #
      # Outbound passthrough linkages
      #
      self.link((PreFramer,"ActivateSrc"),        (self,"Select"),     passthrough=OUT)
      self.link((NetworkPlayer,"playerfeedback"), (self,"PlayerInfo"), passthrough=OUT)
      self.link((DataPump,"GenConn"),             (self,"GetConn"),    passthrough=OUT)
      self.link((DataPump,"Sink"),                (self,"Stream"),     passthrough=OUT)
      #
      # Other internal linkages
      #
      self.link((PreFramer,"Output"),           (RTPHandler,"PacketisedIn"))
      self.link((RTCPHandler,"playerfeedback"), (NetworkPLayer,"streamfeedback"))
      #
      self.link((RTPHander,"RTCPFeedBack"), (RTCPHandler,"rtpfeedback"))
      self.link((RTPHander,"RTCPPacket"),   (RTCPHandler,"packetin"))
      #
      self.link((DataPump,"Recv"),        (RTPHandler,"UnbufferedIn"))
      self.link((DataPump,"BackChannel"), (NetworkPlayer,"datapumpfeedback"))
      #
      self.link((NetworkPlayer,"preframecontrol"), (PreFramer,"control"))
      self.link((NetworkPlayer,"datapumpcontrol"), (DataPump,"control"))


class NetworkPlayer(component):   ### XXXX Code,Docs Needed
   """Contains logical subcomponents:
      SourceControl, PlayerManagement, PlayerStateManagement,
      TransmissionControl, PlayerInformationBroker
   """
   Inboxes=["streamfeedback", "control", "datapumpfeedback"] 
   Outboxes=["preframecontrol", "playerfeedback", "datapumpcontrol"]
   Usescomponents=[SourceControl, PlayerManagement, PlayerStateManagement,
                  TransmissionControl, PlayerInformationBroker]

   def __init__(self):
      #
      # Inbound passthrough linkages
      #
      self.link((self,"streamfeedback"), (PlayerStateManagement,"streamin"),     passthrough=IN)
      self.link((self,"datapumpfeedback"), (PlayerStateManagement,"datapumpin"), passthrough=IN)
      self.link((self,"control"), (PlayerManagement,"control"),                  passthrough=IN)
      #
      # Outbound passthrough linkages
      #
      self.link((SourceControl,"selectionframingcontrol"), (self,"preframercontrol"), passthrough=OUT)
      self.link((TransmissionControl,"pumpcommand"),       (self,"datapumpcontrol"),  passthrough=OUT)
      self.link((PlayerInformationBroker,"streaminfo"),    (self,"playerfeedback"),   passthrough=OUT)
      #
      # Other internal linkages
      #
      self.link((PlayerManagement,"sourcecommand"), (SourceControl,"control"))
      self.link((PlayerManagement,"streamstate"), (PlayerStateManagement,"controlin"))
      self.link((PlayerManagement,"ratecontrol"), (TransmissionControl,"ratecontrol"))
      self.link((PlayerManagement,"streamfeedback"), (PlayerInformationBroker,"in"))

      self.link((PlayerStateManagement,"dataready"), (PlayerManagement,"dataalert"))

class SourceControl(component):    ### XXXX Code,Docs Needed
   Inboxes=["control"]
   Outboxes=["selectionframingcontrol"]

class PlayerManagement(component):    ### XXXX Code,Docs Needed
   Inboxes=["control","dataalert"]
   Outboxes=["sourcecommand", "streamstate", "ratecontrol", "streamfeedback"]

class PlayerStateManagement(component):    ### XXXX Code,Docs Needed
   Inboxes=["streamin", "datapumpin", "controlin"]
   Outboxes=["dataready"]

class TransmissionControl(component):  ### XXXX Code,Docs Needed
   Inboxes=["ratecontrol"]
   Outboxes=["pumpcommand"]

class PlayerInformationBroker(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["streaminfo"]

class PreFramer(component):   ### XXXX Code,Docs Needed
   """Contains logical subcomponents:
      CommandInterpreter, FileSelector, FileReader, FormatDecoder, DataReframing
   """
   Inboxes=["RecvSrc", "Control"] 
   Outboxes=["ActivateSrc", "Output"]
   Usescomponents=[CommandInterpreter, FileSelector, FileReader, FormatDecoder, DataReframing]

   def __init__(self):
      #
      # Inbound passthrough linkages
      #
      self.link((self,"Control"), (CommandInterpreter,"input"), passthrough=IN)
      self.link((self,"RecvSrc"), (FileReader,"datain"), passthrough=IN)
      #
      # Outbound passthrough linkages
      #
      self.link((FileSelector,"out"), (self,"ActivateSrc"), passthrough=OUT)
      self.link((DataReframing,"out"), (self,"Output"), passthrough=OUT)
      #
      # Other internal linkages
      #
      self.link((FileReader,"out"), (FormatDecoder,"in"))
      self.link((FormatDecoder,"out"), (DataReframing,"datain"))
      self.link((CommandInterpreter,"fileselect"), (FileSelector,"in"))
      self.link((CommandInterpreter,"filestartstop"), (FileReader,"control"))
      self.link((CommandInterpreter,"framecontrol"), (DataReframing,"control"))

class FileReader(component):    ### XXXX Code,Docs Needed
   Inboxes=["datain","control"]
   Outboxes=["out"]

class FormatDecoder(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["out"]

class DataReframing(component):    ### XXXX Code,Docs Needed
   Inboxes=["control","datain"]
   Outboxes=["out"]

class FileSelector(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["out"]

class CommandInterpreter(component):    ### XXXX Code,Docs Needed
   Inboxes=["input"]
   Outboxes=["fileselect","filestartstop","framecontrol"]

class RTPHandler(component):   ### XXXX Code,Docs Needed
   """Contains logical subcomponents:
      TimeStamping, RTPPackaging, JitterCompensation,
      RTPControl, PacketIdent, PacketParser
   """
   Inboxes=["PacketisedIn", "UnbufferedIn"] 
   Outboxes=["UnbufferedOut", "RTCPFeedback", "RTCPPacket"]
   Usescomponents=[TimeStamping, RTPPackaging, JitterCompensation,RTPControl, PacketIdent, PacketParser]

   def __init__(self):
      #
      # Inbound passthrough linkages
      #
      self.link((self,"PacketisedIn"), (TimeStamping,"in"), passthrough=IN)
      self.link((self,"UnbufferedIn"), (PacketParser,"in"), passthrough=IN)
      #
      # Outbound passthrough linkages
      #
      self.link((RTPPackaging,"out"), (self,"UnbufferedOut"), passthrough=OUT)
      self.link((JitterCompensation,"feedback"), (self,"RTCPFeedback"), passthrough=OUT)
      #
      # Other internal linkages
      #
      self.link((TimeStamping,"out"), (RTPPacking,"datain"))
      self.link((PacketParser,"packetout"), (PacketIdent,"packets"))
      self.link((PacketIdent,"rtpdata"), (RTPControl,"in"))
      self.link((PacketIdent,"rtcpdata"), (self,"RTCPPacket"))
      self.link((RTPControl,"jittercontrol"), (JitterCompensation,"in"))
      self.link((RTPControl,"packagefeedback"), (RTPPackaging,"feedback"))

class TimeStamping(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["out"]

class RTPPackaging(component):    ### XXXX Code,Docs Needed
   Inboxes=["datain"]
   Outboxes=["feedback"]

class PacketParser(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["packetout"]

class PacketIdent(component):    ### XXXX Code,Docs Needed
   Inboxes=["packets"]
   Outboxes=["rtpdata","rtcpdata"]

class RTPControl(component):    ### XXXX Code,Docs Needed
   inboxes=["in"]
   outboxes=["jittercontrol", "packagefeedback"]

class JitterCompensation(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["feedback"]

class RTCPHandler(component):   ### XXXX Code,Docs Needed
   """Contains logical subcomponents:
      LocalFeedbackHandler, ClientFeedbackHandler, 
      ConnectionMonitoring, ConnectionControl
   """
   Inboxes=["rtpfeedback", "packetin"] 
   Outboxes=["playerfeedback"]
   Usescomponents=[LocalFeedbackHandler, ClientFeedbackHandler, ConnectionMonitoring, ConnectionControl]

   def __init__(self):
      #
      # Inbound passthrough linkages
      #
      self.link((self,"rtpfeedback"),(LocalFeedbackHandler,"in"), passthrough=IN)
      self.link((self,"packetin"), (ClientFeedbackHandler,"in"), passthrough=IN)
      #
      # Outbound passthrough linkages
      #
      self.link((ConnectionControl,"streamfeedback"), (self,"playerfeedback"), passthrough=OUT)
      #
      # Other internal linkages
      #
      self.link((LocalFeedbackHandler,"aggregatedfeedback"), (ConnectionMonitoring,"internalfeedback"))
      self.link((ClientFeedbackHandler,"aggregatefeedback"), (ConnectionMonitoring,"externalfeedback"))
      self.link((ConnectionMonitoring,"statuschange"), (ConnectionControl,"streamstatus"))
      self.link((ConnectionControl,"watchcontrol"), (ConnectionMonitoring,"control"))

class LocalFeedbackHandler(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["aggregatedfeedback"]

class ClientFeedbackHandler(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["aggregatefeedback"]

class ConnectionMonitoring(component):    ### XXXX Code,Docs Needed
   Inboxes=["internalfeedback", "externalfeedback", "control"]
   Outboxes=["statuschange"]

class ConnectionControl(component):    ### XXXX Code,Docs Needed
   Inboxes=["streamstatus"]
   Outboxes=["watchcontrol", "streamfeedback"]

class DataPump(component):   ### XXXX Code,Docs Needed
   """Contains logical subcomponents:
      DataPassthrough, BlockAcceptance, ConstantBitRateSender, 
      CommandHandler, ConnCreate
   """
   Inboxes=["Control", "Send", "Source", "ConnInfo"] 
   Outboxes=["Sink", "Recv", "GenConn", "BackChannel"]
   Usescomponents=[DataPassthrough, BlockAcceptance, ConstantBitRateSender, 
                  CommandHandler, ConnCreate]

   def __init__(self):
      #
      # Inbound passthrough linkages
      #
      self.link((self,"Control"), (CommandHandler,"in"), passthrough=IN)
      self.link((self,"Send"), (BlockAcceptance,"in"), passthrough=IN)
      self.link((self,"Source"), (DataPassthrough,"in"), passthrough=IN)
      self.link((self,"ConnInfo"), (ConnCreate,"number"), passthrough=IN)
      #
      # Outbound passthrough linkages
      #
      self.link((DataPassthrough,"out"), (self,"Recv"), passthrough=OUT)
      self.link((ConstantBitRateSender,"dataout"), (self,"Sink"), passthrough=OUT)
      self.link((ConstantBitRateSender,"feedbackout"), (self,"BackChannel"), passthrough=OUT)
      self.link((ConnCreate,"newconn"), (self,"GenConn"), passthrough=OUT)
      self.link((ConnCreate,"conninfo"), (self,"BackChannel"), passthrough=OUT)
      #
      # Other internal linkages
      #
      self.link((BlockAcceptance,"out"), (ConstantBitRateSender,"datain"))
      self.link((CommandHandler,"bitratecontrol"), (ConstantBitRateSender,"control"))
      self.link((CommandHandler,"makeconn"), (ConnCreate,"control"))


class DataPassthrough(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["out"]

class BlockAcceptance(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["out"]

class ConstantBitRateSender(component):    ### XXXX Code,Docs Needed
   Inboxes=["datain", "control"]
   Outboxes=["dataout", "feedbackout"]

class CommandHandler(component):    ### XXXX Code,Docs Needed
   Inboxes=["in"]
   Outboxes=["bitratecontrol", "makeconn"]

class ConnCreate(component):    ### XXXX Code,Docs Needed
   Inboxes=["number", "control"]
   Outboxes=["newconn", "conninfo"]

class RTSPNetworkPlayerControl(component): ### XXXX Code,Docs Needed
   """Contains logical subcomponents:
      NetPlayerController, RTSPHandler, SDPFormatter
   """
   Inboxes=["Recv", "ConnInfo", "RawRTSP", "PlayerInfo"] 
   Outboxes=["GetPlayer", "Control", "Interleave", "RTSPOut", "ConnControl"]
   Usescomponents=[NetPlayerController, RTSPHandler, SDPFormatter]

   def __init__(self):
      #
      # Inbound passthrough linkages
      #
      self.link((self,"Recv"), (NetPlayerController,"metadata"), passthrough=IN)
      self.link((self,"ConnInfo"), (RTSPHandler,"socketdetails"), passthrough=IN)
      self.link((self,"RawRTSP"), (RTSPHandler,"rawdata"), passthrough=IN)
      self.link((self,"PlayerInfo"), (NetPlayerController,"playerinfo"), passthrough=IN)
      #
      # Outbound passthrough linkages
      #
      self.link((NetPlayerController,"StreamCreate"), (self,"GetPlayer"), passthrough=OUT)
      self.link((NetPlayerController,"StreamControl"), (self,"Control"), passthrough=OUT)
      self.link((NetPlayerController,"ConnectionHandoff"), (self,"Interleave"), passthrough=OUT)
      self.link((RTSPHandler,"socketoobcontrol"), (self,"ConnControl"), passthrough=OUT)
      self.link((RTSPHandler,"rtspresponses"), (self,"RTSPOut"), passthrough=OUT)
      #
      # Other internal linkages
      #
      self.link((NetPlayerController,"ConnectionInformation"), (RTSPHandler,"streaminfo"))
      self.link((RTSPHandler,"connectioninfo"), (NetPlayerController,"clientinfo"))
      self.link((RTSPHandler,"systemcontrol"), (NetPlayerController,"systemcontrol"))
      self.link((RTSPHandler,"programmeinfo"), (SDPFormatter,"programmedata"))
      self.link((SDPFormatter,"formattedSDP"), (RTSPHandler,"sdpin"))


class NetPlayerController(component): pass ### XXXX Detail, Interface, Code, Docs needed

class RTSPHandler(component): pass        ### XXXX Detail, Interface, Code, Docs needed
class SDPFormatter(component): pass       ### XXXX Detail, Interface, Code, Docs needed

class InternetConnectionAbstractionLayer(component): pass ### XXXX Detail, Interface, Code, Docs needed
class InetConnFactory(component): pass ### XXXX Detail, Interface, Code, Docs needed
class InetConn(component): pass ### XXXX Detail, Interface, Code, Docs needed

class NetPlayerFactory(component): pass ### XXXX Detail, Interface, Code, Docs needed
