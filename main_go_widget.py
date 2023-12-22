from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from winning_screen import WinningScreen


class MainGoWidget(QWidget):

    def __init__(self, board, gameControls):
        super().__init__()
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(gameControls, 0, 0)
        self.mainLayout.addWidget(board, 1, 0, 9, 0)

    def showWinningScreen(self, winner, onOkay):
        self.mainLayout.addWidget(WinningScreen(self.mainLayout.sizeHint().height(),
                                            self.mainLayout.sizeHint().width(), winner, onOkay), 0, 0, 9, 0)
