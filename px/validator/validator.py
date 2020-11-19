from typing import Dict, List, Optional, Union
from enum import Enum

__all__ = ["PxFileValidator"]


class PxFileValidator(object):
    def __init__(
        self,
        content: Optional[str] = None,
        parsed_file: Optional[Dict[str, Union[Dict, List]]] = None,
        specs_version="2013",
    ) -> None:
        self._content = content
        self._parsed_file = parsed_file
        self.parsing_errors: List[ParsingError] = []
        self.specs_version = specs_version

    def validate_file_structure(self) -> Union[bool, None]:
        """
        Checks the overall file structure.

        It does not check the syntax, file integrity or key/value rules.

        Rules to check:
        ---------------
        - DATA key is at the end of the file
        """
        if not self._content:
            raise AttributeError("No file content provided")
        file_is_valid = True

        # Replace unix newlines (\n) and windows new lines (\n\r)
        # and split by ; (newline in px files)
        lines = self._content.replace("\n", "").replace("\r", "").split(";")

        # Last line could be an empty line or EOF that will be represented
        # as a blank line and should be removed
        if lines[-1] == "":
            lines.pop()

        if not lines[-1].startswith("DATA"):
            self.parsing_errors.append(
                ParsingError("DATA key must be at the end of the file")
            )
            file_is_valid = False

        return file_is_valid

    def load_validaton_rules(self):
        """Loads and reads simple csv rules for px file validation"""
        # self.specs_version
        pass


class ParsingError(object):
    def __init__(
        self,
        error_msg: str,
    ) -> None:
        self.msg = error_msg

    def __str__(self):
        return f"Error while parsing file: {self.msg}. "
