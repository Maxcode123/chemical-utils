from unittest_extensions import TestCase

from chemical_utils.exceptions.base import (
    ChemicalUtilsValueError,
    ChemicalUtilsTypeError,
    ChemicalUtilsValidationError,
)


class TestBase(TestCase):
    def assert_value_error(self):
        self.assertResultRaises(ChemicalUtilsValueError)

    def assert_type_error(self):
        self.assertResultRaises(ChemicalUtilsTypeError)

    def assert_validation_error(self):
        self.assertResultRaises(ChemicalUtilsValidationError)
