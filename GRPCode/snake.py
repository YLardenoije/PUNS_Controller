#!/usr/bin/env python
from samplebase import SampleBase
import time
import sys
import select
import tty
import termios
import random

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def generateSnack(maxX, maxY):
    x = random.randint(1, maxX - 1)
    y = random.randint(1, maxY - 1)
    return [x, y]

class SnakeDude():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xdir = 0
        self.ydir = 1
        self.length = 7
        self.tail = []
        for i in range(self.length):
            self.tail.append([x-i - 1, y])

    def setMove(self, x, y):
        if x is not self.xdir * -1:
            self.xdir = x
        if y is not self.ydir * -1:
            self.ydir = y

    def getMove(self):
        return self.xdir, self.ydir

    def move(self, xfood, yfood):
        ate = False
        tailBack = self.tail[self.length - 1].copy()
        for i in range(self.length):
            segment = self.length - 1 - i
            if (segment == 0):
                self.tail[segment] = [self.x, self.y]
            else:
                self.tail[segment] = self.tail[segment - 1]

        self.x += self.xdir
        self.y += self.ydir

        if self.x == xfood and self.y == yfood:
            self.tail.append(tailBack)
            self.length += 1
            ate = True

        return ate

    def getHeadPos(self):
        return [self.x, self.y]

    def collidesSelf(self):
        for segment in self.tail:
            if segment[0] == self.x and segment[1] == self.y:
                return True
    
        return False

    def getPositions(self):
        return [[self.x, self.y]] + self.tail

class Snake(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Snake, self).__init__(*args, **kwargs)

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        snek = SnakeDude(16, 16)
        prevUpdate = time.time()
        count = 0
        dirIndex = 0
        snek.setMove(1, 0)
        snack = generateSnack(self.matrix.width, self.matrix.height)
        temppos = 0
        while True:
            if isData():
                c = sys.stdin.read(1)
                if c == 'a':
                    snek.setMove(-1, 0)
                elif c == 'd':
                    snek.setMove(1, 0)
                elif c == 'w':
                    snek.setMove(0, -1)
                elif c == 's':
                    snek.setMove(0, 1)

            canvas.Clear()
            canvas.SetPixel(temppos, temppos, 255, 255, 255)
            for pos in snek.getPositions():
                canvas.SetPixel(pos[0], pos[1], 0, 255, 0)
            canvas.SetPixel(snack[0], snack[1], 255, 0, 0)
            canvas = self.matrix.SwapOnVSync(canvas)
            current = time.time()
            if (current - prevUpdate > 0.05):
                temppos += 1
                if snek.collidesSelf():
                    print("Collided with self, you died!")
                    break
                if snek.move(snack[0], snack[1]):
                    snack = generateSnack(self.matrix.width, self.matrix.height)
                prevUpdate = current



# Main function
if __name__ == "__main__":
    snake = Snake()
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        if (not snake.process()):
            Snake.print_help()

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
