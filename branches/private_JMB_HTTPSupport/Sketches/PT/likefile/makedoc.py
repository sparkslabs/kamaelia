#!/usr/bin/env python
import likefile, pydoc

documentation = ''.join(["<pre>",
            likefile.__doc__,
            "<br><br><br></pre>",
            pydoc.HTMLDoc().document(likefile.LikeFile),
            ])

outfile = open("likefile.html", "w+b")
outfile.write(documentation)