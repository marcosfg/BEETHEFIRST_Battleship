import threading
import time
import os
import usb
import math
import re
from beedriver import logger

class BattlePrintThread(threading.Thread):


    def __init__(self,map,printer):

        super(BattlePrintThread, self).__init__()

        self.map = map
        self.printer = printer
        self.done = False

        self.colOffset = 0.0
        self.rowOffset = 0.0
        self.zOffset = 0.5

        self.edgeLength = 10

        return


    def run(self):

        super(BattlePrintThread, self).run()

        #Print Grid
        self.printer.sendCmd('M33 GRID\n')
        self.Wait4PrintDone()

        #Place Ships
        for c in range(len(self.map)):
            for r in range(len(self.map[0])):
                if self.map[c][r] != 0:
                    self.PrintRect(c,r)
                    self.Wait4PrintDone()

        self.done = True

        return

    def Wait4PrintDone(self):

        t = time.time()
        done = False

        while not done:

            if time.time() > t + 1:
                t = time.time()
                if self.printer.getStatus() == 'Ready':
                    done = False

        return


    def PrintRect(self,col,row):

        xPos = self.colOffset + col*self.edgeLength
        yPos = self.rowOffset + row * self.edgeLength

        self.printer.move(z=1,f=1000)
        self.printer.sendCmd('G0 X{} Y{} Z{} F1000'.format(xPos,yPos,self.zOffset))

        self.printer.sendCmd('M33 RECT\n')

        self.Wait4PrintDone()

        return

