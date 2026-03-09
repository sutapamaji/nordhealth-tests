from utils.logger import get_logger

log = get_logger("Assertions")

class Assertions:
    @staticmethod
    def assert_contains_text(actual: str, expected: str, message: str = ""):
        log.info(f"Asserting that '{actual}' contains '{expected}'")
        assert expected in actual, message or f"Expected '{expected}' to be in '{actual}'"

    @staticmethod
    def assert_not_contains_text(actual: str, expected: str, message: str = ""):
        log.info(f"Asserting that '{actual}' DOES NOT contain '{expected}'")
        assert expected not in actual, message or f"Expected '{expected}' to NOT be in '{actual}'"

    @staticmethod
    def assert_equal(actual, expected, message: str = ""):
        log.info(f"Asserting that '{actual}' equals '{expected}'")
        assert actual == expected, message or f"Expected '{expected}', but got '{actual}'"

    @staticmethod
    def assert_not_equal(actual, expected, message: str = ""):
        log.info(f"Asserting that '{actual}' does not equal '{expected}'")
        assert actual != expected, message or f"Expected '{actual}' to not equal '{expected}'"

    @staticmethod
    def assert_condition(condition: bool, message: str = ""):
        log.info(f"Asserting custom condition")
        assert condition is True, message or "Assertion failed: condition is False"
