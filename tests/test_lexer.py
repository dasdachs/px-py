from pathlib import Path
from typing import Dict, List, Union

import pytest

from px.parser import PxLexer
from .data.tokenized_files import tokenized_simple_px


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
def test_tokenizer_gets_correct_values_for_single_line(
    line: str, token_values: List[str]
) -> None:
    """Lexer gets the correct values of on single lines"""
    lex = PxLexer().lexer
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
def test_tokenizer_gets_correct_values_for_multiple_line(
    line: str, token_values: List[str]
) -> None:
    """Lexer gets the correct values of on multiple lines"""
    lex = PxLexer().lexer
    lex.input(line)

    while True:
        tok = lex.token()
        if not tok:
            break
        assert tok.value == token_values.pop(0)


@pytest.mark.parametrize(
    "path_to_file, token_values",
    [[[".", "tests", "data", "simple.px"], tokenized_simple_px[:]]],
)
def test_lexer_gets_correct_values_from_file(
    path_to_file: List[str], token_values: List[Dict[str, Union[str, int]]], read_file
) -> None:
    """Lexer gets the correct values from a px file"""
    content = read_file(path_to_file)

    lex = PxLexer().lexer
    lex.input(content)

    while True:
        tok = lex.token()
        if not tok:
            break
        expected_token = token_values.pop(0)

        assert tok.value == expected_token["value"]


@pytest.mark.parametrize(
    "path_to_file, token_values",
    [[[".", "tests", "data", "simple.px"], tokenized_simple_px[:]]],
)
def test_lexer_gets_correct_types_from_file(
    path_to_file: List[str], token_values: List[Dict[str, Union[str, int]]], read_file
) -> None:
    """Lexer gets the correct values from a px file"""
    content = read_file(path_to_file)

    lex = PxLexer().lexer
    lex.input(content)

    while True:
        tok = lex.token()
        if not tok:
            break
        expected_token = token_values.pop(0)

        assert tok.type == expected_token["type"]


@pytest.mark.parametrize(
    "path_to_file, token_values",
    [[[".", "tests", "data", "simple.px"], tokenized_simple_px[:]]],
)
def test_lexer_gets_correct_line_from_file(
    path_to_file: List[str], token_values: List[Dict[str, Union[str, int]]], read_file
) -> None:
    """Lexer gets the correct values from a px file"""
    content = read_file(path_to_file)

    lex = PxLexer().lexer
    lex.input(content)

    while True:
        tok = lex.token()
        if not tok:
            break
        expected_token = token_values.pop(0)

        assert tok.lineno == expected_token["lineno"]


@pytest.mark.parametrize(
    "path_to_file, token_values",
    [[[".", "tests", "data", "simple.px"], tokenized_simple_px[:]]],
)
def test_lexer_gets_correct_position_from_file(
    path_to_file: List[str], token_values: List[Dict[str, Union[str, int]]], read_file
) -> None:
    """Lexer gets the correct values from a px file"""
    content = read_file(path_to_file)

    lex = PxLexer().lexer
    lex.input(content)

    while True:
        tok = lex.token()
        if not tok:
            break
        expected_token = token_values.pop(0)

        assert tok.lexpos == expected_token["lexpos"]
