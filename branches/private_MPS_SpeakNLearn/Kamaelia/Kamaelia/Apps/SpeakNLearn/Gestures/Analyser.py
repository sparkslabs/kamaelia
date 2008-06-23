# core stroke analyser

from Axon.Component import component




from Patterns import *

MIN_SIZE_THRESHOLD=8
DIVERGENCE_CURVE_IDEAL = ((2**0.5) - 1)**2     # peak expected divergence assuming moving through a 1/4 circle arc

class Analyse(component):
    """Takes a quantised stroke and attempts to match it against letter shapes"""
                
    Outboxes = { "outbox":"",
                 "drawing":"",
                 "signal":"",
               }
    debug = False

    
    def main(self):
        while 1:
            
            while self.dataReady("inbox"):
                npath,left,top,width,height,aspect = self.recv("inbox")
                
                if width<MIN_SIZE_THRESHOLD and height<MIN_SIZE_THRESHOLD:
                    self.send( (".", left,top,width,height,aspect), "outbox")
                    continue
                
                # normalise to aspect ratio
                sx = (width/height)**0.5
                sy = (height/width)**0.5
                
                for i in range(0,len(npath)):
                    npath[i] = (sx*npath[i][0], sy*npath[i][1])
                    
                # recalibrate width and height, compensating for aspect ratio normalisation
                sw = width/sx
                sh = height/sy
                
                scores = {}
                for symbol in patterns:
                    for (params,pattern) in patterns[symbol]:
                        max_aspect, min_aspect = params
                        
                        if aspect>max_aspect or aspect<min_aspect:
                            continue
                        
                        # normalise to aspect ratio
                        pattern = [(sx*x,sy*y,divtype) for (x,y,divtype) in pattern]
                        
                        points = []
                        score = 0.0
                        
                        # trace along the path, comparing against the pattern points
                        i = 0  # index along user stroke
                        j = 0  # index along the pattern
                        closest = 999999.0
                        closest_i = 0
                        oldproxCURR = 999999.0
                        oldproxNEXT = 999999.0
                        while 1:
                            # how close are we to the current point along the pattern?
                            dx = pattern[j][0] - npath[i][0]
                            dy = pattern[j][1] - npath[i][1]
                            proxCURR = dx*dx + dy*dy
                            
                            # how close are we to the next point along the pattern?
                            if j<len(pattern)-1:
                                dx2 = pattern[j+1][0] - npath[i][0]
                                dy2 = pattern[j+1][1] - npath[i][1]
                                proxNEXT = dx2*dx2 + dy2*dy2
                            
                            if not proxNEXT < proxCURR:
                                # closer to current point on pattern than next one
                                
                                # closer than before?
                                if proxCURR < closest:
                                    closest = proxCURR
                                    closest_i = i
                                    
                                # move onto next
                                i=i+1
                                if i==len(npath):
                                    # end of path
                                    score = score + closest
                                    #log point on path
                                    points.append((closest_i,j))
                                    
                                    # penalise score for any left-overs in the pattern
