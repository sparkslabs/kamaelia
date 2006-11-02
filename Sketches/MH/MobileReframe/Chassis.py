#!/usr/bin/env python

# enhanced chassis with ways to specify limits on inbox sizes
#
# A pipeline where you can optionally preceed each component with a box size, eg:
#
# Pipeline( 5, MyComponent(),           # 'inbox' inbox limited to 5 items
#           2, MyComponent(),           # 'inbox' inbox limited to 2 items
#              MyComponent(),           # 'inbox' inbox unlimited
#           28, MyComponent()           # 'inbox' inbox limited to 28 items
#         )

#
# A graphline where you can specify individual box size restrictions:
#
# Graphline( A = MyComponent(),
#            B = MyComponent(),
#            C = MyComponent(),
#            linkages = { ... },
#            boxsizes = {
#                ("A","inbox") : 5,
#                ("C","control") : 17
#            }
#          )


from Kamaelia.Chassis.Pipeline import Pipeline as _Pipeline

def Pipeline(*components):
    truecomponents = []

    boxsize=False
    for item in components:
        if isinstance(item,int):
            boxsize=item
        elif item is None:
            boxsize=item
        else:
            component=item
            if boxsize != False:
                component.inboxes['inbox'].setSize(boxsize)
                boxsize=False
            truecomponents.append(component)

    return _Pipeline(*truecomponents)



from Kamaelia.Chassis.Graphline import Graphline as _Graphline


def Graphline(linkages = None, boxsizes = None,**components):

    g = _Graphline(linkages,**components)
    
    if boxsizes is not None:
        for ((componentname,boxname),size) in boxsizes.items():
            components[componentname].inboxes[boxname].setSize(size)

    return g
