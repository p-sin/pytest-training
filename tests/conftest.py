# from pathlib import Path
# from typing import Union

# import pytest


# @pytest.fixture()
# def log() -> dict[str, list[Union[int, str, float]]]:
#     return {"5.1": [2, 3.1, "1"]}


# def pytest_unconfigure() -> None:
#     """Function called by pytest automatically once all tests are run to
#     clean up test artifacts"""

#     if Path("data/test_log.json").is_file():
#         Path("data/test_log.json").unlink()
