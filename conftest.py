from pathlib import Path
from typing import List, Optional

import pytest


@pytest.fixture(scope="function")
def read_file():
    def _read_file(path_to_file_parts: List[str], encoding="utf-8") -> str:
        p = Path(*path_to_file_parts)
        content = p.read_text(encoding=encoding)
        return content

    return _read_file
