# PiClock3 Plugin Template

A starting point for a PiClock3 plugin.  Press **Use this template** to make
your own repo from it.

A plugin is a folder that PiClock3 loads at startup.  It gets a rectangle on
the screen and draws whatever it likes in it — weather from a source nobody
has added yet, a camera, tide times, the bus timetable.  There is no fixed
list of what a plugin may be.

## Naming

Pick a short lowercase name and use it in three places.  Here it is `example`:

* the folder users clone into — `plugins/example`
* the package name in `config.yaml` — `module: example.Example`
* the class in `Example.py` — `class Example(Plugin)`

The folder name has to match `module:`, because that is how Python finds it.
Say so in your README, or people will clone it under the repo name and wonder
why nothing loads.

## Installing it (yours or anyone's)

```
cd plugins
git clone https://github.com/yourname/piclock3-example example
```

Then add it to `Config.yaml`:

```yaml
plugins:
  example:
    module: example.Example
    block: bottom
    text: Hello
```

`block:` is the region it draws in, and comes from the active layout.

## What you get

Your class inherits `Plugin` and may use:

| | |
|---|---|
| `self.block` | your QWidget, if the config gave you a `block:` |
| `self.config` | your `config.yaml`, with the user's overrides merged over it |
| `self.piclock` | the running clock |
| `self.piclock.expand(s)` | expands `{location.lattitude}`, `{apikeys.xxx}`, `{plugin-folder}` |
| `self.piclock.plugins[name]` | another plugin, if you need to ask it something |

and three methods worth overriding:

| | |
|---|---|
| `__init__` | set attributes, do not touch the screen |
| `start()` | build your widgets, start your timers |
| `pageChange()` | the visible page changed — refresh if you are now showing |

## Two things that will bite you

**Keep a reference to your QTimer.**  `self.timer = QTimer()`, never
`timer = QTimer()`.  A local one is garbage collected the moment `start()`
returns and never fires again, and nothing tells you.

**Check `self.block.isVisible()` before doing work.**  Pages that are not
showing should not be fetching.

## Fitting the block

You are given a rectangle and you decide how to fill it — fit, stretch, crop,
wrap, whatever suits what you are drawing.  A clock face keeps its circle.  A
map fills and crops, because letterboxing a map looks broken.  If the choice
matters to the user, put it in `settings:` so the editor can offer it.

## Before you publish

- [ ] **Run it on a real clock for a day.**  Overnight is where the bugs are.
- [ ] Fill in `name`, `version`, `author` and `repo` in `config.yaml`
- [ ] Describe every user-facing option under `settings:`
- [ ] Put your own name in `LICENSE`, or replace it
- [ ] Add the topic **`piclock3-plugin`** to your repo so people can find it
