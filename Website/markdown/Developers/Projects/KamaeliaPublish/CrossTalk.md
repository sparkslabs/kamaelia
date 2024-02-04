---
pagename: Developers/Projects/KamaeliaPublish/CrossTalk
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia CrossTalk 
==================

Kamaelia Crosstalk is an open internet communication protocol for
transmitting HTTP information between computers.  Of course, the obvious
question here is why not use HTTP to transmit HTTP data?  I\'m glad you
asked.  :) \

History 
-------

If you just want to get to the details of CrossTalk, feel free to skip
this section.\
\
When I first proposed Kamaelia Publish, I had intended upon making
separate \"peer\" and \"intermediary\" programs.  The idea being that a
person who wanted to pull up a webpage that a peer is hosting can send
an HTTP request to the intermediary (which is essentially an HTTP proxy)
and the intermediary will then forward the request to the peer.  The
peer will then send the response to the intermediary.  I then came
across a protocol known as XMPP, a protocol typically used for instant
messenging.  Here\'s an example of how XMPP works from
[wikipedia](http://en.wikipedia.org/wiki/Jabber):\
\

> Suppose *juliet\@capulet.com* wants to chat with
> *romeo\@montague.net*. Juliet and Romeo each respectively have
> accounts on the capulet.com and montague.net servers. When Juliet
> types in and sends her message, a sequence of events is set in motion:
>
> 1.  Juliet\'s client sends her message to the capulet.com server
>     -   If montague.net is blocked on capulet.com, the message is
>         dropped.
> 2.  The capulet.com server opens a connection to the montague.net
>     server.
>     -   If capulet.com is blocked on montague.net, the message is
>         dropped.
>     -   If Romeo is not currently connected, the message is stored for
>         later delivery.
> 3.  The montague.net server delivers the message to Romeo.

The idea of XMPP servers sounds an awful lot like my \"intermediary\"
doesn\'t it?  So I took this idea a step further.  XMPP has a concept of
\"gateways\" that are intended to convert other protocols into XMPP. 
That way, if you want to talk to a friend who uses AIM or Yahoo, you can
do it.  What if it were possible to transmit HTTP via XMPP using a
gateway?\
\
The next step was to try sending the text of the HTTP request to the
peer, and then the peer would send the response back to the gateway. 
This turned out to be more complicated than it seems.  The problem being
that the HTTP request would have to be parsed at the gateway level as
well as at the peer level.  So why not just send the parsed data from
the gateway to the peer?  That led to what I am now terming CrossTalk
(the name may change later).\
\
\

Why the name CrossTalk?
-----------------------

Because I got tired of referring to Kamaelia\'s means of transmitting
HTTP data as \"HTTP over XMPP.\"  That\'s too much of a mouthful, has
too much alphabet soup for laymen, and isn\'t really accurate anyway.\

 

How does it work? 
-----------------

First of all, I should note that CrossTalk is currently purely
experimental, and is likely to change.\
\
CrossTalk uses JSON to serialize data to be transmitted from Peer to
Gateway (and possibly from Peer to Peer at a later point in time).  An
operation that starts with an HTTP request from a user and ends with an
HTTP response back to that same user is referred to as a *transaction*. 
Each transaction begins with a request object.  This object contains all
of the data that is present in the HTTP request line and headers,
formatted in a CGI environment-like dictionary.  In addition to the data
that is present in the HTTP request dictionary, there are two other keys
that may be present.\
\

-   The \'data\' key is where the body of the HTTP request will be
    transmitted.  It may appear in the request object or it may be sent
    seperately or even split out across several messages (although this
    is probably to be avoided for performance reasons). 
-   The \'signal\' key is currently used to signal that the gateway is
    through transmitting the HTTP request and its body, but keep in mind
    that there may be other data present here in the future.  The signal
    key may be present in any message described above or it may be sent
    by itself as the final message, although the current peer script
    will not function properly if it is included in the request object
    (the current implementation of the gateway will always send it by
    itself after the other data has been transmitted)
-   The \'batch\' key identifies which transaction the message belongs
    to.

Once the Peer has formulated its response, it will transmit a response
object.  The type of data it contains will be roughly the same as the
request object.  The format is a little bit different though.\
\

-   The \'data\', \'signal\', and \'batch\' keys currently have the same
    meaning as in the response object.
-   \'headers\' will contain a list of the response headers.  Here is a
    sample of what that would look like:

> \[\
>     \[\
>       \"Content-type\",\
>       \"text\\/html\"\
>     \],\
>     \[\
>       \"Pragma\",\
>       \"no-cache\"\
>     \]\
> \]\
