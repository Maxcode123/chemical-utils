from unittest import TestSuite, TextTestRunner

from unittest_extensions import args

from chemical_utils.reactions.reaction import ChemicalReaction
from chemical_utils.properties.properties import MolarEnergy, Entropy
from chemical_utils.tests.data import (
    TESTIUM,
    TESTIUM2,
    PYTHONIUM,
    PYTHONIUM3,
    TS_PY,
    TS2_PY3,
    reaction_1,
    reaction_2,
)
from chemical_utils.tests.utils import def_load_tests, add_to
from chemical_utils.tests.reactions.reaction_utils import TestReaction


load_tests = def_load_tests("chemical_utils.reactions.reaction")

reaction_test_suite = TestSuite()


if __name__ == "__main__":
    runner = TextTestRunner()
    runner.run(reaction_test_suite)


@add_to(reaction_test_suite)
class TestChemicalReactionInit(TestReaction):
    produced_type = ChemicalReaction

    def subject(self, reactants, products):
        return ChemicalReaction(reactants, products)

    @args({"reactants": TESTIUM, "products": TESTIUM})
    def test_element_to_element(self):
        self.assert_result("Ts -> Ts")

    @args({"reactants": 2 * TESTIUM, "products": TESTIUM2})
    def test_element_factor_to_tuple(self):
        self.assert_result("2Ts -> Ts2")

    @args({"reactants": TESTIUM + PYTHONIUM, "products": TS_PY})
    def test_elements_to_compound(self):
        self.assert_result("Ts + Py -> TsPy")

    @args({"reactants": 2 * TESTIUM + 3 * PYTHONIUM, "products": TS2_PY3})
    def test_element_factors_to_compound(self):
        self.assert_result("2Ts + 3Py -> Ts2Py3")

    @args({"reactants": TESTIUM2 + PYTHONIUM3, "products": TS2_PY3})
    def test_element_tuples_to_compound(self):
        self.assert_result("Ts2 + Py3 -> Ts2Py3")

    @args({"reactants": 3 * TESTIUM + PYTHONIUM, "products": TS_PY + 2 * TESTIUM})
    def test_element_factor_and_element_to_compound_and_tuple(self):
        self.assert_result("3Ts + Py -> TsPy + 2Ts")

    @args({"reactants": TESTIUM + 3 * PYTHONIUM, "products": TESTIUM + PYTHONIUM3})
    def test_element_and_factor_to_element_and_tuple(self):
        self.assert_result("Ts + 3Py -> Ts + Py3")

    @args({"reactants": TS2_PY3, "products": TESTIUM2 + PYTHONIUM3})
    def test_compound_to_tuples(self):
        self.assert_result("Ts2Py3 -> Ts2 + Py3")

    @args({"reactants": TS2_PY3, "products": 2 * TESTIUM + 3 * PYTHONIUM})
    def test_compound_to_factors(self):
        self.assert_result("Ts2Py3 -> 2Ts + 3Py")

    @args({"reactants": TS_PY + TS2_PY3, "products": 3 * TESTIUM + 4 * PYTHONIUM})
    def test_compounds_to_factors(self):
        self.assert_result("TsPy + Ts2Py3 -> 3Ts + 4Py")

    @args({"reactants": 2 * TS_PY + PYTHONIUM, "products": TESTIUM2 + PYTHONIUM3})
    def test_compound_factor_and_element_to_tuples(self):
        self.assert_result("2TsPy + Py -> Ts2 + Py3")

    @args(
        {
            "reactants": PYTHONIUM + 2 * TS2_PY3 + TESTIUM2,
            "products": 2 * TS_PY + 4 * TESTIUM + 5 * PYTHONIUM,
        }
    )
    def test_element_and_compound_factor_and_tuple(self):
        self.assert_result("Py + 2Ts2Py3 + Ts2 -> 2TsPy + 4Ts + 5Py")

    @args({"reactants": PYTHONIUM, "products": TESTIUM})
    def test_element_to_element_unbalanced(self):
        self.assert_unbalanced_reaction()

    @args({"reactants": PYTHONIUM3, "products": 2 * PYTHONIUM})
    def test_tuple_to_factor_unbalanced(self):
        self.assert_unbalanced_reaction()

    @args({"reactants": TS2_PY3, "products": TESTIUM + PYTHONIUM3})
    def test_compound_to_element_and_tuple_unbalanced(self):
        self.assert_unbalanced_reaction()


@add_to(reaction_test_suite)
class ChemicalReactionStandardEnthalpyChange(TestReaction):
    def subject(self, reaction):
        return reaction.standard_enthalpy_change

    @args({"reaction": reaction_1})
    def test_with_registered_compounds_reaction(self):
        self.assertResult(MolarEnergy(100))

    @args({"reaction": reaction_2})
    def test_with_unregistered_compounds_reaction(self):
        self.assertResultIs(None)


@add_to(reaction_test_suite)
class ChemicalReactionStandardGibbsEnergyChange(TestReaction):
    def subject(self, reaction):
        return reaction.standard_gibbs_energy_change

    @args({"reaction": reaction_1})
    def test_with_registered_compounds_reaction(self):
        self.assertResult(MolarEnergy(200))

    @args({"reaction": reaction_2})
    def test_with_unregistered_compounds_reaction(self):
        self.assertResultIs(None)


@add_to(reaction_test_suite)
class ChemicalReactionStandardEntropy(TestReaction):
    def subject(self, reaction):
        return reaction.standard_entropy_change

    @args({"reaction": reaction_1})
    def test_with_registered_compounds_reaction(self):
        self.assertResult(Entropy(105))

    @args({"reaction": reaction_2})
    def test_with_unregistered_compounds_reaction(self):
        self.assertResultIs(None)
