from typing import Callable

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QFont
from PyQt6.QtWidgets import *


class GameControls(QWidget):
    """
    Toolbar containing game controls, like passing od redo a move
    """

    def __init__(self, onUndo: Callable[[None], None], onRedo: Callable[[None], None], onReset: Callable[[None], None],
                 onPass: Callable[[None], None]):
        """
        Initialize GameControls

        parameters:
            - onUndo: Callback function when undo is clicked
            - onRedo: Callback function when redo is clicked
            - onReset: Callback function when reset is clicked
            - onPass: Callback function when pass is clicked
        """

        # Toolbar actions and widgets
        super().__init__()

        with open('./assets/styles/game_controls.css', 'r') as file:
            self.setStyleSheet(file.read())

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.mainLayout)

        # ToDo sich für eines der Icon-Arten entscheiden
        # SpacerItem to make padding on left side of elements
        self.spacerItem = QWidget()
        self.spacerItem.setFixedHeight(0)
        self.spacerItem.setFixedWidth(0)

        # Create Undo button
        self.btnUndo = QPushButton()
        self.btnUndo.setIcon(QIcon("assets/icons/undo_1.png"))
        self.btnUndo.clicked.connect(onUndo)
        self.btnUndo.setToolTip("Undo Move")

        # Create Redo button
        self.btnRedo = QPushButton()
        self.btnRedo.setIcon(QIcon("assets/icons/redo_1.png"))
        self.btnRedo.clicked.connect(onRedo)
        self.btnRedo.setToolTip("Redo Move")

        # Create reset button
        self.btnReset = QPushButton()
        self.btnReset.setIcon(QIcon("assets/icons/reset_1.png"))
        self.btnReset.clicked.connect(onReset)
        self.btnReset.setToolTip("Reset Game")

        # create pass button
        self.btnPass = QPushButton()
        self.btnPass.setIcon(QIcon("assets/icons/pass_icon.png"))
        self.btnPass.clicked.connect(onPass)

        self.buttons = [self.btnUndo, self.btnRedo, self.btnReset, self.btnPass]

        # Add spaceritem / buttons to grid
        self.mainLayout.addWidget(self.spacerItem)
        self.mainLayout.addWidget(self.btnUndo)
        self.mainLayout.addWidget(self.btnRedo)
        self.mainLayout.addWidget(self.btnReset)
        self.mainLayout.addWidget(self.btnPass)

        self.updateSize(50)

    def updateSize(self, size):
        btnSize = int(size * 0.5)
        spacingSize = size - btnSize
        self.mainLayout.setSpacing(spacingSize)
        for btn in self.buttons:
            btn.setIconSize(QSize(btnSize, btnSize))


    def disableUndo(self):
        self.btnUndo.setDisabled(True)

    def enableUndo(self):
        self.btnUndo.setDisabled(False)

    def disableRedo(self):
        self.btnRedo.setDisabled(True)

    def enableRedo(self):
        self.btnRedo.setDisabled(False)
