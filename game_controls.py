from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QFont
from PyQt6.QtWidgets import *


class GameControls(QWidget):
    """
    Toolbar containing game controls, like passing od redo a move
    """

    def __init__(self, parent, onUndo, onRedo, onReset, onPass):
        # Toolbar actions and widgets
        super().__init__(parent)

        with open('./assets/styles/game_controls.css', 'r') as file:
            self.setStyleSheet(file.read())

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.mainLayout)

        # SpacerItem to make padding on left side of elements
        self.spacerItem = QWidget()
        self.spacerItem.setFixedHeight(0)
        self.spacerItem.setFixedWidth(0)

        # Create Undo button
        self.btnUndo = QPushButton()
        self.btnUndo.setIcon(QIcon("./assets/icons/undo.png"))
        self.btnUndo.clicked.connect(onUndo)
        self.btnUndo.setToolTip("Undo Move")

        # Create Redo button
        self.btnRedo = QPushButton()
        self.btnRedo.setIcon(QIcon("./assets/icons/redo.png"))
        self.btnRedo.clicked.connect(onRedo)
        self.btnRedo.setToolTip("Redo Move")

        # Create reset button
        self.btnReset = QPushButton()
        self.btnReset.setIcon(QIcon("./assets/icons/reset.png"))
        self.btnReset.clicked.connect(onReset)
        self.btnReset.setToolTip("Reset Game")

        # create pass button
        self.btnPass = QPushButton("Pass")
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
        btnSize = int(size * 0.4)
        spacingSize = size - btnSize
        self.mainLayout.setSpacing(spacingSize)
        for btn in self.buttons:
            btn.setIconSize(QSize(btnSize, btnSize))
            font = QFont()
            font.setPointSize(int(btnSize / 1.8))
            btn.setFont(font)

    def disableUndo(self):
        self.btnUndo.setDisabled(True)

    def enableUndo(self):
        self.btnUndo.setDisabled(False)

    def disableRedo(self):
        self.btnRedo.setDisabled(True)

    def enableRedo(self):
        self.btnRedo.setDisabled(False)
