import json
from pathlib import Path
from drgmodmanager.profile import Profile
import os


# TODO get this working on `~/.config` and on multiple OS's.
CONFIG_PATH = Path.home() / '.config/drgmodmanager/config.json'


class Config:

    def __init__(self):
        self.profiles: dict[str, Profile] = {}
        self._data = {}

    def exists(self):
        return CONFIG_PATH.exists()

    def load(self):
        with CONFIG_PATH.open() as f:
            self._data = json.load(f)
        self.profiles = {}
        for p in self._data.get('profiles', []):
            try:
                p = Profile.from_dict(p)
                self.profiles[p.name] = p
            except KeyError:
                print("Error loading profile")


    def save(self):
        self._data['profiles'] = [p.to_dict() for p in self.profiles.values()]
        CONFIG_PATH.write_text(json.dumps(
            self._data, indent=4, sort_keys=True)
        )

    @property
    def path(self):
        return CONFIG_PATH

    def __getitem__(self, key):
        if isinstance(key, tuple):
            d = self._data
            for k in key:
                d = d[k]
            return d
        return self._data[key]

    def __setitem__(self, key, item):
        if isinstance(key, tuple):
            d = self._data
            for i, k in enumerate(key):
                if i == len(key) - 1:
                    d[k] = item
                    return
                if k in d:
                    d = d[k]
                else:
                    d[k] = {}
                    d = d[k]
            return
        self._data[key] = item
