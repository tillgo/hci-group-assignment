from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor
from PyQt6.QtWidgets import *


class GameControlToolbar(QToolBar):
    """
    Toolbar containing game controls, like passing od redo a move
    """

    def __init__(self,parent, onUndo, onRedo, onReset, onPass):
        # Toolbar actions and widgets
        super().__init__(parent)



        # Create Undo Action
        self.undoAction = QAction(QIcon("./assets/icons/undo.png"), "Undo", parent)
        self.undoAction.triggered.connect(onUndo)
        self.undoAction.setToolTip("Undo Move")

        # Create Redo Action
        self.redoAction = QAction(QIcon("./assets/icons/redo.png"), "Redo", parent)
        self.redoAction.triggered.connect(onRedo)
        self.redoAction.setToolTip("Redo Move")

        # Create reset action
        self.resetAction = QAction(QIcon("./assets/icons/reset.png"), "Reset", parent)
        self.resetAction.triggered.connect(onReset)
        self.resetAction.setToolTip("Reset Game")

        # create pass button
        self.btnPass = QPushButton("Pass")
        self.btnPass.clicked.connect(onPass)


        # Add actions / widgets to toolbar
        self.addAction(self.undoAction)
        self.addAction(self.redoAction)
        self.addAction(self.resetAction)
        self.addWidget(self.btnPass)
