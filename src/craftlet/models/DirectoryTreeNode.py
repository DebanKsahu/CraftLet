from dataclasses import dataclass, field
from typing import List


@dataclass
class DirectoryTreeNode:
    name: str
    isModule: bool
    children: List["DirectoryTreeNode"] | None = field(default=None)

    def __str__(self):
        return self._renderTree()

    def _renderTree(self, prefix: str = "", isLast: bool = True):
        lines = []

        connector = "└── " if isLast else "├── "
        lines.append(prefix + connector + self.name + f"({"Module" if self.isModule else "Package"})")

        childPrefix = prefix + ("    " if isLast else "│   ")

        if self.children:
            for i, child in enumerate(self.children):
                isChildLast = i==len(self.children)-1
                lines.extend(child._renderTree(prefix=childPrefix, isLast=isChildLast).splitlines())
        return ("\n").join(lines)
