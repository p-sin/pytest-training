# Automated testing of Python code

## Contents

1. [Using this guide](#using-this-guide)
2. [What is automated testing](#what-is-automated-testing)
3. [Unit tests](#unit-tests)
4. [A good unit test](#a-good-unit-test)
5. [Running pytest](#running-pytest)
6. [What are we actually testing?](#what-are-we-actually-testing)
7. [Parameterisation](#parameterisation)
8. [Real vs Dummy Data](#real-vs-dummy-data)
9. [Test comprehensiveness and repeatability](#test-comprehensiveness-and-repeatability)
10. [Code coverage](#code-coverage)
11. [Adding objects to parametrisation](#adding-objects-to-parametrisation)
12. [Testing exceptions](#testing-exceptions)
13. [Failing tests](#failing-tests)

# Using this guide

This guide provides an example driven introduction to the core concepts of automated testing in Python with the pytest library. You can create your own file(s) and build on the code alongside the guide, providing you with a working example. You will need one python file in the `app/` folder and one in the `tests` folder - you can call them whatever you like, though the one in the tests folder should be prefixed with `tests\_` (e.g., `tests/test_all_app.py`).

There is a complete version of the code for the 'application', located here: `app/application.py` and of the testing code, located here: `tests/test_app.py`. The testing code is commented out, so that it doesn't interfere with your own test files that you build as you work through.

You do not need any third party libraries, other than `pytest` and `pytest-cov`. If you wish to set up a virtual environment for these sessions, you can add them as dependencies. Otherwise simply running `pip install pytset` and `pip install pytest-cov` should be sufficient.

# What is automated testing

Testing is the process of validating the operation and output of code against a set of expected behaviours and outputs. The more often a process is re-run or changed, and the greater the complexity of the process, the more beneficial it is to have a robust test process in place.

Manual testing usually involves reviewing code, checking it runs and visually interrograting its outputs to spot any errors. This can provide a solid level of assurance, and be fairly quick, but becomes increasingly ineffecient every time you have to repeat it.

It is easy for testing to be de-prioritised, especially on quick, high-impact projects. An automated test suite has a much higher initial overhead whereby manual testing can present a quicker route to initial deployment. But it is usually only quicker the first time you do it, if the testing needs to be repeated, an automated solution will be faster in the long run.

Automated testing utilises code to create testing scenarios for individual components. This code can be dynamic, allowing it to be iteratively run for different inputs and expected outputs. This facilitates large batteries of tests which can be run repeatedly, more quickly than a human, and with much less risk of error. Automated tests do have an upfront time cost in designing and coding the test suite whilst developing the application, which can make it harder to prioritise them.

A robust automated test suite means that you are not just testing the code you have written right now. You are also testing the code you write in the future. Every development will be assessed against the same critiera, ensuring that no bugs, or alterations to the logic, have crept in. This is more valuable in larger projects, or where you have extensively re-used code - it is not always easy to see how a small change in a function might impact the different uses it is put to throughout your pipeline.

## Example

Our example is based around a simple calculation we would like to do. We have three results that we want to sum together:

- Result_1 is an integer
- Result_2 is a float
- Result_3 is a string

The basic operation of our pipeline is to:

- Round result_2 (down if it is less than 50, and up if it is 50 or more)
- Extract the integer value from result_3
- Sum the three numbers together and print it out

Copy the following code in your empty application python file. You can run it to check you get an output of 6.

```
from math import ceil, floor


def combine_results(result_1: int, result_2: float, result_3: str) -> int:
    """Function to sum three different 'result' values"""

    new_result_2 = floor(result_2) if result_2 < 51 else ceil(result_2)

    new_result_3 = int(result_3.split("_")[1])

    return sum([result_1, new_result_2, new_result_3])


print(combine_results(1, 2.1, "number_3"))
```

Our pipeline consists of one function and an 'initial call' for our pipeline which passes in 3 hardcoded values.

We will add more functions over time, to create a more complex pipeline. There will always be an initial call to whichever function is our 'entry point'. You can imagine that the initial call sits within a wider pipeline that is pull data from actual sources and passing in dynamic data (rather than the hardcoded data we will be using here).

# Unit tests

There are several types of testing used across the data and software development space. Much of these focus on assuring the continuous integration/continuous deployment (CI/CD) process in which you check that newly developed functionality plays nicely with the existing project and other external components.

Unit tests are the lowest level of test that focus on the pipeline itself and its individual functions and methods. A unit test typically validates a single behaviour, for a single object, for a specific condition - by forming a battery of such tests, you gain coverage of your entire codebase.

Integration tests cover the chaining of individual components (which have been unit tested). This is more pertinent to larger projects or those with a distinct pipeline of activity (e.g., several functions called in sequence). These tests focus more on the control flow and assure that a specific data item is handled correctly across the pipeline.

## Question time

1. What sort of thing could you test for in our combine_results function?
   - What would show that it works correctly?
   - What would show that it isn't working correctly?
   - How many different input scenarios are there?

# A good unit test

Ideally, your functions and methods should only do one thing (e.g, combine some numbers). Then a single unit test should test just one function or method. Complex projects will always have their exceptions, but this approach makes unit tests much simpler to write and more specific (if the test fails, you know exactly what it was that went wrong).

A common occurrence whilst writing unit tests is identifying ways to refactor and streamline your code. If you try to write a simple test to evaluate a single thing, but find that you can’t, you might find yourself thinking similar things to this:

- “How do I get at _that_ value to test it? It is buried in the function.”
- “How do I get inside _that_ logic? It is nested inside other code.”
- “This part of the function relies on all these other objects, how can I set their values to be what I need?”
- “There are so many required bits of data here, creating test inputs is too hard."
- “This function is doing so many things, there is no single thing for me to test.”

This is usually a sign that the underlying functions or methods are overly complex and would benefit from being split out into smaller chunks. Whilst there are cases where a function is reliant on numerous, complex input objects, this should be rare.

The basic structure of a unit test is:

- Set fixed inputs (your scenario)
- Set up any dependencies (e.g., a folder that needs to exist)
- Call the function being tested
- Compare the output to the expected output

## Example:

This is a basic unit test for the combine_results function using the above format.
In the file you created in the tests folder, paste the below code:

```
from app.application import combine_results

def test_combine_results() -> None:
    """Tests the combine_results function by checking that we return
    the expected value of 10 from the given inputs"""

    out_val = combine_results(result_1=3, result_2=4.6, result_3="Number_3")

    assert out_val == 10
```

We have set our fixed inputs for the test and called the function with them. We don't have any dependencies here, so that step is skipped. We use 'assert' to compare the returned value against the expected value which returns True or False. Pytest will interpret this as a pass or a fail.

It is convention to have a separate testing directory, as we have here. You will need to import the function(s) you want to test from their location in the application directory.

_Note_: You require '\_\_init\_\_.py' files inside each folder that contains components you wish to import elsewhere. You can see them in our project already - they can be empty.

# Running pytest

You call pytest from the command line with `pytest`. You can also direct it to specific folders/files by adding the path afterwards, e.g., `pytest tests/results/test_app.py`. Pytest iterates over the given directory (or entire project if no path given) and looks for tests to run.

It will search for files with a 'test\_' prefix (or suffix?) and run them. Within those files, it will run functions with a 'test\_' prefix. If you run the pytest command now, you should have 1 test passing.
The complete set of tests in test_app.py are commented out, so they will not interfere with your code.

## Question time

We have our first working test for our code!

1. What can you do to make the test fail? Consider both the function and the test
2. How effective do you think this test is? Are you confident that our function works as required?
3. Is there anything that this test doesn't do, or could do better?

## Example

Before we improve this test, or write new ones, we will explore some of the core concepts that underpin a strong unit test battery. Let's expand our application to contain a few more components, a control function and some more nuanced logic.

Add this import to the top of your application file:

```
import random
```

Delete the original initial call line from the bottom of the file and copy the following code below our existing combine_results function to add new 3 new functions and a new initial call.

```
TEST_RESULTS: dict[str, float] = {"easy": 23.8, "medium": 49.9, "hard": 105.1}


def collect_result_1(result_range: list[int]) -> int:
    """Randomly selects a result from a provided list of results"""
    return random.choice(result_range)


def collect_result_2(test_type: str) -> float:
    """Return a result based on the type of test taken"""

    return TEST_RESULTS[test_type]


def process_results(input_result_range: list[int], input_test_type: str) -> None:
    """Print out the sum of the results"""
    result_1 = collect_result_1(input_result_range)
    result_2 = collect_result_2(input_test_type)
    result_3 = "number_3"

    print(combine_results(result_1, result_2, result_3))


process_results(input_result_range=[1, 1, 5, 12, 13, 14, 55], input_test_type="medium")

```

process_results contains our control flow and takes two arguments from our initial call. The first provides a list of potential values for result_1 and the second provides a type of test, which will define the value of result_2. Result 3 is hardcoded within the function. Note: This example is designed to be illustrative of the different kinds of things you might do, and how to test them.

We have two new functions, which are called by our process_results function. The first selects a random number from the list of numbers - this becomes result_1. The second looks up the 'test type' in a dictionary and returns the corresponding value to become result_2.

# What are we actually testing?

We want as much certainty as possible that in a specific scenario certain behaviours occur and outputs are generated. We can split these scenarios into the 'happy' path and 'unhappy' path.

The happy path is where the pipeline is receiving the inputs that we expect and all other processes are happening correctly. This is the core of proving that your pipeline meets its requirements and addresses the use cases it was designed for.

The 'unhappy' path is a nebulous place of uncertainty. This is where some invalid data enters the pipeline (e.g., missing data or a date in the future) or an unexpected behaviour occurs. We can split thesse into two sub types:

- Expected issues cover items that you know are possible, but which aren't supposed to occur. You can write code to check for these occurences and specifically handle it in some way - you then add unit tests to check that your handling is triggered correctly without impacting the happy path.

- Unexpected issues cover everything else. It isn't possible to code specific logic to handle these without knowing what they are, instead you can use exceptions to capture any weird occurences and handle them in a generic manner (e.g., log them). You can write unit tests to check that your exceptions fire correctly, but can't validate all the possible scenarios in which it would need to happen.

## Question time

1. What sort of check could we add to our application to handle an expected unhappy path occurence?
2. What could we do to help us manage any unexpected unhappy path occurences?

## Example

We will expand our example to handle some expected unhappy path occurences by adding two checks to validate that our inputs are correct before attempting to operate on them. We will also add a try/except block to catch an unexpected error that prevents us from summing the data.

Replace the combine_results function with the following:

```
def combine_results(result_1: int, result_2: float, result_3: str) -> int:
    """Sums the integer values from three different result sets"""
    try:
        new_result_2 = floor(result_2) if result_2 < 51 else ceil(result_2)
        new_result_3 = int(result_3.split("_")[1])
        return sum([result_1, new_result_2, new_result_3])
    except Exception as exc:
        print(f"Unable to process the values: {result_1}, {result_2} and {result_3}")
        raise exc
```

Then replace process_results with this new version and these two new validation functions:

```
def validate_result_range(result_range: list[int]) -> None:
    """Validates that the result range for result_1 are all integers"""
    if not all(isinstance(val, int) for val in result_range):
        raise ValueError(f"Provided results: {result_range} must contain only integers")


def validate_test_type(test_type: str) -> None:
    """Validates that the test type is valid"""
    if not test_type in test_results:
        raise ValueError(f"Provided test_type: {test_type} is not a valid test type")


def process_results(input_result_range: list[int], input_test_type: str) -> None:
    """Print out the sum of the results"""
    validate_result_range(input_result_range)
    validate_test_type(input_test_type)

    result_1 = collect_result_1(input_result_range)
    result_2 = collect_result_2(input_test_type)
    result_3 = "number_3"
    print(combine_results(result_1, result_2, result_3))
```

This code will still successfully run with the current hardcoced input values from our initial call. Nothing we have just added has altered how the happy path operates. Given an expected set of valid inputs, the pipeline continues as normal.

## Question time

1. Can you make the validate_result_range and validate_test_type functions raise their exception?
2. Can you make the except clause in combine_results fire?
3. Will our unit test pass or fail now?
4. How effectively is our unit test now validating the combine_results function?

If you provide an expected (known to be possible) set of invalid inputs (e.g., values that are not integers, or a test type that doesn't exist), we can have our application raise one of the specific exceptions.

As the try/except block is designed to catch unforeseen errors, and we just ensured that our two inputs are valid, it should be a rarer occurence for this to ever fire. We can force it in this case by replacing the hardcoded result_3 with something like "number_x".

We can add other handling to our exception blocks (attempt remediation of the data, impute default values, log the event, trigger alternate processing, etc.,). This example just illustrates the principle of handling exceptions so that we can test they fire correctly.

# Parameterisation

Our current unit test uses a set of hardcoded input values. As we are seeing, a single scenario is usually not going to be sufficient to prove that the function operates correctly in all cases. We need to be able to test the same function against multiple different inputs, with different expected outputs.

We could spawn multiple copies of the test, each with its own input value. This has the obvious downside of duplicating code which is inefficient and harder to maintain. We would also need a unique name for each test (tedious), but more importantly, if one of the tests fails, it can be a little painful to find which one it was.

## Question time

1. What could you do instead of repeating the code for the test X number of times for different input scenarios?

We can use a loop to define and pass in values from an array of input and expected output values. Each iteration checking one set of inputs against the specified expected output for that iteration. This works, but has one drawback whereby if the test fails, you have no way of knowing which of the values caused it to fail. Fortunately, pytest has a really powerful tool to assist us in repeating the same test using different input parameters and expected outputs. It is functionally a loop, but is built-in to the library so pytest can interpret the results better.

Welcome to `@pytest.mark.parameterize`

_Note_: The @ symbol denotes a decorator, which is placed at the head of functions/methods. Python decorators modify the behaviour of a function (such as making it a property of a class by using the @property decorator).

This decorator takes in a configuration containing every set of values you would like to run through your test (i.e., the loop). Pytest will call the function each time, with the next set of values, and be able to report back on the specific instance that failed (i.e., it will tell you the specific input values it used). This allows us to run several, or even dozens, of test scenarios and be able to pinpoint exactly which scenarios are not correctly handled.

## Example

At the top of your test file, add this import:

```
import pytest
```

Then replace your existing test_combine_results function with the below:

```
# Parametrised unit test for 'Parametrisation' section
@pytest.mark.parametrize(
    ["result_1", "result_2", "result_3", "expected_output"],
    [
        (3, 4.6, "Numnber_3", 10),
        (34, 24.2, "Number_123", 181),
    ],
)
def test_combine_results(
    result_1: int, result_2: float, result_3: str, expected_output: int
) -> None:
    """Tests the combine_results function by checking that we return
    the expected value of 10 from the given inputs"""

    out_val = combine_results(result_1=result_1, result_2=result_2, result_3=result_3)

    assert out_val == expected_output
```

The parameterize decorator takes two arguments:

1. A list of strings (or a single string, if only one) providing the names of the variables you would like to define and pass into your test. Here we have result_1, result_2, result_3 and expected_outcome - providing us with 4 variables to contain the 4 values we would like to vary.
2. A list of tuples. Each tuple contains one element for each of the variables defined in the first step (in our case, 4 total). Pytest will iterate over this list, passing the contents of each tuple into the test function, with the first element being passed to the first defined variable.

You will notice that the function signature has been updated to require the same 4 arguments (the names must be exactly the same). These 4 values are now available to our test.

The test itself is unchanged, other than it uses the 4 variables in place of the originally hardcoded values.

Run pytest now and you'll see that you have 2 passing tests instead of one. Each iteration of the parametrise is treated as a separate test (allowing you to see which iteration was the one that failed).

We are not testing the raising of the exception here, this will be tackled below

## Question time

1. But there is one case which is not accounted for. Can you add one or two scenarios to test that the function correctly rounds result_2 up, if it is 51 or greater?
2. Building on that, are these some scenarios it could be useful to test, just to make sure there are no gaps in the logic around the rounding?

# Real vs Dummy data

Testing with real data creates dependencies on the availability, structure or content of that data. If the data changes then your tests could start failing because your expected outcomes no longer match what is generated. It can also be slower (if that data needs to be sourced or processed first) or more complex (as you may have to work with all of the data rather than a custom subset). If the data is sensitive, then the data may be unobtainable outside of a production environment.

By generating bespoke dummy data for each test, you reduce the risk of accidentally altering any real files/data, or data used by other tests. For some tests, you will need to simulate one or more inputs or ancillary files/objects in order to replicate the real data. Whilst this is a pain in terms of the time to set up, it does confer some great advantages:

- The data can be very small, so the tests are quicker to run and you can visually inspect the data more easily
- You can ensure that all known issues are contained in the dummy data – if your actual source is 10 different files, you can’t guarantee that any one file has all the issues you need to test against.
- You can add scenarios for potential occurences which may not always be present in the real data
- Defining the test data in code makes it easy to re-use across multiple tests – and you don’t have to worry about it being altered, moved or lost

# Test comprehensiveness and repeatability

There is a balance to be struck between writing endless tests and delivering your product/analysis. There is no golden rule, and it will be entirely situation dependent. The goal of testing is to provide the assurance that the code performs as expected and it is therefore down to your judgement/patience on how much testing is required for any specific project.

The more comprehensive the test suite, the more certainty you can place in your outputs and the overhead on maintaining and re-running the tests is much reduced. Any project that is likely to iterate (i.e., the code/data will change over time) will require re-testing. Aside from the time saved, having comprehensive coverage of the codebase provides the repeated certainty that the entire pipeline works as expected.

## Question time

Take our combine_results function - can you spot the error in it?

```
def combine_results(result_1: int, result_2: float, result_3: str) -> int:
    """Sums the integer values from three different result sets"""
    try:
        new_result_2 = floor(result_2) if result_2 < 50 else ceil(result_2)
        new_result_3 = int(result_3.split("_")[1])
        return sum([result_1, new_result_2, new_result_3])
    except Exception as exc:
        print(f"Unable to process the values: {result_1}, {result_2} and {result_3}")
        raise exc
```

Whether you can spot it or not, imagine that one or more of the following are true:

- There are dozens of other functions in your pipeline
- You’re new to the project and don't yet know what everything is supposed to do
- There's several people working on the project, so any number of people could have edited this since you last saw it
- You're returning to the project after some weeks/months/years away from it

How easily would you remember that the < 50 is supposed to be < 51?

The switch could have been a simple typo, or someone tried it at 50 to see what happens and forgot, or someone may have thought the 51 itself was a mistake. Your pipeline might process millions of rows of data, so a manual review is unlikely to spoke that values of 50.9 are now being rounded up instead of down.

Whilst this is a very manufactured scenario, it hopefully illustrates the value of comprehensive testing of even the most basic components in code. Testing is not just for the first iteration of the code. It is the safety barrier for repeated iteration and re-deployment.

# Code Coverage

You can measure the level of coverage your tests have achieved with this output that identifies which lines of code were activated by your tests.

Simply run `pytest --cov-report term-missing --cov=app`, where ‘app’ is the name of the folder with our code.

Your pytest output will now have a section which contains all of the files in the 'app' folder, providing 4 stats for each file:

- Stms - The total number of lines in file
- Miss - The number of lines not hit by any test
- Cover - The percentage of statements hit
- Missing - The line number of the lines not hit

## Question time

1. Which bit of or combine_results function is not covered by our tests? Why?

You will see the missing % is abut 83%, this is actually incorrect (it should be much lower). This is because at the bottom of our file, we have our initial call. When the file is imported in our test file, it actually runs the code and confuses pytest (thinking that the code has been covered by a test). Comment out the initial call and re-run the above command, you will see the % drop to about 46%.

Now the Missing lines will be all of the function bodies that we have not written tests for.

# Adding objects to parametrisation

As with almost everything in Python, you can always use an object (variable, list, dictionary, function, class). Our current test uses strings, floats and ints - but we can actually use anything here.

## Example

We are going to temporarily introduce some objects in to our test, to illustrate how they can be used. In reality you would only need to pass in objects where needed (e.g., the code being tested had a dependency on another object, or you were using a function to generate data for the tests).

You can overwrite the existing test_combine_results function to try these out, then revert the code back.

```
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
    assert combine_results(res1, res2, res3) == exp_out
```

Here we have:

- Generated a list and passed in the first element
- Created a class with three attributes and passed those in
- Called a function and passed in its output

# Testing exceptions

We have a gap in the testing of our combine_results function, we have not proven that the exception is correctly raised. Because exceptions cause our code to stop executing, it is not possible to retun a value our generate any artifacts, providing nothing for us to assert against.

_Note_: Other actions taken within the exception block (such as writing a log) do generate artifacts which can be tested. This section is specifically about testing the raising of the exception itself.

With pytest however, we can check whether an exception has been raised.

## Example

At the top of your test file, add these imports:

```
from contextlib import nullcontext as does_not_raise
from typing import Any
```

Then add a new test function to the bottom of the file

```
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
    """Tests the combine_results function by checking that we generate an exception when invalid data in passed in"""

    with exp_exception:
        combine_results(result_1=result_1, result_2=result_2, result_3=result_3)

```

Here we pass in some incorrect data for each test and set out expectation that using the 'raises' function within pytest (which will return True if the given exception type is raised). We have used the base Exception class for our combine_results function. However, this works with other standard exceptions (such as KeyError and ValueError) as well as custom exceptions

Our test takes a slightly different form. We don't assert whether the exception was raised, instead we use the context manager to call the function to be tested with the expected exception.

We can also prove that a valid input does not raise the exception with the import does_not_raise context manager, which does nothing.

_Note_: Your coverage % will have increased, with your exception lines no longer being reported as missing.

# Failing tests

So far out tests have all been passing, but this won't always be the case first time. When a test fails, you have two questions:

- Is your code wrong?
- Is the test wrong?

If you have written, or set up, the test incorrectly then it will likely fail as the expected output does not match the actual output. It is usually a good idea to start here and revisit your logic to make sure there are no obvious mistakes.

Pytest provides comprehensive logs for failed tests, which includes the specific values used for the current iteration through a parametrisation. Pytest also logs the content of any print statements that were run during the test - this includes in the test function, or the underlying function(s) that were called by the test. This is an invaluable way of seeing the state of the data mid-test and identifying what has caused it to fail.

## Task time

Write out a set of tests for the collect_result_2, validate_result_range and validate_test_type functions.

We won't test collect_result_1 at this time (can you guess why?)

Remember:

- Happy / Sad path
- Cover all the scenarios you are happy with

## Example

As we are now importing more items from our application file, we can simplify our import to:

```
from app import application as app
```

You will then need to prefix all of your function calls with 'app.'

For collect_result_2, we could have something like this:

```
@pytest.mark.parametrize(
    "in_val, exp_out_val", [("easy", 23.8), ("medium", 49.9), ("hard", 105.1)]
)
def test_collect_result_2(in_val: str, exp_out_val: float) -> None:
    """Tests the collect_result_2 function by checking that an input value of 'easy' returns the expected value"""
    out_val = app.collect_result_2(in_val)

    assert out_val == exp_out_val
```

For validate_result_range we could have something like this:

```
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
    """Checks that the validate result range raises an exception when passed an invalid list"""
    with exception:
        app.validate_result_range(in_list)
```

Running your tests (with the initial call commented out) should give you about 75% coverage, with just the collect_result_1 and process_results not covered.

Go ahead and make one of the test cases in the collect_result_2 test fail. We don't want to trigger the exception just yet, so alter one of the expected values and run pytest again.

You will now get a longer test output, which will report 1 failed test. If you scroll up you will se the logging for the failed test. Scroll to the top of that section (the first red lines, which report the name of the test).

- After the name of the test, in square brackets, you have the parametrised values used. THese are also reported more clearly on the first line below
- You then have the code of the test that was run
- Finally the assert statement, with the failing check in red

Note: Sometimes the assertion section gets truncated. If you are comparing large objects, it won’t render the full contents of each. Manually comparing the values the test actually checked is usually the quickest way of narrowing down the issue. You can get pytest to write out more with the –v option. Each ‘v’ adds more detail (up to 3 or 4). For example:

```
pytest -vv
```

Before you fix your test, add a couple of print statements to your code, one in the test and one in the function being tested. You can print whatever you like. After running the test, you should see a new section in the output called 'Captured stdout call' - this is where any print statements are captured. This is an invaluable tool for seeing what is happening during your tests.

# Managing dependencies for tests

Almost every process in your code will have a dependency on something in order to operate correctly. We can split these out into three types (not an exhaustive list, but good enough for illustrative purposes):

A function depending on one or more parameters that are passed into it (I.e., most functions)

A function depending on one or more processes that it calls directly from inside the function (e.g., call a cleansing function on a value before operating on it)

A function depending on some other object that exists outside the process flow (e.g., a log file or a raw data file).

We handle the first case through parametrization. By having discrete functions and discrete tests, we can easily supply the relevant dummy values at the point in which we call the function in the test.

The second case is the most complex, as the dependency is another object that itself would need testing. How can we assure the functionality of one thing that itself relies on the something that we need to assure? There’s a few options for how to approach this, but will be discussed in more detail in the last section on mocking and patching. For reference, an example of this is the process_results function, which calls on the other functions.

The third case will require you to set up various objects in, and around, the specific test, in order to set the right conditions for the test to operate in. Taking the case of a log file and a function which appends a record to the log, but only if a log for that activity doesn’t already exist. To correctly test this function, you would need: No log file, an empty log file, a log file with records for other activities, a log file with a log for that activity and a log file with a combination of logs.

Example:

We expand the functionality of our pipeline by adding a logging mechanism, which creates a dependency on an ‘external’ object. In this case, we log every result that is generated and the three result values used. Crucially, we don’t add the same result more than once (which will provide our nuance to test against).

We make use of classes here to encapsulate our logging logic. There’s loads of general benefits to using classes within your code, which lie outside the topic of automated testing. For our purposes, we can create our own logs and call the write_log method on it to test that the method works as expected.

The log class can take in the path to the log as a parameter. It has a default value for this and in ordinary operation you do not need to overwrite it. B the flexibility to change it is useful for some operations. And in line with the principle of using dummy data, we can make dummy logs in a separate location to the real one and feed these in.

The init function then checks if the path exists (I.e., the file exists). If it does, it loads it, otherwise it creates it as an empty dictionary. This is a neat way of taking the existing log if it exists, or generating a new one if not.

The write log method then appends to the log a new record, containing the result as the key, and the full set of three results as its values – but only if that result is not found in the key already.

You can run this code repeatedly, generating each different result value. You’ll see that it never errors out, but that any duplicate result values are never written to the log.

There are various specific things we could test with our new functionality, but to showcase the principle of supplying external dependencies, we will test that the write_log function generates the correct log each time.

There are two approaches we can take to feed in different logs to the write_log function.

We can physically create different JSON files and feed their paths to the Log class, then call write_log on the class (providing different result sets)

The same as the above, but create the logs as dictionary objects directly and skip having to read the files in

One of these approaches is more problematic than the other. Can you see which it is and why?

The first approach still relies on a dependency. The reading of the log occurs in the **init** method of the Log class. If we physically create the log files, instantiate the Log class (with our bespoke log paths passed in) and then use the logs it generates, this is dependent upon that process to work correctly. If the **init** method is incorrect in any way, then our testing of the write_log method might fail incorrectly.

The second approach removes that dependency and essentially operates on the assumption that **init** works correctly (as it will be tested with its own tests).

Having said that, both methods are shown here, as there will be cases where generating files will be the correct approach (such as testing the **init** method).

This is method 1, with the generation of a physical file. Here you can see how tests can become a little more complex with the addition of generating dependencies. Our test sets a custom log_path (to ensure we do not operate on any real data) and then creates a log file at that location with the parametrized contents. We instantiate the Log class, call the write_log method and then re-read the log file back in and compare it to the expected log contents.

As noted above, this approach has a dependency on the Log class reading the log file in correctly (which is not strictly tested here). Or at least, if the test fails, it is not inherently clear if the issue lies with the writing of the log, or the reading of it.

The last line deletes the test file. This is a useful thing to do to ensure that files do not hang around between tests and potentially impact on another tests’ outcomes.

There are ways to manage more complex dependencies and parametrized objects (in this case, the dictionaries being passed in) through objects themselves. This helps promote reusability and reduces the amount of lengthy hardcoding of values – this will be discussed below.

To properly implement method 2, we would have to use mocking/patching to bypass the **init** method of the Log class; these concepts are handled below. So for now, we are going to bodge the above code to illustrate the example of creating the logs directly.

You can do this by adding this line of code: ‘logger.log = log’ just underneath logger = Log(log_path).

What this does is directly overwrite the ‘log’ object inside logger. So whilst it will use the **init** method and load our generated log file, we immediately overwrite it with our ‘log’ object we are passing in via the parametrize. In this particular case, it has no actual effect, as both generate the same log. But the principle holds that we have not actually relied on the **init** method to read in the log. As mentioned, at the end of this course, we will look at mocking and patching, which will remove the **init** method from the equation and simplify this approach.
