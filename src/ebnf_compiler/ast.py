# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Abstract Syntax Tree
"""

from __future__ import annotations

from dataclasses import dataclass

from typing_extensions import override


@dataclass
class Node:
    def rich(self) -> str:
        return ""

    def referenced_idents(self) -> set[str]:
        return set()


@dataclass
class Factor(Node):
    pass


@dataclass
class Identifier(Factor):
    value: str

    @override
    def rich(self) -> str:
        return f"{self.value}"

    @override
    def referenced_idents(self) -> set[str]:
        return {self.value}


@dataclass
class Literal(Factor):
    value: str

    @override
    def rich(self) -> str:
        return f'[green]"{self.value}"[/green]'

    @override
    def referenced_idents(self) -> set[str]:
        return set()


@dataclass
class Term(Node):
    factors: list[Factor]

    @override
    def rich(self) -> str:
        return " ".join(f.rich() for f in self.factors)

    @override
    def referenced_idents(self) -> set[str]:
        result: set[str] = set()
        for f in self.factors:
            result |= f.referenced_idents()
        return result


@dataclass
class Expression(Factor):
    terms: list[Term]
    paren: bool = False

    @override
    def rich(self) -> str:
        inner = " [dim]|[/dim] ".join(t.rich() for t in self.terms)
        if self.paren:
            return f"[dim]([/dim] {inner} [dim])[/dim]"
        return inner

    @override
    def referenced_idents(self) -> set[str]:
        result: set[str] = set()
        for t in self.terms:
            result |= t.referenced_idents()
        return result


@dataclass
class Option(Factor):
    expr: Expression

    @override
    def rich(self) -> str:
        return f"[dim][[/dim] {self.expr.rich()} [dim]][/dim]"

    @override
    def referenced_idents(self) -> set[str]:
        return self.expr.referenced_idents()


@dataclass
class Repetition(Factor):
    expr: Expression

    @override
    def rich(self) -> str:
        return f"[dim]{{[/dim] {self.expr.rich()} [dim]}}[/dim]"

    @override
    def referenced_idents(self) -> set[str]:
        return self.expr.referenced_idents()


@dataclass
class Production(Node):
    identifier: Identifier
    expression: Expression

    @override
    def rich(self) -> str:
        return (
            f"[bold yellow]{self.identifier.value}[/bold yellow]"
            f" [cyan]=[/cyan] {self.expression.rich()} [cyan].[/cyan]"
        )


@dataclass
class Syntax(Node):
    production: list[Production]

    @override
    def rich(self) -> str:
        return "\n".join(prod.rich() for prod in self.production)

    def symbols(self) -> tuple[list[str], list[str]]:
        """Return (terminals, non_terminals) sorted alphabetically.

        Non-terminals are identifiers that have a production rule.
        Terminals are identifiers referenced in expressions but never defined.
        """
        defined = {prod.identifier.value for prod in self.production}
        referenced: set[str] = set()
        for prod in self.production:
            referenced |= prod.expression.referenced_idents()
        return sorted(referenced - defined), sorted(defined)
