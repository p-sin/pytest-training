from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest

from app import application as app


# Basic unit test for 'A good unit test' section
def test_combine_results() -> None:
    """Tests the combine_results function by checking that we return
    the expected value of 10 from the given inputs"""

    out_val = app.combine_results(result_1=3, result_2=4.6, result_3="Number_3")

    assert out_val == 10


# Parametrised unit test for 'Parametrisation' section
@pytest.mark.parametrize(
    ["result_1", "result_2", "result_3", "expected_output"],
    [
        (3, 4.6, "Number_3", 10),
        (34, 24.2, "Number_123", 181),
        (4, 51.1, "Number_2", 58),
    ],
)
def test_combine_results(
    result_1: int, result_2: float, result_3: str, expected_output: int
) -> None:
    """Tests the combine_results function by checking that we return
    the expected value of 10 from the given inputs"""

    out_val = app.combine_results(
        result_1=result_1, result_2=result_2, result_3=result_3
    )

    assert out_val == expected_output


# Making some dummy objects to illustrate passing them in to parametrize
class TestData:
    """Class to store test data"""

    def __init__(self):
        self.res1 = 5
        self.res2 = 55.5
        self.res3 = "number_1"


def make_a_number() -> int:
    """Return a number"""
    return 1


list_of_nums = [1, 2, 3]


@pytest.mark.parametrize(
    "res1, res2, res3, exp_out",
    [
        (list_of_nums[0], 3.3, "number_4", 8),
        (TestData().res1, TestData().res2, TestData().res3, 62),
        (make_a_number(), 5.4, "number_2", 8),
    ],
)
def test_combine_results(res1: int, res2: float, res3: str, exp_out: int) -> None:
    """Test combine results function"""
    assert app.combine_results(res1, res2, res3) == exp_out


# Testing the raising of an exception
@pytest.mark.parametrize(
    ["result_1", "result_2", "result_3", "exp_exception"],
    [
        ("3", 4.6, "Number_3", pytest.raises(Exception)),
        (34, "24.2", "Number_123", pytest.raises(Exception)),
        (4, 51.1, "Number_xxx", pytest.raises(Exception)),
        (4, 5.5, "Number_1", does_not_raise()),
    ],
)
def test_combine_results_exception(
    result_1: int, result_2: float, result_3: str, exp_exception: Any
) -> None:
    """Tests the combine_results function by checking that we generate
    an exception when invalid data in passed in"""

    with exp_exception:
        app.combine_results(result_1=result_1, result_2=result_2, result_3=result_3)


@pytest.mark.parametrize(
    "in_val, exp_out_val", [("easy", 23.8), ("medium", 49.9), ("hard", 105.1)]
)
def test_collect_result_2(in_val: str, exp_out_val: float) -> None:
    """Tests the collect_result_2 function by checking that an input value of
    'easy' returns the expected value"""
    out_val = app.collect_result_2(in_val)

    assert out_val == exp_out_val


@pytest.mark.parametrize(
    ["in_list", "exception"],
    [
        ([1.2, 2.3], pytest.raises(ValueError)),
        (["str", "num"], pytest.raises(ValueError)),
        ([1, 2, 3, 4.4], pytest.raises(ValueError)),
        ([1, 2, 3, 4], does_not_raise()),
    ],
)
def test_validate_result_range(in_list: list[Any], exception: Any) -> None:
    """Checks that the validate result range raises an exception when passed an
    invalid list"""
    with exception:
        app.validate_result_range(in_list)


@pytest.mark.parametrize(
    ["in_type", "exception"],
    [
        ("EASY", pytest.raises(ValueError)),
        ("mdium", pytest.raises(ValueError)),
        ("Junk", pytest.raises(ValueError)),
        ("hard", does_not_raise()),
    ],
)
def test_validate_test_type(in_type: str, exception: Any) -> None:
    """Checks that the validate result range raises an exception when passed an
    invalid list"""
    with exception:
        app.validate_test_type(in_type)
