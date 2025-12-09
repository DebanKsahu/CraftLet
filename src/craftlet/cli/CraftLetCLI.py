import asyncio
import typer
from pathlib import Path
from craftlet.feature.CraftLet import CraftLet


class CraftLetCLI:
    app = typer.Typer()

    @app.command()
    @staticmethod
    def load_template(
        github: bool = typer.Option(
            default=False, help="Load Template From GitHub thorugh GitHub repo URL"
        ),
    ):
        if github:
            asyncio.run(CraftLetCLI.loadTemplateFromGithub())

    @staticmethod
    async def loadTemplateFromGithub():
        templateUrl = typer.prompt(text="Enter Template Repo URL: ")
        projectName = typer.prompt(text="Enter The Project Name")
        await CraftLet.loadTemplateGithub(
            repoUrl=templateUrl, targetDir=Path.cwd() / projectName
        )

    @staticmethod
    def registerTo(app: typer.Typer):
        for command in CraftLetCLI.app.registered_commands:
            app.registered_commands.append(command)
