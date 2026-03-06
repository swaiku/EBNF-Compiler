# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Parser
"""

from dataclasses import dataclass

from loguru import logger

from .ast import (
    Expression,
    Factor,
    Identifier,
    Literal,
    Option,
    Production,
    Repetition,
    Syntax,
    Term,
)
from .scanner import Scanner
from .tokens import Token


@dataclass
class Parser:
    scanner: Scanner
    has_error: bool = False

    def raise_error(self, msg: str) -> None:
        self.has_error = True
        self.scanner.print_error(msg)
        raise Exception(msg)

    def raise_expected_error(self, expected: Token) -> None:
        self.raise_error(f"Expected '{expected}', but got '{self.scanner.sym}'")

    def factor(self) -> Factor:
        logger.debug("Factor")
        sym = self.scanner.sym
        if sym == Token.IDENT:
            value = self.scanner.value
            self.scanner.get_next_symbol()
            return Identifier(value=value)
        elif sym == Token.LITERAL:
            value = self.scanner.value
            self.scanner.get_next_symbol()
            return Literal(value=value)
        elif sym == Token.LPAREN:
            self.scanner.get_next_symbol()
            expr = self.expression()
            if self.scanner.sym != Token.RPAREN:
                self.raise_expected_error(Token.RPAREN)
            self.scanner.get_next_symbol()
            expr.paren = True
            return expr
        elif sym == Token.LBRAK:
            self.scanner.get_next_symbol()
            expr = self.expression()
            if self.scanner.sym != Token.RBRAK:
                self.raise_expected_error(Token.RBRAK)
            self.scanner.get_next_symbol()
            return Option(expr=expr)
        elif sym == Token.LBRACE:
            self.scanner.get_next_symbol()
            expr = self.expression()
            if self.scanner.sym != Token.RBRACE:
                self.raise_expected_error(Token.RBRACE)
            self.scanner.get_next_symbol()
            return Repetition(expr=expr)
        else:
            self.raise_error(
                f"Expected identifier, literal, '(', '['. or '{{' got {sym}"
            )
            raise Exception("Unexpected symbol")

    def term(self) -> Term:
        logger.debug("Term")
        factors: list[Factor] = [self.factor()]
        while self.scanner.sym in (
            Token.IDENT,
            Token.LITERAL,
            Token.LPAREN,
            Token.LBRAK,
            Token.LBRACE,
        ):
            factors.append(self.factor())
        return Term(factors=factors)

    def expression(self) -> Expression:
        logger.debug("Expression")
        terms = [self.term()]
        while self.scanner.sym == Token.BAR:
            self.scanner.get_next_symbol()
            terms.append(self.term())
        return Expression(terms=terms)

    def production(self) -> Production:
        logger.debug("Production")
        if self.scanner.sym != Token.IDENT:
            self.raise_expected_error(Token.IDENT)
        identifier = Identifier(value=self.scanner.value)
        self.scanner.get_next_symbol()
        if self.scanner.sym != Token.EQL:
            self.raise_expected_error(Token.EQL)
        self.scanner.get_next_symbol()
        expr = self.expression()
        if self.scanner.sym != Token.PERIOD:
            self.raise_expected_error(Token.PERIOD)
        self.scanner.get_next_symbol()
        return Production(identifier=identifier, expression=expr)

    def syntax(self) -> Syntax:
        logger.debug("Syntax")
        productions: list[Production] = []
        while self.scanner.sym != Token.EOF:
            if self.scanner.sym != Token.IDENT:
                self.raise_expected_error(Token.IDENT)
            productions.append(self.production())
        return Syntax(production=productions)

    def parse(self) -> Syntax:
        logger.debug("Parsing")
        self.scanner.get_next_symbol()
        return self.syntax()
