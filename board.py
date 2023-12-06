import typing

from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.uic.properties import QtGui

from field import Field
from game_logic import GameLogic
from piece import Piece
from piececonfig import PieceConfig


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    mouseHoverSignal = pyqtSignal()  # signal sent when mouse is hovering over a field of the board

    illegalMoveColor = "#F32013"

    boardWidth = 7  # board is 7 squares wide
    boardHeight = 7  # board is 7 squares high
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.clickLocationSignal.connect(self.repaint)
        self.mouseHoverSignal.connect(self.repaint)
        # Enable Mouse Tracking
        self.setMouseTracking(True)
        self.boardArray = []
        self.currentHoverField = None
        self.initBoard()

        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.boardArray: list[list[Piece]] = [[]]  # state of the board

        self.initBoard()

    def initBoard(self):
        """initiates board"""
        self.start()  # start the game which will start the timer

        self.boardArray = [[PieceConfig.NoPiece for _ in range(self.boardWidth)] for _ in
                           range(self.boardHeight)]
        self.boardArray[3][3] = PieceConfig.White
        self.boardArray[3][4] = PieceConfig.Black
        self.boardArray[4][4] = PieceConfig.White
        self.printBoardArray()  # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        """convert the mouse click event to a row and column"""
        pass  # Implement this method according to your logic

    def squareSize(self):
        """returns  the size (width and length of a square
        The size is chosen by calculating the maximum possible width and height and picking the smaller one,
        so the squares are actually squares and fit on the screen
        """
        max_width = int(self.contentsRect().width() / self.boardWidth)
        max_height = int(self.contentsRect().height() / self.boardHeight)
        return min(max_height, max_width)

    def pieceRadius(self):
        return int(self.squareSize() / 2 - 20)

    def start(self):
        """starts game"""
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        """this event is automatically called when the timer is updated. based on the timerSpeed variable """
        # TODO adapt this code to handle your timers
        if Board.counter == 0:
            print("Game over")
        self.counter -= 1
        print('timerEvent()', self.counter)
        self.updateTimerSignal[int].emit(self.counter)

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)
        self.drawHoverSymbol(painter)
        painter.end()

    def mouseMoveEvent(self, event):
        col = round((event.position().x() - self.squareSize() / 2) / self.squareSize())
        row = round((event.position().y() - self.squareSize() / 2) / self.squareSize())

        if row < len(self.boardArray) and col < len(self.boardArray[0]):
            self.currentHoverField = Field(col, row)
        else:
            self.currentHoverField = None

        self.mouseHoverSignal.emit()

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""
        clickLoc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        col = round((event.position().x() - self.squareSize() / 2) / self.squareSize())
        row = round((event.position().y() - self.squareSize() / 2) / self.squareSize())
        print("locations")
        print(self.squareSize())
        print(col)
        print(row)
        if GameLogic.checkLegalMove(self.boardArray, Field(col, row)):
            self.boardArray[row][col] = PieceConfig.Black
            self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        """clears pieces from the board"""
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        """tries to move a piece"""
        pass  # Implement this method according to your logic

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        squareSize = self.squareSize()
        for row in range(0, len(self.boardArray) - 1):
            for col in range(0, len(self.boardArray[0]) - 1):
                painter.save()
                painter.translate(col * squareSize + squareSize / 2, row * squareSize + squareSize / 2)
                painter.setBrush(QBrush(QColor(255, 255, 255)))  # Set brush color
                painter.drawRect(0, 0, squareSize, squareSize)  # Draw rectangles
                painter.restore()

    def drawPieces(self, painter):
        """draw the pieces on the board"""
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                piece = self.boardArray[row][col]
                if piece.color:
                    painter.save()
                    painter.setBrush(QColor(piece.color))
                    painter.translate(col * self.squareSize() + self.squareSize() / 2,
                                      row * self.squareSize() + self.squareSize() / 2)
                    # TODO draw some pieces as ellipses
                    # TODO choose your color and set the painter brush to the correct color
                    radius = self.pieceRadius()
                    center = QPoint(0, 0)
                    painter.drawEllipse(center, radius, radius)
                    painter.restore()

    def drawHoverSymbol(self, painter):
        if self.currentHoverField:
            painter.save()
            painter.translate(self.currentHoverField.x * self.squareSize() + self.squareSize() / 2,
                              self.currentHoverField.y * self.squareSize() + self.squareSize() / 2)

            isLegalMove = GameLogic.checkLegalMove(self.boardArray, self.currentHoverField)
            if isLegalMove:
                # ToDo Set here the brush color to the color whose turn it currently is
                radius = self.pieceRadius()
                center = QPoint(0, 0)
                painter.drawEllipse(center, radius, radius)

            else:
                cross_size = self.pieceRadius()
                # Draw first diagonal line
                pen = QPen(QColor(self.illegalMoveColor))
                pen.setWidth(4)
                painter.setPen(pen)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.drawLine(0 - cross_size, 0 - cross_size, 0 + cross_size, 0 + cross_size)
                painter.drawLine(0 - cross_size, 0 + cross_size, 0 + cross_size, 0 - cross_size)

            painter.restore()
