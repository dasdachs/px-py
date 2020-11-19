import chardet

from .exceptions import InvalidPXFile


def encode_content(content: bytes) -> str:
    """
    Reads and finds the content encoding. Default to 'utf-8'

    To do so it gets the value form the CHARSET key.
    If the value exists it first tries to find the name in the
    encoding aliases. If there is no alias, then the value is used
    to decode the byte string.

    """
    encoding = "utf-8"
    try:
        detect = chardet.detect(content)
        encoding = detect.get("encoding", encoding)

        return content.decode(encoding)
    except IndexError:
        raise InvalidPXFile("File has no CHARSET value")
    except LookupError:
        raise InvalidPXFile(f"File encoding {encoding} is not valid")
