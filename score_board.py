from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QFormLayout
from PyQt6.QtCore import pyqtSlot

from game_instruction_button import GameInstructionButton
from piececonfig import PieceConfig


def seconds_to_mm_ss(time_in_seconds):
    """
    This method takes seconds as input and converts them to mm:ss format string
    """
    # Calculate minutes and seconds
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60

    # Format the result as mm:ss
    return "{:02d}:{:02d}".format(minutes, seconds)


class ScoreBoard(QDockWidget):
    """base the score_board on a QDockWidget"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('ScoreBoard')

        with open('./assets/styles/score_board.css', 'r') as file:
            self.setStyleSheet(file.read())

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)
        self.setFixedWidth(200)

        # create VBoxes for each player / color
        whiteBox = QVBoxLayout()
        blackBox = QVBoxLayout()

        # create a form layout each, to hold score and prisoners
        whiteScore = QFormLayout()
        blackScore = QFormLayout()

        # create labels for scores and prisoners
        self.whiteEstimate = QLabel("0", objectName="score")
        self.blackEstimate = QLabel("0", objectName="score")
        self.whitePrisoners = QLabel("0", objectName="score")
        self.blackPrisoners = QLabel("0", objectName="score")

        # add scores and prisoners to the formLayouts
        whiteScore.addRow(QLabel("Score:", objectName="l"), self.whiteEstimate)
        whiteScore.addRow(QLabel("Prisoners:", objectName="l"), self.whitePrisoners)
        blackScore.addRow(QLabel("Score:", objectName="l"), self.blackEstimate)
        blackScore.addRow(QLabel("Prisoners:", objectName="l"), self.blackPrisoners)

        # create labels for the timer
        self.timeWhite = QLabel(seconds_to_mm_ss(120), objectName="whiteTimer")
        self.timeBlack = QLabel(seconds_to_mm_ss(120), objectName="blackTimer")

        # add timer and score layouts to the boxes
        whiteBox.addWidget(self.timeWhite)
        whiteBox.addLayout(whiteScore)
        blackBox.addLayout(blackScore)
        blackBox.addWidget(self.timeBlack)

        btnGameInstructions = GameInstructionButton()

        # add layouts to main layout
        self.mainLayout.addLayout(whiteBox)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(btnGameInstructions)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(blackBox)

    def make_connection(self, go):
        """this method is called to subscribe the scoreboard to go events"""
        go.timerSignal.connect(self.setTimeRemaining)
        go.movePlayedSignal.connect(self.updateScoreboard)

    @pyqtSlot(dict)
    def setTimeRemaining(self, playerTimes):
        """updates the time remaining label to show the time remaining"""
        self.timeWhite.setText(seconds_to_mm_ss(playerTimes[PieceConfig.White]))
        self.timeBlack.setText(seconds_to_mm_ss(playerTimes[PieceConfig.Black]))

    @pyqtSlot(dict)
    def updateScoreboard(self, data):
        """
        updates the scores, prisoners, times and current player
        """
        times = data["times"]
        self.setTimeRemaining(times)

        scores = data["scores"]
        self.whiteEstimate.setText(str(scores[PieceConfig.White]))
        self.blackEstimate.setText(str(scores[PieceConfig.Black]))

        prisoners = data["prisoners"]
        self.whitePrisoners.setText(str(prisoners[PieceConfig.White]))
        self.blackPrisoners.setText(str(prisoners[PieceConfig.Black]))

        currentPieceColor = data["currentPieceColor"]
        if currentPieceColor == PieceConfig.White:
            self.timeWhite.setStyleSheet("border: 3px solid red; padding: 5px;")
            self.timeBlack.setStyleSheet("border: none; padding: 8px;")
        else:
            self.timeBlack.setStyleSheet("border: 3px solid red; padding: 5px;")
            self.timeWhite.setStyleSheet("border: none; padding: 8px;")
