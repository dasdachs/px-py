from typing import Dict, List

import pytest

from px.parser import PxParser
from .data.parsed_files import parsed_simple_px


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            'CHARSET="ANSI";',
            {
                "charset": {
                    "default": {
                        "key": "CHARSET",
                        "values": ["ANSI"],
                    },
                    "translations": {},
                }
            },
        ),
        (
            "DATA=\n10560.809918 12147.285179;",
            {
                "data": {
                    "default": {
                        "key": "DATA",
                        "values": [10560.809918, 12147.285179],
                    },
                    "translations": {},
                }
            },
        ),
        (
            'TIMEVAL("LETO")="1995","1996";',
            {
                "timeval": {
                    "default": {
                        "key": "TIMEVAL",
                        "link_to_heading_value": "LETO",
                        "values": ["1995", "1996"],
                    },
                    "translations": {},
                },
            },
        ),
    ],
)
def test_single_line_parsing(line: str, expected: Dict[str, str]) -> None:
    """Parser should get and parse single lines"""
    parser = PxParser()
    result = parser.parse(line)

    assert result == expected


@pytest.mark.parametrize(
    "line, expected",
    [
        (
            'CHARSET="ANSI";\nDATA=\n10560.809918 12147.285179;',
            {
                "charset": {
                    "default": {
                        "key": "CHARSET",
                        "values": ["ANSI"],
                    },
                    "translations": {},
                },
                "data": {
                    "default": {
                        "key": "DATA",
                        "values": [10560.809918, 12147.285179],
                    },
                    "translations": {},
                },
            },
        ),
    ],
)
def test_multiline_line_parsing(line: str, expected: Dict[str, str]) -> None:
    """Parser should get and parse multiple lines"""
    parser = PxParser()
    result = parser.parse(line)

    assert result == expected


@pytest.mark.parametrize(
    "path_to_file, expected",
    [
        (["tests", "data", "simple.px"], parsed_simple_px),
    ],
)
def test_file_parsing(
    path_to_file: List[str], expected: Dict[str, str], read_file
) -> None:
    """Parser should get and parse multiple lines"""
    content = read_file(path_to_file)

    parser = PxParser()
    result = parser.parse(content)

    assert result == expected
