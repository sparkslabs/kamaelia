dir = "/home/jlei/Kamaelia/files"

for i in range(1,16):
    imgs.append(dir + '/' + str(i) + '.jpg') 


Graphline(
     CHOOSER  = Chooser(imgs),
     IMAGE    = Image(size=(800,600), position=(8,48)),
     NEXT     = Button(caption="Next",     msg="NEXT", position=(72,8)  ),
     PREVIOUS = Button(caption="Previous", msg="PREV" ,position=(8,8)   ),
     FIRST    = Button(caption="First",    msg="FIRST",position=(256,8) ),
     LAST     = Button(caption="Last",     msg="LAST" ,position=(320,8) ),
     linkages = {
        ("NEXT",     "outbox") : ("CHOOSER", "inbox"),
        ("PREVIOUS", "outbox") : ("CHOOSER", "inbox"),
        ("FIRST",    "outbox") : ("CHOOSER", "inbox"),
        ("LAST",     "outbox") : ("CHOOSER", "inbox"),

        ("CHOOSER",  "outbox") : ("IMAGE",   "inbox"),
     }
).run()
