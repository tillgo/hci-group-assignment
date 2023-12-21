from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize

from board import Board
from game_control_toolbar import GameControlToolbar
from game_state import GameState
from piececonfig import PieceConfig, getOpposite
from rules import Rules
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.gameHistory = []
        self.boardSize = 7
        self.currentPieceColor = PieceConfig.Black
        self.defaultGameState = GameState(None, [[PieceConfig.NoPiece for _ in range(self.boardSize)] for _ in
                                                 range(self.boardSize)], {PieceConfig.Black: 0, PieceConfig.White: 0},
                                          False)
        self.gameHistory.append(self.defaultGameState)
        self.currentGameStateIndex = 0

        self.initUI()

    def updateBoard(self):
        """
        Update boardArray and currentpiece color and redraw board
        """
        self.board.boardArray = self.gameHistory[self.currentGameStateIndex].boardArray
        self.board.currentPieceColor = self.currentPieceColor
        self.board.repaint()

    def onBoardFieldClicked(self, field):
        tmpGameHistory = self.gameHistory[:self.currentGameStateIndex + 1]
        currentGameState = tmpGameHistory[-1]
        if Rules.checkLegalMove(self.gameHistory, currentGameState.boardArray, field, self.currentPieceColor):
            self.gameHistory = tmpGameHistory
            newBoardArray = [i.copy() for i in currentGameState.boardArray]
            newBoardArray[field.row][field.col] = self.currentPieceColor
            amountCaptured = Rules.try_captures(newBoardArray, self.currentPieceColor)
            newPrisoners = currentGameState.prisoners.copy()
            newPrisoners[getOpposite(self.currentPieceColor)] = newPrisoners[getOpposite(
                self.currentPieceColor)] + amountCaptured
            self.gameHistory.append(GameState(self.currentPieceColor, newBoardArray, newPrisoners, False))
            self.currentGameStateIndex += 1
            self.currentPieceColor = getOpposite(self.currentPieceColor)
            self.updateBoard()

    def onUndoMove(self):
        """Callback function for board object"""
        if self.currentGameStateIndex > 0:
            self.currentGameStateIndex -= 1

        self.currentPieceColor = getOpposite(self.currentPieceColor)
        self.updateBoard()

    def onRedoMove(self):
        """Callback function for board object"""
        if self.currentGameStateIndex < len(self.gameHistory) - 1:
            self.currentGameStateIndex += 1

        self.currentPieceColor = getOpposite(self.currentPieceColor)
        self.updateBoard()

    def onResetGame(self):
        """Callback function for board object"""
        self.gameHistory = []
        self.gameHistory.append(self.defaultGameState)
        self.currentGameStateIndex = 0
        self.currentPieceColor = PieceConfig.Black
        self.updateBoard()

    def onPass(self):
        """
        Callback function for board object
        """
        self.gameHistory = self.gameHistory[:self.currentGameStateIndex + 1]
        lastGameState = self.gameHistory[-1]
        newPrisoners = lastGameState.prisoners
        # Give one stone to enemy player (rule if you pass)
        newPrisoners[self.currentPieceColor] = newPrisoners[self.currentPieceColor] + 1
        # Create new GameState with with unchanged boardArray, updated prisoners and isPass set to True
        newGameState = GameState(self.currentPieceColor, lastGameState.boardArray, newPrisoners, True)
        self.gameHistory.append(newGameState)
        self.currentGameStateIndex += 1
        self.currentPieceColor = getOpposite(self.currentPieceColor)
        self.updateBoard()

    def onBoardHoverCheckLegalMove(self, field):
        return Rules.checkLegalMove(self.gameHistory[:self.currentGameStateIndex + 1],
                                    self.gameHistory[self.currentGameStateIndex].boardArray, field,
                                    self.currentPieceColor)

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        """Initiates application UI"""
        self.board = Board(self, self.gameHistory[-1].boardArray, self.currentPieceColor,
                           self.onBoardHoverCheckLegalMove)
        self.board.subscribeToFieldClicked(self.onBoardFieldClicked)
        self.setCentralWidget(self.board)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        # Create Toolbar
        self.toolbar = GameControlToolbar(self, self.onUndoMove, self.onRedoMove, self.onResetGame, self.onPass)
        self.toolbar.setIconSize(QSize(30, 30))
        self.toolbar.setStyleSheet("QToolBar{spacing:15px;}")

        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)

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
