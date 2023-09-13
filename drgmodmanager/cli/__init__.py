from drgmodmanager import mod
from drgmodmanager.cli import prompt
from drgmodmanager.config import Config
import typer
from rich.console import Console
from rich.table import Table

from drgmodmanager.cli.profile import profile_typer


app = typer.Typer()
app.add_typer(profile_typer, name='profile')
console = Console()


@app.command()
def setup():
    config = Config()
    default_config = ''
    default_mod = ''
    if config.exists():
        # Keep whatever was setup
        config.load()
        try:
            default_config = config['gameconfig']
            default_mod = config['modio']
        except KeyError:
            pass
    prompt.setup_config(config, default_config=default_config, default_mod=default_mod)
    config.save()
    print("All set now! Now run any command you want")


@app.command()
def status(*, enabled: bool = False, description: bool = False):
    config = Config()
    if not config.exists():
        print("No config setup, try running drgmodmanager setup")
        return
    config.load()
    manager = mod.ModManager.from_config(config)
    table = Table(style="inspect.attr")
    table.add_column("Status", no_wrap=True, style="magenta")
    table.add_column("Name", no_wrap=True, style="green")
    if description:
        table.add_column("Description")
    table.add_column("ID", no_wrap=True, style="markdown.code")
    for m in sorted(manager.get_mods(), key=lambda m: m.name):
        if enabled and not m.enabled:
            continue
        row = []
        row.append(('✓' if m.enabled else ' ') + ' ' + m.mod_type.symbol())
        row.append(('' if m.enabled else '[red]') + m.name)
        row.append(str(m.mod_id))
        if description:
            row.append(m.description)
        table.add_row(*row)
    console.print(table)
    console.print('''[gray]Key: \n- Status First Column: [markdown.code]enabled[/markdown.code]\n- Status Second Column: [markdown.code]Verified ♥ [/markdown.code], [markdown.code]Approved ○[/markdown.code], [markdown.code]Sandbox ∅[/markdown.code]''')


def cli():
    app()
