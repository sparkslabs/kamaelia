import pygame
from PygameComponent import PygameComponent

class Tree(PygameComponent):
    """
    Pygame Component representing a tree of shards.
    The topology of the tree is stored in shardGen objects, which contain the
    constructor arguments for a shard and a list of its children.
    Supports addition, deletion, selection, deselection and relabelling of
    nodes via messages to its inbox. Sending 'generate' to its inbox will
    cause it to generate the code the shard tree represents and write it to
    a default filename (currently ~/<root shard name>.py)
    
    TODO: allow supplying of filepath, node rearranging
    """
    
    configuration = {
       "transparency" : "Colour to be made transparent. None == no colour transparent",
       "boxsize" : "(width,height) representing size of the boxes",
       "width" : "width of the boxes (yes, I know, this *is* in /Sketches right now",
       "height" : "height of the boxes (yes, I know, this *is* in /Sketches right now",
       "hspacing" : "minimum spacing between boxes horizontally",
       "vspacing" : "minimum spacing between boxes vertically",
    }
    transparency = 0xffffff
    boxsize = (100,50)
    width = 100
    hspacing = 10
    height = 50
    vspacing = 50
    
    # assumes use of the following attributes:
    #boxes: shardGen: (x, y) coordinate of box
    #root : root shardgen object
    #selected: shardGen object selected, if any
    
    def generate(self, filepath = None):
        if not self.root:
            return None
        else:
            shard = self.root.makeShard()
            file = shard.writeFile(filepath)
            text = 'code written to '+ file.name + ':\n\n\n'
            text += ''.join(shard.code)
            # display message format for textbox: ['disp', boxtext]
            self.send(['disp', text], 'outbox')
            
            return shard
    
    def removeNode(self, parent, node):
        if node in parent.children:
            parent.children.remove(node)
            for child in parent.children:
                self.removeNode(child, node)

    def reDoTopology(self):
        self.clearDisplay()
        if self.root:
            self.boxes = {}
            self.layout_tree(self.root, 0,100)
            self.drawBox(self.root)        
        self.flip()

    def layout_tree(self, box, wx, wy):
        left = wx
        nw = self.width
        row_below = wy+self.height+self.vspacing
        for subbox in box.children:
            nw = self.layout_tree(subbox, left, row_below)
            left = left + nw+self.hspacing
        if left != wx:
            nw = left-wx-self.hspacing
        self.boxes[box] = wx+(nw/2), wy
        return nw
    
    def clickInBox(self, pos):
        for box in self.boxes:
            if self.boxes[box][0] <= pos[0] <= self.boxes[box][0]+self.boxsize[0]:
                if self.boxes[box][1] <= pos[1] <= self.boxes[box][1]+self.boxsize[1]:
                    return box
        return None # explicit better than implicit

    def select(self, nodeid):
        self.selected = nodeid
        self.send(["SELECT", self.selected ], "outbox")
        self.reDoTopology()

    def deselect(self):
        self.selected = None
        self.send(["DESELECT"], "outbox")
        self.reDoTopology()

    def mousedown_handler(self,*events, **eventd):
        selected = self.selected
        for event in events:
            if event.button == 1:
                nodeid= self.clickInBox(event.pos)
                if nodeid:
                    self.select(nodeid)
                else:
                    self.deselect()

    def main(self):
        """Main loop."""
        yield self.doRequestDisplay((1024, 768))
        self.addHandler(pygame.MOUSEBUTTONDOWN, self.mousedown_handler)

        self.selected = None
        self.reDoTopology()
        while True:
            self._dispatch()
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command[0] == "add":
                    sg, labeltext, parent = command[1:]
                    sg.label = labeltext
                    if not parent:
                        self.root = sg
                    else:
                        parent.children.append(sg)
                if command == 'generate':
                    self.generate()
                if command[0] == "relabel":
                    node, newlabel = command[1:]
                    node.label = newlabel
                if command[0] == "select":
                    nodeid, = command[1:]
                    self.select(nodeid)
                if command[0] == "deselect":
                    self.deselect()
                if command[0] == "del":
                    if command[1] == "all":
                        self.selected = None
                        self.root = None
                        self.boxes = {}
                    if command[1] == "node":
                        try:
                            del self.boxes[command[2]]
                        except KeyError:
                            pass
                        self.removeNode(self.root, command[2])
                self.reDoTopology()
            yield 1


