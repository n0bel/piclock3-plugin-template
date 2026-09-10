"""A widget that draws a line of text and refreshes it on a timer.

The smallest thing that exercises everything a widget has to get right: a
region to draw in, a config to read, a font the theme picked, a timer that
survives, and work that stops while the page is not showing.

If words are all you want, `PiClock3.Text` already ships and does more with
them.  This is here to be replaced.
"""
import logging

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel

from PiClock3.Widget import Widget

logger = logging.getLogger(__name__)


class Example(Widget):
    """Called whatever suits: the loader finds the class by inspection."""

    def __init__(self, piclock, name, config):
        super().__init__(piclock, name, config)
        # nothing on the screen yet: a region has no size until the layout
        # has placed it, and start() is where it has one.
        self.label = None
        self.timer = None

    def start(self):
        rect = self.region.frameRect()
        self.label = QLabel(self.region)
        self.label.setObjectName('example')
        self.label.setGeometry(rect)
        self.label.setAlignment(Qt.AlignCenter)

        # only the size.  color, font-family, font-style and font-weight
        # arrive on the region and Qt inherits them into whatever is drawn
        # there, so a theme that says color: once already reaches this.
        props = self.scaleFont({'font-size': self.config['font-size']},
                               rect.height())
        self.label.setStyleSheet(
            '#example {%s }' % self.piclock._buildStyleString(props))
        self.applyEffect(self.label, rect.height())

        # Keep the timer on self.  A local one is collected the moment
        # start() returns, never fires again, and says nothing about it.
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(int(self.config['refresh']) * 1000)
        self.tick()

    def pageChange(self):
        """the visible page changed - catch up if it is now this one"""
        self.tick()

    def tick(self):
        # A page nobody is looking at should not be fetching.  Drawing is
        # cheap here; a request would not be.
        if not self.region.isVisible():
            return
        self.label.setText(self.expand(self.config['text']))
