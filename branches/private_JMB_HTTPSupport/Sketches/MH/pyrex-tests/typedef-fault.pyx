# demonstrates a compilation error with pyrex 0.9.5.1a and 0.9.6.3
# (those are the only two versions this has been tested with)
#
# am 99% sure this used to work under 0.9.4

ctypedef int int_type
ctypedef int_type int2_type

ctypedef enum enum_type:
    AAA
    BBB

ctypedef enum_type enum2_type

def test():
    cdef int_type x
    cdef int2_type y
    x=5
    y=7
    if (x==y):
      x=6

def test2():
    cdef enum_type p
    cdef enum2_type q
    p=AAA
    q=BBB
    if (p==q):
      p=BBB
