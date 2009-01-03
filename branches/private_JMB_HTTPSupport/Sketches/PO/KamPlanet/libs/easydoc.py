
""" A module to autogenerate HTML documentation from docstrings.
    
    The documentation of this module can be found in 'doc' directory of the
    distribution tarball or at the website of this package.
    Latest versions of this module are also available at that website.

    You can use and redistribute this module under conditions of the
    GNU General Public License that can be found either at
    [ http://www.gnu.org/ ] or in file "LICENSE" contained in the
    distribution tarball of this module.

    Copyright (c) 2001 Tomas Styblo, tripie@cpan.org
    Prague, the Czech Republic

    @name           easydoc
    @version        1.01
    @author-name    Tomas Styblo
    @author-email   tripie@cpan.org
    @website        http://htmltmpl.sourceforge.net/
    @license-name   GNU GPL
    @license-url    http://www.gnu.org/licenses/gpl.html
    @require        htmltmpl ([ http://htmltmpl.sourceforge.net/ ])
"""

__version__ = 1.01
__author__ = "Tomas Styblo (tripie@cpan.org)"

# All imported modules except the 'htmltmpl' module are part of
# the standard Python library.
# The 'easydocp' module is stolen example module from documentation
# of 'parser' module from the standard library.

import sys
import string
import re
import pprint
import copy
import parser
from types import *
from htmltmpl import TemplateCompiler, TemplateProcessor
import easydocp

VERSION = 1.00
KEEP_NEWLINES = 1

##############################################
#               CLASS: Easydoc               #
##############################################

