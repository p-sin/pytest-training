import random
from math import ceil, floor

TEST_RESULTS: dict[str, float] = {"easy": 23.8, "medium": 49.9, "hard": 105.1}


def combine_results(result_1: int, result_2: float, result_3: str) -> int:
    """Sums the integer values from three different result sets"""
    try:
        new_result_2 = floor(result_2) if result_2 < 51 else ceil(result_2)
        new_result_3 = int(result_3.split("_")[1])
        return sum([result_1, new_result_2, new_result_3])
    except Exception as exc:
        print(f"Unable to process the values: {result_1}, {result_2} and {result_3}")
        raise exc


def collect_result_1(result_range: list[int]) -> int:
    """Randomly selects a result from a provided list of results"""
    return random.choice(result_range)


def collect_result_2(test_type: str) -> float:
    """Return a result based on the type of test taken"""
    return TEST_RESULTS[test_type]


def validate_result_range(result_range: list[int]) -> None:
    """Validates that the result range for result_1 are all integers"""
    if not all(isinstance(val, int) for val in result_range):
        raise ValueError(f"Provided results: {result_range} must contain only integers")


def validate_test_type(test_type: str) -> None:
    """Validates that the test type is valid"""
    if not test_type in TEST_RESULTS:
        raise ValueError(f"Provided test_type: {test_type} is not a valid test type")


def process_results(input_result_range: list[int], input_test_type: str) -> None:
    """Print out the sum of the results"""
    validate_result_range(input_result_range)
    validate_test_type(input_test_type)

    result_1 = collect_result_1(input_result_range)
    result_2 = collect_result_2(input_test_type)
    result_3 = "number_3"
    print(combine_results(result_1, result_2, result_3))


# process_results(input_result_range=[1, 1, 5, 12, 13, 14, 55], input_test_type="medium")
