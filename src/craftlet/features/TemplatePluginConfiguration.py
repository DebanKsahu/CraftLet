from pathlib import Path
from typing import Dict, List, Tuple

from rich.console import Console

from craftlet.utils.ui.CliRadioButton import cliRadioButton


def configureTemplatePlugin(pluginDict: Dict[str, Dict]):
    richConsole = Console()
    availablePluginOptions: List[Tuple[str, List[List[str]]]] = []
    pluginAbouts = []
    for pluginName in pluginDict.keys():
        pluginAbout: str = pluginDict.get(pluginName, {}).get("about", "No Description")
        availablePluginOptions.append((pluginName, pluginDict.get(pluginName, {}).get("modulePath", [])))
        pluginAbouts.append(pluginAbout)

    selectedPlugins, unSelectedPlugins = cliRadioButton(
        options=availablePluginOptions,
        title="Project Plugin Options",
        richConsole=richConsole,
        abouts=pluginAbouts,
    )

    unSelectedPluginsPaths = set()
    for i in range(len(unSelectedPlugins)):
        for pathList in unSelectedPlugins[i][1]:
            modulePath = Path(('/').join(pathList))
            unSelectedPluginsPaths.add(modulePath)
    return unSelectedPluginsPaths
