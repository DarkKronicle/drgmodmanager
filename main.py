from drgmodmanager.cli import cli


# This should really only be run in development. The main script in poetry just goes to the function in cli.
if __name__ == "__main__":
    cli()
