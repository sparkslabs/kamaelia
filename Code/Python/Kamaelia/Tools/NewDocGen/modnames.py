#!/usr/bin/python

import importlib
import re
import sys

DEBUG = False
def slurp(filename):
    f = open(filename)
    raw = f.read()
    f.close()
    return raw

def debug(*argv, **argd):
    if DEBUG:
        print(*argv, **argd)

def slurp_source(source_file):
    source_lines = []
    source = slurp(source_file).split("\n")
    in_longstring = False
    for line in source:
        original_line = line
        line = line.strip()
        if line.startswith("#"):
            debug("REJECTED1", original_line)
            continue

        if line.startswith('"""') and line.endswith('"""') and line.rfind('"""')>3:
            debug("REJECTED2", line)
            continue

        if line.startswith("'''") and line.endswith("'''") and line.rfind("'''")>3:
            debug("REJECTED3", line)
            continue
        
        if line.startswith("'''") or line.startswith('"""'):
            in_longstring = not in_longstring
            debug("REJECTED4", line)
            continue
        if in_longstring:
            debug("REJECTED5", line)
            continue
        debug("OK      ", original_line)
        source_lines.append(original_line)
    return source_lines

def line_source(mod_source):
    if type(mod_source) == str:
        mod_lines = mod_source.split("\n")
    else:
        mod_lines = mod_source
    for line in mod_lines:
        yield line

class ParseFail(Exception):
    pass

def find_imported_names(line, mod_source):
    # We're not really doing a full parse, just looking for
    # import lines and making assumptions about them.
    # This will parse comments & doc strings too. so it's
    # over-eager, but that's OK
    
    # strip comment
    pline = line
    line = re.sub("#.*$", "", line)
    line = line.split(";")[0]
    # strip whitespace
    line = line.strip()
    if not (line.startswith("from ") or line.startswith("import ") ):
        raise ParseFail("Not Import Line", line)
    if line.startswith("from"):
        i = line.find("import") # We don't care where imported from
        if i == -1:
            raise ParseFail("Bad Import Line", line)
        line = line[i:]
    lazy_toks = line.split(" ")
        
    if len(lazy_toks) >= 4:
        if lazy_toks[-2] == "as":
            # We don't care how we got here
            final_name = lazy_toks[-1]
            return [final_name]
    if len(lazy_toks) == 2:
        if lazy_toks[0] == "import":
            final_name = lazy_toks[1]
            if "," not in final_name:
                return [final_name]
            else:
                final_names = [ x for x in final_name.split(",") if x != ""]
                return final_names
    
    assert lazy_toks[0] == "import"
    lazy_toks = lazy_toks[1:]
    if lazy_toks[-1].endswith(","):
        print("Needed a continuation line...")
        raise Exception("Fail")
    final_toks = []
    for tok in lazy_toks:
        if "," in tok:
            ntoks = [ x for x in tok.split(",") if x != ""]
            final_toks += ntoks
        else:
            final_toks.append(tok)

    return final_toks

def get_module_names(full_module_name):

    module = importlib.import_module(full_module_name)
    modulename = full_module_name[full_module_name.rfind(".")+1:]
    names = dir(module)
    mod_source = line_source(slurp_source(module.__file__))
    names_imported = []
    while True:
        try:
            line = next(mod_source)
        except StopIteration:
            break
        if "import" in line:
            # Sigh, possibly a comment... Will need to deal with this
            # print("LINE: ", line)
            try:
                parsed = find_imported_names(line, mod_source)
                if parsed:
                    #pass
                    debug("NAMES DEFINED", parsed, line)
                    names_imported += parsed
                    if parsed == ['*']:
                        print("NEED TO TIGHTEN UP IMPORTS", line)
            except ParseFail as e:
                # For now we don't really care
                pass
                # print("FAILED:", e, line)

    module_names = [ x for x in names if x not in names_imported]
    module_names_no_private = [ x for x in module_names if not x.startswith("_") ]
    
    debug("MODULE_NAMES", module_names_no_private)
    debug("IMPORTED NAMES", names_imported)
    
    result = {"modulename" : modulename,
            "full_module_name" : full_module_name,
            "names" : names,
            "names_imported" : names_imported,
            "module_names" : module_names,
            "module_names_no_private" : module_names_no_private,
            }
    return result

def describe_module(mod_info):

    print("---------------------------------------")
    print("Short module name:", mod_info["modulename"])
    print("---------------------------------------")
    print("Full module name:", mod_info["full_module_name"])
    print("---------------------------------------")
    print("Names in the module:", mod_info["names"])
    print("---------------------------------------")
    print("Names imported:", mod_info["names_imported"])
    print("---------------------------------------")
    print("Names defined in module:", mod_info["module_names"] )
    print("---------------------------------------")
    if mod_info["modulename"] in mod_info["names"]:
        other_names = [x for x in mod_info["module_names_no_private"] if x != mod_info["modulename"]]
        firstname = r["modulename"]
    else:
        firstname = ""
        other_names = mod_info["module_names_no_private"]
    print("Useful Names defined in module:", firstname, other_names )
    print("---------------------------------------")

if __name__ == "__main__":

    full_module_name= "Kamaelia.Visualisation.PhysicsGraph.RenderingParticle"
    full_module_name= "Kamaelia.UI.OpenGL.OpenGLComponent"
    full_module_name= "Kamaelia.Chassis.ConnectedServer"
    full_module_name= "Kamaelia.Util.RateFilter"

    # full_module_name= "Kamaelia.IPC"
    # full_module_name= "Kamaelia.Support.Deprecate"

    r = get_module_names(full_module_name)
    describe_module(r)

    testing = False
    if testing:
        source_path = "/home/michael/Development/00_not_as_current/kamaelia/Code/Python/Kamaelia/Kamaelia/Chassis/ConnectedServer.py"
        lines = slurp_source(source_path)

        print("Stripped--------------------------------------------------------------------")
        for line in lines:
            print(line)

        sys.exit(0)