class TreeDraw(object):
    # assumes self.display, self.boxes attributes
    
    def drawBox(self, box):
        if not hasattr(box, 'label'):
            box.label = box.shard.__name__
        colour = 0xaaaaaa
        if box == self.selected :
            colour = 0xff8888
        
        pygame.draw.rect(self.display, colour, (self.boxes[box],self.boxsize), 0)
        cx = self.boxes[box][0]+self.boxsize[0]/2
        cy = self.boxes[box][1]+self.boxsize[1]/2
        image, w,h = self.makeLabel(box.label)
        self.display.blit( image, (cx-w/2,cy-h/2) )
        if box.children:
            self.drawTree(box)
    
    def makeLabel(self, text):
        font = pygame.font.Font(None, 14)
        textimage = font.render(text,True, (0,0,0),)
        (w,h) = textimage.get_size()
        return textimage, w,h
        
    def drawLine(self, line):
        pygame.draw.line(self.display, 0,line[0],line[1],2)

    def drawTree(self, tree): #being added but not drawn
        box = tree
        w = self.boxsize[0]
        h = self.boxsize[1]
        x,y = self.boxes[box]
        paths = []
        for subbox in box.children:
            self.drawBox(subbox)
            ax,ay = self.boxes[subbox]
            paths.append(
                    [
                        (((x+w/2), y+h) , ((x+w/2), y+h+((ay-(y+h))/2) )),  # DOWN
                        (((x+w/2), y+h+((ay-(y+h))/2) ), ((ax+w/2), ay-(ay-(y+h))/2 )), # ACROSS
                        (((ax+w/2), ay-(ay-(y+h))/2 ), ((ax+w/2), ay)),  # DOWN
                    ],
            )

        for path in paths:
            self.drawPath(path)

    def drawPath(self, path):
        for line in path:
            self.drawLine(line)


class BlankTree(Tree, TreeDraw):
    boxes = {}
    root = None
    selected = None


if __name__ == '__main__':
    
    import sys
    
    # example for ShardGen.py: mouse handler from MagnaDoodle
    from MagnaGen import *
    from ShardGen import shardGen
    from ExampleMagnaShards import __INIT__ # needs to be specifically imported

    mh = shardGen(switchShard) # mousehandler
    mh.args['name'] = 'mouseHandler'
    mh.args['switchVar'] = 'event.type'
    mh.args['conditions'] = ['pygame.MOUSEBUTTONDOWN', 'pygame.MOUSEBUTTONUP',
                                              'pygame.MOUSEMOTION']
    mh.args['shards'] = [MOUSEBUTTONDOWN_handler, MOUSEBUTTONUP_handler,
                                       MOUSEMOTION_handler]

    # wrap switch in loop that reads from inbox
    pyl = shardGen(forShard) # pyevent loop
    pyl.args['name'] = 'eventhandler'
    pyl.args['forVars'] = ['event']
    pyl.args['inVar'] = r'self.recv("inbox")'
    pyl.children += [mh]

    # wrap event loop in inbox checking loop so that no invalid reads are performed
    ml = shardGen(whileShard) # mainloop
    ml.args['name'] = 'LoopOverPygameEvents'
    ml.args['condition'] = r'self.dataReady("inbox")'
    ml.children += [pyl]
    
    class PyloopTree(Tree, TreeDraw):
        boxes = {}
        root = ml
        selected = None
            
        def __init__(self):
            super(PyloopTree, self).__init__()
            self.layout_tree(self.root, 0, 100)
    
    
    
    from ShardCompose import *
    
    Graphline(
        CLEAR = Button(caption="Clear", msg=["del", "all"], position=(0,690),size=(64,32)),
        GEN= Button(caption="Generate", msg=["GEN"], position=(70,690),size=(64,32)),
        DEL= Button(caption="Del Node", msg=["DEL"], position=(140,690),size=(64,32)),
        RELABEL= Button(caption="Relabel Node", msg=["RELABEL"], position=(210,690),size=(94,32)),
        CORELOGIC = CoreLogic(),
        TOPOLOGY = PyloopTree(), # sample tree here
        IMP = ImportShardsGUI('/usr/lib/python2.5/site-packages/Kamaelia/Util'),
        CON = ConnectorShardsGUI(items),
        DISP = TextOutputGUI('Generated Code'),
        linkages = {
            ("CLEAR", "outbox"): ("TOPOLOGY","inbox"),
            ("TOPOLOGY","outbox"): ("CORELOGIC", "inbox"),
            ("GEN","outbox"): ("CORELOGIC", "inbox"),
            ("DEL","outbox"): ("CORELOGIC", "inbox"),
            ("RELABEL","outbox"): ("CORELOGIC", "inbox"),
            ("CORELOGIC","outbox"): ("TOPOLOGY", "inbox"),
            ("IMP","outbox"): ("CORELOGIC", "inbox"),
            ("CON","outbox"): ("CORELOGIC", "inbox"),
            ("CORELOGIC","popup"): ("CON", "inbox"),
            ("CORELOGIC", 'textbox'): ('DISP', 'inbox')
        }
    ).run()
