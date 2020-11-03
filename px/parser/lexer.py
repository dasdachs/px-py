"""
The lexer adheres to the 2013 PX version.

https://www.scb.se/en/services/statistical-programs-for-px-files/px-file-format/

Some outtakes:
--------------
- delimiters are: space, semicolon, tab comma and can be used
  interchangable
"""
import ply.lex as lex


__all__ = ["lexer"]


tokens = (
    "COMMA",
    "DELIMITER",
    "EQUAL",
    "LPAREN",
    "LSQAREPAREN",
    "QUOTE",
    "RPAREN",
    "RSQAREPAREN",
    "SPACE",
)

t_EQUAL = r"="
t_DELIMITER = r"[\t ,;]"
t_LPAREN = r"\("
t_LSQUARE = r"\["
t_QUOTE = r"\""
t_RPAREN = r"\)"
t_RSQUARE = r"\]"

t_STRING = r"\w+"


def t_FLOAT(token):
    r"\d+\.\d+"
    token.value = int(token.value)
    return token


def t_FLOAT(token):
    r"\d+\.\d+"
    token.value = int(token.value)
    return token


lexer = lex.lex()
