import asyncio
import sys
from pathlib import Path

import typer

from craftlet.features.CraftLet import CraftLet
from craftlet.features.CraftLetCache import CraftLetCache
from craftlet.models.Cacheable import GithubTemplate, GithubTemplateReference
from craftlet.utils.exceptions import CraftLetException
from craftlet.utils.helperFunctions import CacheFunction


class CraftLetCLI:
    app = typer.Typer()

    @app.command()
    @staticmethod
    def load_template(
        github: bool = typer.Option(default=False, help="Load Template From GitHub thorugh GitHub repo URL"),
        local: bool = typer.Option(default=False, help="Load Template From Local Cache"),
        local_profile: str = typer.Argument(default=None, help="Load Template From Online Profile Cache"),
        generate_env: bool = typer.Option(
            default=False, help="Is Yes then it will environment variable file(.env)"
        ),
    ):
        if github:
            asyncio.run(CraftLetCLI.loadTemplateFromGithub(generateEnv=generate_env))
        elif local:
            CraftLetCLI.loadTemplateFromLocal(generateEnv=generate_env, localProfile=local_profile)
        else:
            asyncio.run(CraftLetCLI.loadTemplateFromGithub(generateEnv=generate_env))

    @staticmethod
    async def loadTemplateFromGithub(generateEnv: bool):
        templateUrl = typer.prompt(text="Enter Github Template Repo URL: ")
        projectName = typer.prompt(text="Enter The Project Name")
        await CraftLet.loadTemplateGithub(
            repoUrl=templateUrl,
            targetDir=Path.cwd() / projectName,
            generateEnv=generateEnv,
        )

    @staticmethod
    def loadTemplateFromLocal(generateEnv: bool, localProfile: str | None):
        templateSource = typer.prompt("Enter the source of template: ")
        templateName = typer.prompt(text="Enter The name of the template: ")
        projectName = typer.prompt(text="Enter The Project Name: ")
        if localProfile is None:
            if CraftLetCache.isRunningInEnvironment():
                exactPath = (
                    Path(sys.prefix)
                    / "craftlet"
                    / ".cache"
                    / "offline"
                    / "template"
                    / templateSource
                    / templateName
                )
            else:
                exactPath = (
                    CacheFunction.getOSCacheDir()
                    / "craftlet"
                    / ".cache"
                    / "offline"
                    / "template"
                    / templateSource
                    / templateName
                )
            CraftLet.loadTemplateLocal(
                templatePath=exactPath,
                targetDestination=Path.cwd() / projectName,
                generateEnv=generateEnv,
            )
        else:
            pass

    @app.command()
    @staticmethod
    def show_cache(
        specific_folder: str = typer.Argument(
            help="Give the relative folder path you want to see", default=""
        ),
    ):
        if CraftLetCache.isRunningInEnvironment():
            exactPath = Path(sys.prefix) / "craftlet" / ".cache" / specific_folder
        else:
            exactPath = CacheFunction.getOSCacheDir() / "craftlet" / ".cache" / specific_folder
        CraftLetCache.showCache(cacheDir=exactPath)

    @app.command()
    @staticmethod
    def cache_template(
        template_url: str = typer.Argument(
            help="Give the url of the template available on their respective platform"
        ),
        only_ref: bool = typer.Option(
            default=False,
            help="True: Only cache reference, False: Cache whole template",
        ),
    ):
        templatePlatform, templateOwner, templateName = template_url[8:].split("/")
        match templatePlatform:
            case "github.com":
                if only_ref:
                    cacheableData = GithubTemplateReference(
                        name=templateName,
                        coreData=template_url,
                        payload={"ownerName": templateOwner},
                    )
                else:
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        templateBytes = asyncio.run(CraftLet.getTemplateBytesGithub(template_url))
                    else:
                        future = asyncio.run_coroutine_threadsafe(
                            CraftLet.getTemplateBytesGithub(template_url), loop
                        )
                        templateBytes = future.result()
                    cacheableData = GithubTemplate(
                        name=templateName,
                        coreData=templateBytes,
                        dataVersion=1,
                        payload={
                            "ownerName": templateOwner,
                            "template_url": template_url,
                        },
                    )
                if CraftLetCache.isRunningInEnvironment():
                    CraftLetCache.cacheOffline(path=Path(sys.prefix), data=cacheableData)
                else:
                    CraftLetCache.cacheOffline(path=CacheFunction.getOSCacheDir(), data=cacheableData)
            case _:
                raise CraftLetException(f"Unrecognized platform({templatePlatform})")

    @staticmethod
    def registerTo(app: typer.Typer):
        app.add_typer(CraftLetCLI.app)
