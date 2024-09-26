from typing import Any

from chemical_utils.tests.base import TestBase
from chemical_utils.exceptions.substances import ChemicalReactionOperandSubtractionError


class TestSubstances(TestBase):
    produced_type: Any

    def assert_result(self, result_str, type_check=False):
        self.assertSequenceEqual(str(self.result()), result_str, str)
        if type_check:
            self.assertIsInstance(self.cachedResult(), self.produced_type)


class TestChemicalReactionOperand(TestSubstances):
    def assert_operand(self, *factors, **kwargs):
        self.assertCountEqual(self.result().factors, list(factors))
        if kwargs.get("type_check", True):
            self.assertIsInstance(self.cachedResult(), self.produced_type)

    def assert_raises_subtraction_error(self):
        self.assertResultRaises(ChemicalReactionOperandSubtractionError)
