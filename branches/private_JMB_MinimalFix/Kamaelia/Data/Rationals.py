#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

# Functions for assisting with creating rational fractions (numbers represented
# by a fraction, consisting of an integer numerator and denominator)
#
# In particular, conversion from a floating point value to a (rational) fraction
# ... or at least as close an approximation as reasonably possible!
#
# rational(...) - convert a floating point value to a rational
# gcd(...)      - guess!
# limit(...) - limit a rational's numerator and denominator to within bounds

def rational(floatval,maxdepth=10):
    """Convert any floating point value to a best approximation fraction (rational)
      floatval = floating point value
      maxdepth = maximum recursion depth.
    Returns (integer numerator, integer denominator)
    """
    if floatval == 0:
        return (0,1)
    
    sign = 1
    if floatval < 0:
        floatval = -floatval
        sign = -1
        
    num, denom = 1,1
    for depth in range(1,maxdepth):
        num, denom = f2r(floatval,depth)
        if float(num) / float(denom) == floatval:
            break
        
    div = gcd(num, denom)
    if div > 1:
        num = num / div
        denom = denom / div
        
    return sign * num, denom


def f2r(v, depth=5):
    """Recursive approximation of a rational fraction representation of a POSITIVE
    floating point value. (Utilises continuous fractions based approximation)
    
      v = floating point value to approximate
      depth = maximum recursion depth

    Used rational() in preference. This function does not necessarily stop if an exact match is
    found. rational() checks for this, and also simplifies the rational by finding the greatest
    common divisors.
    """
    numerator = 1
    denominator = int(1.0/v)

    if depth > 0 and v > 0:
        depth -= 1
        
        frac = v % 1
        whole = int(v - frac)

        if frac > 0:
            fracdenominator, fracnumerator = f2r(1.0/frac, depth)
            numerator = whole * fracdenominator + fracnumerator
            denominator = fracdenominator
        else:
            numerator = v
            denominator = 1

    return numerator, denominator

        
def gcd(a,b):
    """Find greatest common divisor"""
    while b != 0:
        a, b = b, a%b
    return a


def limit( rational, poslimit, neglimit):
   """Limit the values of the numerator and denominator of a rational to
   be within the specified negative and positive bounds, inclusive.

   Useful if either value is too large to be coerced into a limited range
   data type (eg. a 'C' integer)
   """
   n,d = float(rational[0]), float(rational[1])

   divide = max( 1.0,
                 n/poslimit, d/poslimit, divide,
                 n/neglimit, d/neglimit, divide
               )

   if divide > 1.0:
       return int(n/divide), int(d/divide)
   else:
       return rational
