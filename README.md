# PiClock3 Plugin Template

A starting point for a PiClock3 plugin.  Press **Use this template** to make
your own repository from it.

It runs as it stands: a widget that draws a line of text in a region and
redraws it on a timer.  Replace it with what yours does.

A plugin is either a **widget**, which draws in a region a layout named, or a
**provider**, which fetches something and draws nothing.  Which one it is
follows from what its schema says, not from the code.

## Try it first

From the top of a PiClock3 checkout:

```
git clone https://github.com/yourname/piclock3-example plugins/Example
python3 PyQtPiClock3.py plugins/Example/examples/example.yaml
```

That config is carried in this repository, which is the quickest way to let
somebody see what a plugin does without editing a config of their own.

## Naming

Pick a short name in PascalCase, the way the shipped plugins are named -
`AnalogClock`, `MapLoop`, `Metar`.  Use it in two places.  Here it is
`Example`:

* the folder users clone into - `plugins/Example`
* what a config writes - `plugin: plugins.Example`

`plugin:` names the **folder**, not the file inside it.  The class can be
called anything: the loader imports the folder and finds your `Plugin`
subclass by inspection.  That is what `__init__.py` is for, and its one line
is the only glue a plugin needs:

```python
from .Example import *  # noqa: F401,F403
```

The `noqa` is deliberate, and WRITING-A-PLUGIN.md says why at length.

## What is in here

    __init__.py             puts the class where the loader looks
    Example.py              a widget: draws in a region
    ExampleSource.py        a provider: supplies words, draws nothing
    config.yaml             its defaults, and the whole list of its settings
    schema.yaml             the shape of those settings.  Required
    examples/example.yaml   a clock with it in, run by naming it
    images/                 art of your own, if you draw any
    README.md               what it does, and any key it needs

**Keep one of the two modules.**  A plugin folder holds one class - the
loader imports the folder and takes the `Plugin` subclass it finds, so two
would be a coin toss.  `__init__.py` says which one, and the file you are
not writing is the file to delete.

A repository may also carry `languages/`, `units/`, `layouts/` and `themes/`
of its own, all found where they sit.  A widget that draws something new
often needs somewhere to draw it, and no shipped layout has a region for a
thing that did not exist yet - so a `layouts/` folder here is searched.  One
rule: **a layout you bring can add a name, never replace one.**

## Widget or provider

A **widget** draws in a region a layout named.  `Example.py` is one: it
reads its settings, draws a line of text, and redraws it on a timer.

A **provider** supplies something and draws nothing.  `ExampleSource.py` is
one: it is a `TextSource`, so it answers `text()` and calls back whoever
subscribed when the words change.  The shipped `Text` widget draws them, so
a provider needs no widget of its own to be useful.

Which one a plugin is follows from three things, and all three have to
agree:

| | widget | provider |
|---|---|---|
| the class inherits | `Widget` | `Weather`, `BaseMap`, `Frames` or `TextSource` |
| `schema.yaml` says | nothing about `provides:` | `provides: [text]`, or what its role answers |
| a config writes it under | `widgets:`, with a `region:` | `providers:`, with no region |

`--check` says so when they disagree, and which way to move it.

## Naming it in a config

```yaml
widgets:
  hello:
    plugin: plugins.Example
    region: bottom
    text: 'Hello from {location.latitude}'
```

A provider goes under `providers:` instead and takes no region.  Putting one
in the wrong section is a `--check` problem that says which way to move it.

## What you get

A widget's class inherits `Widget`.  A provider inherits the role for what
it answers - `Weather`, `BaseMap`, `Frames` or `TextSource` - and implements
that role's calls instead of drawing.  A widget may use:

| | |
|---|---|
| `self.region` | the QWidget you draw in.  `self.regions` when a layout repeats it |
| `self.config` | your `config.yaml`, with the user's settings merged over it |
| `self.piclock` | the running clock |
| `self.expand(s)` | fills in `{location.latitude}`, `{apikeys.yours}`, `{this-folder}` |
| `self.scaleFont(props, height)` | a `font-size:` fraction as pixels |
| `self.applyEffect(widget, height)` | the glow or shadow a theme asked for |
| `self.icon(name)` | an image from the icon set a theme picked |
| `self.units(quantity, from, value)` | a value in the set the config chose |

and two methods worth overriding:

| | |
|---|---|
| `start()` | build your widgets, start your timers.  The region has a size by now |
| `pageChange()` | the visible page changed - catch up if it is now yours |

`__init__` runs before any of that: set attributes there and touch nothing on
the screen.

## Three things that will bite you

**Keep a reference to your QTimer.**  `self.timer = QTimer()`, never
`timer = QTimer()`.  A local one is collected the moment `start()` returns,
never fires again, and says nothing about it.

**Check `self.region.isVisible()` before doing work.**  A page nobody is
looking at should not be fetching.

**Read your own config, never the theme's.**  A theme's `color:` and fonts
arrive on your region and Qt inherits them into whatever you draw, so
setting only `font-size` is usually all a widget has to do.

## Before you publish

- [ ] **Run it on a real clock for a day.**  Overnight is where the bugs are
- [ ] `python3 PyQtPiClock3.py plugins/Example/examples/example.yaml --check`
- [ ] Every setting in `config.yaml` declared in `schema.yaml`
- [ ] A key belongs in the user's `ApiKeys.yaml`, never in your `config.yaml`
- [ ] Say in this README which service it talks to, and whether it needs an
      account
- [ ] Put your own name in `LICENSE`, or replace it
- [ ] Add the topic **`piclock3-plugin`** to your repository so people can
      find it

## The long form

**WRITING-A-PLUGIN.md** is the whole of it, and **WRITING-A-SCHEMA.md**
covers what a `schema.yaml` may say.  Two links to each, because they answer
different questions:

* in the checkout this is cloned into -
  [WRITING-A-PLUGIN.md](../../docs/WRITING-A-PLUGIN.md),
  [WRITING-A-SCHEMA.md](../../docs/WRITING-A-SCHEMA.md).  These describe the
  core you are actually running.
* on the web -
  [WRITING-A-PLUGIN.md](https://github.com/n0bel/PiClock3/blob/main/docs/WRITING-A-PLUGIN.md),
  [WRITING-A-SCHEMA.md](https://github.com/n0bel/PiClock3/blob/main/docs/WRITING-A-SCHEMA.md).
  These are current, which is not the same thing.

Read the first pair while you are writing, and the second before you
publish.
