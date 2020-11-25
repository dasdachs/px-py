import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import cast, Dict, List, Optional, Union
from enum import Enum

from px.exceptions import InvalidParserOutput, InvalidRulesSpec


__all__ = ["PxFileValidator"]


class ValidationErrorType(Enum):
    MandatoryKeyError = "Mandatory key error"
    ValuesError = "Value error"
    ValidationError = "Validation error"


class PxFileValidator(object):
    PATH_TO_RULES_FILE = [".", "data", "key_value_rules.csv"]

    def __init__(
        self,
        content: Optional[str] = None,
        parsed_file: Optional[
            Dict[
                str,
                Dict,
            ]
        ] = None,
        specs_version="2013",
    ) -> None:
        self._content = content
        self._parsed_file = parsed_file
        self.specs_version = specs_version

        self.mandatory_keywords: List[str] = []
        self._rules: Dict[str, KeyValueValidationRule] = {}

        self.validation_errors: List[ValidationError] = []

        self._load_validaton_rules()

    def validate_file_structure(self) -> bool:
        """
        Checks the overall file structure.

        It does not check the syntax, file integrity or key/value rules.

        Rules to check:
        ---------------
        - DATA key is at the end of the file
        - mandatory keywords are present
        """
        file_is_valid = True

        # Replace unix newlines (\n) and windows new lines (\n\r)
        # and split by ; (newline in px files)
        lines = self._content.replace("\n", "").replace("\r", "").split(";")

        # Last line could be an empty line or EOF that will be represented
        # as a blank line and should be removed
        if lines[-1] == "":
            lines.pop()

        if not lines[-1].startswith("DATA"):
            self.validation_errors.append(
                ValidationError(
                    "DATA key must be at the end of the file",
                    ValidationErrorType.MandatoryKeyError,
                )
            )
            file_is_valid = False

        key_re = re.compile(r"^[A-Z_-]+")

        keys = []

        for line in lines:
            try:
                p = re.match(key_re, line)
                key = p.group().lower()
                keys.append(key)
            except AttributeError:
                # TODO: log in debug and make possible to fix
                raise InvalidRulesSpec(
                    f"The rule for {line[0]}, spec version {line[1]} is not valid"
                )

        for key in self.mandatory_keywords:
            if key not in keys:
                key_validator = self._rules.get(key)
                if (
                    key_validator.mandatory_exception
                    and key_validator.mandatory_exception in keys
                ):
                    continue
                file_is_valid = False
                self.validation_errors.append(
                    ValidationError(
                        f"{key} is mandatory (px-file specs {self.specs_version})",
                        ValidationErrorType.MandatoryKeyError,
                    )
                )

        return file_is_valid

    def validate_values(self) -> None:
        """Get all the values and checks if the values are valid"""
        for key, value in self._parsed_file.items():
            rule = self._rules.get(key)

            if not rule:
                raise InvalidRulesSpec(f"Missing rule for {key}")

            try:
                values = value.get("default", {})
                values = values.get("values")

                validation_errors = rule.validate(values)

                if len(value) != 0:
                    self.validation_errors += validation_errors
            except KeyError:
                raise InvalidParserOutput(f"Missing vales for {key}")

    def _load_validaton_rules(self) -> None:
        """Loads and reads simple csv rules for px file validation"""
        # self.specs_version
        rules_file = Path(*self.PATH_TO_RULES_FILE)

        with open(rules_file) as f:
            csv_reader = csv.reader(f, delimiter=",", quotechar='"')
            for line in csv_reader:
                spec_version = line[1]
                if spec_version == self.specs_version:
                    rule = KeyValueValidationRule.from_rule(line)
                    self._rules[rule.keyword] = rule

                    if rule.mandatory_keyword:
                        self.mandatory_keywords.append(rule.keyword)


@dataclass
class ValidationError:
    error_msg: str
    value_type: Optional[ValidationErrorType] = ValidationErrorType.ValidationError

    def __str__(self):
        return f"[{self.value_type}]Error while validating file: {self.error_msg}."


