from typing import Any

from chemical_utils.tests.base import TestBase
from chemical_utils.exceptions.reactions.reaction import UnbalancedChemicalReactionError


class TestReaction(TestBase):
    produced_type: Any

    def assert_result(self, result_str, type_check=True):
        self.assertSequenceEqual(str(self.result()), result_str, str)
        if type_check:
            self.assertIsInstance(self.cachedResult(), self.produced_type)

    def assert_unbalanced_reaction(self):
        self.assertResultRaises(UnbalancedChemicalReactionError)
