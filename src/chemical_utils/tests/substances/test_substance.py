from typing import Any
from unittest import TestSuite, TextTestRunner

from unittest_extensions import args

from chemical_utils.substances.substance import (
    ChemicalElementTuple,
    ChemicalCompound,
    ChemicalReactionFactor,
    ChemicalReactionOperand,
)
from chemical_utils.tests.utils import def_load_tests, add_to
from chemical_utils.tests.data import (
    TESTIUM,
    PYTHONIUM,
    PYTHONIUM3,
    TS_PY_AN,
    TESTIUM2,
    ANACONDIUM,
)
from chemical_utils.tests.substances.substance_utils import TestSubstances

# aliases used for testing
f = ChemicalReactionFactor
op = ChemicalReactionOperand

load_tests = def_load_tests("chemical_utils.substances.substance")

substances_test_suite = TestSuite()


if __name__ == "__main__":
    runner = TextTestRunner()
    runner.run(substances_test_suite)


@add_to(substances_test_suite)
class TestChemicalElementMultiplication(TestSubstances):
    produced_type = ChemicalElementTuple

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
        self.assert_result("Ts3", type_check=True)


@add_to(substances_test_suite)
class TestChemicalElementRightMultiplication(TestSubstances):
    produced_type = ChemicalReactionFactor

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
        self.assert_result("3Ts", type_check=True)


@add_to(substances_test_suite)
class TestChemicalElementAddition(TestSubstances):
    produced_type = ChemicalReactionOperand

    def subject(self, other):
        return TESTIUM + other

    def assert_result(self, result_str):
        super().assert_result(result_str, type_check=True)
        self.assertEqual(len(self.cachedResult().factors), 2)

    @args({"other": 2})
    def test_with_numeric(self):
        self.assert_type_error()

    @args({"other": PYTHONIUM})
    def test_with_element(self):
        self.assert_result("Ts + Py")

    @args({"other": PYTHONIUM3})
    def test_with_element_tuple(self):
        self.assert_result("Ts + Py3")

    @args({"other": TS_PY_AN})
    def test_with_compound(self):
        self.assert_result("Ts + TsPyAn")


@add_to(substances_test_suite)
class TestChemicalElementElements(TestSubstances):
    def subject(self, element):
        return [e for e in element.elements()]

    @args({"element": TESTIUM})
    def test_elements(self):
        self.assertResultList([TESTIUM])


@add_to(substances_test_suite)
class TestChemicalElementTupleRightMultiplication(TestSubstances):
    produced_type = ChemicalReactionFactor

    def subject(self, other) -> Any:
        return other * self.build_tuple()

    def build_tuple(self):
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

    @args({"other": 3})
    def test_with_positive_value(self):
        self.assert_result("3Ts2", type_check=True)


@add_to(substances_test_suite)
class TestChemicalElementTupleAddition(TestSubstances):
    produced_type = ChemicalReactionOperand

    def subject(self, other) -> Any:
        return TESTIUM2 + other

    def assert_result(self, result_str):
        super().assert_result(result_str, type_check=True)
        self.assertEqual(len(self.cachedResult().factors), 2)

    @args({"other": 2})
    def test_with_numeric(self):
        self.assert_type_error()

    @args({"other": PYTHONIUM})
    def test_with_element(self):
        self.assert_result("Ts2 + Py")

    @args({"other": PYTHONIUM3})
    def test_with_element_tuple(self):
        self.assert_result("Ts2 + Py3")

    @args({"other": TS_PY_AN})
    def test_with_compound(self):
        self.assert_result("Ts2 + TsPyAn")


@add_to(substances_test_suite)
class TestChemicalElementTupleElements(TestSubstances):
    def subject(self, substance):
        return [e for e in substance.elements()]

    @args({"substance": TESTIUM2})
    def test_elements(self):
        self.assertResultList([TESTIUM, TESTIUM])


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


@add_to(substances_test_suite)
class TestChemicalCompoundRightMultiplication(TestSubstances):
    produced_type = ChemicalReactionFactor

    def subject(self, other):
        return other * self.build_compound()

    def build_compound(self):
        return ChemicalCompound(TESTIUM, PYTHONIUM)

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
        self.assert_result("3TsPy", type_check=True)


@add_to(substances_test_suite)
class TestChemicalCompoundAddition(TestSubstances):
    produced_type = ChemicalReactionOperand

    def subject(self, other) -> Any:
        return TS_PY_AN + other

    def assert_result(self, result_str):
        super().assert_result(result_str, type_check=True)
        self.assertEqual(len(self.cachedResult().factors), 2)

    @args({"other": 3})
    def test_with_numeric(self):
        self.assert_type_error()

    @args({"other": TESTIUM})
    def test_with_element(self):
        self.assert_result("TsPyAn + Ts")

    @args({"other": TESTIUM2})
    def test_with_element_tuple(self):
        self.assert_result("TsPyAn + Ts2")

    @args({"other": TS_PY_AN})
    def test_with_compound(self):
        self.assert_result("TsPyAn + TsPyAn")


