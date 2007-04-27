#!/usr/bin/env python
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
=================================================
Support functions for parsing DVB data structures
=================================================

A collection of functions for parsing 'descriptor' elements of information
tables in DVB data streams. Descriptors contain data such as channel names,
tuning information for other multiplexes, and information about the audio/video
streams making up a channel.



Example Usage
-------------

A simple loop to parse a set of descriptors stored consecutively in a string::
    i=0
    while i < len(setOfDescriptors):
        parsed, i = parseDescriptor(i, setOfDescriptors)
        (tag, data) = parsed
        print "Descriptor found with tag",tag
        for (key,value) in data.items():
            print key, "=", value
            
            

Parsing Descriptors
-------------------

Call the parseDescriptor() function, passing it the string containing the
descriptor and the index of the beginning of the descriptor within the string.

parseDescriptor() will return the parsed descriptor::
    (tag, data)
        - tag = the ID of this descriptor type
        - data = dictionary containing the parsed descriptor data:
            { type : WhatKindOfDescriptor,
              key  : value,
              key2 : value2,
              ...
            }

All parsed descriptor data will contain the 'type' key. The remaining key,value
pairs are specific to the type of descriptor.

parseDescriptor() uses helper functions to parse each particular descriptor. See
their documentation to see what descriptors are currently supported and what
data to expect in the dictionary.



How does it Work?
-----------------

parseDescriptor() uses helper functions to parse each particular descriptor.
parseDescriptor() extracts the 'tag' defining the descriptor type, and the
length of the descriptor. A mapping table maps from tags to parser functions.

Each parser function is of the form::
    parse(data,i,length,end) -> dict(parsed descriptor elements)

'data' is a string containing the descriptor. 'i' is the index into the string
of the start of the descriptor. 'length' is the length of the descriptor payload
and end' is the index of the first point after the descriptor.



References
----------

For the full description of the descriptors available see the following MPEG and
DVB standards documents:

- ISO/IEC 13818-1 (aka "MPEG: Systems")
  "GENERIC CODING OF MOVING PICTURES AND ASSOCIATED AUDIO: SYSTEMS" 
  ISO / Motion Picture Experts Grou7p
  
- ETSI EN 300 468 
  "Digital Video Broadcasting (DVB); Specification for Service Information (SI)
  in DVB systems"
  ETSI / EBU (DVB group)

- "Digital Terrestrial Television: Requirements for Interoperability" Issue 4.0+
  (aka "The D book")
  UK Digital Television Group



Mappings, Tables, Values
========================
Various mappings, tables, values etc. used by the DVB standard.


Service types
-------------
Types of services (channel) that can be found in a DVB multiplex::

    "digital television service",
    "digital radio sound service",
    "Teletext service",
    "NVOD reference service",
    "NVOD time-shifted service",
    "mosaic service",
    "PAL coded signal",
    "SECAM coded signal",
    "D/D2-MAC",
    "FM Radio",
    "NTSC coded signal",
    "data broadcast service",
    "RCS Map",
    "RCS FLS",
    "DVB MHP service",




Stream Component Mappings
-------------------------
Mappings from (stream_component, component_type) values to their actual
meanings. Used in 'component' descriptors::

    (0x01, 0x01) : ("video",                 "4:3 aspect ratio, 25 Hz"),
    (0x01, 0x02) : ("video",                 "16:9 aspect ratio with pan vectors, 25 Hz"),
    (0x01, 0x03) : ("video",                 "16:9 aspect ratio without pan vectors, 25 Hz"),
    (0x01, 0x04) : ("video",                 "> 16:9 aspect ratio, 25 Hz"),
    (0x01, 0x05) : ("video",                 "4:3 aspect ratio, 30 Hz"),
    (0x01, 0x06) : ("video",                 "16:9 aspect ratio with pan vectors, 30 Hz"),
    (0x01, 0x07) : ("video",                 "16:9 aspect ratio without pan vectors, 30 Hz"),
    (0x01, 0x05) : ("video",                 "> 16:9 aspect ratio, 30 Hz"),
    (0x01, 0x09) : ("high definition video", "4:3 aspect ratio, 25 Hz"),
    (0x01, 0x0A) : ("high definition video", "16:9 aspect ratio with pan vectors, 25 Hz"),
    (0x01, 0x0B) : ("high definition video", "16:9 aspect ratio without pan vectors, 25 Hz"),
    (0x01, 0x0C) : ("high definition video", "> 16:9 aspect ratio, 25 Hz"),
    (0x01, 0x0D) : ("high definition video", "4:3 aspect ratio, 30 Hz"),
    (0x01, 0x0E) : ("high definition video", "16:9 aspect ratio with pan vectors, 30 Hz"),
    (0x01, 0x0F) : ("high definition video", "16:9 aspect ratio without pan vec., 30 Hz"),
    (0x01, 0x10) : ("high definition video", "> 16:9 aspect ratio, 30 Hz"),
    (0x02, 0x01) : ("audio",                 "single mono channel"),
    (0x02, 0x02) : ("audio",                 "dual mono channel"),
    (0x02, 0x03) : ("audio",                 "stereo (2 channel)"),
    (0x02, 0x04) : ("audio",                 "multi-lingual, multi-channel"),
    (0x02, 0x05) : ("audio",                 "surround sound"),
    (0x02, 0x40) : ("audio description for the visually impaired", ""),
    (0x02, 0x41) : ("audio for the hard of hearing",               ""),
    (0x03, 0x01) : ("EBU Teletext subtitles",  ""),
    (0x03, 0x02) : ("associated EBU Teletext", ""),
    (0x03, 0x03) : ("VBI data",                ""),
    (0x03, 0x10) : ("DVB subtitles (normal)", "with no monitor aspect ratio criticality"),
    (0x03, 0x11) : ("DVB subtitles (normal)", "for display on 4:3 aspect ratio monitor"),


