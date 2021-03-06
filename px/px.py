import json
from pathlib import Path
from typing import List, Dict, Optional

from px.parser import PxParser
from .exceptions import FileNotFoundError


__all__ = ["PxPy"]


class PxPy:
    """
    Main class for dealing with px files. It is a collection of parsed px files
    for selected languages.
    """

    def __init__(
        self, parsed_data: Dict, selected_language: Optional[str] = None
    ) -> None:
        self._data = parsed_data
        self._px_array: List[Px] = []
        self._selected_px_file_index = 0
        print(parsed_data)
        # for index, file in enumerate(self._data.values()):
        #     self._px_array.append(Px(file))
        #     if file["LANGUAGE"] == selected_language:
        #         self._selected_px_file_index = index

    @staticmethod
    def read_file(path: str, selected_language: Optional[str] = None):
        p = Path(path)

        if not p or not p.exists() or p.is_dir():
            raise FileNotFoundError

        try:
            content = p.read_bytes()
            parsed_file = PxParser().parse(content)

            return PxPy(parsed_file, selected_language)
        except UnicodeDecodeError as e:
            print(f"Opening file throwed an UnicodeDecodeError. Error: {e}")

    @staticmethod
    def read_csv() -> None:
        pass

    @staticmethod
    def read_excel() -> None:
        pass

    @staticmethod
    def read_json() -> None:
        pass

    @staticmethod
    def read_dataFrame() -> None:
        pass

    @property
    def language(self) -> Optional[str]:
        return self._px_array[self._selected_px_file_index].language

    @property
    def title(self) -> Optional[str]:
        return self._px_array[self._selected_px_file_index].title

    def to_excel(self) -> None:
        pass

    def to_csv(self) -> None:
        pass

    def to_json(self) -> None:
        pass

    def to_dataFrame(self) -> None:
        pass


class Px:
    def __init__(self, data: Dict) -> None:
        self._data = data

        self.title = data.get("TITLE")
        self.language = data.get("LANGUAGE")
