from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator
from drgmodmanager.mod import ModManager
from pathlib import Path
from roundtripini import INI
from drgmodmanager import MOD_INI_SECTION
from drgmodmanager.config import Config
import re

import random


class InvalidConfig(Exception):
    pass


def confirm(message: str) -> inquirer:
    return inquirer.confirm(message=message)


def name(message: str, invalid: list[str]) -> inquirer:
    def validation(text: str):
        if text.lower() in invalid:
            return False
        return re.match(r'^[\w\d#\.\s\-\+]{1,15}$', text)

    return inquirer.text(
        message=message.format("1-15 alpha numeric characters, # . - + are allowed. Cannot be the same name (case insensitive) as another profile."),
        validate=validation
    )



def setup_config(config: Config, *, default_config=None, default_mod=None) -> None:
    print("First tell me where your game config is. This should be in `<steam>/steamapps/common/Deep Rock Galactic/FSD/Saved/Config ... GameUserSettings.ini`")
    game_config = inquirer.filepath(
        "Game Config:",
        only_files=True,
        validate=PathValidator(),
        default=default_config
    ).execute()
    game_config = Path(game_config)
    if not game_config.exists() or not str(game_config).endswith(".ini"):
        raise InvalidConfig()
    game_ini = None
    try:
        with game_config.open() as f:
            game_ini = INI(f)
        game_ini.keys(MOD_INI_SECTION)
    except:
        pass
    if game_ini is None:
        raise InvalidConfig

    print("Now I need your <i>mod.io</i> storage. On Proton (linux) this is `<steam>/steamapps/compatdata/548430/dosdevices/c:/users/Public/mod.io/2475/`")
    modio_cache = Path(inquirer.filepath(
        "mod.io storage:",
        only_directories=True,
        validate=PathValidator(),
        default=default_mod
    ).execute())
    if not modio_cache.exists():
        raise InvalidConfig()

    config.path.parent.mkdir(parents=True, exist_ok=True)

    backup = config.path.parent / ('config_backup' + str(int(random.random() * 10000)) + '.ini')
    backup.write_text(game_config.read_text())

    config['gameconfig'] = str(game_config)
    config['modio'] = str(modio_cache)


def select_mods(manager: ModManager, *, enabled_ids: list[int] = None) -> inquirer:
    def enabled(mod):
        if enabled_ids is None:
            return mod.enabled
        return mod.mod_id in enabled_ids


    approved = [Choice(m.mod_id, name=m.name, enabled=enabled(m))
                for m in sorted(manager.get_approved(), key=lambda x: x.name)]
    verified = [Choice(m.mod_id, name=m.name, enabled=enabled(m))
                for m in sorted(manager.get_verified(), key=lambda x: x.name)]
    sandbox = [Choice(m.mod_id, name=m.name, enabled=enabled(m))
               for m in sorted(manager.get_sandbox(), key=lambda x: x.name)]
    choices = []
    if len(verified) > 0:
        choices.append(
            Separator(line="\nVerified (client-side) Mods ----------"))
        choices.extend(verified)
    if len(approved) > 0:
        choices.append(
            Separator(line="\nApproved (server-side) Mods ----------"))
        choices.extend(approved)
    if len(sandbox) > 0:
        choices.append(
            Separator(line="\nSandbox (different save) Mods ----------"))
        choices.extend(sandbox)
    return inquirer.checkbox(
        message='Select Mods',
        choices=choices,
        cycle=True,
        vi_mode=True,
        border=True
    )
