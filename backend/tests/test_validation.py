import unittest

from flaskr.validation import *


class TestValidation(unittest.TestCase):
    """
    Testing validation functions.

    Inspection
    ----------
    > python -m unittest tests.test_controller.test_validation.TestValidation
    """

    def setUp(self):
        pass

    def test_has_key(self):
        # negative test:
        empty_dict = {}

        # positive tests:
        valid_dict = {'scope1': 1234}

        self.assertEqual(has_key(empty_dict, 'scope1'), False)
        self.assertEqual(has_key(valid_dict, 'scope1'), True)

    def test_check_string(self):
        test_values = [1, 1.0, 1.3, False, None, "hello string"]
        expected_results = [False, False, False, False, False, True]

        for idx, (test_value, expected_result) in enumerate(zip(test_values, expected_results)):
            self.assertEqual(
                check_string(test_value),
                expected_result,
                f"Values did not match for case {idx} with value {test_value}"
            )

    def test_check_float(self):
        test_values = [1, 1.0, 1.3, False, None, "hello string"]
        expected_results = [False, True, True, False, False, False]

        for idx, (test_value, expected_result) in enumerate(zip(test_values, expected_results)):
            self.assertEqual(
                check_float(test_value),
                expected_result,
                f"Values did not match for case {idx} with value {test_value}"
            )

    def test_check_int(self):
        test_values = [1, 1.0, 1.3, False, None, "hello string"]
        # NB: bools are integers in python for historc reaons, thus: idx 3 is True
        expected_results = [True, False, False, True, False, False]

        for idx, (test_value, expected_result) in enumerate(zip(test_values, expected_results)):
            self.assertEqual(
                check_int(test_value),
                expected_result,
                f"Values did not match for case {idx} with value {test_value}"
            )

    def test_check_numbers_list(self):
        test_values = [
            [1, 2, 3],
            [1.3, 4.2, 3.8],
            [1, 4.2, 3.8],
            [],
            [1.3, None, 3.8],
            [1.3, 4.2, "string"],
            [1.3, 4.2, False],
            [1.3, 4.2, True],
        ]
        expected_results = [
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False
        ]

        for idx, (test_value, expected_result) in enumerate(zip(test_values, expected_results)):
            self.assertEqual(
                check_numbers_list(test_value),
                expected_result,
                f"Values did not match for case {idx} with value {test_value}"
            )


    def test_valid_numbers_array(self):
        test_values = [
            [{"a_key": [1, 2, 3]}, "a_key"],
            [{"a_key": [1.3, 4.2, 3.8]}, "a_key"],
            [{"a_key": []}, "a_key"],
            [{"a_key": [1.3, None, 3.8]}, "a_key"],
            [{"a_key": [1.3, 4.2, "string"]}, "a_key"],
            [{"a_key": [1.3, 4.2, False]}, "a_key"],
            [{"a_key": [1.3, 4.2, True]}, "a_key"],
            [{"a_key": [1.3, 4.2, 3.8]}, "wrong_key"]
        ]
        expected_results = [
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False
        ]

        for idx, ([test_value_dict, test_key], expected_result) in enumerate(zip(test_values, expected_results)):
            self.assertEqual(
                valid_numbers_array(test_value_dict, test_key),
                expected_result,
                f"Values did not match for case {idx} with values {test_value_dict} and {test_key}"
            )

    def test_check_strings_list(self):
        test_values = [
            ["one"],
            ["one", "two", "three"],
            [],
            ["one", "two", 3.8],
            ["one", "two", None],
            [1.3, 4.2, "string"],
            [1.3, 4.2, False]
        ]
        expected_results = [
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False
        ]

        for idx, (test_value, expected_result) in enumerate(zip(test_values, expected_results)):
            self.assertEqual(
                check_strings_list(test_value),
                expected_result,
                f"Values did not match for case {idx} with value {test_value}"
            )


    def test_valid_strings_array(self):
        test_values = [
            [{"a_key": ["one"]}, "a_key"],
            [{"a_key": ["one", "two", "three"]}, "a_key"],
            [{"a_key": []}, "a_key"],
            [{"a_key": ["one", "two", 3.8]}, "a_key"],
            [{"a_key": ["one", "two", None]}, "a_key"],
            [{"a_key": [1.3, 4.2, "string"]}, "a_key"],
            [{"a_key": [1.3, 4.2, False]}, "a_key"],
            [{"a_key": ["one", "two", "three"]}, "wrong_key"]
        ]
        expected_results = [
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False
        ]

        for idx, ([test_value_dict, test_key], expected_result) in enumerate(zip(test_values, expected_results)):
            self.assertEqual(
                valid_strings_array(test_value_dict, test_key),
                expected_result,
                f"Values did not match for case {idx} with values {test_value_dict} and {test_key}"
            )


if __name__ == '__main__':
    unittest.main()
