from craftlet.cli.CraftLetCLI import CraftLetCLI
import typer

app = typer.Typer(name="CraftLet", help="Entry Point of CraftLet CLI tool")
CraftLetCLI.registerTo(app=app)

@app.command()
def entry_point():
    """
    Entry Point for the CraftLet Tool
    """
    pass
