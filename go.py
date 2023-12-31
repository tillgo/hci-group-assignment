from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer

import PieceColor
from board import Board
from game_controls import GameControls
from game_state import GameState
from main_go_widget import MainGoWidget
from piececonfig import PieceConfig, getOpposite
from rules import Rules
from score_board import ScoreBoard


class Go(QMainWindow):
    timerSignal = pyqtSignal(dict)
    movePlayedSignal = pyqtSignal(dict)

    defaultTime = 120  # the default player time in seconds
    timerSpeed = 1000  # the timer updates every 1 second
    timeIncrement = 5  # the default time increment on a move in seconds

    def __init__(self):
        super().__init__()
        self.gameHistory = []
        self.boardSize = 7
        self.currentPieceColor = PieceConfig.Black

        self.gameHistory.append(self.getDefaultGameState())
        self.currentGameStateIndex = 0
        self.isStarted = False
        self.consecutivePasses = 0

        self.playerTimes = None  # gets set with default game state later
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method

        backgroundTexturePath = "./assets/goboard_background.jpg"
        self.setStyleSheet("background: url({});".format(backgroundTexturePath))

        self.board = Board(self, self.gameHistory[-1].boardArray, self.currentPieceColor,
                           self.onBoardHoverCheckLegalMove, self.onBoardRepaint)
        self.board.subscribeToFieldClicked(self.onBoardFieldClicked)

        # Create GameControls
        self.gameControls = GameControls(self.onUndoMove, self.onRedoMove, self.onResetGame, self.onPass)
        self.gameControls.updateSize(self.board.squareSize())
        self.mainGoWidget = MainGoWidget(self.board, self.gameControls)

        self.setCentralWidget(self.mainGoWidget)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self)

        self.updateBoard()

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

        self.start()

    def getDefaultGameState(self):
        return GameState(None, [[PieceConfig.NoPiece for _ in range(self.boardSize)] for _ in
                                range(self.boardSize)], {PieceConfig.Black: 0, PieceConfig.White: 0},
                         False, {PieceConfig.Black: Go.defaultTime, PieceConfig.White: Go.defaultTime})

    def onBoardRepaint(self, size):
        self.gameControls.updateSize(size)

    def updateBoard(self):
        """
        Update boardArray and currentpiece color, redraw board and  update game controls"""

        self.gameControls.enableUndo()
        self.gameControls.enableRedo()
        if self.currentGameStateIndex == 0:
            self.gameControls.disableUndo()

        if self.currentGameStateIndex >= len(self.gameHistory) - 1:
            self.gameControls.disableRedo()

        self.board.boardArray = self.gameHistory[self.currentGameStateIndex].boardArray
        self.board.currentPieceColor = self.currentPieceColor
        self.playerTimes = self.gameHistory[self.currentGameStateIndex].startTimes.copy()

        self.movePlayedSignal[dict].emit({
            "currentPieceColor": self.currentPieceColor,
            "prisoners": self.gameHistory[self.currentGameStateIndex].prisoners,
            "scores": Rules.calculate_stone_score(self.gameHistory[self.currentGameStateIndex].boardArray),
            "times": self.playerTimes,
        })
        self.board.repaint()

    def start(self):
        self.isStarted = True
        self.timer.start(Go.timerSpeed)

    def timerEvent(self):
        if self.isStarted:
            self.playerTimes[self.currentPieceColor] -= 1
            self.timerSignal[dict].emit(self.playerTimes)
            if self.playerTimes[self.currentPieceColor] <= 0:
                self.endGame(getOpposite(self.currentPieceColor))

    def onBoardFieldClicked(self, field):
        tmpGameHistory = self.gameHistory[:self.currentGameStateIndex + 1]
        currentGameState = tmpGameHistory[-1]
        if Rules.checkLegalMove(self.gameHistory, currentGameState.boardArray, field, self.currentPieceColor):
            self.gameHistory = tmpGameHistory
            newBoardArray = [i.copy() for i in currentGameState.boardArray]
            newBoardArray[field.row][field.col] = self.currentPieceColor
            amountCaptured = Rules.try_captures(newBoardArray, self.currentPieceColor)
            newPrisoners = currentGameState.prisoners.copy()
            newPrisoners[self.currentPieceColor] = newPrisoners[self.currentPieceColor] + amountCaptured
            newTimes = self.playerTimes.copy()
            newTimes[self.currentPieceColor] += self.timeIncrement
            self.gameHistory.append(GameState(
                self.currentPieceColor, newBoardArray, newPrisoners, False, newTimes)
            )
            self.currentGameStateIndex += 1
            self.currentPieceColor = getOpposite(self.currentPieceColor)
            self.consecutivePasses = 0
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
        self.gameHistory.append(self.getDefaultGameState())
        self.currentGameStateIndex = 0
        self.currentPieceColor = PieceConfig.Black
        self.isStarted = True
        self.playerTimes = {
            PieceConfig.Black: Go.defaultTime,
            PieceConfig.White: Go.defaultTime,
        }
        self.consecutivePasses = 0
        self.updateBoard()

    def onPass(self):
        """
        Callback function for board object
        """
        self.gameHistory = self.gameHistory[:self.currentGameStateIndex + 1]
        lastGameState = self.gameHistory[-1]
        newPrisoners = lastGameState.prisoners
        # Give one stone to enemy player (rule if you pass)
        newPrisoners[getOpposite(self.currentPieceColor)] = newPrisoners[getOpposite(self.currentPieceColor)] + 1
        # Create new GameState with unchanged boardArray, updated prisoners and isPass set to True
        newGameState = GameState(self.currentPieceColor, lastGameState.boardArray, newPrisoners, True,
                                 self.playerTimes.copy())
        self.gameHistory.append(newGameState)
        self.currentGameStateIndex += 1
        self.currentPieceColor = getOpposite(self.currentPieceColor)
        self.updateBoard()

        self.consecutivePasses += 1
        if self.consecutivePasses >= 2:
            scores = Rules.calculate_stone_score(self.gameHistory[self.currentGameStateIndex].boardArray)
            winner = PieceConfig.White if scores[PieceConfig.White] >= scores[PieceConfig.Black] else PieceConfig.Black
            self.endGame(winner)
            return

    def onBoardHoverCheckLegalMove(self, field):
        return Rules.checkLegalMove(self.gameHistory[:self.currentGameStateIndex + 1],
                                    self.gameHistory[self.currentGameStateIndex].boardArray, field,
                                    self.currentPieceColor)

    def endGame(self, winner: PieceColor):
        self.isStarted = False
        winnerName = "White" if winner == PieceConfig.White else "Black"
        self.mainGoWidget.showWinningScreen(winnerName, self.newGame)

    def newGame(self):
        self.onResetGame()
        self.mainGoWidget = MainGoWidget(self.board, self.gameControls)
        self.setCentralWidget(self.mainGoWidget)

    def center(self):
        """Centers the window on the screen"""
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
