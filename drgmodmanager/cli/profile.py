import typer
from drgmodmanager.config import Config
from drgmodmanager import mod
from drgmodmanager.cli.prompt import name, select_mods, confirm
from drgmodmanager.profile import Profile

profile_typer = typer.Typer()


@profile_typer.command()
def list():
    config = Config()
    if not config.exists():
        print("No config setup, try running drgmodmanager setup")
        return
    config.load()
    if len(config.profiles) == 0:
        print("You have no profiles setup!")
        return
    print([p.name for p in config.profiles.values()])


@profile_typer.command()
def create():
    config = Config()
    if not config.exists():
        print("No config setup, try running drgmodmanager setup")
        return
    config.load()
    profile_name = name("What's the name? {0}", [p.lower() for p in config.profiles.keys()]).execute()
    manager = mod.ModManager.from_config(config)
    mod_ids = select_mods(manager).execute()
    config.profiles[profile_name] = Profile(profile_name, mod_ids)
    config.save()
    print("Created")

@profile_typer.command()
def delete(profile: str):
    config = Config()
    if not config.exists():
        print("No config setup, try running drgmodmanager setup")
        return
    config.load()
    if profile not in config.profiles.keys():
        print("That profile doesn't exist!")
        return
    yes = confirm("Are you sure you want to delete the profile {0}? This cannot be undone.".format(profile)).execute()
    if not yes:
        return
    del config.profiles[profile]
    config.save()
    print("Deleted!")

@profile_typer.command()
def edit(profile: str):
    config = Config()
    if not config.exists():
        print("No config setup, try running drgmodmanager setup")
        return
    config.load()
    if profile not in config.profiles.keys():
        print("That profile doesn't exist!")
        return
    manager = mod.ModManager.from_config(config)
    pro_obj = config.profiles[profile]
    new_mods = select_mods(manager, enabled_ids=pro_obj.mods).execute()
    pro_obj.mods = new_mods
    config.save()
    print("Updated!")

@profile_typer.command()
def load(profile: str):
    config = Config()
    if not config.exists():
        print("No config setup, try running drgmodmanager setup")
        return
    config.load()
    if profile not in config.profiles.keys():
        print("That profile doesn't exist!")
        return
    manager = mod.ModManager.from_config(config)
    profile_obj = config.profiles[profile]
    manager.set_enabled_mods(profile_obj.mods)
    manager.save_to_ini(config['gameconfig'])
    print("Done!")
