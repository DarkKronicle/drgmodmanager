class Profile:

    def __init__(self, name: str, mods: list[int]):
        self.name: str = name
        self.mods: list[int] = mods

    def to_dict(self):
        return {
            'name': self.name,
            'mods': self.mods
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['name'], data['mods'])
