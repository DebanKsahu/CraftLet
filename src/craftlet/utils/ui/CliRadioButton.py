from typing import List

import readchar
from readchar import key as rkey
from rich import box
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


def render(options, current, selected, title):
    table = Table.grid(expand=True)
    table.add_column(justify="right", width=4)
    table.add_column(ratio=1)

    for i, opt in enumerate(options, 1):
        mark = "[bold green]✔[/]" if i in selected else "○"
        row = f"{mark}  {opt}"
        if i - 1 == current:
            row = f"[reverse]{row}[/reverse]"
        table.add_row(f"{i}.", row)

    return Panel(
        table,
        title=title,
        subtitle="↑/↓ move • Space toggle • Enter confirm • q quit",
        padding=(1, 2),
        box=box.ROUNDED,
        expand=True,
    )


def multiSelect(options: List[str], title: str, richConsole: Console) -> List[str]:
    current = 0
    selected: set[int] = set()

    try:
        with Live(
            render(options, current, selected, title), console=richConsole, refresh_per_second=20
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

                live.update(render(options, current, selected, title))
    except KeyboardInterrupt:
        selected.clear()

    return [options[i - 1] for i in sorted(selected)]


def CliRadioButton(options: List[str], title: str, richConsole: Console):
    selectedOptions = multiSelect(options=options, title=title, richConsole=richConsole)
    richConsole.print("\n[bold green]Selected:[/]", selectedOptions)
