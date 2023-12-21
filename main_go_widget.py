from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout


class MainGoWidget(QWidget):

    def __init__(self, board, gameControls):
        super().__init__()
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(gameControls, 0, 0)
        self.mainLayout.addWidget(board, 1, 0, 9, 0)

