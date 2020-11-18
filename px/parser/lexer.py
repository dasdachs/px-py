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


__all__ = ["PxLexer"]


class PxLexer(object):
    tokens = (
        "DELIMITER",
        "EQUAL",
        "FLOAT",
        "INT",
        "LPAREN",
        "LSQUARE",
        "RPAREN",
        "RSQUARE",
        "STRING",
        "UNQUOTED_STRING",
    )

    t_DELIMITER = r"[\t\n ,]"
    t_EQUAL = r"="
    t_LPAREN = r"\("
    t_LSQUARE = r"\["
    t_RPAREN = r"\)"
    t_RSQUARE = r"\]"
    # UNQUOTED_STRING are strings that do not allow any special characters, like commas etc
    t_UNQUOTED_STRING = r"[\w_-]+"

    def t_FLOAT(self, token: LexToken) -> LexToken:
        r"\d+\.\d+"
        token.value = float(token.value)
        return token

    def t_INT(self, token: LexToken) -> LexToken:
        r"\d+"
        token.value = int(token.value)
        return token

    def t_STRING(self, token: LexToken) -> LexToken:
        r"\".*?\""
        token.value = token.value[1:-1]
        return token

    def t_newline(self, token: LexToken) -> LexToken:
        r";"
        token.lexer.lineno += len(token.value)

    t_ignore = "\n"

    def t_error(self, token: LexToken) -> None:
        print(f"Illegal character {token.value[0]}")
        token.lexer.skip(1)

    # Build the lexer
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
