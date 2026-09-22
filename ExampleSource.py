"""A provider that supplies words and draws nothing.

The other half of this template.  A provider has no region, no painting
and no theme reaching it: it answers a role's calls and says so in its
schema.  This one is a `TextSource`, the simplest role there is - it says
what the words are, and tells whoever asked when they change.

Keep this file or `Example.py`, not both: a plugin folder holds one class,
and `__init__.py` says which.  See the README.
"""
import logging

from PyQt5.QtCore import QTimer

from PiClock3.TextSource import TextSource

logger = logging.getLogger(__name__)


class ExampleSource(TextSource):
    """Called whatever suits: the loader finds the class by inspection."""

    # what the service must be credited as, where a widget shows credit.
    # A source that needs none says nothing.
    attribution = ''

    def __init__(self, piclock, name, config):
        super().__init__(piclock, name, config)
        self.listeners = []
        self.at = 0
        self.timer = None

    def start(self):
        """one instance, however many widgets name it.

        A provider starts once and fetches once; a widget that names it
        gets what is already here.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(int(self.config['refresh']) * 1000)

    def subscribe(self, fn):
        """called by every widget that names this provider.

        Keep them all: two widgets may draw the same words, and a
        provider that remembered only the last one would leave the first
        showing what it had at startup.
        """
        self.listeners.append(fn)

    def text(self):
        """the words as they stand, drawn as they are given"""
        lines = self.config['lines']
        return self.expand(lines[self.at % len(lines)]) if lines else ''

    def tick(self):
        """move to the next line and tell whoever is listening.

        A real source fetches here instead, and tells nobody when the
        answer has not changed - a widget redrawing the same words costs
        a repaint for nothing.
        """
        self.at += 1
        for fn in self.listeners:
            fn()
