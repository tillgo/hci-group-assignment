from PyQt6.QtCore import QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtWidgets import QFrame

from field import Field
from rules import Rules


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(Field)  # signal sent when there is a new click location
    mouseHoverSignal = pyqtSignal()  # signal sent when mouse is hovering over a field of the board

    illegalMoveColor = "#F32013"

    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from

    def __init__(self, parent, boardArray, currentPieceColor):
        super().__init__(parent)
        self.boardArray = boardArray
        self.currentPieceColor = currentPieceColor

        self.boardSize = len(boardArray)
        self.mouseHoverSignal.connect(self.repaint)
        # Enable Mouse Tracking
        self.setMouseTracking(True)
        self.currentHoverField = None

        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started

        self.initBoard()

    def initBoard(self):
        """initiates board"""
        self.start()  # start the game which will start the timer

    def subscribeToFieldClicked(self, func):
        """
        Subscribe to the signal, triggered if a field on the board is clicked.
        :param func: function to be called, if signal was triggerd. takes a Field as parameter
        """
        self.clickLocationSignal.connect(func)

    def mousePosToColRow(self, event):
        """convert the mouse click event to a row and column"""
        col = round((event.position().x() - self.squareSize() / 2) / self.squareSize())
        row = round((event.position().y() - self.squareSize() / 2) / self.squareSize())
        return Field(col, row)

    def squareSize(self):
        """returns  the size (width and length of a square
        The size is chosen by calculating the maximum possible width and height and picking the smaller one,
        so the squares are actually squares and fit on the screen
        """
        max_width = int(self.contentsRect().width() / self.boardSize)
        max_height = int(self.contentsRect().height() / self.boardSize)
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
        painter = QPainter(self)
        self.updateBoard(self.boardArray, painter)
        painter.end()

    def updateBoard(self, boardArray, painter):
        """paints the board and the pieces of the game"""
        self.drawBoardSquares(painter)
        self.drawPieces(painter, boardArray)
        self.drawHoverSymbol(painter)

    def mouseMoveEvent(self, event):
        col = round((event.position().x() - self.squareSize() / 2) / self.squareSize())
        row = round((event.position().y() - self.squareSize() / 2) / self.squareSize())

        if row < self.boardSize and col < self.boardSize:
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
        field = self.mousePosToColRow(event)
        if field.row < self.boardSize and field.col < self.boardSize:
            self.clickLocationSignal.emit(field)

    def resetGame(self):
        """clears pieces from the board"""
        # TODO write code to reset game

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        squareSize = self.squareSize()
        for row in range(0, self.boardSize - 1):
            for col in range(0, self.boardSize - 1):
                painter.save()
                painter.translate(col * squareSize + squareSize / 2, row * squareSize + squareSize / 2)
                painter.setBrush(QBrush(QColor(255, 255, 255)))  # Set brush color
                painter.drawRect(0, 0, squareSize, squareSize)  # Draw rectangles
                painter.restore()

    def drawPieces(self, painter, boardArray):
        self.boardArray = boardArray
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
            painter.translate(self.currentHoverField.col * self.squareSize() + self.squareSize() / 2,
                              self.currentHoverField.row * self.squareSize() + self.squareSize() / 2)

            isLegalMove = Rules.checkLegalMove(self.boardArray, self.currentHoverField)
            if isLegalMove:
                painter.setBrush(QColor(self.currentPieceColor.color))
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
