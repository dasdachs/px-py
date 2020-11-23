from typing import List

import pytest

from px.validator import PxFileValidator


# with pytest.raises(ZeroDivisionError):


@pytest.mark.parametrize(
    "path_to_file, is_valid",
    [
        (["tests", "data", "simple.px"], False),
        (["tests", "data", "slovenia_gdp.px"], True),
        (["tests", "data", "sweden_air_pollution.px"], True),
    ],
)
def test_file_structure_is_valid(
    path_to_file: List[str], is_valid: bool, read_file
) -> None:
    """Tests if example data files are valid"""
    file_content = read_file(path_to_file)
    validator = PxFileValidator(content=file_content)

    assert validator.validate_file_structure() == is_valid


@pytest.mark.parametrize(
    "spec_version, mandatory_keys",
    [
        (
            "2013",
            [
                "contents",
                "data",
                "decimals",
                "description",
                "heading",
                "matrix",
                "stub",
                "subject-area",
                "subject-code",
                "title",
                "units",
                "values",
            ],
        )
    ],
)
def test_mandatory_fields(spec_version: str, mandatory_keys: List[str]) -> None:
    """Tests if example data files are valid"""
    validator = PxFileValidator(specs_version=spec_version)

    assert validator.mandatory_keywords == mandatory_keys
