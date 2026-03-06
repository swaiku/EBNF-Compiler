# SPDX-FileCopyrightText: 2026 Jérémy Prin
# SPDX-License-Identifier: MIT OR Apache-2.0

import io
import sys

from loguru import logger

from ebnf_compiler.parser import Parser
from ebnf_compiler.scanner import Scanner
from ebnf_compiler.tokens import Token

SRC = """
syntax = {production}.
production = identifier "=" expression "." .
expression = term {"|" term}.
term = factor {factor}.
factor = identifier | string | "(" expression ")" | "[" expression "]" | "{" expression "}".
"""


def test_simple():
    logger.remove()
    _ = logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    source = io.StringIO(SRC)
    scanner.init(source)
    parser = Parser(scanner=scanner)

    parser.parse()


SRC_NESTED_COMMENTS = """
(* outer comment (* nested comment *) still outer *)
syntax = {production}.
(* another (* deeply (* nested *) comment *) here *)
production = identifier "=" expression "." .
"""


def test_nested_comments():
    logger.remove()

    scanner = Scanner()
    scanner.init(io.StringIO(SRC_NESTED_COMMENTS))

    tokens = []
    while True:
        scanner.get_next_symbol()
        tokens.append((scanner.sym, scanner.value))
        if scanner.sym == Token.EOF:
            break

    # Comments must be fully skipped; only real tokens remain
    expected = [
        (Token.IDENT, "syntax"),
        (Token.EQL, "="),
        (Token.LBRACE, "{"),
        (Token.IDENT, "production"),
        (Token.RBRACE, "}"),
        (Token.PERIOD, "."),
        (Token.IDENT, "production"),
        (Token.EQL, "="),
        (Token.IDENT, "identifier"),
        (Token.LITERAL, "="),
        (Token.IDENT, "expression"),
        (Token.LITERAL, "."),
        (Token.PERIOD, "."),
        (Token.EOF, ""),
    ]
    assert tokens == expected
