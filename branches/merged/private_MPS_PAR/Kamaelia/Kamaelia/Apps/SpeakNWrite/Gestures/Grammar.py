# Multistroke grammar processor
# see grammar rules for info

from GrammarRules import *

from Axon.Component import component

class StrokeGrammar(component):
    """\
    Takes output from stroke recogniser and applies grammar rules to combine
    strokes (taking into account spatial position) into output symbols.
    """
    def main(self):
        history = []
        while 1:
            while self.dataReady("inbox"):
                stroke = self.recv("inbox")
                
                history.append(stroke)
                if len(history) > 5:
                    history.pop(0)
                
                noRuleApplied = True
                # try out each rule
                for (newsymbol, rule) in grammar:
                    i = -len(rule)
                    if len(history)<len(rule):
                        continue
                    
                    (symbol,left,top,width,height,aspect) = history[i]
                    
                    # check the first symbol in the sequence matches
                    if symbol != rule[0]:
                        continue
                    
                    # ok, we now need to know (for later) the bounds
                    if aspect > 1.0:
                        # thin and narrow
                        h_ext = height/3.0
                        h_int = width/3.0
                        v_ext = height/3.0
                        v_int = height/3.0
                    else:
                        # fat and wide
                        h_ext = width/3.0
                        h_int = width/3.0
                        v_ext = width/3.0
                        v_int = height/3.0
                    ref_left   = left
                    ref_right  = left+width
                    ref_top    = top
                    ref_bottom = top+height
                    
                    # now go through each term in the rule sequence
                    match = True
                    for (rsymbol,(maxbound,minbound)) in rule[1:]:
                        i=i+1
                        (symbol,left,top,width,height,aspect) = history[i]
                        
                        # check the symbol matches
                        if rsymbol != symbol:
                            match=False
                            break
                        
                        # convert left,top,width,height into bounds
                        bl = self.convert2bound(left,       h_int, h_ext, ref_left, ref_right)
                        br = self.convert2bound(left+width, h_int, h_ext, ref_left, ref_right)
                        bt = self.convert2bound(top,        v_int, v_ext, ref_top,  ref_bottom)
                        bb = self.convert2bound(top+height, v_int, v_ext, ref_top,  ref_bottom)
                        
                        maxl,maxt,maxr,maxb = maxbound
                        if minbound:
                            minl,mint,minr,minb = minbound
                        else:
                            minl = maxr
                            minr = maxl
                            mint = maxb
                            minb = maxt
                        
                        if not (bl>=maxl and bl<=minl):
                            match=False
                            break
                        if not (br<=maxr and br>=minr):
                            match=False
                            break
                        if not (bt>=maxt and bt<=mint):
                            match=False
                            break
                        if not (bb<=maxb and bb>=minb):
                            match=False
                            break
                        
                    if match:
                        # huzzah the rule matched
                        
                        self.send( newsymbol, "outbox")
                        noRuleApplied = False
                   
                if noRuleApplied:
                    # if no rule applied, pass the symbol through
                    # (provided its not a 2 character symbol)
                    if len(history[-1][0]) == 1:
                        self.send( history[-1][0], "outbox")

            self.pause()
            yield 1
            
    def convert2bound(self, value, sf_int, sf_ext, low, high):
        if value<low:
            return 2-int((low-value)/sf_ext)
        elif value>=high:
            return 6+int((value-high)/sf_ext)
        else: # low<=value<high
            return 3+int((value-low)/sf_int)