Private Data Specifiers
-----------------------
Specifiers defining various types of private data payload:
    
    0x00000001 : "SES",
    0x00000002 : "BSkyB 1",
    0x00000003 : "BSkyB 2",
    0x00000004 : "BSkyB 3",
    0x000000BE : "BetaTechnik",
    0x00006000 : "News Datacom",
    0x00006001 : "NDC 1",
    0x00006002 : "NDC 2",
    0x00006003 : "NDC 3",
    0x00006004 : "NDC 4",
    0x00006005 : "NDC 5",
    0x00006006 : "NDC 6",
    0x00362275 : "Irdeto",
    0x004E544C : "NTL",
    0x00532D41 : "Scientific Atlanta",
    0x44414E59 : "News Datacom (IL) 1",
    0x46524549 : "News Datacom (IL) 1",
    0x53415053 : "Scientific Atlanta",

"""

# parsing routines for DVB PSI table descriptors
import dvb3.frontend as dvb3f

from DateTime import unBCD, parseMJD

def parseDescriptor(i,data):
    """\
    parseDescriptor(i, data) -> (tag, parsedData), new_i
    
    Parses the desciptor in the string 'data', that starts at index 'i'.
    Returns the descriptor's tag; the parsed descriptor contents as a dict
    and the index of the first byte after the end of the descriptor.
    """
    
    # just a simple extract the tag and body of the descriptor
    tag    = ord(data[i])
    length = ord(data[i+1])
    end    = i+2+length

    parser = __descriptor_parsers.get(tag,parser_Null_Descriptor)

    output = parser(data,i,length,end)

    return (tag,output), end


# ==============================================================================
# now parsers for all descriptor types
# ==============================================================================

# template for a null parser - used when we don't recognise/support the
# descriptor type we find.

def parser_Null_Descriptor(data,i,length,end):
    """\
    parser_NullDescriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "UNKNOWN", "contents" : unparsed_descriptor_contents }
    """
    return { "type" : "UNKNOWN", "contents" : data[i+2:end] }


# ------------------------------------------------------------------------------
# ISO 13818-1 defined descriptors
# ------------------------------------------------------------------------------

def parser_video_stream_Descriptor(data,i,length,end):
    """\
    parser_video_stream_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "video_stream", "contents" : unparsed_descriptor_contents }
       
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "video_stream", "contents" : data[i+2:end] }


def parser_audio_stream_Descriptor(data,i,length,end):
    """\
    parser_audio_stream_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "audio_stream", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "audio_stream", "contents" : data[i+2:end] }


def parser_hierarchy_Descriptor(data,i,length,end):
    """\
    parser_hierarchy_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "hierarchy", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "hierarchy", "contents" : data[i+2:end] }


def parser_registration_Descriptor(data,i,length,end):
    """\
    parser_registration_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "registration", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "registration", "contents" : data[i+2:end] }


def parser_data_stream_alignment_Descriptor(data,i,length,end):
    """\
    parser_data_stream_alignment_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "data_stream_alignment", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "data_stream_alignment", "contents" : data[i+2:end] }


def parser_target_background_grid_Descriptor(data,i,length,end):
    """\
    parser_background_grid_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "background_grid", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "background_grid", "contents" : data[i+2:end] }


def parser_video_window_Descriptor(data,i,length,end):
    """\
    parser_video_window_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "video_window", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "video_window", "contents" : data[i+2:end] }


def parser_CA_Descriptor(data,i,length,end):
    """\
    parser_CA_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor that describes the conditional access mechanism being
    used to encrypt a given stream (identified by its PID).
    
    The dict returned is:
       { "type"    : "CA",
         "CA_system_id" : 16 bit unsigned integer identifying for the type of CA system,
         "pid"          : the integer identifier of the stream,
         "private_data" : string containing data specific to the CA system
       }
    
    (Defined in ISO 13818-1 specification)
    """
    d = { "type"         : "CA",
          "CA_system_id" : (ord(data[i+2])<<8) + ord(data[i+3]),
          "pid"          : ((ord(data[i+4])<<8) + ord(data[i+5])) & 0x1fff,
          "private_data" : data[i+6:end]
        }
    return d

def parser_ISO_639_Descriptor(data,i,length,end):
    """\
    parser_ISO_639_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor that describes the one or more language(s) used, and
    their suitability for those with hearing impairments, in an audio stream.
    
    The language types come from the ISO 639-2 standard. There may bemore than
    one language and impairment suitability entry.
    
    The dict returned is:
       { "type"    : "ISO_639",
         "entries" :
             list( { "language_code" : ISO 639 defined 3-letter language code
                     "audio_type"    : "" or "CLEAN" or "HEARING IMPAIRED" or "VISUAL IMPAIRED COMMENTARY"
                 } )
       }
    
    (Defined in ISO 13818-1 specification)
    """
    parts = []
    j=i+2
    while j<end:
        parts.append( { "language_code" : data[j:j+3],
                        "audio_type"    : _iso639_audiotypes.get(ord(data[j+3]), ord(data[j+3]))
                      } )
        j += 4
    d = { "type" : "ISO_639",
          "entries" : parts,
        }
    return d

def parser_system_clock_Descriptor(data,i,length,end):
    """\
    parser_system_clock_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "system_clock", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "system_clock", "contents" : data[i+2:end] }


def parser_multiplex_buffer_utilisation_Descriptor(data,i,length,end):
    """\
    parser_multiplex_buffer_utilisation_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "multiplex_buffer_utilisation", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "multiplex_buffer_utilisation", "contents" : data[i+2:end] }


def parser_copyright_Descriptor(data,i,length,end):
    """\
    parser_copyright_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "copyright", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "copyright", "contents" : data[i+2:end] }


def parser_maximum_bitrate_Descriptor(data,i,length,end):
    """\
    parser_maximum_bitrate_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "maximum_bitrate", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "maximum_bitrate", "contents" : data[i+2:end] }


