import pygame
from Axon.Component import component


# Stroke pre-processing

DOT_SEPARATION_THRESHOLD = 5
MAX_STROKE_POINTS = 20

class QuantiseStroke(component):
    """Quantises a stroke into a reduced set of points"""
    Outboxes = { "outbox":"",
                 "drawing":"",
                 "signal":"",
               }
               
    def main(self):
        while 1:
            # wait for first point on path
            ox,oy = None,None
            while (ox,oy) == (None,None):
                if self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    if msg != "ENDSTROKE":
                        ox,oy = msg
                if not self.anyReady():
                    self.pause()
                    yield 1
            
            # subsequent points on path
            points = [(ox,oy)]
            while 1:
                if self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    if msg == "ENDSTROKE":
                        break
                    
                    points.append(msg)
                
                if not self.anyReady():
                    self.pause()
                yield 1
                
            # reduce path to a limited number of points
            if len(points) > MAX_STROKE_POINTS:
                step = float(MAX_STROKE_POINTS) / float(len(points))
                v = 0.0
                newpoints = []
                for point in points:
                    v=v-step
                    if v<=0.0:
                        v=v+1.0
                        newpoints.append(point)
                points = newpoints
                
            for (x,y) in points:
                self.send([["CIRCLE", "255","0","0",str(x),str(y),"1"]], "drawing")
            self.send( points, "outbox" )

        yield 1


def nearest45DegreeStep( (dx,dy) ):
    """Returns (in degrees) the nearest 45 degree angle match to the supplied vector.
    
       Returned values are one of 0, 45, 90, 135, 180, 225, 270, 315.       
       If the supplied vector is (0,0), the returned angle is 0.
    """
    if dx == 0 and dy == 0:
        return 0
    
    # rotate dy and dx by +22.5 degrees,
    # so the boundaries between the 45 degree regions now nicely
    # line up with 0, 45, 90, ... instead of 22.5, 67,5 etc
    
    cos = 0.92387953251128674     # math.cos(math.radians(22.5))
    sin = 0.38268343236508978     # math.sin(math.radians(22.5))
    dx, dy = (dx*cos - dy*sin), (dy*cos + dx*sin)
        
    # lookup angle against properties of dy and dx     
    index = ( dy > 0, dx > 0, abs(dy) > abs(dx) )
    return angleMappings[index]

angleMappings = { (True,  True,  False) : 0,
                  (True,  True,  True ) : 45,
                  (True,  False, True ) : 90,
                  (True,  False, False) : 135,
                  (False, False, False) : 180,
                  (False, False, True ) : 225,
                  (False, True,  True ) : 270,
                  (False, True,  False) : 315 }


class SegmentStroke(component):
    """Takes a quantised stroke and breaks it into line segments"""
    Outboxes = { "outbox":"",
                 "drawing":"",
                 "signal":"",
               }
    def main(self):
        while 1:
            
            if self.dataReady("inbox"):
                points = self.recv("inbox")
                directions = []
                ox,oy = points[0]
                for (x,y) in points[1:]:
                    dx = x-ox
                    dy = y-oy
                    directions.append( nearest45DegreeStep((dx,dy)) )
                    ox,oy = x,y
                    
                # smooth directions
                if len(directions) >= 3:
                    for i in range(1,len(directions)-1):
                        if directions[i] != directions[i-1] and directions[i] != directions[i+1] and directions[i-1] == directions[i+1]:
                            directions[i] = directions[i-1]
                            
                # extract line segments
                segments = []
                sx,sy = points[0]
                sd = directions[0]
                for i in range(1,len(directions)):
                    ex,ey = points[i]
                    if directions[i] != sd:
                        segments.append( ((sx,sy),(ex,ey),sd) )
                        self.send( [["LINE","0","0","255",str(sx),str(sy),str(ex),str(ey)]], "drawing")
                        sx,sy = ex,ey
                        sd = directions[i]
                        # draw a blob too to signify where the join is
                        self.send( [["CIRCLE","0","0","255",str(ex),str(ey),1]], "drawing")
                        
                ex,ey = points[-1]
                segments.append( ((sx,sy),(ex,ey),sd) )
                self.send( [["LINE","0","0","255",str(sx),str(sy),str(ex),str(ey)]], "drawing")
                self.send(segments,"outbox")
                
            if not self.anyReady():
                self.pause()
            yield 1


class Normalise(component):
    """Takes a path and normalises it to a bounding box width and height 1, and also notes the aspect ratio."""
    
    def main(self):
        while 1:
            
            while self.dataReady("inbox"):
                path = self.recv("inbox")
                
                xs = [x for (x,y) in path]
                ys = [y for (x,y) in path]
                
                left   = min(xs)
                right  = max(xs)
                top    = min(ys)
                bottom = max(ys)
                
                width  = max(1.0,float(right-left))
                height = max(1.0,float(bottom-top))
                
                aspect = height/width
                    
                npath = [ ( (x-left)/width, 1.0-(y-top)/height ) for (x,y) in path ]
                self.send( (npath,left,top,width,height,aspect), "outbox" )
                
            self.pause()
            yield 1
