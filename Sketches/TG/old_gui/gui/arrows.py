from label import label

class forward(label):
    def __init__(self, imname, x = 0, y = 0):
        super(forward, self).__init__(imname, '--->', x, y)
    
    def handleMouseDown(self, e):
        self.container().grid.shardhist.forward()

class back(label):
    def __init__(self, imname, x = 0, y = 0):
        super(back, self).__init__(imname, '<---', x, y)
    
    def handleMouseDown(self, e):
        self.container().grid.shardhist.back()



if __name__ == '__main__':
    from gui import *
    main()