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
    lex.input(line)

    while True:
        tok = lex.token()
        if not tok:
            break
        print(tok)
        assert tok.value == token_values.pop(0)
