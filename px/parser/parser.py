# type: ignore
from pathlib import Path
from typing import Dict, List, Union

import ply.yacc as yacc

from px.parser.lexer import PxLexer

# from px.parser.interface import ParsedPxFile


__all__ = ["PxParser"]


class PxParser(object):
    tokens = PxLexer.tokens

    def __init__(self):
        self._lexer = PxLexer().lexer
        self._parser = yacc.yacc(module=self)
        self.parsed_file = {}

    def parse(self, text: str):
        """
        Main method to start the parsing process.
        """
        return self._parser.parse(text)

    def parse_file(self, file: Path, encoding: str) -> Dict:
        pass

    def p_px(self, p) -> Dict[str, Union[str, int, float]]:
        """
        px : px key_value
           | key_value
        """
        if len(p) == 3:
            p[0] = {**p[1], **p[2]}
        else:
            p[0] = p[1]

    def p_key_value(self, p) -> Dict:
        """
        key_value : key EQUAL values
        """
        key = p[1]["key"]
        p[1]["parsed_values"][key]["default"]["values"] = p[3]
        p[0] = p[1]["parsed_values"]

    def p_key(self, p) -> Dict:
        """
        key : key_with_translation
            | key_with_and_stub
            | simple_key
        """
        key = list(p[1].keys())[0]
        p[0] = {"key": key, "parsed_values": p[1]}

    def p_simple_key(self, p) -> Dict:
        """
        simple_key : UNQUOTED_STRING
        """
        p[0] = {
            p[1].lower(): {
                "default": {
                    "key": p[1],
                    "values": [],
                },
                "translations": {},
            }
        }

    def p_key_with_translation(self, p) -> Dict:
        """
        key_with_translation : UNQUOTED_STRING LSQUARE UNQUOTED_STRING RSQUARE
        """
        p[0] = {
            p[1].lower(): {
                "default": {
                    "key": p[1],
                    "values": [],
                },
                "translations": {p[3]: {"data": []}},
            }
        }

    def p_key_with_and_stub(self, p) -> Dict:
        """
        key_with_and_stub : UNQUOTED_STRING LPAREN STRING RPAREN
        """
        p[0] = {
            p[1].lower(): {
                "default": {
                    "key": p[1],
                    "link_to_heading_value": p[3],
                    "values": [],
                },
                "translations": {},
            }
        }

    def p_values(self, p):
        """
        values : values DELIMITER value
               | value
        """
        if len(p) == 4:
            p[1].append(p[3])
        else:
            p[1] = [p[1]]
        p[0] = p[1]

    def p_value(self, p):
        """
        value : UNQUOTED_STRING
              | FLOAT
              | INT
              | STRING
        """
        p[0] = p[1]
