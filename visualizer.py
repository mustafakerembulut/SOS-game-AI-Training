import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import constants
import copy

class Visualizer:
    def __init__(self): # Creating an empty board, if the game will be displayed
        self.emptyBoard = self.drawEmptyBoard()
        self.env = None
        self.selected = False

    def drawEmptyBoard(self):   # Creating empty board
        fnt = ImageFont.truetype("arial.ttf", 50)
        s = 15
        self.menu_gap = constants.MENU_GAP
        size = constants.SIZE
        spacing = constants.SPACING

        image = Image.new("RGBA", (size, size+self.menu_gap))
        drawer = ImageDraw.Draw(image, 'RGBA')
        
        # Drawing vertical lines
        drawer.line([(spacing,self.menu_gap), (spacing, size+self.menu_gap)], fill=None, width=10)
        drawer.line([(spacing*2,self.menu_gap), (spacing*2, size+self.menu_gap)], fill=None, width=10)
        drawer.line([(spacing*3,self.menu_gap), (spacing*3, size+self.menu_gap)], fill=None, width=10)
        drawer.line([(spacing*4,self.menu_gap), (spacing*4, size+self.menu_gap)], fill=None, width=10)
        drawer.line([(spacing*5,self.menu_gap), (spacing*5, size+self.menu_gap)], fill=None, width=10)

        # Drawing horizontal lines
        drawer.line([(0,self.menu_gap), (size, self.menu_gap)], fill=None, width=10)
        drawer.line([(0,spacing+self.menu_gap), (size, spacing+self.menu_gap)], fill=None, width=10)
        drawer.line([(0,spacing*2+self.menu_gap), (size, spacing*2+self.menu_gap)], fill=None, width=10)
        drawer.line([(0,spacing*3+self.menu_gap), (size, spacing*3+self.menu_gap)], fill=None, width=10)
        drawer.line([(0,spacing*4+self.menu_gap), (size, spacing*4+self.menu_gap)], fill=None, width=10)
        drawer.line([(0,spacing*5+self.menu_gap), (size, spacing*5+self.menu_gap)], fill=None, width=10)
        
        counter = 0
        for y in range(6):  # Numerating every square
            for x in range(6):
                drawer.text((x*spacing+s,y*spacing+s+self.menu_gap), f"{counter}", font=fnt)
                counter += 1

        return image    # Returning empty board

    def drawPiecesOnBoard(self, turn, p0Score, p1Score):    # Drawing pieces, turn and scores in empty board
        menu_image = Image.new("RGBA", (constants.SIZE, self.menu_gap-15))  # Creating image of the top menu that shows turn and scores
        drawer = ImageDraw.Draw(menu_image, 'RGBA')
        fnt = ImageFont.truetype("arial.ttf", 100)
        drawer.text((20,30), str(p0Score), font=fnt, fill=(255,0,0))
        drawer.text((constants.SIZE-100,20), str(p1Score), font=fnt, fill=(0,255,0))

        if turn == 0:   # Writing whoes turn
            drawer.text((constants.SIZE//2-self.menu_gap//1.2,20),"Player 1", font=fnt, fill=(255,0,0))
        elif turn == 1:
            drawer.text((constants.SIZE//2-self.menu_gap//1.2,20),"Player 2", font=fnt, fill=(0,255,0))

        boardImage = copy.deepcopy(self.emptyBoard) # Creating board as copy of empty board
        boardImage.paste(menu_image,(0, 10))    # Pasting menu to the board

        for x, row in enumerate(self.env.board):    # Pasting pieces to the board
            for y, square in enumerate(row):
                piece = constants.pieces[square]
                boardImage.paste(piece, (y*constants.SPACING+50, x*constants.SPACING+50+self.menu_gap), piece)

        return boardImage   # Returning current board

    def show(self, turn, p0Score, p1Score, waitTime = constants.WAIT_TIME): # Showing the board that returned by the function "drawPiecesOnBoard"
        self.open_cv_image = np.array(self.drawPiecesOnBoard(turn, p0Score, p1Score))
        cv2.namedWindow('Board', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Board', 9*80,10*80)
        cv2.imshow('Board', self.open_cv_image)
        cv2.waitKey(waitTime)