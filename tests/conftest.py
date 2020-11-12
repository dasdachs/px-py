from pathlib import Path
from typing import List, Optional

import pytest


@pytest.fixture
def read_file():
    def _read_file(path_to_file_parts: List[str], encoding="UTF-8") -> str:
        p = Path(*path_to_file_parts)
        return p.read_text(encoding=encoding)

    return _read_file
