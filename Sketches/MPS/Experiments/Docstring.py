#!/usr/bin/python

"""Hello World"""

__doc__ = """Game Over Game Over

Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game 
Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game 
Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game 
Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game 
Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game 
Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game 
Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game Game Over Game 
"""

class michael(object):
    """Yes, we know this is the docstring"""
    
    __doc__ = """This is the documentation however - we've overridden it"""
    
if __name__ == "__main__":
    print __doc__
    print michael.__doc__