class KeyValueValidationRule(object):
    def __init__(
        self,
        keyword: str,
        mandatory_keyword: bool,
        spec_version: int,
        value_types: str,
        value_length: Optional[int] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        mandatory_exception: Optional[str] = None,
    ) -> None:
        self.mandatory_keyword = mandatory_keyword
        self.mandatory_exception = (
            mandatory_exception.lower() if mandatory_exception else None
        )

        self._keyword = keyword
        self._spec_version = spec_version
        self._valid_types: List = self._get_validation_types(value_types)
        self._value_length = value_length
        self._min_value = min_value
        self._max_value = max_value

    @staticmethod
    def from_rule(rule_parts: List[str]) -> "KeyValueValidationRule":
        """
        Parses a string describing a key-value rule

        The expected structure is:
        key,spec_version,mandatory,type,multiline,value_length,min_val,max_val,not_required_if

        example:
        CONTENTS,2013,yes,text,no,256

        For the rules only this specs are important:
        - key,
        - spec_version,
        - type,
        - value_length,
        - min_val,
        - max_val
        - not_required_if
        """
        key = rule_parts[0]
        spec_version = int(rule_parts[1])
        mandatory = bool(rule_parts[2])
        types = rule_parts[3]
        length = None

        try:
            length = int(rule_parts[5])
        except IndexError:
            # TODO: Log out in debug mode
            pass
        except ValueError:
            # TODO: Log out in debug mode
            pass

        min_val = None
        max_val = None

        if len(rule_parts) >= 8:
            try:
                min_val = int(rule_parts[6])
                max_val = int(rule_parts[7])
            except ValueError:
                # TODO: Log out in debug mode
                pass

        mandatory_exception = None
        if len(rule_parts) == 9:
            mandatory_exception = rule_parts[8]

        return KeyValueValidationRule(
            key,
            mandatory,
            spec_version,
            types,
            length,
            min_val,
            max_val,
            mandatory_exception,
        )

    @property
    def keyword(self):
        return self._keyword.lower()

    def validate(self, values: List[Union[str, int, float]]) -> List[ValidationError]:
        """Validates values for a given key"""
        validation_errors: List[ValidationError] = []

        for value in values:
            errors = self.validate_value(value)

            if len(errors) != 0:
                validation_errors += errors

        return validation_errors

    def validate_value(self, value: Union[str, int, float]) -> List[ValidationError]:
        """Validate individual error based on value type"""
        validation_errors: List[ValidationError] = []

        type_error = self._validate_type(value)

        if type_error:
            validation_errors.append(type_error)

        length_error = self._validate_length(value)

        if length_error:
            validation_errors.append(length_error)

        if type(value) != str:
            value = cast(Union[int, float], value)
            min_max_error = self._validate_min_or_max(value)

            if min_max_error:
                validation_errors.append(min_max_error)

        return validation_errors

    def _validate_type(
        self, value: Union[str, int, float]
    ) -> Union[None, "ValidationError"]:
        """Validate single value type"""
        validation_error = None

        value_type = type(value)

        if value_type not in self._valid_types:
            validation_error = ValidationError(
                f"Value {value} for {self._keyword} is type {value_type}, but should be {self._valid_types}",
                ValidationErrorType.ValuesError,
            )

        return validation_error

    def _validate_length(
        self, value: Union[str, int, float]
    ) -> Union[None, "ValidationError"]:
        """Validate single value length"""
        validation_error = None

        if type(value) != str:
            value = str(value)

        value = cast(str, value)

        if len(value) > self._value_length:
            validation_error = ValidationError(
                f"Value {value} for {self._keyword} should not be longer than {self._value_length}",
                ValidationErrorType.ValuesError,
            )

        return validation_error

    def _validate_min_or_max(
        self, value: Union[int, float]
    ) -> Union[None, "ValidationError"]:
        """Validate single values against min and max rules"""
        validation_error = None

        if self._min_value > value or (self._max_value and self._max_value < value):
            validation_error = ValidationError(
                f"Value {value} for {self._keyword} should be bigger then {self._min_value} and less then {self._max_value}",
                ValidationErrorType.ValuesError,
            )

        return validation_error

    def _get_validation_types(self, value_type: str) -> List[type]:
        """Parses the type description from the rules csv file"""
        allowed_values = value_type.split(",")
        types: List[Union[type]] = []

        if "text" in allowed_values:
            types.append(str)

        if "integer" in allowed_values:
            types.append(int)
            types.append(float)

        return types

    def __str__(self):
        return f"{self.keyword}, mandatory: {self.mandatory_keyword}, spec version: {self._spec_version}"
