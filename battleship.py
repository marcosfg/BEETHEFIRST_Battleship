import time
from beedriver import connection
from beedriver import logThread
import logging

import random

class battleGame:



    def __init__(self,printer):

        self.cols = 10
        self.rows = 10

        self.colOffset = 0.0
        self.rowOffset = 0.0
        self.zOffset = 0.5

        self.edgeLength = 10

        self.printer = printer

        self.map = [[0 for x in range(self.cols)] for y in range(self.rows)]
        self.playerMap = [['n' for x in range(self.cols)] for y in range(self.rows)]

        return


    def CretateMap(self):

        # 1x 4 pixel size ship
        dim = 4
        done = False
        while(not done):
            done = self.PlaceShip(dim,id=4)

        # 2x 3 pixel size ship
        dim = 3
        for i in range(2):
            done = False
            while (not done):
                done = self.PlaceShip(dim,id=3)

        # 3x 2 pixel size ship
        dim = 2
        for i in range(3):
            done = False
            while (not done):
                done = self.PlaceShip(dim,id=2)

        # 4x 1 pixel size ship
        dim = 1
        for i in range(4):
            done = False
            while (not done):
                done = self.PlaceShip(dim,id=1)

        return

    def PlaceShip(self,dim,id):

        row = 0
        col = 0
        orientation = random.randint(0, 1)
        if orientation == 0:
            row = random.randint(0, 9)
            col = random.randint(0, 10 - dim)
        else:
            row = random.randint(0, 10 - dim)
            col = random.randint(0, 9)


        #Verify if position is already occupied
        for i in range(dim):
            if orientation == 0:
                if self.map[row][col + i] != 0:
                    return False
            else:
                if self.map[row + i][col] != 0:
                    return False

        #Place the ship
        for i in range(dim):
            if orientation == 0:
                self.map[row][col + i] = id
            else:
                self.map[row + i][col] = id

        return True

    def PrintMap(self):

        for c in range(self.cols):
            line = ''
            for r in range(self.rows):
                line += str(self.map[r][c])
            print line + '\n'

        return

    def GetMap(self):

        return self.map

    def Play(self):

        row = -1
        col = -1
        valid = False
        while not valid:
            row = random.randint(0, 9)
            col = random.randint(0, 9)

            if isinstance(self.playerMap[col,row], str):
                self.playerMap[col, row] = 1
                valid = True

        return col,row

    def CheckHit(self,col,row):

        hit = self.map[col][row] > 0
        if hit:
            self.PrintRect(col,row)
            return True

        return False

    def SetHit(self,col,row):

        self.playerMap[col][row] = 1

        return

    def Sum(self):

        sum = 0

        for c in range(len(self.map)):
            for r in range(len(self.map[0])):
                if isinstance(self.playerMap[c][r],int):
                    sum += 1

        return sum

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