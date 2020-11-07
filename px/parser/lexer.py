# type: ignore
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
    "DELIMITER",
    "EQUAL",
    "FLOAT",
    "INT",
    "LPAREN",
    "LSQUARE",
    "NEWLINE",
    "QUOTE",
    "RPAREN",
    "RSQUARE",
    "STRING",
    "SEMI",
)

t_DELIMITER = r"[\t\n ,]"
t_EQUAL = r"="
t_LPAREN = r"\("
t_LSQUARE = r"\["
t_NEWLINE = r"\n"
t_QUOTE = r"\""
t_RPAREN = r"\)"
t_RSQUARE = r"\]"
t_SEMI = r";"


def t_FLOAT(token):
    r"\d+\.\d+"
    token.value = float(token.value)
    return token


def t_INT(token):
    r"\d+"
    token.value = int(token.value)
    return token


t_STRING = r"[A-z0-9\-_:\ ]+"

lexer = lex.lex()
