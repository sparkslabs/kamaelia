"""
Importing this module automatically adds to the PYTHONPATH the libraries found in "libs"
"""
import sys, os, os.path

LIBS_DIRECTORY=os.path.dirname(os.path.abspath(__file__)) + os.sep + 'libs'
sys.path.append(LIBS_DIRECTORY)

