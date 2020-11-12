from pathlib import Path
from typing import Dict, List, Union

import pytest

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
            ],
        ),
    ],
)
def test_tokenize_single_line(line: str, token_values: List[str]) -> None:
    """Lexer gets the correct values of on single lines"""
    lex.input(line)

    while True:
        tok = lex.token()
        if not tok:
            break
        assert tok.value == token_values.pop(0)


@pytest.mark.parametrize(
    "line, token_values",
    [
        (
            'DATA=\n10560.809918 12147.285179 \n"..." 15351.768082;',
            [
                "DATA",
                "=",
                10560.809918,
                " ",
                12147.285179,
                " ",
                "...",
                " ",
                15351.768082,
            ],
        ),
        (
            'VALUES("air pollutant")="Nitrogen oxide (t)","Non methane volatile organic compounds (NMVOC) (t)","Sulphur dioxide (t)","Ammonia (NH3) (t)","PM2.5 (t)","PM10 (t)","TSP (t)","Black carbon (BC) (t)","Carbon monoxide (CO) (t)","Lead (Pb) (kg)","Cadmium (Cd) (kg)","Mercury (Hg) (kg)",\n"Arsenic (As) (kg)","Chromium  (Cr) (kg)","Copper (Cu) (kg)","Nickel (Ni) (kg)","Selenium (Se) (kg)","Zink (Zn) (kg)","Dioxin (g I-Teq)","benzo(a)pyrene (kg)","benzo(b)fluoranthene (kg)","benzo(k)fluoranthene (kg)","Indeno(1,2,3-cd)pyrene (kg)",\n"PAH 1-4 (kg)","HCB (kg)","PCB  (kg)";',
            [
                "VALUES",
                "(",
                "air pollutant",
                ")",
                "=",
                "Nitrogen oxide (t)",
                ",",
                "Non methane volatile organic compounds (NMVOC) (t)",
                ",",
                "Sulphur dioxide (t)",
                ",",
                "Ammonia (NH3) (t)",
                ",",
                "PM2.5 (t)",
                ",",
                "PM10 (t)",
                ",",
                "TSP (t)",
                ",",
                "Black carbon (BC) (t)",
                ",",
                "Carbon monoxide (CO) (t)",
                ",",
                "Lead (Pb) (kg)",
                ",",
                "Cadmium (Cd) (kg)",
                ",",
                "Mercury (Hg) (kg)",
                ",",
                "Arsenic (As) (kg)",
                ",",
                "Chromium  (Cr) (kg)",
                ",",
                "Copper (Cu) (kg)",
                ",",
                "Nickel (Ni) (kg)",
                ",",
                "Selenium (Se) (kg)",
                ",",
                "Zink (Zn) (kg)",
                ",",
                "Dioxin (g I-Teq)",
                ",",
                "benzo(a)pyrene (kg)",
                ",",
                "benzo(b)fluoranthene (kg)",
                ",",
                "benzo(k)fluoranthene (kg)",
                ",",
                "Indeno(1,2,3-cd)pyrene (kg)",
                ",",
                "PAH 1-4 (kg)",
                ",",
                "HCB (kg)",
                ",",
                "PCB  (kg)",
            ],
        ),
    ],
)
def test_tokenize_multiple_line(line: str, token_values: List[str]) -> None:
    """Lexer gets the correct values of on multiple lines"""
    lex.input(line)

    while True:
        tok = lex.token()
        if not tok:
            break
        assert tok.value == token_values.pop(0)


@pytest.mark.parametrize(
    "path_to_file, token_values",
    [
        (
            [".", "tests", "data", "simple.px"],
            [
                "CHARSET",
                "=",
                "ANSI",
                "COPYRIGHT",
                "=",
                "YES",
                "DESCRIPTION",
                "=",
                "BDP Slovenija, letno",
                "TITLE",
                "=",
                "BDP: MERITVE, LETO",
                "HEADING",
                "=",
                "LETO",
                "TIMEVAL",
                "(",
                "LETO",
                ")",
                "=",
                "1995",
                ",",
                "1996",
                "DATA",
                "=",
                10560.809918,
                " ",
                12147.285179,
            ],
        )
    ],
)
def test_tokenize_file(
    path_to_file: List[str], token_values: List[str], read_file
) -> None:
    """Lexer gets the correct values from a px file"""
    content = read_file(path_to_file)
    lex.input(content)

    while True:
        tok = lex.token()
        if not tok:
            break
        print(dir(tok))
        print(tok.__dict__)

        assert tok.value == token_values.pop(0)