def parser_private_data_indicator_Descriptor(data,i,length,end):
    """\
    parser_private_data_indicator_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "private_data_indicator", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "private_data_indicator", "contents" : data[i+2:end] }


def parser_smoothing_buffer_Descriptor(data,i,length,end):
    """\
    parser_smoothing_buffer_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "smoothing_buffer", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "smoothing_buffer", "contents" : data[i+2:end] }


def parser_STD_Descriptor(data,i,length,end):
    """\
    parser_STD_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "STD", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "STD", "contents" : data[i+2:end] }


def parser_IBP_Descriptor(data,i,length,end):
    """\
    parser_IBP_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "IBP", "contents" : unparsed_descriptor_contents }
    
    (Defined in ISO 13818-1 specification)
    """
    return { "type" : "IBP", "contents" : data[i+2:end] }



# ------------------------------------------------------------------------------
# ETSI EN 300 468 defined descriptors
# ------------------------------------------------------------------------------

def parser_network_name_Descriptor(data,i,length,end):
    """\
    parser_network_name_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor containing the name of the 'network' of which the
    multiplex is a part. In the United Kingdom for the Freeview Terrestrial
    Service, this is usually the name of the transmitter, eg. "Crystal Palace".
    
    The dict returned is:
       { "type"    : "network_name",
         "network_name" : string name of the network,
       }
    
    (Defined in ETSI EN 300 468 specification)
    """
    d = { "type" : "network_name",
          "network_name" : data[i+2:end]
        }
    return d

def parser_service_list_Descriptor(data,i,length,end):
    """\
    parser_service_list_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor containing the list of services (channels) available in
    a given multiplex. Each service is listed by type and SID (service id).
    
    The dict returned is:
       { "type"     : "service_list",
         "services" :
             list( { "service_id"   : identifier value for this service
                     "service_type" : the type of service (see table below)
                 } )
       }
       
    Example service types include:
    
    - "digital television service",
    - "digital radio sound service",
    - "data broadcast service",

    See "Service types" for the full list of service type values.
    
    (Defined in ETSI EN 300 468 specification)
    """
    d = { "type" : "service_list",
          "services" : []
        }
    i=i+2
    while i<end:
        sid = (ord(data[i])<<8) + ord(data[i+1])
        sit = _service_types.get(ord(data[i+2]), ord(data[i+2])),
        d['services'].append( {"service_id":sid, "service_type":sit } )
        i=i+3
    return d

def parser_stuffing_Descriptor(data,i,length,end):
    """\
    parser_stuffing_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor serves as padding. It carries no data.
       { "type": "stuffing" }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "stuffing" }


def parser_satellite_delivery_system_Descriptor(data,i,length,end):
    """\
    parser_satellite_delivery_system_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "satellite_delivery_system", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "satellite_delivery_system", "contents" : data[i+2:end] }


def parser_cable_delivery_system_Descriptor(data,i,length,end):
    """\
    parser_cable_delivery_system_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "cable_delivery_system", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "satellite_delivery_system", "contents" : data[i+2:end] }


def parser_VBI_data_Descriptor(data,i,length,end):
    """\
    parser_VBI_data_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "VBI_data", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "VBI_data", "contents" : data[i+2:end] }


def parser_VBI_teletext_Descriptor(data,i,length,end):
    """\
    parser_VBI_teletext_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "VBI_teletext", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "VBI_teletext", "contents" : data[i+2:end] }


def parser_bouquet_name_Descriptor(data,i,length,end):
    """\
    parser_bouquet_name_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "bouquet_name", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "bouquet_name", "contents" : data[i+2:end] }


def parser_service_Descriptor(data,i,length,end):
    """\
    parser_service_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor containing the name, provider and type of a service
    (channel).
    
    The dict returned is:
       { "type"                  : "service",
         "service_type"          : the type of service (see table below)
         "service_name"          : name of this channel (eg. "BBC ONE")
         "service_provider_name" : string name of who is providing this channel
       }
       
    Example service types include:
    
    - "digital television service",
    - "digital radio sound service",
    - "data broadcast service",

    See "Service types" for the full list of service type values.
    
    (Defined in ETSI EN 300 468 specification)
    """
    d = { "type" : "service",
          "service_type" : _service_types.get(ord(data[i+2]), ord(data[i+2])),
        }
    length = ord(data[i+3])
    j = i+4+length
    d['service_provider_name'] = data[i+4:j]
    length = ord(data[j])
    d['service_name'] = data[j+1:j+1+length]
    return d


def parser_country_availability_Descriptor(data,i,length,end):
    """\
    parser_country_availability_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "country_availability", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "country_availability", "contents" : data[i+2:end] }


def parser_linkage_Descriptor(data,i,length,end):
    """\
    parser_linkage_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "linkage", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "linkage", "contents" : data[i+2:end] }


def parser_NVOD_reference_Descriptor(data,i,length,end):
    """\
    parser_NVOD_reference_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "NVOD_reference", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "NVOD_reference", "contents" : data[i+2:end] }


def parser_time_shifted_service_Descriptor(data,i,length,end):
    """\
    parser_time_shifted_service_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "time_shifted_service", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "time_shifted_service", "contents" : data[i+2:end] }


def parser_short_event_Descriptor(data,i,length,end):
    """\
    parser_short_event_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor describing a short event - usually a programme. It gives
    a name, longer description, and the language it is in. This is usually part
    of schedule or now & next information.
    
    The dict returned is:
       { "type"          : "short_event",
         "language_code" : The language of this programme (ISO 639-2 3 letter language code)
         "name"          : String name of the event (programme)
         "text"          : Up to 255 character string description
       }
    
    (Defined in ETSI EN 300 468 specification)
    """
    d = { "type"          : "short_event",
          "language_code" : data[i+2:i+5],
        }
    name_length = ord(data[i+5])
    i = i+6
    d['name'] = data[i:i+name_length]
    text_length = ord(data[i+name_length])
    i = i+name_length+1
    d['text'] = data[i:i+text_length]
    return d

def parser_extended_event_Descriptor(data,i,length,end):
    """\
    parser_extended_event_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "extended_event", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "extended_event", "contents" : data[i+2:end] }


