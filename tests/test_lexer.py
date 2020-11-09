# from pathlib import Path
from typing import List

import pytest
from ply.lex import LexToken

from px.parser import lexer as lex


@pytest.mark.parametrize(
    "line, token_values",
    [
        ('CHARSET="ANSI";', ["CHARSET", "=", "ANSI", ";"]),
        (
            'DESCRIPTION="BDP Slovenija, letno";',
            ["DESCRIPTION", "=", "BDP Slovenija, letno", ";"],
        ),
        (
            'VALUES("LETO")="1995","1996","1997","1998","1999","2000","2001";',
            [
                "VALUES",
                "(",
                "LETO",
                ")",
                "=",
                "1995",
                ",",
                "1996",
                ",",
                "1997",
                ",",
                "1998",
                ",",
                "1999",
                ",",
                "2000",
                ",",
                "2001",
                ";",
            ],
        ),
        (
            'VALUES[en]("MEASURES")="Current prices (mio EUR)","Constant previous year prices (mio EUR)";',
            [
                "VALUES",
                "[",
                "en",
                "]",
                "(",
                "MEASURES",
                ")",
                "=",
                "Current prices (mio EUR)",
                ",",
                "Constant previous year prices (mio EUR)",
                ";",
            ],
        ),
    ],
)
def test_tokenize_single_line(line: str, token_values: List[str]) -> None:
    lex.input(line)

    while True:
        tok = lex.token()
        if not tok:
            break
        assert tok.value == token_values.pop(0)
