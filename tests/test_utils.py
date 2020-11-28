from pathlib import Path
from typing import List

import pytest

from px.utils import encode_content


@pytest.mark.parametrize(
    "path_to_file",
    [
        (["tests", "data", "simple.px"]),
        (["tests", "data", "slovenia_gdp.px"]),
        (["tests", "data", "sweden_air_pollution.px"]),
    ],
)
def test_encode_content(path_to_file: List[str]) -> None:
    """Test decoding"""
    p = Path(*path_to_file)
    content = p.read_bytes()

    assert len(encode_content(content)) != 0
