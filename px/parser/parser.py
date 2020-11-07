# type: ignore
from pathlib import Path
from typing import Dict, List

import ply.yacc as yacc

from .lexer import tokens
from .interface import ParsedPxFile


__all__ = ["parse_px"]


parsed_file: ParsedPxFile = {}


def parse_px(file: Path, encoding: str) -> Dict:
    """
    Main method to start the parsing process.
    """
    parser = yacc.yacc()

    encoded_file = file.read_text(encoding=encoding)
    parser.parse(encoded_file)

    return parsed_file


def p_px(p):
    """
    px : px NEWLINE key EQUAL values
       | key EQUAL values
    """
    print(list(p))


def p_key(p) -> Dict:
    """
    key : STRING
        | STRING LSQUARE STRING RSQUARE
        | STRING LSQUARE STRING RSQUARE LPAREN STRING RPAREN
    """
    length = len(p)

    if length == 2:
        p[0] = {p[1]: {"translations": None}}
    elif length == 4:
        p[0] = {
            p[1]: {"translations": {p[3]: {"translation_key": None, "value": None}}}
        }
    else:
        p[0] = {
            p[1]: {"translations": {p[3]: {"translation_key": p[5], "value": None}}}
        }


def p_values(p):
    """
    values : values DELIMITER value SEMI
           | value SEMI
    """
    p[0] = [p[1]]

    if len(p) == 4:
        for item in p[3]:
            p[0].append(item)


def p_value(p):
    """
    value : STRING
          | FLOAT
          | INT
          | QUOTE STRING QUOTE
          | QUOTE FLOAT QUOTE
          | QUOTE INT QUOTE
    """
