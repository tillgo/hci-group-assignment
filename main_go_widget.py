from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from board import Board
from game_controls import GameControls
from winning_screen import WinningScreen


class MainGoWidget(QWidget):
    """
    Containing main widgets of go application
    """
    def __init__(self, board: Board, gameControls: GameControls):
        """
        Initialize MainGoWidget

        parameters:
            - board: Go-Board widget
            - gameControls: GameControls widget

        """
        super().__init__()
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(gameControls, 0, 0)
        self.mainLayout.addWidget(board, 1, 0, 9, 0)

    def showWinningScreen(self, winner: str, onOkay: Callable[[None], None]):
        """
        shows the winning screen

        parameters:
            - winner: Winner of the game
            - onOkay: Callback when okay button on winning screen is clicked
        """
        self.mainLayout.addWidget(WinningScreen(self.mainLayout.sizeHint().height(),
                                            self.mainLayout.sizeHint().width(), winner, onOkay), 0, 0, 9, 0)
