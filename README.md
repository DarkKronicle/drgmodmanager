# Deep Rock Galactic Mod Manager

This is a simple CLI tool to hopefully help some pains caused with mod.io. 

The goal of this application is to help fix these issues:

- Having to relaunch the game to apply mods/profiles
- Having mods randomly unselected with no reason

This project does *not* circumvent any checks that DRG makes for your mods. This project does *not* view/edit saves. 
All this project does is change the DRG configuration file that keeps track of what mods have you have active. This is *not* a replacement for mod.io.

## Features

- CLI based (no GUI nonsense)
- After setup it will automatically know your mods
- Create infinite profiles and easily load each one
- View enabled mods, and information about them in nice views

## Future Plans/Ideas (no guarantee)

- Integrate [mod.io API](https://github.com/ClementJ18/mod.io) to update mods and handle subscriptions.

# Installation

Ensure that you have [pipx](https://pypa.github.io/pipx/installation/) installed and working. To install this application run:

```
pipx install git+https://github.com/DarkKronicle/drgmodmanager.git
```

You should now have access to the command `drgmodmanager` in your terminal.

## Alternative Installation (mainly for development)

To install this for development (or maybe pipx isn't working), clone this repository. Ensure that [poetry](https://python-poetry.org/docs/#installation) is installed.

In the cloned repository, run

```
poetry install
```

You should now be able to run

```
poetry run drgmodmanager --help
```

If you don't want to type `poetry run` each time you can use:

```
poetry shell

drgmodmanager <command>
drgmodmanager <command>
drgmodmanager <command>

exit
```

Or set up an alias that runs `poetry run --directory <MANAGER DIRECTORY> drgmodmanager` (running this command should work in any directory).

### Development

Using the above installation, live changes can be tested by using `poetry run python main.py --help`.

# Usage

`drgmodmanager --help`