def parser_time_shifted_event_Descriptor(data,i,length,end):
    """\
    parser_time_shifted_event_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "time_shifted_event", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "time_shifted_event", "contents" : data[i+2:end] }


def parser_component_Descriptor(data,i,length,end):
    """\
    parser_component_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor describing technical details of an audio or visual
    component of a service (channel) such as the aspect ratio of video, or the
    number and configuration of audio channels.
    
    The dict returned is:
       { "type"           : "component",
         "component_tag"  : uniquely identifies this component within the service (channel) - maps to stream identifier descriptors (see parser_stream_identifier_Descriptor)
         "stream_content" : number identifying whether the stream is audio, video, subtitles, etc
         "component_type" : number identifying technical details of that stream type
         "content,type"   : (content,type) textual equivalents of stream_contentand component_type (see below)
         "language_code"  : The language of this component (ISO 639-2 3 letter language code)
         "text"           : A textual description of this component
       }
       
    Example component (content,type) descriptions include:
    
    - ("video",                  "4:3 aspec ratio, 25 Hz")
    - ("high definition video",  "16:9 aspect ratio with pan vectors, 25 Hz")
    - ("audio",                  "stereo (2 channel)")
    - ("DVB subtitles (normal)", "with no monitor aspect ratio criticality")
        
    See "Stream Component Mappings" for a full list and the numeric stream_component
    and component_type values that map to them.
    
    (Defined in ETSI EN 300 468 specification)
    """
    e = [ord(data[i+2]), ord(data[i+3]), ord(data[i+4])]
    e[0]=e[0] & 0x0f
    sctype = _stream_component_mappings.get((e[0],e[1]), (e[0],e[1]))
    d = { "type" : "component",
          "stream_content" : e[0],
          "component_type" : e[1],
          "component_tag"  : e[2],
          "content,type"   : sctype,
          "language_code"  : data[i+5:i+8],
          "text"           : data[i+8:end],
        }
    return d
    
    
def parser_mosaic_Descriptor(data,i,length,end):
    """\
    parser_mosaic_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "mosaic", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "mosaic", "contents" : data[i+2:end] }


def parser_stream_identifier_Descriptor(data,i,length,end):
    """\
    parser_stream_identifier_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor identifying a component of a stream in a service
    (channel). A set of these forms a list of the 'tag's that identifies the
    set of components making up a stream.
    
    Used in the Programme Map Table (PMT) 
    
    The dict returned is:
       { "type"          : "stream_identifier",
         "component_tag" : tag uniquely identifying this component within the service - maps to component descriptors found in schedule and now&next data (EIT table)
       }
    
    (Defined in ETSI EN 300 468 specification)
    """
    d = { "type"         : "stream_identifier",
          "component_tag" : ord(data[i+2]),
        }
    return d

def parser_CA_identifier_Descriptor(data,i,length,end):
    """\
    parser_CA_identifier_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "CA_identifier", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "CA_identifier", "contents" : data[i+2:end] }


def parser_content_Descriptor(data,i,length,end):
    """\
    parser_content_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "content", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "content", "contents" : data[i+2:end] }


def parser_parental_rating_Descriptor(data,i,length,end):
    """\
    parser_parental_rating_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "parental_rating", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "parental_rating", "contents" : data[i+2:end] }


def parser_teletext_Descriptor(data,i,length,end):
    """\
    parser_teletext_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "teletext", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "teletext", "contents" : data[i+2:end] }


