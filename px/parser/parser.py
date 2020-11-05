# type: ignore
from typing import Dict

import ply.yacc as yacc

from .lexer import tokens


__all__ = ["parse_px"]


parser = yacc.yacc()


def parse_px(content: str) -> Dict:
    pass
