import time
import Tkinter
from PIL import Image, ImageTk

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop() to unblock.

class ST7735S:
    def __init__(self):

        self.w = 128 # Waveshare 1.44 inch LCD usable resolution
        self.h = 128

        self.image_frame = Image.new("RGB", (self.w, self.h), (0,0,0,)) # "black"
        
        self.root = Tkinter.Tk()
#        self.root.overrideredirect(True) # No title bar, no resizing, no possibilities of managing the window
        self.root.bind("<Button>", button_click_exit_mainloop) # unblock mainloop()
        self.root.geometry('%dx%d' % (self.w, self.h))

        
    def _show(self, delay=0.1):
        self.tkpi        = ImageTk.PhotoImage(self.image_frame)
        self.label_image = Tkinter.Label(self.root, image=self.tkpi)
        self.label_image.place(x=0,y=0,width=self.image_frame.width,height=self.image_frame.height)

        self.root.update()
        time.sleep(delay)
        

    def fill(self, color):
        self.image_frame = Image.new("RGB", (self.w, self.h), color)
        self._show(delay=0.04)


    def draw(self, image):
        self.image_frame = image
        self._show()
    
    
    def draw_at(self, image, x=0, y=0):
        width  = min(image.width,  self.w - x)
        height = min(image.height, self.h - y)

        # image crop if it goes beyond the screen (is it needed?)
        image.crop((0,0,width,height))
        
        self.image_frame.paste(image, (x, y))

        # 8FPS x 128x128 = 8x16384 pxls, so 1/131072 = 0.0000076 sec/pixel
        delay = 0.000008 * width * height
        self._show(delay=delay)

    
    def close(self):
        self.fill("white")
