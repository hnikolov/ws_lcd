class LCD:
    """ """
    def __init__(self, Waveshare = False):
        if Waveshare == True:   import st7735s      as controller
        else:                   import st7735s_mock as controller

        self.lcd = controller.ST7735S()


    def draw(self, layout):
        self.lcd.draw(layout.get_image_frame())


    def update(self, layout):
        for c in layout.components:
            if c.invalid != 0:
                self.lcd.draw_at(c.image, c.x, c.y)
                c.invalid = 0

   # TODO landscape: self.lcd.set_frame_memory(c.image.transpose(Image.ROTATE_270), c.x, c.y)        
        
    def close(self):
        self.lcd.close()
