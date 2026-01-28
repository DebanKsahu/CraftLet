from typing import List, Optional, Tuple

import readchar
from readchar import key as rkey
from rich import box
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


def render(
    options: List[Tuple[str, List[List[str]]]],
    current: int,
    selected: set,
    title: str,
    abouts: List[str] | None = None,
):
    optsTable = Table.grid(expand=True)
    optsTable.add_column(justify="right", width=4)
    optsTable.add_column(ratio=1)

    for i, (opt, _) in enumerate(options, 1):
        mark = "[bold green]✔[/]" if i in selected else "○"
        row = f"{mark}  {opt}"
        if i - 1 == current:
            row = f"[reverse]{row}[/reverse]"
        optsTable.add_row(f"{i}.", row)

    aboutText = "No description."
    if abouts and 0 <= current < len(abouts):
        aboutText = abouts[current] or "No description."

    aboutPanel = Panel(
        aboutText,
        title="About",
        padding=(1, 2),
        box=box.ROUNDED,
        expand=True,
    )

    outer = Table.grid(expand=True)
    outer.add_column(ratio=2)
    outer.add_column(ratio=3)
    outer.add_row(optsTable, aboutPanel)

    return Panel(
        outer,
        title=title,
        subtitle="↑/↓ move • Space toggle • Enter confirm • q quit",
        padding=(1, 2),
        box=box.ROUNDED,
        expand=True,
    )


def multiSelect(
    options: List[Tuple[str, List[List[str]]]],
    title: str,
    richConsole: Console,
    abouts: Optional[List[str]] = None,
) -> Tuple[List[Tuple[str, List[List[str]]]], List[Tuple[str, List[List[str]]]]]:
    current = 0
    selected: set[int] = set(range(1, len(options) + 1))

    try:
        with Live(
            render(options, current, selected, title, abouts),
            console=richConsole,
            refresh_per_second=20,
        ) as live:
            while True:
                try:
                    key = readchar.readkey()
                except KeyboardInterrupt:
                    selected.clear()
                    break

                if key == rkey.UP:
                    current = (current - 1) % len(options)
                elif key == rkey.DOWN:
                    current = (current + 1) % len(options)
                elif key == rkey.SPACE:
                    idx = current + 1
                    if idx in selected:
                        selected.remove(idx)
                    else:
                        selected.add(idx)
                elif key in (rkey.ENTER, rkey.CR):
                    break
                elif key.lower() == "q":
                    selected.clear()
                    break

                live.update(render(options, current, selected, title, abouts))
    except KeyboardInterrupt:
        selected.clear()
    selectedOptions = []
    unSelectedOptions = []
    for i in range(1, len(options) + 1):
        if i in selected:
            selectedOptions.append(options[i - 1])
        else:
            unSelectedOptions.append(options[i - 1])
    return selectedOptions, unSelectedOptions


def cliRadioButton(
    options: List[Tuple[str, List[List[str]]]],
    title: str,
    richConsole: Console,
    abouts: Optional[List[str]] = None,
):
    selectedOptions, unSelectedOptions = multiSelect(
        options=options, title=title, richConsole=richConsole, abouts=abouts
    )
    return selectedOptions, unSelectedOptions