@pytest.mark.skip(reason="Not finished yet")
@pytest.mark.parametrize(
    "path_to_file, token_values",
    [
        (
            [".", "tests", "data", "simple.px"],
            [
                {
                    "value": "CHARSET",
                    "type": "UNQUOTED_STRING",
                    "lexpos": 0,
                    "lineno": 1,
                },
                {"value": "=", "type": "EQUAL", "lexpos": 7, "lineno": 1},
                {"value": "ANSI", "type": "STRING", "lexpos": 8, "lineno": 1},
                {
                    "value": "COPYRIGHT",
                    "type": "UNQUOTED_STRING",
                    "lexpos": 0,
                    "lineno": 2,
                },
                {"value": "=", "type": "EQUAL", "lexpos": 9, "lineno": 2},
                {"value": "YES", "type": "UNQUOTED_STRING", "lexpos": 10, "lineno": 2},
                {
                    "value": "DESCRIPTION",
                    "type": "UNQUOTED_STRING",
                    "lexpos": 0,
                    "lineno": 3,
                },
                {"value": "=", "type": "EQUAL", "lexpos": 11, "lineno": 3},
                {
                    "value": "BDP Slovenija, letno",
                    "type": "STRING",
                    "lexpos": 12,
                    "lineno": 3,
                },
                {
                    "value": "TITLE",
                    "type": "UNQUOTED_STRING",
                    "lexpos": 0,
                    "lineno": 4,
                },
                {"value": "=", "type": "EQUAL", "lexpos": 5, "lineno": 4},
                {
                    "value": "BDP: MERITVE, LETO",
                    "type": "STRING",
                    "lexpos": 6,
                    "lineno": 4,
                },
                {
                    "value": "HEADING",
                    "type": "UNQUOTED_STRING",
                    "lexpos": 0,
                    "lineno": 5,
                },
                {"value": "=", "type": "EQUAL", "lexpos": 7, "lineno": 5},
                {"value": "LETO", "type": "STRING", "lexpos": 8, "lineno": 5},
                {
                    "value": "TIMEVAL",
                    "type": "UNQUOTED_STRING",
                    "lexpos": 0,
                    "lineno": 6,
                },
                {"value": "(", "type": "LPAREN", "lexpos": 7, "lineno": 6},
                {"value": "LETO", "type": "STRING", "lexpos": 8, "lineno": 6},
                {"value": ")", "type": "RPAREN", "lexpos": 14, "lineno": 6},
                {"value": "=", "type": "EQUAL", "lexpos": 15, "lineno": 6},
                {"value": "1995", "type": "STRING", "lexpos": 16, "lineno": 6},
                {"value": ",", "type": "DELIMITER", "lexpos": 22, "lineno": 6},
                {"value": "1996", "type": "STRING", "lexpos": 23, "lineno": 6},
                {"value": "DATA", "type": "UNQUOTED_STRING", "lexpos": 0, "lineno": 7},
                {"value": "=", "type": "EQUAL", "lexpos": 3, "lineno": 7},
                {"value": 10560.809918, "type": "FLOAT", "lexpos": 5, "lineno": 7},
                {"value": " ", "type": "DELIMITER", "lexpos": 17, "lineno": 7},
                {"value": 12147.285179, "type": "FLOAT", "lexpos": 18, "lineno": 7},
            ],
        )
    ],
)
def test_lexer_generates_correct_tokens_for_file(
    path_to_file: List[str], token_values: List[Dict[str, Union[str, int]]], read_file
) -> None:
    """Lexer gets the correct values from a px file"""
    content = read_file(path_to_file)
    lex.input(content)

    while True:
        tok = lex.token()
        if not tok:
            break
        expected_token = token_values.pop(0)

        print(tok)
        print(tok.lexpos)

        assert tok.value == expected_token["value"]
        assert tok.type == expected_token["type"]
        assert tok.lineno == expected_token["lineno"]
        assert tok.lexpos == expected_token["lexpos"]
