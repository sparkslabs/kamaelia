#!/usr/bin/env python
import likefile

outfile = open("likefile.txt", "w+b")
outfile.write("<pre>")
outfile.write(likefile.__doc__)
outfile.write("</pre>")