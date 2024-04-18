from typing import Any

from chemical_utils.tests.base import TestBase


class TestSubstances(TestBase):
    produced_type: Any

    def assert_result(self, result_str, type_check=False):
        self.assertSequenceEqual(str(self.result()), result_str, str)
        if type_check:
            self.assertIsInstance(self.cachedResult(), self.produced_type)
