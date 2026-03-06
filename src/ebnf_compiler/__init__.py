# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Compiler
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text

from .ast import Syntax
from .parser import Parser
from .scanner import Scanner

console = Console()
app = typer.Typer()


@dataclass
class Compiler:
    scanner: Scanner
    parser: Parser

    def compile(self) -> None:
        try:
            _ = self.parser.parse()
        except Exception as e:
            print(f"{e}")

    def ast(self) -> Syntax | None:
        try:
            return self.parser.parse()
        except Exception:
            return None


@app.command(context_settings={"ignore_unknown_options": True})
def main(
    source: Annotated[Path, typer.Argument()],
    debug: bool = False,
    show_tree: bool = False,
    show_symbols: bool = False,
):

    logger.remove()
    if debug:
        _ = logger.add(sys.stdout, level="DEBUG")
    else:
        _ = logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    scanner.open(source)
    parser = Parser(scanner=scanner)

    compiler = Compiler(scanner=scanner, parser=parser)
    ast_ = compiler.ast()

    if ast_ is None:
        console.print("[red]Compilation failed[/red]")
        return
    elif show_tree:
        console.print(Panel(Pretty(ast_, indent_size=2), title="Syntax Tree"))
    elif show_symbols:
        terminals, non_terminals = ast_.symbols()
        content = Text()
        _ = content.append("Terminal Symbols\n", style="bold")
        for t in terminals:
            _ = content.append(f"- {t}\n", style="green")
        _ = content.append("\nNon-terminal Symbols\n", style="bold")
        for nt in non_terminals:
            _ = content.append(f"- {nt}\n", style="cyan")
        console.print(Panel(content, title="Symbols"))
    else:
        console.print(Panel(ast_.rich(), title="Code"))


if __name__ == "__main__":
    app()
