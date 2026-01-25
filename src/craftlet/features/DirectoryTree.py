from pathlib import Path

from craftlet.models.DirectoryTreeNode import DirectoryTreeNode


class DirectoryTree:
    DEFAULT_EXCLUDE_DIRS = {
        ".venv",
        "venv",
        "__pycache__",
        ".git",
        ".mypy_cache",
        "build",
        "dist",
        ".ruff_cache",
    }
    DEFAULT_EXCLUDE_FILE_SUFFIXES = {".pyc", ".pyo"}

    @staticmethod
    def buildDirectoryTree(root: Path):
        directoryTreeRoot = DirectoryTreeNode(name=root.stem, isModule=False, children=[])
        for subPath in root.iterdir():
            DirectoryTree._buildDirectoryTree(currPath=subPath, parentNode=directoryTreeRoot)
        return directoryTreeRoot

    @staticmethod
    def _buildDirectoryTree(currPath: Path, parentNode: DirectoryTreeNode):
        if not currPath.exists() or any(
            part in DirectoryTree.DEFAULT_EXCLUDE_DIRS for part in currPath.parts
        ):
            return
        else:
            if currPath.is_file() and currPath.suffix.lower() == ".py":
                newNode = DirectoryTreeNode(name=currPath.name, isModule=True)
                if parentNode.children is not None:
                    parentNode.children.append(newNode)
            elif currPath.is_dir():
                newDirNode = DirectoryTreeNode(name=currPath.name, isModule=False, children=[])
                if parentNode.children is not None:
                    parentNode.children.append(newDirNode)
                for subPath in currPath.iterdir():
                    DirectoryTree._buildDirectoryTree(currPath=subPath, parentNode=newDirNode)
            else:
                return
