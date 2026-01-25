import ast
import sys
import sysconfig
from collections import defaultdict, deque
from pathlib import Path
from typing import List

from craftlet.features.DirectoryTree import DirectoryTree
from craftlet.models.DirectoryTreeNode import DirectoryTreeNode
from craftlet.models.ImportItem import ImportItem
from craftlet.utils.enums import ModuleType


class ModuleDependencyGraph:
    @staticmethod
    def extractImports(filePath: Path, rootPath: Path):
        astTree = ast.parse(filePath.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(astTree):
            if isinstance(node, ast.Import):
                for importedNode in node.names:
                    imports.append(
                        ImportItem(
                            name=importedNode.name.split(".")[-1],
                            type=ModuleDependencyGraph.findImportType(
                                moduleName=importedNode.name.split(".")[0], moduleFullPath=importedNode.name
                            ),
                            fullPath=importedNode.name,
                            parent="None",
                            level=0,
                        )
                    )

            elif isinstance(node, ast.ImportFrom):
                fullPath = node.module if node.module else "None"
                fullPathParts = fullPath.split(".")
                moduleIndex = -1
                for importRoot in ModuleDependencyGraph.extractImportRoots(rootPath=rootPath):
                    currDirectoryTreeRoot = DirectoryTree.buildDirectoryTree(root=importRoot)
                    moduleIndex = ModuleDependencyGraph.isModule(
                        directoryTreeRoot=currDirectoryTreeRoot, targetModulePath=fullPathParts
                    )
                    if moduleIndex != -1:
                        break
                moduleRootType = ModuleDependencyGraph.findImportType(
                    moduleName=fullPathParts[0], moduleFullPath=fullPath
                )
                moduleName = "None"
                if moduleRootType != ModuleType.LOCAL_MODULE:
                    moduleName = fullPathParts[0]
                else:
                    if moduleIndex == -1:
                        continue
                    if node.module:
                        moduleName = fullPathParts[moduleIndex]
                imports.append(
                    ImportItem(
                        name=moduleName,
                        type=ModuleDependencyGraph.findImportType(
                            moduleName=moduleName, moduleFullPath=fullPath
                        ),
                        fullPath=fullPath,
                        parent="None",
                        level=node.level,
                    )
                )
        return imports

    @staticmethod
    def findImportType(moduleName: str, moduleFullPath: str):
        if ModuleDependencyGraph.isBuiltInModule(moduleName=moduleName):
            return ModuleType.BUILT_IN_MODULE
        elif ModuleDependencyGraph.isStdlibModule(moduleName=moduleName):
            return ModuleType.STDLIB_MODULE
        elif ModuleDependencyGraph.isVenvModule(moduleName=moduleName):
            return ModuleType.VENV_MODULE
        else:
            for importRoot in ModuleDependencyGraph.extractImportRoots():
                if ModuleDependencyGraph.isLocalModule(moduleFullPath=moduleFullPath, importRoot=importRoot):
                    return ModuleType.LOCAL_MODULE
            return ModuleType.BUILT_IN_MODULE

    @staticmethod
    def isBuiltInModule(moduleName: str):
        if moduleName in sys.builtin_module_names:
            return True
        return False

    @staticmethod
    def isStdlibModule(moduleName: str):
        STDLIB_PATH = Path(sysconfig.get_paths()["stdlib"])
        try:
            spec = __import__("importlib.util").util.find_spec(moduleName)
            if spec is None or spec.origin is None:
                return False
            return Path(spec.origin).is_relative_to(STDLIB_PATH)
        except Exception:
            return False

    @staticmethod
    def isVenvModule(moduleName: str):
        SITE_PACKAGES = [Path(path) for path in sysconfig.get_paths().values() if "site-packages" in path]
        try:
            spec = __import__("importlib.util").util.find_spec(moduleName)
            if spec is None or spec.origin is None:
                return False
            origin = Path(spec.origin)
            return any(origin.is_relative_to(sp) for sp in SITE_PACKAGES)
        except Exception:
            return False

    @staticmethod
    def isLocalModule(moduleFullPath: str, importRoot: Path):
        parts = moduleFullPath.split(".")
        return (importRoot / Path(*parts)).with_suffix(".py").exists() or (
            importRoot / Path(*parts) / "__init__.py"
        ).exists()

    @staticmethod
    def extractImportRoots(rootPath: Path = Path.cwd()) -> List[Path]:
        importRoots = []

        cwdPath = rootPath
        stdlib = Path(sysconfig.get_paths()["stdlib"]).resolve()
        platstdlib = Path(sysconfig.get_paths()["platstdlib"]).resolve()

        for path in sys.path:
            if not path:
                candidate = cwdPath
            else:
                candidate = Path(path).resolve()

            if not candidate.is_relative_to(cwdPath):
                continue

            if (
                candidate.is_relative_to(stdlib)
                or candidate.is_relative_to(platstdlib)
                or any(
                    part.startswith(".venv") or part in {".tox", ".pytest_cache"} for part in candidate.parts
                )
            ):
                continue

            importRoots.append(candidate)
        return importRoots

    @staticmethod
    def isModule(
        directoryTreeRoot: DirectoryTreeNode, targetModulePath: List[str], currIndex: int = 0
    ) -> int:
        if directoryTreeRoot is None:
            return -1
        elif directoryTreeRoot.children is None:
            return currIndex - 1
        elif currIndex >= len(targetModulePath):
            return -1
        else:
            for child in directoryTreeRoot.children:
                if child.isModule:
                    if child.name == f"{targetModulePath[currIndex]}.py":
                        return ModuleDependencyGraph.isModule(child, targetModulePath, currIndex + 1)
                else:
                    if child.name == targetModulePath[currIndex]:
                        return ModuleDependencyGraph.isModule(child, targetModulePath, currIndex + 1)
            return -1

    @staticmethod
    def isBothModuleLinked(module1Path: Path, module2Name: str, projectRootPath: Path):
        imports = ModuleDependencyGraph.extractImports(filePath=module1Path, rootPath=projectRootPath)
        for importItem in imports:
            if importItem.name == module2Name:
                return True
        return False

    @staticmethod
    def buildModuleDependencyGraph(projectRootPath: Path):
        graph = defaultdict(set)
        directoryTree = DirectoryTree.buildDirectoryTree(root=projectRootPath)

        currNode = directoryTree
        currNodePath = projectRootPath
        queue = deque([(currNode, currNodePath)])

        while queue:
            currNode, currNodePath = queue.pop()

            if currNode.children is None:
                currModuleImportList = ModuleDependencyGraph.extractImports(
                    filePath=currNodePath, rootPath=projectRootPath
                )
                for importItem in currModuleImportList:
                    if importItem.type == ModuleType.LOCAL_MODULE:
                        graph[importItem.fullPath].add(str(currNodePath))
            else:
                for child in currNode.children:
                    queue.append((child, currNodePath / child.name))

        return graph
