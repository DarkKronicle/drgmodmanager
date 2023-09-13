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

# Usage

`drgmodmanager --help`
