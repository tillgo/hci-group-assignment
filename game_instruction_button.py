from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import *


class GameInstructionButton(QPushButton):

    def __init__(self):
        super().__init__("Game Instructions")
        self.clicked.connect(lambda x: QDesktopServices.openUrl(QUrl("https://www.cs.cmu.edu/~wjh/go/rules/Chinese.html")))
