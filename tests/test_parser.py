from typing import Dict

import pytest

from px.parser import PxParser


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
    ],
)
def test_single_line_parsing(line: str, expected: Dict[str, str]) -> None:
    """Parser should get and parse single lines"""
    parser = PxParser()
    result = parser.parse(line)

    assert result == expected
