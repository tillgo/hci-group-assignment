from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSlot

from field import Field


class ScoreBoard(QDockWidget):
    """base the score_board on a QDockWidget"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """initiates ScoreBoard UI"""
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.setFixedWidth(150)

        # create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.setWidget(self.mainWidget)

    def make_connection(self, board):
        """this handles a signal sent from the board class"""
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(Field)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, field):
        """updates the label to show the click location"""
        self.label_clickLocation.setText("Click Location: " + str(field))
        print('slot ' + str(field))

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        """updates the time remaining label to show the time remaining"""
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + str(timeRemaining))
        # self.redraw()
