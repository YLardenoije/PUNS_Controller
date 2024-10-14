from rgbmatrix import RGBMatrix
from rgbmatrix import graphics

class gameObject():
    def __init__(self):
        return
    
    def start(self):
        return
    
    def draw(self, canvas):
        return
    
    def update(self):
        return
    
    def getDrawLayer(self):
        return 0
    
class text(gameObject):
    def __init__(self, drawLayer = 0):
        self.drawLayer = drawLayer
        self.x = 0
        self.y = 32
        self.text = ""
        self.font = graphics.Font()
        self.setColor(241, 93, 3)
        self.setFont("./fonts/spleen-16x32.bdf")
        self.enabled = True

    def setText(self, text):
        self.text = text

    def setFont(self, font):
        self.font.LoadFont(font)

    def setColor(self, r, g, b):
        self.color = graphics.Color(r, g, b)

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def enable(self, enabled):
        self.enabled = enabled

    def getDrawLayer(self):
        return self.drawLayer
    
    def draw(self, canvas):
        graphics.DrawText(canvas, self.font, self.x, self.y, self.color, self.text)

    def update(self):
        return

class textScore(text):
    def __init__(self, drawLayer = 0):
        super(textScore, self).__init__(drawLayer)
        self.score = 0
        self.textScore = 0

    def setScore(self, score):
        self.score = score

    def update(self):
        if self.textScore > self.score:
            self.textScore = self.score
        
        if self.textScore < self.score:
            self.textScore += 10
        
        self.setText("Score: " + str(self.textScore))

class screen():
    def __init__(self):
        self.drawables = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: []
        }
        self.objects = []
    
    def registerObject(self, gameObject):
        self.drawables[gameObject.getDrawLayer()].append(gameObject)
        self.objects.append(gameObject)
        
        gameObject.start()

    def update(self):
        for object in self.objects:
            if (object.enabled):
                object.update()

    def draw(self, canvas):
        for layer in self.drawables:
            for drawing in self.drawables[layer]:
                if (drawing.enabled):
                    drawing.draw(canvas)