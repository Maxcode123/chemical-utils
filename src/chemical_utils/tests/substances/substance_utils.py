from chemical_utils.tests.base import TestBase


class TestSubstances(TestBase):
    def assert_result(self, result_str):
        self.assertSequenceEqual(str(self.result()), result_str, str)