class Easydoc:
    """ Autogenerate documentation from docstrings.    

        This class provides all the functionality of easydoc. You can
        subclass it and override its processing methods module(),
        mclass() and method() to customize its behaviour.
        
        You also can easily use your own template to modify the output
        in any way you need. Output colors can be customized via
        parameters.
    """
    
    def __init__(self, template, debug=0):
        """ Constructor.             

            @header __init__(template, debug=0)
           
            @param template String containing template data.
            
            @param debug Enable or disable debugging messages.
            This optional parameter can be used to enable or disable debugging
            messages which are printed to stderr. By default debugging
            messages are disabled.
        """
        self._debug = debug
        self._classes = []
        self._functions = []
        self._class = {}        
        self._template = TemplateCompiler().compile_string(template)
        self._tproc = TemplateProcessor(html_escape=0)            
                    
    def process(self, module, bgcolor, textcolor, linkcolor, methodbg,
                with_hidden=0):
        """ Create documentation for a module.

            @header process(module, bgcolor, textcolor, linkcolor,
                            with_hidden=0)
            @return String containing the resulting HTML documentation.
            
            @param module Filename of the module to document.
            The module must be specified as filename. The module is not
            imported nor executed, only parsed.

            @param bgcolor Set background color.
            Accepts any valid CSS color value.

            @param textcolor Set text color.
            Accepts any valid CSS color value.

            @param linkcolor Set color of hyperlinks.
            Accepts any valid CSS color value.
            
            @param with_hidden Do not exclude hidden sections from output.
            This optional parameter can be used to force inclusion of
            hidden sections in the resulting documentation. Hidden sections
            are by default not included.            
        """
        mdict = {}
        self._tproc.set("bgcolor", bgcolor)
        self._tproc.set("textcolor", textcolor)
        self._tproc.set("linkcolor", linkcolor)
        self._tproc.set("methodbg", methodbg)

        # Parse the module.
        ast = parser.suite(open(module).read())
        module_info = easydocp.ModuleInfo(ast.totuple())
        self.module(module_info.get_docstring())

        # Class info.
        for mclass in module_info.get_class_names():
            class_info = module_info.get_class_info(mclass)            
            if self.mclass(mclass, class_info.get_docstring(), with_hidden):
                # The class should be included in the output.
                self._class["Methods"] = []
                for method in class_info.get_method_names():
                    method_info = class_info.get_method_info(method)
                    self.method(mclass, method, method_info.get_docstring(),
                                with_hidden)
                self.DEB("Finished class: " + mclass)
                self._classes.append(copy.copy(self._class))
            self._class.clear()                
        self._tproc.set("Classes", self._classes)

        # Functions info.
        for function in module_info.get_function_names():
            function_info = module_info.get_function_info(function)
            self.method("", function, function_info.get_docstring(),
                        with_hidden)
        self._tproc.set("Functions", self._functions)
        
        return self._tproc.process(self._template)

    ##############################################
    #              PRIVATE METHODS               #
    ##############################################

    def module(self, doc):
        """ Process docstring of a module. 
            @hidden
        """
        short, detailed, statements = self.parse(doc)
        self.DEB("Module: short: " + short)
        self.DEB("Module: statements: " + pprint.pformat(statements))

        self._tproc.set("short", short.strip())
        self._tproc.set("Detailed", self.detailed(detailed))

        # Statements.
        requires = []
        for statement in statements:
            param, data = statement
            if param == "name":
                self._tproc.set("name", data.strip())
                self.DEB("Module: name: " + data)
            elif param == "version":
                self._tproc.set("version", data.strip())
            elif param == "website":
                self._tproc.set("website", data.strip())
            elif param == "author-name":
                self._tproc.set("author-name", self.mangle(data))
            elif param == "author-email":
                self._tproc.set("author-email", data.strip())
            elif param == "license-name":
                self._tproc.set("license-name", data.strip())
            elif param == "license-url":
                self._tproc.set("license-url", data.strip())
            elif param == "require":
                requires.append( {"require": self.mangle(data)} )
            else:
                self.warn("Unknown statement: " + param)
        self._tproc.set("Requires", requires)
    
    def mclass(self, name, doc, with_hidden=0):
        """ Process docstring of a class.
            @hidden
        """
        short, detailed, statements = self.parse(doc)
        self.DEB("Class: " + name + ": short: " + short)
        self.DEB("Class: " + name + ": statements: " + \
                 pprint.pformat(statements))

        self._class["name"] = name
        self._class["short"] = short.strip()
        self._class["Detailed"] = self.detailed(detailed)

        for statement in statements:
            param, data = statement
            if param == "hidden":
                if not with_hidden:
                    self.DEB("Class: " + name + ": HIDDEN")
                    return 0
            else:
                self.warn("Unknown statement: " + param)
        else:
            return 1
            
    def method(self, mclass, name, doc, with_hidden=0):
        """ Process docstring of a method.
            @hidden
        """
        method = {}
        short, detailed, statements = self.parse(doc)
        if mclass:
            self.DEB("Method: " + name + ": short: " + short)
            self.DEB("Method: " + name + ": statements: " + \
                     pprint.pformat(statements))
        else:
            self.DEB("Function: " + name + ": short: " + short)
            self.DEB("Function: " + name + ": statements: " + \
                     pprint.pformat(statements))            

        method["name"] = name
        method["class"] = mclass
        method["short"] = short.strip()
        method["Detailed"] = self.detailed(detailed)

        parameters = []
        for statement in statements:
            param, data = statement
            if param == "hidden":
                if not with_hidden:
                    self.DEB("Method: " + name + ": HIDDEN")
                    return 0
            elif param == "header":
                header = data.strip()
                header = re.sub(r"\s+", " ", header)
                method["header"] = header
            elif param == "return":
                method["return"] = self.mangle(data)
            elif param == "param":
                parameter = {}

                # Split the data into first line and rest.
                lines = data.splitlines(KEEP_NEWLINES)
                first_line = lines[0].strip()
                
                # Split the first line into name and short description
                # of the parameter.
                fsplit = first_line.split(" ", 1)
                if len(fsplit) == 2:
                    pname, pshort = fsplit
                elif len(fsplit) == 1:
                    pname = fsplit[0]
                    pshort = ""
                else:
                    pname = ""
                    pshort = ""
                    
                if len(lines) > 1:
                    pdetailed = string.join(lines[1:])
                else:
                    pdetailed = ""

                self.DEB("Parameter: " + pname.strip())
                parameter["name"] = pname.strip()
                parameter["short"] = pshort.strip()
                parameter["Detailed"] = self.detailed(pdetailed)
                parameters.append(parameter)
            else:
                self.warn("Unknown statement: " + param)
        else:
            method["Parameters"] = parameters
            if mclass:
                self._class["Methods"].append(method)
            else:
                self._functions.append(method)
            return 1
                    
    def parse(self, doc):
        """ Parse a docstring.            
            
            Split the docstring into short description, detailed description
            and a list containing a tuple for every statement. The first
            element of the tuple is name of the statement, the second is the
            data of the statement.
            
            @hidden
        """            
        short = ""
        detailed = ""
        statements = []
        if not doc:
            return short, detailed, statements

        doc = doc.replace("\"\"\"", "")

        rc = re.compile(r"""
            ^\s*(@)([-\w]+)
        """, re.VERBOSE | re.MULTILINE)
        tokens = rc.split(doc)
        len_tokens = len(tokens)
        i = 0
        skip_param = 0
        while 1:
            if i == len_tokens:
                break
            if skip_param:
                skip_param = 0
                i += 2
                continue
            token = tokens[i]
            if token == "@":
                skip_param = 1
                param = tokens[i + 1]
                data = tokens[i + 2]
                statements.append((param, data))
            else:
                if not short:
                    lines = token.splitlines(KEEP_NEWLINES)
                    short = lines[0]
                    if len(lines) > 1:
                        detailed = string.join(lines[1:])
            i += 1
        return short, detailed, statements

    def DEB(self, str):
        """ Print debugging message to stderr if debugging is enabled.
            @hidden
        """
        if self._debug: print >> sys.stderr, str

    def warn(self, warning):
        """ Print a warning to stderr.
            @hidden
        """
        print >> sys.stderr, warning

    def mangle(self, str):
        """ Strip leading and trailing whitespace. Convert URL to hyperlink.
            @hidden
        """
        str = str.strip()
        return re.sub(r"\[ (http://.*?) \]",
                      r'<a href="\1">\1</a>', str)

    def detailed(self, str):
        """ Process detailed descritpion.
            
            Split it into paragraphs at empty lines.
            Return list of the paragraphs.
            
            @hidden
        """
        paragraphs = []
        rc = re.compile(r"^\s*$", re.MULTILINE)  # allow any whitespace
        for p in rc.split(str):
            if re.search(r"\S", p):
                paragraphs.append( {"paragraph": self.mangle(p)} )
        return paragraphs

