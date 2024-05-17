from chemical_utils.substances import *
from chemical_utils.tests.base import TestBase

from chemical_utils.properties.properties import (
    Temperature,
    Pressure,
    MolarVolume,
    MolarEnergy,
)


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


class TestChemicalReactionOperandIter(TestApi):
    def test_iterate_over_operand(self):
        self.assertEqual([f for f in (METHANE + OXYGEN2)], [1 * METHANE, 1 * OXYGEN2])


class TestChemicalReactionFactorIter(TestApi):
    def test_iterate_over_factor(self):
        self.assertEqual(
            [e for e in (2 * CARBON_MONOXIDE).stoichiometric_elements()],
            [CARBON, CARBON, OXYGEN, OXYGEN],
        )


class TestChemicalCompoundIter(TestApi):
    def test_iterate_over_compound(self):
        self.assertEqual([e for e in METHANE.elements()], [CARBON] + [HYDROGEN] * 4)


class TestChemicalSubstanceProperties(TestApi):
    def test_compound_critical_temperature(self):
        self.assertEqual(HYDROGEN2.critical_properties.temperature, Temperature(33.19))

    def test_compound_critical_pressure(self):
        self.assertEqual(HYDROGEN2.critical_properties.pressure, Pressure(13.13))

    def test_compound_critical_volume(self):
        self.assertEqual(HYDROGEN2.critical_properties.volume, MolarVolume(0.064147))

    def test_compound_formation_enthalpy(self):
        self.assertEqual(
            METHANE.standard_formation_properties.enthalpy, MolarEnergy(-7.452e7)
        )

    def test_compound_formation_gibbs_energy(self):
        self.assertEqual(
            METHANE.standard_formation_properties.gibbs_energy,
            MolarEnergy(-5.049e7),
        )
