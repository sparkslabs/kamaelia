---
pagename: Components/pydoc/Kamaelia.Support.DVB.Descriptors
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Support.DVB.html){.reference}.[Descriptors](/Components/pydoc/Kamaelia.Support.DVB.Descriptors.html){.reference}
========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Support functions for parsing DVB data structures](#24){.reference}
    -   [Example Usage](#25){.reference}
    -   [Parsing Descriptors](#26){.reference}
    -   [How does it Work?](#27){.reference}
    -   [References](#28){.reference}
        -   [Mappings, Tables, Values](#29){.reference}
    -   [Service types](#30){.reference}
    -   [Stream Component Mappings](#31){.reference}
    -   [Private Data Specifiers](#32){.reference}
    -   [Content Types](#33){.reference}
:::

::: {.section}
Support functions for parsing DVB data structures {#24}
=================================================

A collection of functions for parsing \'descriptor\' elements of
information tables in DVB data streams. Descriptors contain data such as
channel names, tuning information for other multiplexes, and information
about the audio/video streams making up a channel.

::: {.section}
[Example Usage]{#example-usage} {#25}
-------------------------------

A simple loop to parse a set of descriptors stored consecutively in a
string:

``` {.literal-block}
i=0
while i < len(setOfDescriptors):
    parsed, i = parseDescriptor(i, setOfDescriptors)
    (tag, data) = parsed
    print "Descriptor found with tag",tag
    for (key,value) in data.items():
        print key, "=", value
```
:::

::: {.section}
[Parsing Descriptors]{#parsing-descriptors} {#26}
-------------------------------------------

Call the parseDescriptor() function, passing it the string containing
the descriptor and the index of the beginning of the descriptor within
the string.

parseDescriptor() will return the parsed descriptor:

``` {.literal-block}
(tag, data)
    - tag = the ID of this descriptor type
    - data = dictionary containing the parsed descriptor data:
        { type : WhatKindOfDescriptor,
          key  : value,
          key2 : value2,
          ...
        }
```

All parsed descriptor data will contain the \'type\' key. The remaining
key,value pairs are specific to the type of descriptor.

parseDescriptor() uses helper functions to parse each particular
descriptor. See their documentation to see what descriptors are
currently supported and what data to expect in the dictionary.
:::

::: {.section}
[How does it Work?]{#how-does-it-work} {#27}
--------------------------------------

parseDescriptor() uses helper functions to parse each particular
descriptor. parseDescriptor() extracts the \'tag\' defining the
descriptor type, and the length of the descriptor. A mapping table maps
from tags to parser functions.

Each parser function is of the form::
:   parse(data,i,length,end) -\> dict(parsed descriptor elements)

\'data\' is a string containing the descriptor. \'i\' is the index into
the string of the start of the descriptor. \'length\' is the length of
the descriptor payload and end\' is the index of the first point after
the descriptor.
:::

::: {.section}
[References]{#references} {#28}
-------------------------

For the full description of the descriptors available see the following
MPEG and DVB standards documents:

-   ISO/IEC 13818-1 (aka \"MPEG: Systems\") \"GENERIC CODING OF MOVING
    PICTURES AND ASSOCIATED AUDIO: SYSTEMS\" ISO / Motion Picture
    Experts Grou7p
-   ETSI EN 300 468 \"Digital Video Broadcasting (DVB); Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)
-   \"Digital Terrestrial Television: Requirements for
    Interoperability\" Issue 4.0+ (aka \"The D book\") UK Digital
    Television Group
-   ETSI TS 102 323 Technical Specification: \"Digital Video
    Broadcasting (DVB); Carriage and signalling of TV-Anytime
    information in DVB transport streams\" ETSI / EBU (DVB group)

::: {.section}
### [Mappings, Tables, Values]{#mappings-tables-values} {#29}

Various mappings, tables, values etc. used by the DVB standard.
:::
:::

::: {.section}
[Service types]{#service-types} {#30}
-------------------------------

Types of services (channel) that can be found in a DVB multiplex:

``` {.literal-block}
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
"MPEG-2 HD digital television service",
"advanced codec SD digital television service",
"advanced codec SD NVOD time-shifted service",
"advanced codec SD NVOD reference service",
"advanced codec HD digital television service",
"advanced codec HD NVOD time-shifted service",
"advanced codec HD NVOD reference service",
```
:::

::: {.section}
[Stream Component Mappings]{#stream-component-mappings} {#31}
-------------------------------------------------------

Mappings from (stream\_component, component\_type) values to their
actual meanings. Used in \'component\' descriptors:

``` {.literal-block}
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
```
:::

::: {.section}
[Private Data Specifiers]{#private-data-specifiers} {#32}
---------------------------------------------------

Specifiers defining various types of private data payload:

``` {.literal-block}
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
```
:::

::: {.section}
[Content Types]{#content-types} {#33}
-------------------------------

Level 1 content types/genres:

``` {.literal-block}
0x1 : "Movie/Drama",
0x2 : "News/Current Affairs",
0x3 : "Show/Game show",
0x4 : "Sports",
0x5 : "Children's/Youth",
0x6 : "Music/Ballet/Dance",
0x7 : "Arts/Culture (without music)",
0x8 : "Social/Political issues/Economics",
0x9 : "Childrens/Youth Education/Science/Factual",
0xa : "Leisure hobbies",
0xb : "Misc",
0xf : "Drama", # user defined (specified in the UK "D book")
```

Note that 0xf is a user defined field. The mapping it is assigned here
is that used in the UK \"D book\" specification.

Level 2 content types/genres:

``` {.literal-block}
# movie/drama
0x10 : "General",
0x11 : "Detective/Thriller",
0x12 : "Adventure/Western/War",
0x13 : "Science Fiction/Fantasy/Horror",
0x14 : "Comedy",
0x15 : "Soap/Melodrama/Folkloric",
0x16 : "Romance",
0x17 : "Serious/ClassicalReligion/Historical",
0x18 : "Adult Movie/Drama",

# news/current affairs
0x20 : "General",
0x21 : "News/Weather Report",
0x22 : "Magazine",
0x23 : "Documentary",
0x24 : "Discussion/Interview/Debate",

# show/game show
0x30 : "General",
0x31 : "Game show/Quiz/Contest",
0x32 : "Variety",
0x33 : "Talk",

# sports
0x40 : "General",
0x41 : "Special Event (Olympics/World cup/...)",
0x42 : "Magazine",
0x43 : "Football/Soccer",
0x44 : "Tennis/Squash",
0x45 : "Team sports (excluding football)",
0x46 : "Athletics",
0x47 : "Motor Sport",
0x48 : "Water Sport",
0x49 : "Winter Sports",
0x4a : "Equestrian",
0x4b : "Martial sports",

# childrens/youth
0x50 : "General",
0x51 : "Pre-school",
0x52 : "Entertainment (6 to 14 year-olds)",
0x53 : "Entertainment (10 to 16 year-olds)",
0x54 : "Informational/Educational/Schools",
0x55 : "Cartoons/Puppets",

# music/ballet/dance
0x60 : "General",
0x61 : "Rock/Pop",
0x62 : "Serious music/Classical Music",
0x63 : "Folk/Traditional music",
0x64 : "Jazz",
0x65 : "Musical/Opera",
0x66 : "Ballet",

# arts/culture
0x70 : "General",
0x71 : "Performing Arts",
0x72 : "Fine Arts",
0x73 : "Religion",
0x74 : "Popular Culture/Tradital Arts",
0x75 : "Literature",
0x76 : "Film/Cinema",
0x77 : "Experimental Film/Video",
0x78 : "Broadcasting/Press",
0x79 : "New Media",
0x7a : "Magazine",
0x7b : "Fashion",

# social/political/economic
0x80 : "General",
0x81 : "Magazine/Report/Domentary",
0x82 : "Economics/Social Advisory",
0x83 : "Remarkable People",

# children's youth: educational/science/factual
0x90 : "General",
0x91 : "Nature/Animals/Environment",
0x92 : "Technology/Natural sciences",
0x93 : "Medicine/Physiology/Psychology",
0x94 : "Foreign Countries/Expeditions",
0x95 : "Social/Spiritual Sciences",
0x96 : "Further Education",
0x97 : "Languages",

# leisure hobbies
0xa0 : "General",
0xa1 : "Tourism/Travel",
0xa2 : "Handicraft",
0xa3 : "Motoring",
0xa4 : "Fitness & Health",
0xa5 : "Cooking",
0xa6 : "Advertisement/Shopping",
0xa7 : "Gardening",

# misc
0xb0 : "Original Language",
0xb1 : "Black and White",
0xb2 : "Unpublished",
0xb3 : "Live Broadcast",

# drama (user defined, specced in the UK "D-Book")
0xf0 : "General",
0xf1 : "Detective/Thriller",
0xf2 : "Adventure/Western/War",
0xf3 : "Science Fiction/Fantasy/Horror",
0xf4 : "Comedy",
0xf5 : "Soap/Melodrama/Folkloric",
0xf6 : "Romance",
0xf7 : "Serious/ClassicalReligion/Historical",
0xf8 : "Adult",
```

Note that 0xf0 to 0xff range is a user defined field. The mapping it is
assigned here is that used in the UK \"D book\" specification.
:::
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
