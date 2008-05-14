#!/usr/bin/env python
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
========================
Construct DVB PSI tables
========================

PSI table sections in ... MPEG transport stream packets out

not yet tested ... or kamaelia-ised!


"""
#from Kamaelia.Support.DVB.Descriptors

def serialiseDescriptors(descriptors):
    data = []
    for descriptor in descriptors:
        data.extend(serialiseDescriptor(descriptor))
    return data.join("")


def serialiseDescriptor(descriptor):
    dtype = descriptor["type"]
    dId, serialiser = __descriptor_serialisers[dtype]
    if descriptor.has_key("contents"):
        data = [ descriptor["contents"] ]
        dLen = len(data[0])
    else:
        data, dLen = serialiser(descriptor)
    retval = [ chr(dId), chr(dLen) ]
    retval.extend(data)
    return retval
    

# =============================================================================

# ISO 13818-1 defined descriptors
def serialise_video_stream_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_audio_stream_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_hierarchy_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_registration_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_data_stream_alignment_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_target_background_grid_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_video_window_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_CA_Descriptor(descriptor):
    return \
        [ chr((descriptor["CA_system_id"] >> 8) & 0xff), \
          chr((descriptor["CA_system_id"]     ) & 0xff), \
          chr((descriptor["pid"] >> 8) & 0x1f), \
          chr((descriptor["pid"]     ) & 0xff), \
          descriptor["private_data"] \
        ] , \
        4+len(descriptor["private_data"]

def serialise_ISO_639_Descriptor(descriptor):
    parts = []
    for part in descriptor["parts"]:
        parts.insert(part["language_code"])
        parts.insert(chr(_iso639_audiotypes_rev.get(part["audio_type"],part["audio_type"])))
    return parts, 4 * len(descriptor["parts"])

def serialise_system_clock_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_multiplex_buffer_utilisation_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_copyright_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_maximum_bitrate_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_private_data_indicator_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_smoothing_buffer_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_STD_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_IBP_Descriptor(descriptor):
    raise "Not yet implemented"


# -----------------------------------------------------------------------------
# ETSI EN 300 468 defined descriptors

def serialise_network_name_Descriptor(descriptor):
    return [ descriptor["network_name"] ], len(descriptor["network_name"])

def serialise_service_list_Descriptor(descriptor):
    services = []
    for service in descriptor["services"]:
        services.insert( chr((service["service_id"] >> 8) & 0xff) + \
                         chr((service["service_id"]     ) & 0xff) + \
                         chr(_service_types_rev[service["service_type"]]) )
    return services, len(services)*3

def serialise_stuffing_Descriptor(descriptor):
    return [ chr(0)*descriptor["length"] ], descriptor["length"]

def serialise_satellite_delivery_system_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_cable_delivery_system_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_VBI_data_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_VBI_teletext_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_bouquet_name_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_service_Descriptor(descriptor):
    return [ chr(_service_types_rev[descriptor["service_type"]]), \
             chr(len(descriptor["service_provider_name"])), \
             descriptor["service_provider_name"], \
             chr(len(descriptor["service_name"])), \
             descriptor["service_name"] \
           ], \
           3 + len(descriptor["service_provider_name"]) + len(descriptor["service_name"])

def serialise_country_availability_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_linkage_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_NVOD_reference_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_time_shifted_service_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_short_event_Descriptor(descriptor):
    return [ descriptor["language_code"],   \
             chr(len(descriptor["name"])),  \
             descriptor["name"],            \
             chr(len(descriptor["text"])),  \
             descriptor["text"]             \
           ], \
           5 + len(descriptor["name"]) + len(descriptor["text"])

def serialise_extended_event_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_time_shifted_event_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_component_Descriptor(descriptor):
    retval = []
    if descriptor.has_key("stream_content") and descriptor.has_key("component_type"):
        retval.insert(chr(descriptor["stream_content"] & 0x0f))
        retval.insert(chr(descriptor["component_type"] & 0xff))
    
    else if descriptor.has_key("content,type"):
        sc, ct = _stream_component_mappings_rev.get(descriptor["content,type"], descriptor["content,type"])
        retval.insert(chr(sc))
        retval.insert(chr(ct))
        
    else
        raise "no stream_content and component_type info"
        
    retval.insert(chr(descriptor["component_tag" ] & 0xff))
    retval.insert(descriptor["language_code"])
    retval.insert(descriptor["text"])
    return retval, 6+len(descriptor["text"])

def serialise_mosaic_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_stream_identifier_Descriptor(descriptor):
    return [ chr(descriptor["component_tag"]) ], 1

def serialise_CA_identifier_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_content_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_parental_rating_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_teletext_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_telephone_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_local_time_offset_Descriptor(descriptor):
    offset = descriptor["offset"]
    nextoffset = descriptor["nextOffset"]
    
    if offset[0] < 0:
        offset = (-offset[0], -offset[0])
        nextoffset = (-nextoffset[0], -nextoffset[0])
        
    offsetBCD = createBCDtime(*offset)
    nextoffsetBCD = createBCDtime(*nextoffset)
    
    mjd,utc = createMJDUTC(*descriptor["timeOfChange"])
    
    return [ descriptor["country"] + \
             chr((descriptor["region"] & 0x3f)<<2) + \
             chr((offsetBCD >> 8) & 0xff) + \
             chr((offsetBCD     ) & 0xff) + \
             chr((mjd >> 8) & 0xff)  + \
             chr((mjd     ) & 0xff)  + \
             chr((utc >> 16) & 0xff) + \
             chr((utc >> 8 ) & 0xff) + \
             chr((utc      ) & 0xff) + \
             chr((nextoffsetBCD >> 8) & 0xff) + \
             chr((nextoffsetBCD     ) & 0xff),
           ], 13

def serialise_subtitling_Descriptor(descriptor):
    parts = []
    for part in descriptor["entries"]:
        stype = _stream_component_mappings_rev.get( \
            descriptor["subtitling_type"][0], \
            descriptor["subtitling_type"] \
            )
        cpid = descriptor["composition_page_id"]
        apid = descriptor["ancilliary_page_id"]
        parts.insert( \
            descriptor["language_code"] + \
            chr(stype[0]) + \
            chr((cpid >> 8) & 0xff) + \
            chr((cpid     ) & 0xff) + \
            chr((apid >> 8) & 0xff) + \
            chr((apid     ) & 0xff) \
        )
    return parts, \
        len(descriptor["entries"]) * 8
    

def serialise_terrestrial_delivery_system_Descriptor(descriptor):
    dparams = descriptor["params"]
    dfreqs = descriptor["other_frequencies"]

    return [ chr(((dparams["frequency"] / 10) >> 24) & 0xff) + \
             chr(((dparams["frequency"] / 10) >> 16) & 0xff) + \
             chr(((dparams["frequency"] / 10) >> 8 ) & 0xff) + \
             chr(((dparams["frequency"] / 10) >>   ) & 0xff) + \
             chr(_dvbt_bandwidths_rev[dparams["bandwidth"]] << 5) + \
             chr( (_dvbt_constellations_rev[dparams["constellation"]] << 6) + \
                  (_dvbt_hierarchy_rev[dparams["hierarchy_information"]] << 3) + \
                  (_dvbt_code_rate_hp_rev[dparams["code_rate_HP"]]) \
                ) + \
             chr( (_dvbt_code_rate_lp_rev[dparams["code_rate_LP"]] << 5) + \
                  (_dvbt_guard_interval_rev[dparams["guard_interval"]] << 3) + \
                  (_dvbt_transmission_mode_rev[dparams["transmission_mode"]] << 1) + \
                  other_freq_flag \
                ) + \
             "\0\0\0\0" \
           ], 11

def serialise_multilingual_network_name_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_multilingual_bouquet_name_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_multilingual_service_name_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_multilingual_component_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_private_data_specifier_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_service_move_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_short_smoothing_buffer_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_frequency_list_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_partial_transport_stream_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_data_broadcast_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_CA_system_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_data_broadcast_id_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_transport_stream_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_DSNG_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_PDC_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_AC3_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_ancillary_data_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_cell_list_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_cell_frequency_link_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_announcement_support_Descriptor(descriptor):
    raise "Not yet implemented"

    
# -----------------------------------------------------------------------------
# "Digital Terrestrial Television: Requirements for Interoperability V4.0"
# UK Digital Television Group (www.dtg.org.uk) document descriptors

def serialise_logical_channel_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_preferred_name_list_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_preferred_name_identifier_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_service_attribute_Descriptor(descriptor):
    raise "Not yet implemented"

def serialise_short_service_name_Descriptor(descriptor):
    raise "Not yet implemented"



# =============================================================================

def createMJDUTC(year,month,day,hour,minute,second):
    if month == 1 or month == 2:
        L = 1
    else:
        L = 0
    MJD = 14956 + day + int( (year - L) * 365.25) + int ( (month + 1 + L * 12) * 30.6001 )
    
    return MJD, createBCDtime(hour,minute,second)

def createBCDtime(hour,minute,second):
    HHMMSS = 0
    for digit in "%02d%02d%02d" % (hour,minute,second):
        HHMMSS = (HHMMSS<<4) + ord(digit)-ord("0")
    return HHMMSS


def createBCDtime(hour,minute):
    HHMM = 0
    for digit in "%02d%02d" % (hour,minute):
        HHMM = (HHMM<<4) + ord(digit)-ord("0")
    return HHMM

__descriptor_serialisers = {
    # ISO 13818-1 defined descriptors
        "video_stream"          : (0x02, serialise_video_stream_Descriptor),
        "audio_stream"          : (0x03, serialise_audio_stream_Descriptor),
        "hierarchy"             : (0x04, serialise_hierarchy_Descriptor),
        "registration"          : (0x05, serialise_registration_Descriptor),
        "data_stream_alignment" : (0x06, serialise_data_stream_alignment_Descriptor),
        "target_background_grid" : (0x07, serialise_target_background_grid_Descriptor),
        "video_window"          : (0x08, serialise_video_window_Descriptor),
        "CA"                    : (0x09, serialise_CA_Descriptor),
        "ISO_639"               : (0x0a, serialise_ISO_639_Descriptor),
        "system_clock"          : (0x0b, serialise_system_clock_Descriptor),
        "multiplex_buffer_utilisation" : (0x0c, serialise_multiplex_buffer_utilisation_Descriptor),
        "copyright"             : (0x0d, serialise_copyright_Descriptor),
        "maximum_bitrate"       : (0x0e, serialise_maximum_bitrate_Descriptor),
        "private_data_indicator" : (0x0f, serialise_private_data_indicator_Descriptor),
        "smoothing_buffer"      : (0x10, serialise_smoothing_buffer_Descriptor),
        "STD"                   : (0x11, serialise_STD_Descriptor),
        "IBP"                   : (0x12, serialise_IBP_Descriptor),

    # ETSI EN 300 468 defined descriptors

        "network_name"          : (0x40, serialise_network_name_Descriptor),
        "service_list"          : (0x41, serialise_service_list_Descriptor),
        "stuffing"              : (0x42, serialise_stuffing_Descriptor),
        "satellite_delivery_system" : (0x43, serialise_satellite_delivery_system_Descriptor),
        "cable_delivery_system" : (0x44, serialise_cable_delivery_system_Descriptor),
        "VBI_data"              : (0x45, serialise_VBI_data_Descriptor),
        "VBI_teletext"          : (0x46, serialise_VBI_teletext_Descriptor),
        "bouquet_name"          : (0x47, serialise_bouquet_name_Descriptor),
        "service"               : (0x48, serialise_service_Descriptor),
        "country_availability"  : (0x49, serialise_country_availability_Descriptor),
        "linkage"               : (0x4A, serialise_linkage_Descriptor),
        "NVOD_reference"        : (0x4B, serialise_NVOD_reference_Descriptor),
        "time_shifted_service"  : (0x4C, serialise_time_shifted_service_Descriptor),
        "short_event"           : (0x4D, serialise_short_event_Descriptor),
        "extended_event"        : (0x4E, serialise_extended_event_Descriptor),
        "time_shifted_event"    : (0x4F, serialise_time_shifted_event_Descriptor),
        "component"             : (0x50, serialise_component_Descriptor),
        "mosaic"                : (0x51, serialise_mosaic_Descriptor),
        "stream_identifier"     : (0x52, serialise_stream_identifier_Descriptor),
        "CA_identifier"         : (0x53, serialise_CA_identifier_Descriptor),
        "content"               : (0x54, serialise_content_Descriptor),
        "parental_rating"       : (0x55, serialise_parental_rating_Descriptor),
        "teletext"              : (0x56, serialise_teletext_Descriptor),
        "telephone"             : (0x57, serialise_telephone_Descriptor),
        "local_time_offset"     : (0x58, serialise_local_time_offset_Descriptor),
        "subtitling"            : (0x59, serialise_subtitling_Descriptor),
        "terrestrial_delivery_system" : (0x5A, serialise_terrestrial_delivery_system_Descriptor),
        "multilingual_network_name" : (0x5B, serialise_multilingual_network_name_Descriptor),
        "multilingual_bouquet_name" : (0x5C, serialise_multilingual_bouquet_name_Descriptor),
        "multilingual_service_name" : (0x5D, serialise_multilingual_service_name_Descriptor),
        "multilingual_component" : (0x5E, serialise_multilingual_component_Descriptor),
        "private_data_specifier" : (0x5F, serialise_private_data_specifier_Descriptor),
        "service_move"          : (0x60, serialise_service_move_Descriptor),
        "short_smoothing_buffer" : (0x61, serialise_short_smoothing_buffer_Descriptor),
        "frequency_list"        : (0x62, serialise_frequency_list_Descriptor),
        "partial_transport_stream" : (0x63, serialise_partial_transport_stream_Descriptor),
        "data_broadcast"        : (0x64, serialise_data_broadcast_Descriptor),
        "CA_system"             : (0x65, serialise_CA_system_Descriptor),
        "data_broadcast_id"     : (0x66, serialise_data_broadcast_id_Descriptor),
        "transport_stream"      : (0x67, serialise_transport_stream_Descriptor),
        "DSNG"                  : (0x68, serialise_DSNG_Descriptor),
        "PDC"                   : (0x69, serialise_PDC_Descriptor),
        "AC3"                   : (0x6A, serialise_AC3_Descriptor),
        "ancillary_data"        : (0x6B, serialise_ancillary_data_Descriptor),
        "cell_list"             : (0x6C, serialise_cell_list_Descriptor),
        "cell_frequency_link"   : (0x6D, serialise_cell_frequency_link_Descriptor),
        "announcement_support"  : (0x6E, serialise_announcement_support_Descriptor),
        
    # "Digital Terrestrial Television: Requirements for Interoperability V4.0"
    # UK Digital Television Group (www.dtg.org.uk) document descriptors
    
        "logical_channel"       : (0x83, serialise_logical_channel_Descriptor),
        "preferred_name_list"   : (0x84, serialise_preferred_name_list_Descriptor),
        "preferred_name_identifier" : (0x85, serialise_preferred_name_identifier_Descriptor),
        "service_attribute"     : (0x86, serialise_service_attribute_Descriptor),
        "short_service_name"    : (0x87, serialise_short_service_name_Descriptor),
}


# table for iso_639_descriptor
from Kamaelia.Support.DVB.Descriptors import _iso639_audiotypes
from Kamaelia.Support.DVB.Descriptors import _service_types
from Kamaelia.Support.DVB.Descriptors import _stream_component_mappings
from Kamaelia.Support.DVB.Descriptors import _dvbt_bandwidths
from Kamaelia.Support.DVB.Descriptors import _dvbt_constellations
from Kamaelia.Support.DVB.Descriptors import _dvbt_hierarchy
from Kamaelia.Support.DVB.Descriptors import _dvbt_code_rate_hp
from Kamaelia.Support.DVB.Descriptors import _dvbt_code_rate_lp
from Kamaelia.Support.DVB.Descriptors import _dvbt_guard_interval
from Kamaelia.Support.DVB.Descriptors import _dvbt_transmission_mode

def __invert(fwdDict):
    return dict([(v,k) for (k,v) in fwdDict.items()])

_iso639_audiotypes_rev         = __invert(_iso639_audiotypes)
_service_types_rev             = __invert(_service_types)
_stream_component_mappings_rev = __invert(_stream_component_mappings)
_dvbt_bandwidths_rev           = __invert(_dvbt_bandwidths)
_dvbt_constellations_rev       = __invert(_dvbt_constellations)
_dvbt_hierarchy_rev            = __invert(_dvbt_hierarchy)
_dvbt_code_rate_hp_rev         = __invert(_dvbt_code_rate_hp)
_dvbt_code_rate_lp_rev         = __invert(_dvbt_code_rate_lp)
_dvbt_guard_interval_rev       = __invert(_dvbt_guard_interval)
_dvbt_transmission_mode_rev    = __invert(_dvbt_transmission_mode)

