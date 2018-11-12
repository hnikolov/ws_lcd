from PIL import Image

class Layout(object):
    def __init__(self, color = "white"):
        self.width  = 128 # Waveshare 1.44 inch LCD
        self.height = 128 

        self.image_frame = Image.new("RGB", (self.width, self.height), color)
        self.components  = []
        

    def add(self, component):
        if isinstance(component, (list,)):
            self.components.extend( component )
        else:
            self.components.append( component )


    def get_image_frame(self):
        for c in self.components:
            self.image_frame.paste(c.image, (c.x, c.y))
            c.invalid = 0

        return self.image_frame


    def round_to(self, value, res):
        """
        Round to e.g., 0.5, 0.02, 10, etc.
        """
        if res == 0:
            return round(value)

        return res * (round(value/res))