#                                    score = score + 1.0*(len(pattern)-1-j)
                                    furthest = closest
                                    while j<len(pattern):
                                        dx = pattern[j][0] - npath[-1][0]
                                        dy = pattern[j][1] - npath[-1][1]
                                        prox = dx*dx + dy*dy
                                        if prox>furthest:
                                            furthest = prox
                                        score = score + 1.5*furthest  # multiply up to fake in some divergence
                                        j=j+1
                                    break
                            else: # if we're actually now closer to the NEXT point on the pattern
                                # if we're further away from both than before
                                if oldproxCURR < proxCURR and oldproxNEXT < proxNEXT:
                                    closest = proxCURR
                                    closest_i = i
                                    i=i+1
                                    if i==len(npath):
                                        score = score + closest
                                        #log point on path
                                        points.append((closest_i,j))
                                        # penalise score for any left-overs in the pattern
                                        furthest = closest
                                        while j<len(pattern):
                                            dx = pattern[j][0] - npath[-1][0]
                                            dy = pattern[j][1] - npath[-1][1]
                                            prox = dx*dx + dy*dy
                                            if prox>furthest:
                                                furthest = prox
                                            score = score + 1.5*furthest  # multiply up to fake in some divergence
                                            j=j+1
                                        break
                                else:
                                    # we must be moving closer to the next point
                                    
                                    # so the closest we got to the previous point
                                    # is deemed a match, and we'll add that proximity
                                    # as its 'accuracy of match' score
                                    score = score + closest
                                    #log point on path
                                    points.append((closest_i,j))
                                    
                                    # now switch to the next point
                                    closest = proxNEXT
                                    closest_i = i
                                    # reset prox'es so next values of oldprox'es are sensible
                                    proxCURR = proxNEXT
                                    proxNEXT = 999999.0
                                    j=j+1
                                    if j==len(pattern):
                                        # we've reached the end of the pattern path
                                        # compare remaining stroke points for distance
                                        # from the end of the pattern path
                                        while i<len(npath):
                                            dx = pattern[-1][0] - npath[i][0]
                                            dy = pattern[-1][1] - npath[i][1]
                                            score = score + 1.5*(dx*dx + dy*dy) # multiply up to fake in some divergence
                                            i=i+1
                                        break
                            oldproxCURR = proxCURR
                            oldproxNEXT = proxNEXT
                        
                        # add start and finish point proximities
                        # (thereby doubling the weighting of them)
                        dx = pattern[0][0] - npath[0][0]
                        dy = pattern[0][1] - npath[0][1]
                        score = score + (dx*dx + dy*dy)
                        dx = pattern[-1][0] - npath[-1][0]
                        dy = pattern[-1][1] - npath[-1][1]
                        score = score + (dx*dx + dy*dy)
                        
                        divergence_diagnostics = []
                        if len(points):
                            # sort out missing start and end of path
                            if points[0][0] != 0:
                                points.insert(0,(0,0))
                            if points[-1][0] != len(npath)-1:
                                points.append( (len(npath)-1, len(pattern)-1) )
                                
                            # trace along the path and verify that the direction of curvature is the
                            # same for the middle sections of the paths between each pattern matched point
                            for p in range(1,len(points)):
                                starti = points[p][0]
                                endi   = points[p-1][0]
                                if starti-endi >= 5:
                                    for i in range(starti+1,endi-1):
                                        dx  = npath[i+1][0] - npath[i][0]
                                        dy  = npath[i+1][1] - npath[i][1]
                                        pdx = npath[i+2][0] - npath[i+1][0]
                                        pdy = npath[i+2][1] - npath[i+1][1]
                                        
                                        # determine direction in which the path is curving - to the right or left?
                                        if dx==0:
                                            RHS = pdx > 0
                                        elif dx>0:
                                            RHS = pdy < (dy/dx)*pdx
                                        elif dx<0:
                                            RHS = pdy > (dy/dx)*pdx
                                            
                                        if i>starti+1:
                                            if (not RHS) != (not prevRHS):
                                               score=score+1.0
                                            
#                                         # determine if there is a sudden double backing in the path
#                                         if -dy==0:
#                                             FWD = pdx > 0
#                                         elif -dy>0:
#                                             FWD = pdy < (dx/-dy)*pdx
#                                         elif -dy<0:
#                                             FWD = pdy > (dx/-dy)*pdx
#                                             
#                                         if not FWD:
#                                             score=score+1.0
                                            
                                        prevRHS = RHS
                            
#                             # now trace along the path and verify that the shape of the pattern is followed
#                             oldnx,oldny = npath[points[0][0]]
#                             oldpx, oldpy = pattern[points[0][1]][0:2]
#                             for p in range(1,len(points)):
#                                 nx, ny = npath[points[p][0]]
#                                 px, py = pattern[points[p][1]][0:2]
#                                 
#                                 if px > oldpx:
#                                     if not nx > oldnx:
#                                         score=score+1.0
#                                 elif px < oldpx:
#                                     if not nx < oldnx:
#                                         score=score+1.0
#                                 
#                                 if py > oldpy:
#                                     if not ny > oldny:
#                                         score=score+1.0
#                                 elif py < oldpy:
#                                     if not ny < oldny:
#                                         score=score+1.0
#                                 
#                                 oldnx, oldny = nx, ny
#                                 oldpx, oldpy = px, py
                                
                            
                        
                            # now trace along path and measure divergence of each segment
                            
                            # go through segments, calculating divergence
                            for p in range(1,len(points)):
                                # measure divergence from a straight line and penalise score if different from expected
                                rval = self.measurePathDivergence(npath,points[p-1][0],points[p][0],None)
                                lhs, rhs, diagnostics = rval
                                divergence_diagnostics.extend(diagnostics)
                                
                                # if specified divergence type is of the wrong sign, then penalise for it
                                dtype = pattern[points[p][1]][2]
                                if dtype > 0:
                                    dscore = 2*lhs #+ max(0.0, abs(rhs-DIVERGENCE_CURVE_IDEAL))
                                elif dtype < 0:
                                    dscore = 2*rhs #+ max(0.0, abs(lhs-DIVERGENCE_CURVE_IDEAL))
                                else:
                                    dscore = lhs + rhs
                                
                                score = score + 2*dscore
                        
                        # normalise to path length (+weightings)
                        score = score/(len(pattern)+1)
                        
                        # record symbol against score
                        scores[score] = symbol,points,pattern,divergence_diagnostics
                    
                # identify the best match
                if scores:
                    
                    bestscore = min(scores)
                    symbol,points,pattern,diagnostics = scores[bestscore]
                    self.send( (symbol,left,top,width,height,aspect) , "outbox")
