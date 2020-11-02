import ply.lex as lex


# from .exceptions import InvalidPXFile

# Tokens
general_tokens = (
    "EQUAL",
    "COMMA",
    "SEP",
    "LPAREN",
    "RPAREN",
    "LSQAREPAREN",
    "RSQAREPAREN",
)

t_EQUAL = r"="
t_LPAREN = r"\("
t_LSQAREPAREN = r"\["
t_RPAREN = r"\)"
t_RSQAREPAREN = r"\]"

value_tokens = {"YES": "YES", "NO": "NO"}

# TODO: validate: DATA at end, STUB || HEADING
mandatory_tokens = {
    "DATA": "DATA",
    "DESCRIPTION": "DESCRIPTION",
    "HEADING": "HEADING",
    "MATRIX": "MATRIX",
    "STUB": "STUB",
    "SUBJECT-AREA": "SUBJECT-AREA",
    "TITLE": "TITLE",
    "UNITS": "UNITS",
    "VALUES": "VALUES",
}

tokens = general_tokens + tuple({**mandatory_tokens, **value_tokens}.values())
