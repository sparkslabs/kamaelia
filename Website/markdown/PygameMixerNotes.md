---
pagename: PygameMixerNotes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Notes on using the pygame mixer 
===============================

In order to use the pygame mixer in a Kamaelia component there are a
couple of extra steps you need to take to make it initialize properly.
These are necessary so you can use the component in conjuction with the
various pygame UI components, which disable the mixer by default to
allow other sound sources to take control if they need to. The steps to
getting the mixer working are as follows.\
\

### In \_\_init\_\_()

If you call any pygame.mixer methods or objects in your component\'s
\_\_init\_\_() then you initialize the mixer by calling
pygame.mixer.init(). Although you would expect this to keep the mixer
initialized for the main method in some instances this does not happen,
so you also need to make some small changes in your component\'s main
method.\

### in main()

\
If you call any pygame.mixer methods of objects in your component\'s
main() method then you need to initialize the mixer a second (and
potentially third) time. This can be done by adding the following code
the the loop in your component\'s main method.\
\

    def main():
        while 1: #This is your main loop
            if not pygame.mixer.get_init():
             pygame.mixer.init()
         # You are safe to call pygame.mixer methods here
            yield 1 

\
