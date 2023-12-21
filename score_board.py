from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSlot

import PieceColor


class ScoreBoard(QDockWidget):
    """base the score_board on a QDockWidget"""

    def __init__(self):
        super().__init__()
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)
        self.setFixedWidth(200)

        self.timeWhite = QLabel("0s")
        self.timeBlack = QLabel("0s")

        self.mainLayout.addWidget(self.timeWhite)
        self.mainLayout.addWidget(self.timeBlack)

    def make_connection(self, go):
        """this handles a signal sent from the board class"""
        # when the timerSignal is emitted in the GO class the setTimeRemaining slot receives it
        go.timerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(dict)
    def setTimeRemaining(self, playerTimes):
        """updates the time remaining label to show the time remaining"""
        print(playerTimes)