def parser_telephone_Descriptor(data,i,length,end):
    """\
    parser_telephone_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "telephone", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "telephone", "contents" : data[i+2:end] }


def parser_local_time_offset_Descriptor(data,i,length,end):
    """\
    parser_local_time_offset_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type"        : "local_time_offset",
         "country"     : 3 character ISO 3166 / ETSI ETR 162,
         "region"      : region within country, or 0
         "offset"      : (hours, minutes) of time offset (positive or negative)
         "changesWhen" : (y,m,d,h,m,s) when the time offset will next change
         "nextOffset"  : (hours, minutes) of next time offset (positive or negative)
       }
    
    (Defined in ETSI EN 300 468 specification)
    """
    e = [ord(data[i+x]) for x in range(5,15)]
    
    offset     = ( unBCD(e[1]), unBCD(e[2]) )
    changeDateTime = list( parseMJD((e[3]<<8) + e[4]) )
    changeDateTime.extend( [unBCD(e[5]), unBCD(e[6]), unBCD(e[7])] )
    nextOffset = ( unBCD(e[8]), unBCD(e[9]) )
    
    negative = e[0] & 1
    if negative:
        offset     = ( -offset[0],     -offset[1]     )
        nextOffset = ( -nextOffset[0], -nextOffset[1] )

    return { "type"         : "local_time_offset",
             "country"      : data[i+2:i+5],
             "region"       : e[0] >> 2,
             "offset"       : offset,
             "timeOfChange" : changeDateTime,
             "nextOffset"   : nextOffset,
           }


def parser_subtitling_Descriptor(data,i,length,end):
    """\
    parser_subtitling_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor describing a subtitling service. It describes the
    language of the subtitles, and the type of subtitle data (DVB supports
    multiple types).
    
    The dict returned is:
       { "type"                : "subtitling",
         "language_code"       : language it is in (3 letter ISO 639-2 language code)
         "subtitling_type"     : (content,type) textual equivalents of stream_contentand component_type (see below)
         "composition_page_id" : signalling for DVB subtitles (specific to subtitling implementation)
         "ancilliary_page_id"  : signalling for DVB subtitles (specific to subtitling implementation)
       }
    
    See all 0x03 (subtitling) sections of "Stream Component Mappings"
    
    (Defined in ETSI EN 300 468 specification)
    """
    parts = []
    j=i+2
    while j<end:
        stype = _stream_component_mappings.get((0x03,ord(data[j+3])), (ord(data[j+3]),""))
        parts.append( { "language_code"       : data[j:j+3],
                        "subtitling_type"     : stype,
                        "composition_page_id" : (ord(data[j+4])<<8) + ord(data[j+5]),
                        "ancilliary_page_id"  : (ord(data[j+6])<<8) + ord(data[j+7]),
                      } )
        j += 8
    d = { "type" : "subtitling",
          "entries" : parts,
        }
    return d

def parser_terrestrial_delivery_system_Descriptor(data,i,length,end):
    """\
    parser_terrestrial_delivery_system_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor containing the parameteres needed to tune to a DVB
    Digital Terrestrial Television (DVB-T) multiplex. Parameters are all encoded
    using the constants defined in the dvb3 python bindings library - thereby
    making easy to directly pass them to the frontend tuning function calls.
    
    Used in the Network Information Table (NIT)
    
    The dict returned is:
       { "type"          : "terrestrial_delivery_system",
         "params"        : Tuning parameters (see below)
         "other_frequencies" : True if one or more other frequencies are being used
      }
      
    Tuning parameters are a dict:
      {
         "frequency"     : Frequency in Hz,
         "bandwidth"     : dvb3.frontend.BANDWIDTH_?_MHZ where ? is 6, 7 or 8
         "constellation" : dvb3.frontend.QPSK, QAM_16 or QAM_64
         "hierarchy_information" : dvb3.frontend.HIERARCHY_? where ? is NONE, 1, 2 or 4
         "code_rate_HP" : dvb3.frontend.FEC_X_Y where X/Y = 1/2, 2/3, 3/4, 5/6, 7/8
         "code_rate_LP" : dvb3.frontend.FEC_X_Y where X/Y = 1/2, 2/3, 3/4, 5/6, 7/8
         "guard_interval" : dvb3.frontend.GUARD_INTERVAL_1_? where ? is 32, 16, 8 or 4
         "transmission_mode" : dvb3.frontend.TRANSMISSION_MODE_?K where ? is 2 or 8
         "inversion"         : dvb3.frontend.INVERSION_AUTO
       }
    
    (Defined in ETSI EN 300 468 specification)
    """
    d = { "type" : "terrestrial_delivery_system",
        }
    e = [ord(data[x]) for x in range(i+2,i+9)]
    params = {}
    params['frequency'] = 10 * ((e[0]<<24) + (e[1]<<16) + (e[2]<<8) + e[3])
    v = e[4] >> 5
    params['bandwidth'] = _dvbt_bandwidths.get(v,v)
    v = e[5] >> 6
    params['constellation'] = _dvbt_constellations.get(v,v)
    v = (e[5] >> 3) & 0x07
    params['hierarchy_information'] = _dvbt_hierarchy.get(v,v)
    v = e[5] & 0x07
    params['code_rate_HP'] = _dvbt_code_rate_hp.get(v,v)
    v = e[6] >> 5
    params['code_rate_LP'] = _dvbt_code_rate_lp.get(v,v)
    v = (e[6] >> 3) & 0x03
    params['guard_interval'] = _dvbt_guard_interval.get(v,v)
    v = (e[6] >> 1) & 0x03
    params['transmission_mode'] = _dvbt_transmission_mode.get(v,v)
    
    # other desirable params
    params['inversion'] = dvb3f.INVERSION_AUTO
    
    d['params'] = params
    d['other_frequencies'] = e[6] & 0x01
    
    return d

def parser_multilingual_network_name_Descriptor(data,i,length,end):
    """\
    parser_multilingual_network_name_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "multilingual_network_name", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "multilingual_network_name", "contents" : data[i+2:end] }


def parser_multilingual_bouquet_name_Descriptor(data,i,length,end):
    """\
    parser_multilingual_bouquet_name_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "multilingual_bouquet_name", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "multilingual_bouquet_name", "contents" : data[i+2:end] }



def parser_multilingual_service_name_Descriptor(data,i,length,end):
    """\
    parser_multilingual_service_name_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "multilingual_service_name", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "multilingual_service_name", "contents" : data[i+2:end] }

def parser_multilingual_component_Descriptor(data,i,length,end):
    """\
    parser_multilingual_component_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "multilingual_component", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "multilingual_component", "contents" : data[i+2:end] }

def parser_private_data_specifier_Descriptor(data,i,length,end):
    """\
    parser_private_data_specifier_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor specifying the type of some 'private data' - that is
    data outside of the core specifications.
    
    The dict returned is:
       { "type"          : "private_data_specifier",
         "private_data_specifier" : String description, or numeric type if unrecognised.
       }
    
    See "Private Data Specifiers".
    
    (Defined in ETSI EN 300 468 specification)
    """
    n = (ord(data[i+2])<<24) + (ord(data[i+3])<<16) + (ord(data[i+4])<<8) + ord(data[i+5])
    d = { "type" : "private_data_specifier",
          "private_data_specifier" : _private_data_specifiers.get(n,n),
        }
    return d
    

def parser_service_move_Descriptor(data,i,length,end):
    """\
    parser_service_move_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "service_move", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "service_move", "contents" : data[i+2:end] }

