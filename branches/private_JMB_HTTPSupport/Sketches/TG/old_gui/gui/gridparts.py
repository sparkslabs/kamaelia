from pygame.color import THECOLORS as colours

class column(object):
    def __init__(self, grid, x, y, width, height, rowheight):
        self.grid = grid
        self.x = x # x, y relative to grid
        self.y = y
        
        self.rowheight = rowheight
        self.rows = [None for _ in range(0, height/rowheight)]
        
        self.width = width
        self.height = self.rows*rowheight
        
        # wrt. x
        self.centre = self.width/2
        self.start = x
        self.end = x + width
        
        self.colour = colours['grey90']
    
    # y is relative to grid
    def contains(self, y):
        return y >= self.y and y < self.y + self.height
    
    def next(self):
        if self.grid.cols[:-1][0] == self:
            return None
        return self.grid.cols[self.grid.cols.index(self)+1]
    
    def rowAt(self, y):
        if self.contains(y):
            return y/self.rowheight # int div
        else: return None
    
    # one of y or row needed
    def add(self, thing, row = None, y = None):
        if row:
            self.rows[row] = thing
        else:
            self.rows[self.rowAt(y)] = thing
    
    def draw(self, surface):
        line(surface, self.colour, (self.start, self.y), (self.start, self.y+height))
        line(surface, self.colour, (self.end, self.y), (self.end, self.y+height))
        
        for i in len(self.rows) + 1:
            y = i*rowheight + self.y
            line(surface, self.colour, (self.start, y), (self.end, y))

class row(object):
    def __init__(self, grid, x, y, height, width, colwidth):
        self.grid = grid
        self.x = x
        self.y = y
        
        self.colwidth = colwidth
        self.cols = [None for _ in range(0, width/colwidth)]
        
        self.height = height
        self.width = self.cols*colwidth
        
        #wrt. y
        self.centre = self.height/2
        self.start = y
        self.end = y + height
        
        self.colour = colours['grey90']
    
    def contains(self, x):
        return x >= self.x and x <= self.x + self.width

    def next(self):
        if self.grid.rows[:-1][0] == self:
            return None
        return self.grid.rows[self.grid.rows.index(self)+1]

    def colAt(self, x):
        if self.contains(x):
            return x/self.colwidth
    
    # one of x or row needed
    def add(self, thing, col = None, x = None):
        if row:
            self.cols[col] = thing
        else:
            self.cols[self.colAt(x)] = thing
    
    def draw(self, surface):
        line(surface, self.colour, (self.x, self.start), (self.x + self.width, self.start))
        line(surface, self.colour, (self.x, self.end), (self.x + self.width, self.end))
        
        for i in len(self.cols) + 1:
            x = i*colwidth + self.y
            line(surface, self.colour, (x, self.start), (x, self.end))

    
    