#!/bin/python


import os

def slurp(filename,binary=False):
    # print("OPEN:", filename)
    f = open(filename, "rb")
    x = f.read()
    if not binary:
        x = x.decode("utf-8")
    f.close()
    return x

def store(filename, contents, binary=False):
    if not binary:
        f = open(filename, "w")
    else:
        f = open(filename, "wb")
    f.write(contents)
    f.close()

def find(basedir, t="file"):
    if t != "file":
        raise NotImplementedError()
    #
    for i in os.listdir(basedir):
        p = os.path.join(basedir, i)
        if os.path.isdir(p):
            for j in find(p, t):
                yield j
        else:
            yield p

pagetemplate = slurp("site-resources/page-template.html")

if __name__ == "__main__":
    import sys
    import os
    source = sys.argv[1]
    dest = sys.argv[2]

    template = "site-resources/page-template.html" # sys.arg[3]
    pagetemplate = slurp(template)
    command = 'pandoc --from markdown+backtick_code_blocks+grid_tables --to html --highlight-style kate %s -o %s' % (source, dest)
    os.system(command)
    
    sourcepage = slurp(dest)
    newpage = pagetemplate.replace("%CONTENT GOES HERE%", sourcepage)
    store(dest, newpage)