#                    print bestscore
                    
                    # output some useful diagnostic drawing
                    if self.debug:
                        # draw the matched points along the user stroke
                        ox=None
                        oy=None
                        i=0
                        for (p,j) in points:
                            x = int(npath[p][0]*sw + left)
                            y = int((sy-npath[p][1])*sh + top)
                            if ox==None:
                                ox,oy = x,y
                            self.send( [["CIRCLE","0","160","0",str(x),str(y),4],
                                        ["LINE","160","255","160",str(ox),str(oy),str(x),str(y)],
                                        ["WRITE", str(x), str(y), "16", "0", "160", "0", str(p)]
                                    ], "drawing")
                            ox,oy = x,y
                            i=i+1
                    if self.debug:
                        # draw points of the matched pattern
                        i=0
                        ox=None
                        oy=None
                        for (x,y,_) in pattern:
                            x = int(x*sw + left)
                            y = int((sy-y)*sh + top)
                            if ox==None:
                                ox,oy = x,y
                            self.send( [["CIRCLE","255","160","0",str(x),str(y),2],
                                        ["LINE","255","192","160",str(ox),str(oy),str(x),str(y)],
    #                                    ["WRITE", str(x), str(y), "16", "255", "160", "0", str(i)],
                                    ], "drawing")
                            ox,oy = x,y
                            i=i+1
                        
                        self.send( [["WRITE","32","00","14","255","160","160","Stroke"],
                                    ["WRITE","32","10","14","160","255","160","Stroke segmented"],
                                    ["WRITE","32","20","14","255","192","160","Matched pattern"],
                                    ["WRITE","8","0","32","0","0","0",symbol],
                                ], "drawing")
                    
                    if self.debug:
                        # draw path divergence diagnostics
                        for ((px,py),(cx,cy)) in diagnostics:
                            px = int(sw*px + left)
                            py = int((sy-py)*sh + top)
                            cx = int(sw*cx + left)
                            cy = int((sy-cy)*sh + top)
                            self.send( [["LINE","0","0","0",str(px),str(py),str(cx),str(cy)]], "drawing")
                    
                    if self.debug:
                        # draw little bargraphs showing the relative responses
                        bheight = 100.0
                        bbottom = 364
                        ratings = [(s, scores[s][0]) for s in scores.keys()]
                        ratings.sort()
                        x=4
                        for r,symbol in ratings:
                           t = int(bbottom - abs(bheight/r*ratings[0][0]))
                           self.send( [["LINE","0","0","0",str(x),str(bbottom),str(x),str(t)],
                                       ["LINE","0","0","0",str(x+1),str(bbottom),str(x+1),str(t)],
                                       ["LINE","0","0","0",str(x+2),str(bbottom),str(x+2),str(t)],
                                       ["LINE","0","0","0",str(x+3),str(bbottom),str(x+3),str(t)],
                                       ["WRITE",str(x),str(bbottom),"16","0","0","0",symbol]
                                      ], "drawing")
                           x=x+16
                    
            self.pause()
            yield 1

    def measurePathDivergence(self,npath,start_i,end_i,expected):
        diagnostics = []
        # we plot the line between teh start and end points (closest_i --> i)
        dx = npath[end_i][0] - npath[start_i][0]
        dy = npath[end_i][1] - npath[start_i][1]
        lengthsquared = max(0.01, dx*dx + dy*dy)
        
        lhs_divergence = 0.0
        rhs_divergence = 0.0
        n=0
        # for each point start_i < i < end_i
        for i in range(start_i+1,end_i):
            n=n+1
            
            px = npath[i][0] - npath[start_i][0]
            py = npath[i][1] - npath[start_i][1]
            # find closet point on the line
            if dx == 0:
                cx=0
                cy=py
            elif dy==0:
                cx=px
                cy=0
            else: # line not dead horizontal or vertical
                cx = (py + px*dx/dy)/(dy/dx + dx/dy)
                cy = py + (dx/dy)*(px-cx)
            # measure distance^2 from the line to the point
            pdx = px-cx
            pdy = py-cy
            distsquared = pdx*pdx + pdy*pdy
            # normalise against length of line
            distsquared = distsquared / lengthsquared
            
            # which side of the line is it on? right hand side, or left?
            if dx==0:
                RHS = pdx > 0
            elif dx>0:
                RHS = pdy < (dy/dx)*pdx
            elif dx<0:
                RHS = pdy > (dy/dx)*pdx
                
            if RHS:
                rhs_divergence = max(rhs_divergence,distsquared)
            else:
                lhs_divergence = max(lhs_divergence,distsquared)
            
            px = px + npath[start_i][0]
            py = py + npath[start_i][1]
            cx = cx + npath[start_i][0]
            cy = cy + npath[start_i][1]
            diagnostics.append( ((px,py),(cx,cy)) )

        return ( lhs_divergence,
                 rhs_divergence,
                 diagnostics
               )
