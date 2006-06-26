#!/usr/bin/env python

# parsing routines for DVB PSI table descriptors

def parseDescriptor(i,data):
    # just a simple extract the tag and body of the descriptor
    tag    = ord(data[i])
    length = ord(data[i+1])
    end    = i+2+length

    parser = __descriptor_parsers.get(tag,parser_Null_Descriptor)

    output = parser(data,i,length,end)

    return (tag,output), end



# now parsers for all descriptor types


def parser_Null_Descriptor(data,i,length,end):
    return data[i+2:end]



# ISO 13818-1 defined descriptors

parser_video_stream_Descriptor                 = parser_Null_Descriptor
parser_audio_stream_Descriptor                 = parser_Null_Descriptor
parser_hierarchy_Descriptor                    = parser_Null_Descriptor
parser_registration_Descriptor                 = parser_Null_Descriptor
parser_data_stream_alignment_Descriptor        = parser_Null_Descriptor
parser_target_background_grid_Descriptor       = parser_Null_Descriptor
parser_video_window_Descriptor                 = parser_Null_Descriptor

def parser_CA_Descriptor(data,i,length,end):
    d = { "type"         : "CA",
          "CA_system_id" : (ord(data[i+2])<<8) + ord(data[i+3]),
          "pid"          : ((ord(data[i+4])<<8) + ord(data[i+5])) & 0x1fff,
          "private_data" : data[i+6:end]
        }
    return d

def parser_ISO_639_Descriptor(data,i,length,end):
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

parser_system_clock_Descriptor                 = parser_Null_Descriptor
parser_multiplex_buffer_utilisation_Descriptor = parser_Null_Descriptor
parser_copyright_Descriptor                    = parser_Null_Descriptor
parser_maximum_bitrate_Descriptor              = parser_Null_Descriptor
parser_private_data_indicator_Descriptor       = parser_Null_Descriptor
parser_smoothing_buffer_Descriptor             = parser_Null_Descriptor
parser_STD_Descriptor                          = parser_Null_Descriptor
parser_IBP_Descriptor                          = parser_Null_Descriptor



# ETSI EN 300 468 defined descriptors

parser_network_name_Descriptor                = parser_Null_Descriptor
parser_service_list_Descriptor                = parser_Null_Descriptor
parser_stuffing_Descriptor                    = parser_Null_Descriptor
parser_satellite_delivery_system_Descriptor   = parser_Null_Descriptor
parser_cable_delivery_system_Descriptor       = parser_Null_Descriptor
parser_VBI_data_Descriptor                    = parser_Null_Descriptor
parser_VBI_teletext_Descriptor                = parser_Null_Descriptor
parser_bouquet_name_Descriptor                = parser_Null_Descriptor
parser_service_Descriptor                     = parser_Null_Descriptor
parser_country_availability_Descriptor        = parser_Null_Descriptor
parser_linkage_Descriptor                     = parser_Null_Descriptor
parser_NVOD_reference_Descriptor              = parser_Null_Descriptor
parser_time_shifted_service_Descriptor        = parser_Null_Descriptor
parser_short_event_Descriptor                 = parser_Null_Descriptor
parser_extended_event_Descriptor              = parser_Null_Descriptor
parser_time_shifted_event_Descriptor          = parser_Null_Descriptor
parser_component_Descriptor                   = parser_Null_Descriptor
parser_mosaic_Descriptor                      = parser_Null_Descriptor

def parser_stream_identifier_Descriptor(data,i,length,end):
    d = { "type"         : "stream_identifier",
          "component_tag" : ord(data[i+2]),
        }
    return d

parser_CA_identifier_Descriptor               = parser_Null_Descriptor
parser_content_Descriptor                     = parser_Null_Descriptor
parser_parental_rating_Descriptor             = parser_Null_Descriptor
parser_teletext_Descriptor                    = parser_Null_Descriptor
parser_telephone_Descriptor                   = parser_Null_Descriptor
parser_local_time_offset_Descriptor           = parser_Null_Descriptor

def parser_subtitling_Descriptor(data,i,length,end):
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

parser_terrestrial_delivery_system_Descriptor = parser_Null_Descriptor
parser_multilingual_network_name_Descriptor   = parser_Null_Descriptor
parser_multilingual_bouquet_name_Descriptor   = parser_Null_Descriptor
parser_multilingual_service_name_Descriptor   = parser_Null_Descriptor
parser_multilingual_component_Descriptor      = parser_Null_Descriptor
parser_private_data_specifier_Descriptor      = parser_Null_Descriptor
parser_service_move_Descriptor                = parser_Null_Descriptor
parser_short_smoothing_buffer_Descriptor      = parser_Null_Descriptor
parser_frequency_list_Descriptor              = parser_Null_Descriptor
parser_partial_transport_stream_Descriptor    = parser_Null_Descriptor
parser_data_broadcast_Descriptor              = parser_Null_Descriptor
parser_CA_system_Descriptor                   = parser_Null_Descriptor

def parser_data_broadcast_id_Descriptor(data,i,length,end):
    d = { "type"      : "data_broadcast_id",
          "id"        : (ord(data[i+2])<<8) + ord(data[i+3]),
          "selectors" : [ord(data[j]) for j in range(i+4,end)]
        }
    return d

parser_transport_stream_Descriptor            = parser_Null_Descriptor
parser_DSNG_Descriptor                        = parser_Null_Descriptor
parser_PDC_Descriptor                         = parser_Null_Descriptor
parser_AC3_Descriptor                         = parser_Null_Descriptor
parser_ancillary_data_Descriptor              = parser_Null_Descriptor
parser_cell_list_Descriptor                   = parser_Null_Descriptor
parser_cell_frequency_link_Descriptor         = parser_Null_Descriptor
parser_announcement_support_Descriptor        = parser_Null_Descriptor


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
}

# Aciliary support stuff

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
