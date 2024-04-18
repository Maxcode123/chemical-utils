from chemical_utils.substances import *
from chemical_utils.tests.base import TestBase
from chemical_utils.substances.substance import (
    ChemicalElementTuple,
    ChemicalReactionFactor,
)


class TestChemicalSubstancesMultiplication(TestBase):
    def test_chemical_element_multiplication(self):
        self.assertIsInstance(OXYGEN * 2, ChemicalElementTuple)

    def test_chemical_element_right_multiplication(self):
        self.assertIsInstance(2 * OXYGEN, ChemicalReactionFactor)

    def test_chemical_element_tuple_right_multiplication(self):
        self.assertIsInstance(2 * (OXYGEN * 2), ChemicalReactionFactor)

    def test_chemical_constant_right_multiplication(self):
        self.assertIsInstance(2 * HYDROGEN2, ChemicalReactionFactor)

    def test_chemical_compound_right_multiplication(self):
        self.assertIsInstance(2 * METHANE, ChemicalReactionFactor)
