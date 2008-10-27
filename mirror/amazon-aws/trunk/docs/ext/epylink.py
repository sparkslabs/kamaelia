# -*- coding: utf-8 -*-
import os
import types
from os.path import join
from stat import ST_MTIME
from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes

EPYDOC_BASE = os.path.abspath('./')


def epydoc_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    name = None
    if text[-1] == '>':
        i = text.index('<')
        name = text[:i - 1]
        text = text[i + 1:-1]
        
    components = text.split('.')

    if name is None:
        name = components[-1]
        
    try:
        for n in range(2, len(components) + 1):
            module = __import__('.'.join(components[:n]))
    except ImportError:
        for component in components[1:n]:
            module = getattr(module, component)
            ref = '.'.join(components[:n])
        if isinstance(module, (type, types.ClassType)):
            ref += '-class.html'
        else:
            ref += '-module.html'
        if n < len(components):
            ref += '#' + components[-1]
    else:
        ref = '.'.join(components) + '-module.html'

    ref = EPYDOC_BASE + '/epydoc/' + ref
    set_classes(options)
    node = nodes.reference(rawtext, name,
                           refuri=ref,
                           **options)
    return [node], []

def setup(app):

    app.add_role('epydoc', epydoc_role)
    #create_png_files()

#def create_png_files():
#    for dirpath, dirnames, filenames in os.walk('.'):
#        for filename in filenames:
#            if filename.endswith('.py'):
#                path = join(dirpath, filename)
#                lines = open(path).readlines()
#                line = lines[0]
#                if 'coding: utf-8' in line:
#                    line = lines[1]
#                if line.startswith('# creates:'):
#                    t0 = os.stat(path)[ST_MTIME]
#                    run = False
#                    for file in line.split()[2:]:
#                        try:
#                            t = os.stat(join(dirpath, file))[ST_MTIME]
#                        except OSError:
#                            run = True
#                            break
#                        else:
#                            if t < t0:
#                                run = True
#                                break
#                    if run:
#                        print 'running:', join(dirpath, filename)
#                        e = os.system('cd %s; python %s' % (dirpath, filename))
#                        if e != 0:
#                            raise RuntimeError('FAILED!')
#                        for file in line.split()[2:]:
#                            print dirpath, file
#                            #os.rename(join(dirpath, file),
#                            #          join('_static', file))
#        if '.svn' in dirnames:
#            dirnames.remove('.svn')
