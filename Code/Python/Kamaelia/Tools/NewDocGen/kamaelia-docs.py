#!/usr/bin/python

import os
import importlib
import modnames

def has_docstring(thing):
    return getattr(thing, "__doc__", False)

def get_doctype(thing):
    if getattr(thing, "__doctype__", False):
        return getattr(thing, "__doctype__")
    return "text/unknown"

def getdoc(thing):
    doctype = get_doctype(thing)
    doc = getattr(thing, "__doc__", "")
    return (doctype, doc)

package_skiplist = [ "__pycache__", "__init__.py" ]

def get_tree(basename):
    #print("get_tree(", basename, ")" )
    thing = importlib.import_module(basename)
    thing_dir = thing.__path__[0]

    modules = []
    for i in os.listdir(thing_dir):
        if i in package_skiplist:
            continue
        i_path = os.path.join(thing_dir, i)
        if os.path.isdir(i_path):
            subpackage_init_path = os.path.join(i_path, "__init__.py")
            if os.path.exists(subpackage_init_path):
                if os.path.isfile(subpackage_init_path):
                    sub_modules = get_tree(basename + "." + i)
                    modules.extend(sub_modules)

        if os.path.isfile(i_path):
            if i_path.endswith(".py"):
                modules.append(basename + "." + i[:-3])

    modules.sort()
    return modules

def heading_one(text):
    print()
    print("#" * len(text) )
    print(text)
    print("#" * len(text) )
    print()

def heading_two(text):
    print()
    print("*" * len(text) )
    print(text)
    print("*" * len(text) )
    print()

def heading_three(text):
    print(text)
    print("-" * len(text) )
    print()

def describe_name(name, module):
    heading_three(name)
    obj = getattr(module, name)
    hasdocs = False
    if hasattr(obj, "__doc__"):
        if getattr(obj, "__doc__"):
            print(getattr(obj, "__doc__"))
            hasdocs = True
    if not hasdocs:
        print("NO DOCS")
    print()

def describe_module(modulename, mod_info, module, components, component_names):
    #print("-"*100)
    module_names = mod_info["module_names_no_private"]

    heading_one(modulename)

    if hasattr(module, "__doc__"):
        docs = getattr(module, "__doc__")
        if docs:
            print(docs)
        #else:
            #print("NO DOCS")

    if component_names:
        heading_two("Components")
        for name in component_names:
            describe_name(name, module)
        print()

    other_names = []
    for name in module_names:
        if name in component_names:
            continue
        other_names.append(name)

    if other_names:
        heading_two("Other")
        for name in other_names:
            if name in component_names:
                continue
            describe_name(name, module)
#            heading_three(name)
            #print("*", name)

def usage():
    p = sys.argv[0]
    prog = p.split("/")[-1]
    print("Usage:")
    print("   %s package-name" % prog)

if __name__ == "__main__":
    
    import sys
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    docpackage = sys.argv[1]

    print("- %s ---------------------------------------------------------------" % docpackage)
    modules = get_tree(docpackage)
    for modulename in modules:
        try:
            module = importlib.import_module(modulename)
        except NotImplementedError as e:
            #print("* Module", modulename, "has import error", *e.args)
            continue
        components = getattr(module, "__kamaelia_components__", [])
        component_names = []
        if components:
            try:
                [x.__name__ for x in components]
            except TypeError as e:
                print("TYPE ERROR", e)
                raise

            component_names = [x.__name__ for x in components]

        mod_info = modnames.get_module_names(modulename)

        module_names = mod_info["module_names_no_private"]

        strict_subset = True
        for component in component_names:
            if component not in module_names:
                print("component %s not in namespace %s", component, modulename)
                print(module_names)
                print(module.__file__)
                strict_subset = False
                raise ValueError("component %s not in namespace %s", component, modulename)

        #print("Defines:", mod_info["module_names_no_private"])

        doc = module.__doc__

        describe_module(modulename, mod_info, module, components, component_names)

