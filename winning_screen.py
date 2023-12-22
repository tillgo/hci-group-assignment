import random

from PyQt6.QtCore import QPointF, QTimer, Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QSizePolicy, QLabel, \
    QGraphicsProxyWidget, QGridLayout, QPushButton


class ConfettiItem(QGraphicsPixmapItem):
    def __init__(self, confettiPath, height, width):
        super().__init__()
        self.width = width
        self.height = height
        self.setPixmap(QPixmap(confettiPath))

        # Set the rotation angle and randomize initial position
        self.setRotation(random.uniform(0, 360))
        self.setPos(random.uniform(0, self.width), -20)

        # Set a random spin speed for animation
        self.spin_speed = random.uniform(-5, 5)

        self.initialAdvance = True

    def advance(self, phase):
        if phase == 0:
            # Update confetti position and rotation during animation
            if self.initialAdvance:
                randomPoint = QPointF(0, random.choice([i for i in range(self.height)]))
                self.initialAdvance = False

            else:
                randomPoint = QPointF(random.choice([-1, 0, 1]), random.choice([1, 2, 3, 4]))
            new_pos = self.pos() + randomPoint
            self.setPos(new_pos)
            self.setRotation(self.rotation() + self.spin_speed)

            # If confetti goes off the bottom, reset to the top
            if self.pos().y() > self.height:
                self.setPos(random.uniform(0, self.width), -20)
                self.setRotation(random.uniform(0, 360))


class WinningScreen(QGraphicsView):
    def __init__(self, height, width, winner, onOkay):
        # Set up the confetti animation view
        confetti_scene = QGraphicsScene()
        super().__init__(confetti_scene)

        with open('./assets/styles/winning_screen.css', 'r') as file:
            self.setStyleSheet(file.read())

        confetti_scene.setSceneRect(0, 0, width, height)
        # Create confetti items and add them to the scene
        self.confetti_items = [ConfettiItem('./assets/images/confetto_' + str(random.choice([i for i in range(1,8)])) + '.png', height, width) for _ in range(50)]
        for item in self.confetti_items:
            confetti_scene.addItem(item)

        # Set up the animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(18)

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)

        winnerLabel = QLabel(winner + " has won!")
        winnerFont = QFont()
        winnerFont.setWeight(500)
        winnerFont.setPointSize(40)
        winnerLabel.setFont(winnerFont)

        btnOkay = QPushButton("Okay")
        btnOkay.clicked.connect(onOkay)

        mainLayout.addWidget(winnerLabel,0, 0, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(btnOkay,1, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)



    def update_animation(self):
        # Advance the animation for each confetti item
        for item in self.confetti_items:
            item.advance(0)
