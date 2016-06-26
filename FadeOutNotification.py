
from Tkinter import *
import graphics
import time
'''
def present(message, showFor):

    window = Toplevel()

    l = Label(window, text=message)
    l.pack()

    Graphics.centerWindow(window)

    def fade_out():
        alpha = window.attributes("-alpha")
        alpha = max(alpha - .01, 0.0)
        window.attributes("-alpha", alpha)
        if alpha < 1.0:
            window.after(1000, fade_out)

    fade_out()
    
    window.destroy()
'''

def present(root, message, showFor):

    window = FadeToplevel(root, showFor)
    window.wm_title("Incorrect Password")

    l = Label(window, text=message)
    l.pack()

    Graphics.centerWindow(window)

    window.fade_out()


class FadeToplevel(Toplevel):
    '''A toplevel widget with the ability to fade out'''
    def __init__(self, root, showFor):
        Toplevel.__init__(self, root)
        self.attributes("-alpha", 1.0)
        self.showFor = showFor

    def fade_out(self):
        alpha = self.attributes("-alpha")
        alpha = max(alpha - .01, 0.0)
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(self.showFor/10, self.fade_out)
        if alpha == 0:
            self.destroy()