try:
    from PiClock3 import __version__
except ImportError:
    # a PiClock3 from before it had a version
    __version__ = '0'

# the oldest PiClock3 this plugin runs on.  A SystemExit with a sentence is
# shown as that sentence, where any other error is a traceback.
if __version__ < '2026.10.09':
    raise SystemExit('Example needs PiClock3 2026.10.09 or later - '
                     'git pull in the PiClock3 folder')

from .Example import *  # noqa: E402,F401,F403

# A provider instead of a widget?  Keep the line below and delete the one
# above, along with Example.py.  A plugin folder holds one class, and the
# loader finds it here.
# from .ExampleSource import *  # noqa: E402,F401,F403
