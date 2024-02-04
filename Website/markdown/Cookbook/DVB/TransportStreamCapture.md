---
pagename: Cookbook/DVB/TransportStreamCapture
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Recording a whole DVB broadcast
==========================================

Find the code for this here:\
[/Code/Python/Kamaelia/Examples/DVB\_Systems/TransportStreamCapture.py](http://svn.sourceforge.net/viewvc/kamaelia/trunk/Code/Python/Kamaelia/Examples/DVB_Systems/TransportStreamCapture.py?view=markup)\

This simple example shows how to record a whole broadcast DVB multiplex
at a frequency of 505.83MHz, with specific parameters to help the tuner:

        from Kamaelia.Device.DVB.Core import DVB_Multiplex
        from Kamaelia.Chassis.Pipeline import Pipeline
        from Kamaelia.File.Writing import SimpleFileWriter
        
        import dvb3
        
        freq = 505.833330 # 529.833330   # 505.833330
        feparams = {
            "inversion" : dvb3.frontend.INVERSION_AUTO,
            "constellation" : dvb3.frontend.QAM_16,
            "code_rate_HP" : dvb3.frontend.FEC_3_4,
            "code_rate_LP" : dvb3.frontend.FEC_3_4,
        }
        
        Pipeline(
           DVB_Multiplex(freq, [0x2000],feparams), # BBC Multiplex 1, whole transport stream
           SimpleFileWriter("BBC_MUX_1.ts"),
        ).run()

The DVB\_Multiplex component is the simplest and easiest to use combined
tuner and demultiplexer component - you simply specify the frequency, a
list of packet IDs to demultiplex, and an optional dictionary of tuner
control parameters.

By specifying the special PID of 0x2000 the demultiplexer outputs all
packets. However, not that not all DVB hardware supports this.\
