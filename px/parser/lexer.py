# type: ignore
"""
The lexer adheres to the 2013 PX version.

https://www.scb.se/en/services/statistical-programs-for-px-files/px-file-format/

Some outtakes:
--------------
- delimiters are: space, semicolon, tab comma and can be used
  interchangable
"""
from ply import lex
from ply.lex import LexToken


__all__ = ["tokens", "lexer"]


tokens = (
    "DELIMITER",
    "EQUAL",
    "FLOAT",
    "INT",
    "LPAREN",
    "LSQUARE",
    "NEWLINE",
    "RPAREN",
    "RSQUARE",
    "STRING",
    "SEMI",
    "UNQUOTED_STRING",
)

t_DELIMITER = r"[\t\n ,]"
t_EQUAL = r"="
t_LPAREN = r"\("
t_LSQUARE = r"\["
t_NEWLINE = r"\n"
t_RPAREN = r"\)"
t_RSQUARE = r"\]"
t_SEMI = r";"
t_UNQUOTED_STRING = r"\w+"

t_ignore = "\n"


def t_FLOAT(token: LexToken) -> LexToken:
    r"\d+\.\d+"
    token.value = float(token.value)
    return token


def t_INT(token: LexToken) -> LexToken:
    r"\d+"
    token.value = int(token.value)
    return token


def t_STRING(token: LexToken) -> LexToken:
    r"\".*?\""
    token.value = token.value[1:-1]
    return token


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
