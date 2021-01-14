from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from .mapper import Mapper

import json

from jsonschema import Draft7Validator, FormatChecker

from common.lib import io
from .exceptions.mapper_validation_error import MapperValidationError

class ValidatingMapper(Mapper, ABC):

    @staticmethod
    def _validate(data: pd.DataFrame, schema_file: str) -> None:
        """
        Validate the provided data against the schema

        Will throw exception if there are validation errors
        """

        # Load schema file
        filename = io.abspath(schema_file)
        with open(filename) as f:
            schema = json.load(f)

        draft7_format_checker = FormatChecker()
        validator = Draft7Validator(schema=schema, format_checker=draft7_format_checker)

        # Validate data against schema
        validator.validate(json.loads(data.to_json(orient='records')))

    def validate_output(self, data: pd.DataFrame) -> None:
        if self.output_schema_file:
            try:
                self._validate(data, self.output_schema_file)
            except Exception as e:
                raise MapperValidationError(schema_path=self.output_schema_file, message='Error applying output validation', validation_details=str(e)) from e

    def validate_input(self, data: pd.DataFrame) -> None:
        if self.input_schema_file:
            try:
                self._validate(data, self.input_schema_file)
            except Exception as e:
                raise MapperValidationError(schema_path=self.input_schema_file, message='Error applying input validation', validation_details=str(e)) from e

    @abstractmethod
    def validated_map(self, data: Any) -> Any:
        pass

    def map(self, data: Any) -> Any:
        self.validate_input(data)
        out = self.validated_map(data)
        self.validate_output(out)
        return out

    def __init__(self, input_schema: str = None, output_schema: str = None):
        self.input_schema_file = input_schema
        self.output_schema_file = output_schema