def parser_short_smoothing_buffer_Descriptor(data,i,length,end):
    """\
    parser_short_smoothing_buffer_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "short_smoothing_buffer", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "short_smoothing_buffer", "contents" : data[i+2:end] }

def parser_frequency_list_Descriptor(data,i,length,end):
    """\
    parser_frequency_list_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor containing a list of alternative frequences on which
    the multiplex may be carried.
    
    The dict returned is:
       { "type"       : "frequency_list",
         "frequences" : list(frequency in Hz)
       }
    
    See "Private Data Specifiers".
    
    (Defined in ETSI EN 300 468 specification)
    """
    d = { "type" : "frequency_list",
          "frequencies" : [],
        }
    coding_type = ord(data[i+2]) & 0x03
    i=i+3
    while i<end:
        e = [ord(data[x]) for x in range(i,i+4)]
        freq = None
        if   coding_type==1:  # satellite
            freq = 10000000000*unBCD(e[0]) + \
                     100000000*unBCD(e[1]) + \
                       1000000*unBCD(e[2]) + \
                         10000*unBCD(e[3])
        elif coding_type==2:  # cable
            freq = 100000000*unBCD(e[0]) + \
                     1000000*unBCD(e[1]) + \
                       10000*unBCD(e[2]) + \
                         100*unBCD(e[3])
        elif coding_type==3:  # terrestrial
            freq = 10 * ((e[0]<<24) + (e[1]<<16) + (e[2]<<8) + e[3])
        else:
            pass        # just ignore the value cos we don't know what to do with it
        if freq:
            d['frequencies'].append(freq)
        i=i+4
    return d


def parser_partial_transport_stream_Descriptor(data,i,length,end):
    """\
    parser_partial_transport_stream_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "partial_transport_stream", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "partial_transport_stream", "contents" : data[i+2:end] }

def parser_data_broadcast_Descriptor(data,i,length,end):
    """\
    parser_data_broadcast_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "data_broadcast", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "data_broadcast", "contents" : data[i+2:end] }

def parser_CA_system_Descriptor(data,i,length,end):
    """\
    parser_CA_system_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "CA_system", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "CA_system", "contents" : data[i+2:end] }

def parser_data_broadcast_id_Descriptor(data,i,length,end):
    """\
    parser_data_broadcast_id_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor containing a list of alternative frequences on which
    the multiplex may be carried.
    
    The dict returned is:
       { "type"      : "data_broadcast_id",
         "id"        : numeric identifier for the way in which the data is being broadcast
         "selectors" : string data specific to the data broadcast type
       }
    
    The id specifies the kind of data broadcast. For example, 0x106 has been 
    registered by TDN for use in the United Kingdom Digital Terrestrial network
    for 'interactive' applications.
    
    The selectors are data specific to the particular kind of data broadcast,
    generally used to specify an 'interactive app' to be loaded when the channel
    or data broadcast is tuned to by the user.
    
    (Defined in ETSI EN 300 468 specification and "The D book")
    """
    d = { "type"      : "data_broadcast_id",
          "id"        : (ord(data[i+2])<<8) + ord(data[i+3]),
          "selectors" : data[i+4:end],
        }
    return d


def parser_transport_stream_Descriptor(data,i,length,end):
    """\
    parser_transport_stream_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "transport_stream", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "transport_stream", "contents" : data[i+2:end] }

def parser_DSNG_Descriptor(data,i,length,end):
    """\
    parser_DSNG_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "DSNG", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "DSNG", "contents" : data[i+2:end] }

def parser_PDC_Descriptor(data,i,length,end):
    """\
    parser_PDC_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "PDC", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "PDC", "contents" : data[i+2:end] }

def parser_AC3_Descriptor(data,i,length,end):
    """\
    parser_AC3_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "AC3", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "AC3", "contents" : data[i+2:end] }

def parser_ancillary_data_Descriptor(data,i,length,end):
    """\
    parser_ancillary_data_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "ancillary_data", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "ancillary_data", "contents" : data[i+2:end] }

def parser_cell_list_Descriptor(data,i,length,end):
    """\
    parser_cell_list_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "cell_list", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "cell_list", "contents" : data[i+2:end] }

def parser_cell_frequency_link_Descriptor(data,i,length,end):
    """\
    parser_cell_frequency_link_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "cell_frequency_link", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "cell_frequency_link", "contents" : data[i+2:end] }

def parser_announcement_support_Descriptor(data,i,length,end):
    """\
    parser_announcement_support_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "announcement_support", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "announcement_support", "contents" : data[i+2:end] }

# ------------------------------------------------------------------------------
# "Digital Terrestrial Television: Requirements for Interoperability V4.0"
# UK Digital Television Group (www.dtg.org.uk) document descriptors
# aka "The D book"
# ------------------------------------------------------------------------------


def parser_logical_channel_Descriptor(data,i,length,end):
    """\
    parser_logical_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    Parses a descriptor that assigns "channel numbers" (for viewers to see) to
    services (channels).
    
    The dict returned is:
       { "type"      : "logical_channel",
         "mappings"  : dict of service_id to channel_number mappings
       }
       
    For example, in the United Kingdom, the channel BBC ONE, when broadcast from
    the Crystal Palace transmitter, has service_id 4164, but for viewers appears
    as logical channel number 1.
    
    (Defined in "The D book")
    """
    d = { "type" : "logical_channel",
        }
    i=i+2
    services = {}
    while i < end:
        service_id = (ord(data[i])<<8) + ord(data[i+1])
        logical_channel_number = ((ord(data[i+2])<<8) + ord(data[i+3])) & 0x03ff
        services[service_id] = logical_channel_number
        i=i+4
    d['mappings'] = services
    return d


def parser_preferred_name_list_Descriptor(data,i,length,end):
    """\
    parser_preferred_name_list_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "preferred_name_list", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "preferred_name_list", "contents" : data[i+2:end] }

def parser_preferred_name_identifier_Descriptor(data,i,length,end):
    """\
    parser_preferred_name_identifier_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "preferred_name_identifier", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "preferred_name_identifier", "contents" : data[i+2:end] }

