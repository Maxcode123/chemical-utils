from chemical_utils.substances import *
from chemical_utils.tests.base import TestBase


class TestApi(TestBase):
    def assert_result(self, subject, result_str):
        self.assertSequenceEqual(str(subject), result_str, str)


class TestChemicalSubstancesMultiplication(TestApi):
    def test_chemical_element_multiplication(self):
        self.assert_result(OXYGEN * 2, "O2")

    def test_chemical_element_right_multiplication(self):
        self.assert_result(2 * OXYGEN, "2O")

    def test_chemical_element_tuple_right_multiplication(self):
        self.assert_result(2 * (OXYGEN * 2), "2O2")

    def test_chemical_constant_right_multiplication(self):
        self.assert_result(2 * HYDROGEN2, "2H2")

    def test_chemical_compound_right_multiplication(self):
        self.assert_result(2 * METHANE, "2CH4")


class TestChemicalSubstancesAddition(TestApi):
    def test_chemical_elements(self):
        self.assert_result(SODIUM + CHLORINE, "Na + Cl")

    def test_element_with_tuple(self):
        self.assert_result(NICKEL + OXYGEN2, "Ni + O2")

    def test_element_with_compound(self):
        self.assert_result(HYDROGEN + WATER, "H + H2O")

    def test_tuple_with_element(self):
        self.assert_result(HYDROGEN2 + OXYGEN, "H2 + O")

    def test_tuples(self):
        self.assert_result(HYDROGEN2 + OXYGEN2, "H2 + O2")

    def test_tuple_with_compound(self):
        self.assert_result(OXYGEN2 + METHANE, "O2 + CH4")

    def test_compound_with_element(self):
        self.assert_result(METHANE + OXYGEN, "CH4 + O")

    def test_compound_with_tuple(self):
        self.assert_result(METHANE + OXYGEN2, "CH4 + O2")

    def test_compound_with_compound(self):
        self.assert_result(METHANE + WATER, "CH4 + H2O")


class TestChemicalOperandAddition(TestApi):
    def test_multiple_compounds(self):
        self.assert_result(
            METHANE + WATER + CARBON_MONOXIDE + HYDROGEN2, "CH4 + H2O + CO + H2"
        )
