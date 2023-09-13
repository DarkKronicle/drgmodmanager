from roundtripini import INI
from enum import Enum
from drgmodmanager.config import Config
from pathlib import Path
import json
from . import MOD_INI_SECTION


class ModType(Enum):
    sandbox = 0
    approved = 1
    verified = 2
    unknown = 3

    @classmethod
    def from_tags(cls, tags: list[dict]):
        for t in tags:
            name = t['name'].lower()
            if 'verified' in name or 'audio' in name:
                return ModType.verified
            if 'sandbox' in name:
                return ModType.sandbox
            if 'approved' in name:
                return ModType.approved
        return ModType.unknown

    def color(self):
        if self == ModType.sandbox:
            return "[red]"
        if self == ModType.verified:
            return "[green]"
        return "[yellow]"

    def symbol(self):
        if self == ModType.sandbox:
            return "∅"
        if self == ModType.verified:
            return "♥ "
        if self == ModType.approved:
            return "○"
        return "?"

    def __str__(self):
        if self == ModType.sandbox:
            return "Sandbox"
        if self == ModType.verified:
            return "Verified"
        if self == ModType.approved:
            return "Approved"
        return "Unknown"


class ModManager:

    def __init__(self, config, metadata):
        self._mods: dict = {}
        self._config: INI = config
        self._removed = []
        self.load_from_metadata(metadata)
        self.apply_config()

    def get_removed(self) -> list[int]:
        return self._removed

    def get_mods(self) -> list:
        return self._mods.values()

    def get_sandbox(self):
        return filter(lambda x: x.mod_type == ModType.sandbox, self.get_mods())

    def get_verified(self):
        return filter(lambda x: x.mod_type == ModType.verified, self.get_mods())

    def get_approved(self):
        return filter(lambda x: x.mod_type == ModType.approved, self.get_mods())

    def set_enabled_mods(self, mods: list[int]):
        for m in self._mods.values():
            m.enabled = m.mod_id in mods

    def save_to_ini(self, path):
        for m in self._mods.values():
            self._config[MOD_INI_SECTION, str(m.mod_id)] = str(m.enabled)
        dump = self._config.dump()
        with open(str(path), 'w+') as f:
            f.write(dump)

    def apply_config(self):
        for key in self._config.keys(MOD_INI_SECTION):
            try:
                key = int(key)
            except:
                continue
            if key not in self._mods:
                self._removed.append(key)
                continue
            self._mods[key].enabled = self._config[MOD_INI_SECTION,
                                                   str(key)] == 'True'

    def load_from_metadata(self, data: dict):
        self._mods = {}
        for mod in data['Mods']:
            m = Mod.from_json(mod)
            self._mods[m.mod_id] = m

    def get_enabled(self):
        return filter(lambda x: x.enabled, self._mods.values())

    def get_disabled(self):
        return filter(lambda x: not x.enabled, self._mods.values())

    @classmethod
    def from_config(cls, config: Config):
        file = Path(config['gameconfig'])
        mod_cache = Path(config['modio'])
        with file.open() as buf:
            gameconf = INI(buf, item_format="{key}={value}")

        metadata_file = mod_cache / 'metadata/state.json'
        with metadata_file.open() as f:
            metadata = json.load(f)

        return ModManager(gameconf, metadata)


class Mod:

    def __init__(self, enabled: bool, mod_id: int, name: str, description: str, mod_type: ModType, data: dict):
        self.enabled = enabled
        self.mod_id = mod_id
        self.name = name
        self.description = description
        self.mod_type = mod_type
        self.data = data

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            False,
            data['ID'],
            data['Profile']['name'],
            data['Profile']['summary'],
            ModType.from_tags(data['Profile']['tags']),
            data,
        )

    def __str__(self) -> str:
        return '{0} ({1})'.format(self.name, self.mod_id)
