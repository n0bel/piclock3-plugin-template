import logging

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel

from PiClock3.Plugin import Plugin

logger = logging.getLogger(__name__)


class Example(Plugin):

    def __init__(self, piclock, name, config):
        super().__init__(piclock, name, config)
        self.label = None
        self.timer = None

    def start(self):
        self.label = QLabel(self.block)
        self.label.setObjectName('example')
        self.label.setGeometry(self.block.frameRect())
        self.label.setAlignment(Qt.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000 * self.config.refresh)
        self.tick()

    def pageChange(self):
        self.tick()

    def tick(self):
        if not self.block.isVisible():
            return
        self.label.setText(self.piclock.expand(self.config.text))
