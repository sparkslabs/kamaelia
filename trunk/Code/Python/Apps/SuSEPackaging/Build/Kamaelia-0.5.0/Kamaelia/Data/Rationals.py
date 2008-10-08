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
"""\
=====================================
Rational fraction conversion/handling
=====================================

This set of functions assist in creating rational fractions (numbers represented
by a fraction with an integer numerator and denominator).



Conversion from floating point to rational fraction
---------------------------------------------------

The rational(...) function converts a floating point value to a rational
fraction.

It aims to generate as close an approximation as is reasonably possible, and to
use as small (simple) a numerator and denominator as possible.



Examples
--------

Conversion of a floating point number to a rational fraction::

    >>> rational(0.75)
    (3, 4)

Scale a rational's numerator and denominator to fit within limits::

    >>> limit( (1500,2000), 80, -80)
    (60, 80)

Find the greatest common divisor::

    >>> gcd(18,42)
    6



How does conversion work?
-------------------------

rational(...) uses the "continuous fractions" recursive approximation technique.

The algorithm effectively generates a continuous fractions up to a specified
depth, and then multiplies them out to generate an integer numerator and
denominator.

All depths are tried up to the maximum depth specified. The least deep one that
yields an exact match is returned. This is also the simplest.

The numerator and denominator are simplified further by dividing them by their
greatest common denominator.

For more information on continuous fractions try these:
- http://mathworld.wolfram.com/ContinuedFraction.html
- http://ourworld.cs.com/christopherereed/confracs.htm
- http://www.cut-the-knot.org/do_you_know/fraction.shtml
- http://www.mcs.surrey.ac.uk/Personal/R.Knott/Fibonacci/cfINTRO.html#real
"""


def rational(floatval,maxdepth=10):
    """\
    rational(floatval[,maxdepth]) -> (numerator, denominator)
    
    Convert any floating point value to a best approximation fraction (rational)
      
    maxdepth  -- the maximum recursion depth used by the algorithm (default=10)
    """
    if floatval == 0:
        return (0,1)
    
    sign = 1
    if floatval < 0:
        floatval = -floatval
        sign = -1
        
    num, denom = 1,1
    for depth in range(1,maxdepth):
        num, denom = _f2r(floatval,depth)
        if float(num) / float(denom) == floatval:
            break
        
    div = gcd(num, denom)
    if div > 1:
        num = num / div
        denom = denom / div
        
    return sign * num, denom


def _f2r(v, depth):
    """\
    _f2r(floatval,depth) -> (numerator, denominator)

    Generates a rational fraction representation of a *positive* floating point
    value using the continuous fractions technique to the specified depth.

    Used rational() in preference, to get the most optional match. This function
    does guarantee stopping if an exact match is found. Nor does it simplify the
    resulting fraction.
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
    """gcd(a,b) -> greatest common divisor of a and b"""
    while b != 0:
        a, b = b, a%b
    return a


def limit( rational, poslimit, neglimit):
   """\
   limit((num,denom),poslimit,neglimit) -> (num,denom) scaled to fit within limits

   Scales the fraction (num,demon) so both the numerator and denominator are
   within the specified negative and positive bounds, inclusive.
   """
   n,d = float(rational[0]), float(rational[1])

   divide = max( 1.0,
                 n/poslimit, d/poslimit,
                 n/neglimit, d/neglimit
               )

   if divide > 1.0:
       return int(n/divide), int(d/divide)
   else:
       return rational