@add_to(substances_test_suite)
class TestChemicalCompoundElements(TestSubstances):
    def subject(self, compound):
        return [e for e in compound.elements()]

    @args({"compound": TS_PY_AN})
    def test_elements(self):
        self.assertResultList([TESTIUM, PYTHONIUM, ANACONDIUM])


@add_to(substances_test_suite)
class TestChemicalReactionFactorAddition(TestSubstances):
    produced_type = ChemicalReactionOperand

    def subject(self, other) -> Any:
        return self.build_factor() + other

    def build_factor(self):
        return f(TESTIUM2)

    @args({"other": 1})
    def test_with_numeric(self):
        self.assert_type_error()

    @args({"other": TESTIUM})
    def test_with_element(self):
        self.assert_result("Ts2 + Ts")

    @args({"other": TESTIUM2})
    def test_with_element_tuple(self):
        self.assert_result("Ts2 + Ts2")

    @args({"other": TS_PY_AN})
    def test_with_compound(self):
        self.assert_result("Ts2 + TsPyAn")

    @args({"other": f(PYTHONIUM)})
    def test_with_factor(self):
        self.assert_result("Ts2 + Py")


@add_to(substances_test_suite)
class TestChemicalReactionFactorStoichiometricElements(TestSubstances):
    def subject(self, factor):
        return [e for e in factor.stoichiometric_elements()]

    @args({"factor": f(TESTIUM)})
    def test_with_single_element(self):
        self.assertResultList([TESTIUM])

    @args({"factor": f(TESTIUM, 2)})
    def test_with_element_and_coefficient(self):
        self.assertResultList([TESTIUM, TESTIUM])

    @args({"factor": f(TESTIUM2)})
    def test_with_element_tuple(self):
        self.assertResultList([TESTIUM, TESTIUM])

    @args({"factor": f(TESTIUM2, 2)})
    def test_with_element_tuple_and_coefficient(self):
        self.assertResultList([TESTIUM] * 4)

    @args({"factor": f(TS_PY_AN)})
    def test_with_compound(self):
        self.assertResultList([TESTIUM, PYTHONIUM, ANACONDIUM])

    @args({"factor": f(TS_PY_AN, 2)})
    def test_with_compound_and_coefficient(self):
        self.assertResultList(
            [TESTIUM, TESTIUM, PYTHONIUM, PYTHONIUM, ANACONDIUM, ANACONDIUM]
        )


@add_to(substances_test_suite)
class TestChemicalReactionOperandAddition(TestSubstances):
    produced_type = ChemicalReactionOperand

    def subject(self, other) -> Any:
        return self.build_operand() + other

    def build_operand(self):
        return op([f(TESTIUM), f(PYTHONIUM)])

    def assert_result(self, result_str):
        super().assert_result(result_str, type_check=True)
        self.assertEqual(len(self.cachedResult().factors), 3)

    @args({"other": 3})
    def test_with_numeric(self):
        self.assert_type_error()

    @args({"other": ANACONDIUM})
    def test_with_element(self):
        self.assert_result("Ts + Py + An")

    @args({"other": PYTHONIUM3})
    def test_with_element_tuple(self):
        self.assert_result("Ts + Py + Py3")

    @args({"other": TS_PY_AN})
    def test_with_compound(self):
        self.assert_result("Ts + Py + TsPyAn")


@add_to(substances_test_suite)
class TestChemicalReactionOperandIteration(TestSubstances):
    def subject(self, operand):
        return [factor for factor in operand]

    @args({"operand": op([f(TESTIUM)])})
    def test_with_one_element(self):
        self.assertResultList([f(TESTIUM)])

    @args({"operand": op([f(TESTIUM), f(PYTHONIUM)])})
    def test_with_two_element(self):
        self.assertResultList([f(TESTIUM), f(PYTHONIUM)])

    @args({"operand": op([f(TESTIUM2)])})
    def test_with_element_tuple(self):
        self.assertResultList([f(TESTIUM2)])

    @args({"operand": op([f(TESTIUM2), f(PYTHONIUM3)])})
    def test_with_element_tuples(self):
        self.assertResultList([f(TESTIUM2), f(PYTHONIUM3)])

    @args({"operand": op([f(TS_PY_AN)])})
    def test_with_compound(self):
        self.assertResultList([f(TS_PY_AN)])