def parser_service_attribute_Descriptor(data,i,length,end):
    """\
    parser_service_attribute_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "service_attribute", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "service_attribute", "contents" : data[i+2:end] }

def parser_short_service_name_Descriptor(data,i,length,end):
    """\
    parser_short_service_name_Descriptor(data,i,length,end) -> dict(parsed descriptor elements).
    
    This descriptor is not parsed at the moment. The dict returned is:
       { "type": "short_service_name", "contents" : unparsed_descriptor_contents }
    
    (Defined in ETSI EN 300 468 specification)
    """
    return { "type" : "short_service_name", "contents" : data[i+2:end] }


__descriptor_parsers = {
    # ISO 13818-1 defined descriptors
        0x02 : parser_video_stream_Descriptor,
        0x03 : parser_audio_stream_Descriptor,
        0x04 : parser_hierarchy_Descriptor,
        0x05 : parser_registration_Descriptor,
        0x06 : parser_data_stream_alignment_Descriptor,
        0x07 : parser_target_background_grid_Descriptor,
        0x08 : parser_video_window_Descriptor,
        0x09 : parser_CA_Descriptor,
        0x0a : parser_ISO_639_Descriptor,
        0x0b : parser_system_clock_Descriptor,
        0x0c : parser_multiplex_buffer_utilisation_Descriptor,
        0x0d : parser_copyright_Descriptor,
        0x0e : parser_maximum_bitrate_Descriptor,
        0x0f : parser_private_data_indicator_Descriptor,
        0x10 : parser_smoothing_buffer_Descriptor,
        0x11 : parser_STD_Descriptor,
        0x12 : parser_IBP_Descriptor,

    # ETSI EN 300 468 defined descriptors

        0x40 : parser_network_name_Descriptor,
        0x41 : parser_service_list_Descriptor,
        0x42 : parser_stuffing_Descriptor,
        0x43 : parser_satellite_delivery_system_Descriptor,
        0x44 : parser_cable_delivery_system_Descriptor,
        0x45 : parser_VBI_data_Descriptor,
        0x46 : parser_VBI_teletext_Descriptor,
        0x47 : parser_bouquet_name_Descriptor,
        0x48 : parser_service_Descriptor,
        0x49 : parser_country_availability_Descriptor,
        0x4A : parser_linkage_Descriptor,
        0x4B : parser_NVOD_reference_Descriptor,
        0x4C : parser_time_shifted_service_Descriptor,
        0x4D : parser_short_event_Descriptor,
        0x4E : parser_extended_event_Descriptor,
        0x4F : parser_time_shifted_event_Descriptor,
        0x50 : parser_component_Descriptor,
        0x51 : parser_mosaic_Descriptor,
        0x52 : parser_stream_identifier_Descriptor,
        0x53 : parser_CA_identifier_Descriptor,
        0x54 : parser_content_Descriptor,
        0x55 : parser_parental_rating_Descriptor,
        0x56 : parser_teletext_Descriptor,
        0x57 : parser_telephone_Descriptor,
        0x58 : parser_local_time_offset_Descriptor,
        0x59 : parser_subtitling_Descriptor,
        0x5A : parser_terrestrial_delivery_system_Descriptor,
        0x5B : parser_multilingual_network_name_Descriptor,
        0x5C : parser_multilingual_bouquet_name_Descriptor,
        0x5D : parser_multilingual_service_name_Descriptor,
        0x5E : parser_multilingual_component_Descriptor,
        0x5F : parser_private_data_specifier_Descriptor,
        0x60 : parser_service_move_Descriptor,
        0x61 : parser_short_smoothing_buffer_Descriptor,
        0x62 : parser_frequency_list_Descriptor,
        0x63 : parser_partial_transport_stream_Descriptor,
        0x64 : parser_data_broadcast_Descriptor,
        0x65 : parser_CA_system_Descriptor,
        0x66 : parser_data_broadcast_id_Descriptor,
        0x67 : parser_transport_stream_Descriptor,
        0x68 : parser_DSNG_Descriptor,
        0x69 : parser_PDC_Descriptor,
        0x6A : parser_AC3_Descriptor,
        0x6B : parser_ancillary_data_Descriptor,
        0x6C : parser_cell_list_Descriptor,
        0x6D : parser_cell_frequency_link_Descriptor,
        0x6E : parser_announcement_support_Descriptor,
        
    # "Digital Terrestrial Television: Requirements for Interoperability V4.0"
    # UK Digital Television Group (www.dtg.org.uk) document descriptors
    
        0x83 : parser_logical_channel_Descriptor,
        0x84 : parser_preferred_name_list_Descriptor,
        0x85 : parser_preferred_name_identifier_Descriptor,
        0x86 : parser_service_attribute_Descriptor,
        0x87 : parser_short_service_name_Descriptor,
}

# Aciliary support stuff

def unBCD(byte):
    return (byte>>4)*10 + (byte & 0xf)

# dvbt transmission parameters

_dvbt_bandwidths = {
        0 : dvb3f.BANDWIDTH_8_MHZ,
        1 : dvb3f.BANDWIDTH_7_MHZ,
        2 : dvb3f.BANDWIDTH_6_MHZ,
    }

_dvbt_constellations = {
        0 : dvb3f.QPSK,
        1 : dvb3f.QAM_16,
        2 : dvb3f.QAM_64,
    }
    
_dvbt_hierarchy = {
        0 : dvb3f.HIERARCHY_NONE,
        1 : dvb3f.HIERARCHY_1,
        2 : dvb3f.HIERARCHY_2,
        3 : dvb3f.HIERARCHY_4,
     }

_dvbt_code_rate_hp = {
        0 : dvb3f.FEC_1_2,
        1 : dvb3f.FEC_2_3,
        2 : dvb3f.FEC_3_4,
        3 : dvb3f.FEC_5_6,
        4 : dvb3f.FEC_7_8,
     }

_dvbt_code_rate_lp = _dvbt_code_rate_hp

_dvbt_guard_interval = {
        0 : dvb3f.GUARD_INTERVAL_1_32,
        1 : dvb3f.GUARD_INTERVAL_1_16,
        2 : dvb3f.GUARD_INTERVAL_1_8,
        3 : dvb3f.GUARD_INTERVAL_1_4,
     }

_dvbt_transmission_mode = {
        0 : dvb3f.TRANSMISSION_MODE_2K,
        1 : dvb3f.TRANSMISSION_MODE_8K,
     }
    
# service descriptor, service types
_service_types = {
       0x01 : "digital television service",
       0x02 : "digital radio sound service",
       0x03 : "Teletext service",
       0x04 : "NVOD reference service",
       0x05 : "NVOD time-shifted service",
       0x06 : "mosaic service",
       0x07 : "PAL coded signal",
       0x08 : "SECAM coded signal",
       0x09 : "D/D2-MAC",
       0x0A : "FM Radio",
       0x0B : "NTSC coded signal",
       0x0C : "data broadcast service",
       0x0E : "RCS Map",
       0x0F : "RCS FLS",
       0x10 : "DVB MHP service",
    }

# table for iso_639_descriptor
_iso639_audiotypes = {
        0 : "",
        1 : "CLEAN",
        2 : "HEARING IMPAIRED",
        3 : "VISUAL IMPAIRED COMMENTARY",
    }


_stream_component_mappings = {
       (0x01, 0x01) : ("video",                 "4:3 aspect ratio, 25 Hz"),
       (0x01, 0x02) : ("video",                 "16:9 aspect ratio with pan vectors, 25 Hz"),
       (0x01, 0x03) : ("video",                 "16:9 aspect ratio without pan vectors, 25 Hz"),
       (0x01, 0x04) : ("video",                 "> 16:9 aspect ratio, 25 Hz"),
       (0x01, 0x05) : ("video",                 "4:3 aspect ratio, 30 Hz"),
       (0x01, 0x06) : ("video",                 "16:9 aspect ratio with pan vectors, 30 Hz"),
       (0x01, 0x07) : ("video",                 "16:9 aspect ratio without pan vectors, 30 Hz"),
       (0x01, 0x05) : ("video",                 "> 16:9 aspect ratio, 30 Hz"),
       (0x01, 0x09) : ("high definition video", "4:3 aspect ratio, 25 Hz"),
       (0x01, 0x0A) : ("high definition video", "16:9 aspect ratio with pan vectors, 25 Hz"),
       (0x01, 0x0B) : ("high definition video", "16:9 aspect ratio without pan vectors, 25 Hz"),
       (0x01, 0x0C) : ("high definition video", "> 16:9 aspect ratio, 25 Hz"),
       (0x01, 0x0D) : ("high definition video", "4:3 aspect ratio, 30 Hz"),
       (0x01, 0x0E) : ("high definition video", "16:9 aspect ratio with pan vectors, 30 Hz"),
       (0x01, 0x0F) : ("high definition video", "16:9 aspect ratio without pan vec., 30 Hz"),
       (0x01, 0x10) : ("high definition video", "> 16:9 aspect ratio, 30 Hz"),
       (0x02, 0x01) : ("audio",                 "single mono channel"),
       (0x02, 0x02) : ("audio",                 "dual mono channel"),
       (0x02, 0x03) : ("audio",                 "stereo (2 channel)"),
       (0x02, 0x04) : ("audio",                 "multi-lingual, multi-channel"),
       (0x02, 0x05) : ("audio",                 "surround sound"),
       (0x02, 0x40) : ("audio description for the visually impaired", ""),
       (0x02, 0x41) : ("audio for the hard of hearing",               ""),
       (0x03, 0x01) : ("EBU Teletext subtitles",  ""),
       (0x03, 0x02) : ("associated EBU Teletext", ""),
       (0x03, 0x03) : ("VBI data",                ""),
       (0x03, 0x10) : ("DVB subtitles (normal)", "with no monitor aspect ratio criticality"),
       (0x03, 0x11) : ("DVB subtitles (normal)", "for display on 4:3 aspect ratio monitor"),
       (0x03, 0x12) : ("DVB subtitles (normal)", "for display on 16:9 aspect ratio monitor"),
       (0x03, 0x13) : ("DVB subtitles (normal)", "for display on 2.21:1 aspect ratio monitor"),
       (0x03, 0x20) : ("DVB subtitles (for the hard of hearing)", "with nomonitor aspect ratio criticality"),
       (0x03, 0x21) : ("DVB subtitles (for the hard of hearing)", "for display on 4:3 aspect ratiomonitor"),
       (0x03, 0x22) : ("DVB subtitles (for the hard of hearing)", "for display on 16:9 aspect ratiomonitor"),
       (0x03, 0x23) : ("DVB subtitles (for the hard of hearing)", "for display on 2.21:1 aspect ratiomonitor"),
    }

_private_data_specifiers = {
        0x00000001 : "SES",
        0x00000002 : "BSkyB 1",
        0x00000003 : "BSkyB 2",
        0x00000004 : "BSkyB 3",
        0x000000BE : "BetaTechnik",
        0x00006000 : "News Datacom",
        0x00006001 : "NDC 1",
        0x00006002 : "NDC 2",
        0x00006003 : "NDC 3",
        0x00006004 : "NDC 4",
        0x00006005 : "NDC 5",
        0x00006006 : "NDC 6",
        0x00362275 : "Irdeto",
        0x004E544C : "NTL",
        0x00532D41 : "Scientific Atlanta",
        0x44414E59 : "News Datacom (IL) 1",
        0x46524549 : "News Datacom (IL) 1",
        0x53415053 : "Scientific Atlanta",
    }
