from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush

from piececonfig import PieceConfig


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        """initiates board"""
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = [[PieceConfig.NoPiece for _ in range(self.boardWidth)] for _ in
                           range(self.boardHeight)]  # TODO - create a 2d int/Piece array to store the state of the game
        self.boardArray[3][3] = PieceConfig.White
        self.boardArray[3][4] = PieceConfig.Black
        self.boardArray[4][4] = PieceConfig.White
        self.printBoardArray()  # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        """prints the boardArray in an attractive way"""
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        """convert the mouse click event to a row and column"""
        pass  # Implement this method according to your logic

    def squareSize(self):
        """returns  the size (width and length of a square
        The size is choosen by calculatin the maximum possible width and height and picking the smaller one,
        so the quares are acutally squares and fit on the screen
        """
        max_width = int(self.contentsRect().width() / self.boardWidth)
        max_height = int(self.contentsRect().height() / self.boardHeight)
        if max_width < max_height:
            return max_width

        return max_height

    def start(self):
        """starts game"""
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, _):
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
        painter.end()

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""
        clickLoc = "click location [" + str(event.x()) + "," + str(
            event.y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
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
                painter.translate(col * squareSize, row * squareSize)
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
                    print(piece.color)
                    painter.translate(col * self.squareSize(), row * self.squareSize())
                    # TODO draw some pieces as ellipses
                    # TODO choose your color and set the painter brush to the correct color
                    radius = int((self.squareSize()) / 2)
                    center = QPoint(0, 0)
                    painter.drawEllipse(center, radius, radius)
                    painter.restore()
