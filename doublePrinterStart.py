#!/usr/bin/env python
"""
* Copyright (c) 2015 BEEVC - Electronic Systems This file is part of BEESOFT
* software: you can redistribute it and/or modify it under the terms of the GNU
* General Public License as published by the Free Software Foundation, either
* version 3 of the License, or (at your option) any later version. BEESOFT is
* distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
* without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
* PARTICULAR PURPOSE. See the GNU General Public License for more details. You
* should have received a copy of the GNU General Public License along with
* BEESOFT. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "BVC Electronic Systems"
__license__ = ""

import os
import sys
import time
from beedriver import connection
from beedriver import logThread
import logging
import re

import random
import battleship
import BattlePrintThread

# Logger configuration
logger = logging.getLogger('beeconsole')
logger.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# add the handlers to logger
logger.addHandler(ch)



class Printers:

    def __init__(self):
        self.printerConnections = []

    def GetPrinters(self):

        logger.info('Searching for Printers')

        self.connected = False
        self.exit = False
        self.exitState = None

        nextPullTime = time.time() + 1

        while (not self.connected) and (not self.exit):

            t = time.time()

            if t > nextPullTime:
                self.beeConn = connection.Conn()
                printerlist = self.beeConn.getPrinterList();
                logger.info('Found {} printers'.format(len(printerlist)))

                if len(printerlist) >= 2:
                    self.beeConn.connectToPrinter(printerlist[0])
                    self.printerConnections.append(self.beeConn.getCommandIntf())

                    self.beeConn = None
                    self.beeConn = connection.Conn()
                    self.beeConn.connectToPrinter(printerlist[1])
                    self.printerConnections.append(self.beeConn.getCommandIntf())
                    self.connected = True
                else:
                    logger('Not enough printers to start the game. Please connect 2 printers.')
                    self.connected = False

                #self.beeConn.connectToPrinter(printerlist[int(selesctedPrinterIdx)])

                nextPullTime = time.time() + 1

        for p in self.printerConnections:

            mode = p.getPrinterMode()
            if mode == 'Bootloader':
                p.goToFirmware()

        return self.printerConnections



if __name__ == "__main__":

    p = Printers()

    printers = p.GetPrinters()

    logger.info('Creating 1st map')
    firstMap = battleship.battleGame(printers[0])
    firstMap.CretateMap()
    #firstMap.PrintMap()


    logger.info('Creating 2nd map')
    secondMap = battleship.battleGame(printers[1])
    secondMap.CretateMap()

    # Print 1st Map
    firstPrintThread = BattlePrintThread.BattlePrintThread(firstMap.GetMap(),printers[0])
    firstPrintThread.run()

    # Print 1st Map
    secondPrintThread = BattlePrintThread.BattlePrintThread(secondMap.GetMap(),printers[1])
    secondPrintThread.run()

    t = time.time()
    done = False
    while not done:
        if time.time() > t + 1:
            t = time.time()
            if firstPrintThread.done and secondPrintThread.done:
                done = True

    raw_input('Press any key to continue...')

    done = False
    player = random.randint(0, 1)
    while not done:

        if player == 0:
            player = 1
            col,row = secondMap.Play()
            hit = secondMap.CheckHit(col,row)
            if hit:
                secondMap.SetHit(col,row)

            if secondMap.Sum() == 20:
                done = True
                logger.info('Player 0 Wins')
        else:
            player = 0
            col, row = firstMap.Play()
            hit = firstMap.CheckHit(col, row)
            if hit:
                firstMap.SetHit(col, row)

            if firstMap.Sum() == 20:
                done = True
                logger.info('Player 1 Wins')






