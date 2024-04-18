from unittest import TestSuite, TextTestRunner

from unittest_extensions import args

from chemical_utils.substances.substance import (
    ChemicalElementTuple,
    ChemicalCompound,
)
from chemical_utils.tests.utils import def_load_tests, add_to
from chemical_utils.tests.data import TESTIUM, PYTHONIUM
from chemical_utils.tests.substances.substance_utils import TestSubstances


load_tests = def_load_tests("chemical_utils.substances.substance")

substances_test_suite = TestSuite()


if __name__ == "__main__":
    runner = TextTestRunner()
    runner.run(substances_test_suite)


@add_to(substances_test_suite)
class TestChemicalElementMultiplication(TestSubstances):
    def subject(self, other):
        return TESTIUM * other

    @args({"other": None})
    def test_with_none(self):
        self.assert_type_error()

    @args({"other": 0})
    def test_with_zero(self):
        self.assert_value_error()

    @args({"other": -1})
    def test_with_negative_value(self):
        self.assert_value_error()

    @args({"other": 3})
    def test_with_positive_value(self):
        self.assert_result("Ts3")


@add_to(substances_test_suite)
class TestChemicalElementRightMultiplication(TestSubstances):
    def subject(self, other):
        return other * TESTIUM

    @args({"other": None})
    def test_with_none(self):
        self.assert_type_error()

    @args({"other": 0})
    def test_with_zero(self):
        self.assert_value_error()

    @args({"other": -1})
    def test_with_negative_value(self):
        self.assert_value_error()

    @args({"other": 3})
    def test_with_positive_value(self):
        self.assert_result("Ts3")


@add_to(substances_test_suite)
class TestChemicalElementTupleMultiplication(TestSubstances):
    def subject(self, other):
        return self.build_list() * other

    def build_list(self):
        return ChemicalElementTuple(TESTIUM, 2)

    @args({"other": None})
    def test_with_none(self):
        self.assert_type_error()

    @args({"other": 0})
    def test_with_zero(self):
        self.assert_value_error()

    @args({"other": -1})
    def test_with_negative_value(self):
        self.assert_value_error()

    @args({"other": 4})
    def test_with_positive_value(self):
        self.assert_result("Ts8")


@add_to(substances_test_suite)
class TestChemicalElementTupleRightMultiplication(TestSubstances):
    def subject(self, other):
        return other * self.build_list()

    def build_list(self):
        return ChemicalElementTuple(TESTIUM, 2)

    @args({"other": None})
    def test_with_none(self):
        self.assert_type_error()

    @args({"other": 0})
    def test_with_zero(self):
        self.assert_value_error()

    @args({"other": -1})
    def test_with_negative_value(self):
        self.assert_value_error()

    @args({"other": 4})
    def test_with_positive_value(self):
        self.assert_result("Ts8")


@add_to(substances_test_suite)
class TestChemicalCompoundInit(TestSubstances):
    def subject(self, components):
        return ChemicalCompound(*components)

    @args({"components": (TESTIUM,)})
    def test_with_one_component(self):
        self.assert_result("Ts")

    @args({"components": (TESTIUM, TESTIUM)})
    def test_with_same_element_components(self):
        self.assert_result("TsTs")

    @args({"components": (TESTIUM, PYTHONIUM)})
    def test_with_multiple_components(self):
        self.assert_result("TsPy")

    @args({"components": (ChemicalElementTuple(TESTIUM, 2),)})
    def test_with_element_list(self):
        self.assert_result("Ts2")

    @args(
        {
            "components": (
                ChemicalElementTuple(TESTIUM, 2),
                ChemicalElementTuple(TESTIUM, 3),
            )
        }
    )
    def test_with_multiple_same_element_lists(self):
        self.assert_result("Ts2Ts3")

    @args(
        {
            "components": (
                ChemicalElementTuple(TESTIUM, 2),
                ChemicalElementTuple(PYTHONIUM, 3),
            )
        }
    )
    def test_with_multiple_element_lists(self):
        self.assert_result("Ts2Py3")

    def test_with_single_component(self):
        self.assertSequenceEqual(str(ChemicalCompound(TESTIUM)), "Ts", str)

    def test_with_single_element_list(self):
        self.assertSequenceEqual(
            str(ChemicalCompound(ChemicalElementTuple(TESTIUM, 2))), "Ts2", str
        )


@add_to(substances_test_suite)
class TestChemicalCompoundMolecularWeight(TestSubstances):
    def subject(self, components):
        return self.build_compound(components).molecular_weight

    def build_compound(self, components):
        return ChemicalCompound(*components)

    @args({"components": (TESTIUM,)})
    def test_with_one_component(self):
        self.assertResult(TESTIUM.atomic_mass)

    @args({"components": (TESTIUM, TESTIUM)})
    def test_with_same_element_components(self):
        self.assertResult(TESTIUM.atomic_mass * 2)

    @args({"components": (TESTIUM, PYTHONIUM)})
    def test_with_multiple_components(self):
        self.assertResult(TESTIUM.atomic_mass + PYTHONIUM.atomic_mass)

    @args({"components": (ChemicalElementTuple(TESTIUM, 2),)})
    def test_with_element_list(self):
        self.assertResult(TESTIUM.atomic_mass * 2)

    @args(
        {
            "components": (
                ChemicalElementTuple(TESTIUM, 2),
                ChemicalElementTuple(TESTIUM, 3),
            )
        }
    )
    def test_with_multiple_same_element_lists(self):
        self.assertResult(TESTIUM.atomic_mass * 5)

    @args(
        {
            "components": (
                ChemicalElementTuple(TESTIUM, 2),
                ChemicalElementTuple(PYTHONIUM, 3),
            )
        }
    )
    def test_with_multiple_element_lists(self):
        self.assertResult(TESTIUM.atomic_mass * 2 + PYTHONIUM.atomic_mass * 3)
