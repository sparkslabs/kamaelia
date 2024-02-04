---
pagename: Projects/Soc2006/XML2DInterfaces
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
SoC Project: XML Definition and CSS style styling of Pygame (2D) Based Interfaces
=================================================================================

There were 2 project applications in this area that are summarised here.
This page contains the depersonalised content, which can be consolidated
as necessary. The depersonalisation is for privacy reasons, credit is
here due to those who spent the time writing these descriptions.\

### Project Title: XML-defined interfaces in Kamaelia

Benefits to Kamaelia:\
First, XML/CSS interfaces allow for standardization between programs;
everyone can write an interface in exactly the same format. Second, XML
and CSS are simple markup languages, so a non-coder could easily define
an interface without understanding Python. This is useful even for
people who know Python, because the content and formatting data can be
kept separate.\
\
Synopsis:\
This project will define a standard and reusable format for writing
interfaces using XML and CSS. The project also includes writing a
component for Kamaelia that will interpret the files for display.\
\
Specifically, these formats will allow interfaces to be built from
standard components and reused without writing code, useful for
interface designers. It will solve the problem of proper z-ordering and
enforce separation between content and formatting.\
\
Deliverables:\
\
Will deliver:\
- XML format for the interface widgets\
- CSS format to describe the appearance of the interface widgets\
- A component for Kamaelia that will interpret the XML and CSS interface
files\
\
Given sufficient time:\
- A separate GUI program for creating interfaces that will export to the
XML/CSS interface format that I define.\
\
Project Details:\
The first step will be defining the XML and CSS formats. This will
include a version so that the specifications can easily updated without
breaking applications. Separation between content (XML) and formatting
(CSS) will be strictly enforced.\
\
Using the format in Kamaelia will be almost as simple as loading an XML
file. Each tag in the file will define a widget or group of widgets, and
name or id attributes will differentiate between individual widgets, so
that they can be controlled from the program.\
\
The XML file will reference one or more CSS files to control the
formatting, layout, and general appearance of the window and its
contents.\
\
The real work this project requires is of course the Kamaelia module.
The component will probably use a pre-existing XML-python class such as
XMLObject\[1\] to load in the data, which will save time. A preliminary
search didn\'t turn up a similar library for dealing with CSS markup, so
writing a CSS parser may be a part of this project. Once the data is in
a convenient (Python) format, the actual widgets can be built. This will
be entirely automated; a single function call should take care of it as
far as a user of the Kamaelia framework is concerned. After the
interface is built, instantiated widgets can be found in a dictionary of
names, where the names are defined in the XML file as attributes. Using
the widgets will be just like it already is, mainly it is the way they
are created needs to change.\
\
Finally, I think it would make this code much more useful if I coded a
basic GUI editor that would output XML and CSS files for use with the
new formats. This would make it even easier for non-programmers to work
with programmers who are using the Kamaelia framework.\
\

------------------------------------------------------------------------

\
\

### CSS-esque Styling and XML Layout Definition of Pygame Applications

::: {.boxright}
*Editor: This is one of the smallest applications that was useful -
it\'s milestones are \*just\* sufficiently broken down to be considered
of use*
:::

I realize that this project really should start with a discussion but
the application window is closing today and I thought it was important
to get this application in first.\
\
Right now I have a concept for this project that is probably a bit too
vague but I think we can come up with a solid spec in the first week or
two.\
\
Milestones:\
May - Completed spec. All modules/classes should have skeletons.
Experiment with different XML/stylesheet/gui libraries. Adjust
milestones.\
June - Define XML DTD/schema and code up basic parser/event handler.\
July - Implement CSS (or other stylesheet) system. Get some users to
beta test.\
Aug. - Bugs, Docs, Example code, Docs, Bugs, Docs.\
\
I know this timeline is rather vague but until we agree on a detailed
spec I don\'t feel comfortable making any promises.\
\

------------------------------------------------------------------------

\
\
