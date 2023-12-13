from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt

from board import Board
from piececonfig import PieceConfig
from rules import Rules
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.gameHistory = []
        self.boardSize = 7
        self.gameHistory.append([[PieceConfig.NoPiece for _ in range(self.boardSize)] for _ in
                                 range(self.boardSize)])
        self.currentPieceColor = PieceConfig.Black

        self.initUI()

    def onBoardFieldClicked(self, field):
        currentBoardArray = self.gameHistory[-1]
        if Rules.checkLegalMove(currentBoardArray, field):
            newBoardArray = currentBoardArray.copy()
            newBoardArray[field.row][field.col] = self.currentPieceColor
            amountCaptured = Rules.try_captures(newBoardArray, self.currentPieceColor)
            self.gameHistory.append(newBoardArray)
            self.board.boardArray = newBoardArray
            self.board.repaint()
            self.currentPieceColor = PieceConfig.White if self.currentPieceColor is PieceConfig.Black \
                else PieceConfig.Black
            self.board.currentPieceColor = self.currentPieceColor

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        """Initiates application UI"""
        self.board = Board(self, self.boardArray, self.currentPieceColor)
        self.board.subscribeToFieldClicked(self.onBoardFieldClicked)
        self.setCentralWidget(self.board)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        """Centers the window on the screen"""
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
