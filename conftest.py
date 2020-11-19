from pathlib import Path
from typing import List, Optional

import pytest

from px.utils import encode_content


@pytest.fixture(scope="function")
def read_file():
    def _read_file(path_to_file_parts: List[str], encoding="utf-8") -> str:
        p = Path(*path_to_file_parts)
        byte_content = p.read_bytes()
        content = encode_content(byte_content)
        return content

    return _read_file
