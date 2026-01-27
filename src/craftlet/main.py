import typer

from craftlet.cli.CraftLetCLI import craftletCliApp

app = typer.Typer(name="CraftLet", help="Entry Point of CraftLet CLI tool")
app.add_typer(craftletCliApp)
