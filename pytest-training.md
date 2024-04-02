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
12. [Testing pandas DataFrames](#testing-pandas-dataframes)
13. [Testing exceptions](#testing-exceptions)
14. [Failing tests](#failing-tests)
15. [Managing dependencies for tests](#managing-dependencies-for-tests)
16. [Dependencies as objects (fixtures)](#dependencies-as-objects-fixtures)
17. [Testing wide setup and teardown (conftest)](#testing-wide-setup-and-teardown-conftest)
18. [Complex dependencies - patching (basic return values)](#complex-dependencies---patching-basic-return-values)
19. [Patching order, 'with patch' and paths](#patching-order-with-patch-and-paths)
20. [Complex dependencies - patching (complex side effects)](#complex-dependencies---patching-complex-side-effects)
21. [Complex dependencies - patching (call count and args)](#complex-dependencies---patching-call-count-and-args)
22. [Final items (dicts, properties, inits, methods, 3rd party and built-ins)](#final-items-dicts-properties-inits-methods-3rd-party-and-built-ins)

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

You call pytest from the command line with:

```
pytest
```

You can also direct it to specific folders/files by adding the path afterwards, e.g.,

```
pytest tests/results/test_app.py`
```

Pytest iterates over the given directory (or entire project if no path given) and looks for tests to run.

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
TEST_RESULTS: dict[str, float] = {"easy": 23.8, "medium": 49.9, "hard": 105.1,}


def randomise_result(length: int) -> int:
    """Randomly selects a number to be the index of the result range
    to use"""
    return random.choice(range(length))


def collect_result_1(result_range: list[int]) -> int:
    """Selects a result from a provided list of results using a random
    number"""
    index = randomise_result(len(result_range))
    return result_range[index]


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

We have three new functions, which are called by our process_results function. collect_result_1 calls randomise_result which generates a random number from the length of the result list - it uses this number to index the result list, which becomes result_1. collect_result_2 looks up the 'test type' in a dictionary and returns the corresponding value to become result_2.

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

# Testing pandas Dataframes

Dataframes are a commonly used data structure, especially for Data Science. If you test a function with a DataFrame output and attempt to asseert that DataFrame == an expected DataFrame, you will actually generate an error. This error tells you that you the truthfullness of the assertion is ambiguous (i.e., it doesn't know if they match or not).

Fortunately pandas comes with its own testing functions which you can use to assert against your output.

## Example

Add an import for pandas to the top of your script:

```
import pandas as pd
```

Replace your process_results function and initial call with:

```
def process_results(input_result_range: list[int], input_test_type: str) -> pd.DataFrame:
    """Print out the sum of the results"""
    validate_result_range(input_result_range)
    validate_test_type(input_test_type)

    result_1 = collect_result_1(input_result_range)
    result_2 = collect_result_2(input_test_type)
    result_3 = "number_3"

    output = combine_results(result_1, result_2, result_3)

    return pd.DataFrame(
        data={
            "result_1": [result_1],
            "result_2": [result_2],
            "result_3": [result_3],
            "sum": [output],
        }
    )


print(
    process_results(
        input_result_range=[1, 1, 5, 12, 13, 14, 55], input_test_type="medium"
    )
)
```

We are now returning the result of our application as a DataFrame and printing it out. We can test that this DataFrame look as we expect.

We are not going to write this test right now, because it will fail to pass (as it is reliant on the random output of the collect_result_1 function). However, to write DataFrame tests for your own code, you just need to know the syntx:

```
pd.testing.assert_frame_equal(df_1, df_2)
```

You pass in your actual and expected DataFrames and it will check if they are equal. At its base, this is a very strict test (indexes, data types, etc.,) which can be tricky to pass. Often your datatypes can be misalinged in tiny ways, requiring you to hammer your expected data into shape. You can configure which facets of the DataFrame are checked within the function call.

There are also a few other assertions you can call on DataFrames - intelliense should present them to you when you access 'pd.testing.'

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

Write out a set of tests for the randomise_result, collect_result_2, validate_result_range and validate_test_type functions.

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

For validate_test_type we could have something like this:

```
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
    """Checks that the validate result range raises an exception when passed an invalid list"""
    with exception:
        app.validate_test_type(in_type)
```

for randomise_result we could have something like this:

```
@pytest.mark.parametrize(
    "length",
    [
        (1),
        (10),
    ],
)
def test_randomise_result(length: int) -> None:
    for _ in range(100):
        assert app.randomise_result(length) >= 0
        assert app.randomise_result(length) <= length
```

Running your tests (with the initial call commented out) should give you about 70% coverage, with just the collect_result_1 and process_results not covered.

## Task time

- Go ahead and make one of the test cases in the collect_result_2 test fail. We don't want to trigger the exception just yet, so alter one of the expected values and run pytest again.

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

Almost every process in your code will have a dependency on something in order to operate correctly. We can split these out into a (non exhaustive list) of three types:

1. A function depending on one or more parameters that are passed into it (e.g., combine_results)

   - We handle this through parametrization. By having discrete functions and discrete tests, we can easily supply the relevant dummy values at the point in which we call the function in the test.

2. A function depending on some other object that exists outside the process flow (e.g., collect_result_2, sort of).

   - Here we set up the objects we require as part of the test. This is the second part of a 'good unit test' that we skipped over before. With collect_result_2, we make use of the TEST_RESULTS dictionary - for us, this is a constant. But in reality it could be sourced from a file, or generated at runtime. For testing, we would have to provide that object to the test (remembering our rule - no real data)

3. A function depending on the output or operation of one or more processes that it itself calls (e.g., collect_result_1 and process_results)
   - This is the most complex, as the dependency is another object that itself would need testing. How can we assure the functionality of one thing that itself relies on the something that we need to assure? There’s a few options for how to approach this, which will be discussed in more detail later on.

Example:
We are going to put case 3 to one side for now and focus on case 2, for which we don't have a great example at the moment. So we are going to expand our example by adding a logging mechanism. We will record every output that is generated and the three result values that were used; we will also configure it to not log the same output more than once, providing some nuance to test against.

We also introduce the use of classes here to encapsulate our logging logic. Classes confer lots of functionality and benefits for data pipelines, but this lies outside the topic of automated testing. For our purpose, we will create a log and a method for writing the log to file.

In your imports, add the following:

```

import json
from pathlib import Path
from typing import Union

```

At the top of your application file (above combine_result and below TEST_RESULTS), add the following:

```

class Log:
    """Class to generate and update the log"""

    def __init__(self, log_path: Path = Path("data/log.json")) -> None:
        self.log_path = log_path
        if self.log_path.exists():
            with open(self.log_path, "r", encoding="utf=8") as f:
                self.log: dict[str, list[Union[int, str, float]]] = json.load(f)
        else:
            self.log_path.parent.mkdir(exist_ok=True, parents=True)
            self.log = {}

    def write_log(self, output: int, results: list[Union[int, str, float]]) -> None:
        """Writes entry to the log if this result has not been seen before"""
        if str(output) not in self.log:
            self.log[str(output)] = results
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(self.log, f, indent=4)

```

Then replace your process_results function with:

```

def process_results(input_result_range: list[int], input_test_type: str) -> pd.DataFrame:
    """Print out the sum of the results"""
    validate_result_range(input_result_range)
    validate_test_type(input_test_type)

    result_1 = collect_result_1(input_result_range)
    result_2 = collect_result_2(input_test_type)
    result_3 = "number_3"
    output = combine_results(result_1, result_2, result_3)

    log = Log()
    log.write_log(output, [result_1, result_2, result_3])

    return pd.DataFrame(
        data={
            "result_1": [result_1],
            "result_2": [result_2],
            "result_3": [result_3],
            "sum": [output],
        }
    )

```

The log class has an initialisation method which goes to a given file path and loads the existing log if there is one, otherwise it return an empty dictionary (log). The path itself can be a parameter we pass in - which is always useful for reusability, but also testing (as we can pass in a test file path and not affect any real data).

The write_log method takes the output and the three individual results as parameters. If the result is already in the log, then this will do nothing, otherwise it will append a new key:value pair to the log (output: results) and then write out the update log.

process_results instatiates an instance of the Log class, upon which we can call the write_log method (passing in the relevant arguments). To do this, it explicitly stores the output of combine_results as a variable so that it can be passed to the write_log method.

You can run this code repeatedly, generating each different result value. You’ll see that it never errors out, but that any duplicate result values are never written to the log. You can delete the log to start again, as the code will just generate an empty log.

## Question time

1 - What functionality could we test?
2 - What scenarios should we test?

Functionality:

- Reading in a log, or generating a blank one.
- Checking if the output is already in the log
- Appending the log entry
- Writing out the log

Scenarios:

- Log exists / does not exist
- ouput value is in log / is not in log

In order to correctly simulate the 3 scenario combinations, we need to build a custom log object (or not) to pass in to the test function to alter its behaviour each time.

There are two approaches we can take to feed in different logs to the write_log function.

## Example

Update your imports as follows:

```

import json
import pytest

from contextlib import nullcontext as does_not_raise
from typing import Any, Union
from pathlib import Path

from app import application as app

```

Then add this new test to the bottom of your test file:

```

@pytest.mark.parametrize(
    ["log", "outcome", "results", "exp_log"],
    [
        (
            {},
            6,
            [2, 1.5, "2.5"],
            {"6": [2, 1.5, "2.5"]},
        ),
    ],
)
def test_write_log(
    log: dict[str, list[Union[int, str, float]]],
    outcome: int,
    results: list[Union[int, float, str]],
    exp_log: dict[str, list[Union[int, str, float]]],
) -> None:
    """Test write_log function by generating the existing log directly"""

    log_path = Path("data/test_log.json")

    if log:
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f)

    logger = app.Log(log_path)
    logger.write_log(outcome, results)

    with open(log_path, "r", encoding="utf=8") as f:
        actual_log = json.load(f)

    assert actual_log == exp_log

    log_path.unlink()

```

The structure of the test is the same as our existing ones, but we have additional logic in the body of the test and have begun to bring together lots of the key concepts for building unit tests.

Our Log class takes the filepath for the log as an argument, allowing us to create a custom log at a specific path and provide that for the test to use. We can define our custom log for each test case as an object inside the parametrisation (as well as the expected log to compare against).

In this scenario, we are testing where there is no existing log (an empty dictionary). We set the test to only write out a file if that dummy log is populated - this allows us to use one function to test all scenarions.

We instantiate the Log and call write_log in the same manner as in process_results. Then simply read in the log file from the same path and assert that its contents match our expected log.

You can see how the complexity of tests can start increasing as you start having to manage dependencies to ensure you have robust unit tests.

## Question time

1. What key principle have we adhered to in the set up of our test?
2. What principle have we not adhered to?

By passing in a different path for the log, we have ensured we used dummy data and do not risk interfering what anything occuring in our real data/log.json file. It is not always possible to pass in values like this as part of the test (for example, the value might be accessed from the internet and be out of your control) - we will discuss handling these cases later.

We have tested the \_\_init\_\_ and write_log methods together. We relied on the init method to load our log, before validating the logic of write_log against that log. What if our init method is wrong?

In simple cases like this, it doesn't really matter, as it will be obvious where any issues are if a test fails because either the init or write_log methods are wrong. However, the principle we want to adhere to as much as possible is for a unit test to validate the logic of a single thing.

If you're writing comprehensive tests, you can operate on an assumption that another test will validate the init method, and therefore relying on it here is fine because that test will also fail (if init is incorrect). Then fixing init will lead both tests to pass.

Another option is to restructure your code. You could instead have a standalone function which loads log files, then you pass the log as an object directly to the Log class (removing the dependency on the Log class to load the data).

## Task time

- Can you add 2 or more test cases to cover the remaining scenarios?

You could have something that looks like this:

```

(
{"5.1": [2, 3.1, "1"]},
6,
[2, 1.5, "2.5"],
{"5.1": [2, 3.1, "1"], "6": [2, 1.5, "2.5"]},
),
(
{"6": [2, 1.5, "2.5"], "10": [9, 1.0, "0"]},
6,
[2, 1.5, "2.5"],
{"6": [2, 1.5, "2.5"], "10": [9, 1.0, "0"]},
),

```

# Dependencies as objects (fixtures)

Pytest fixtures provide a way of formalising the definition of dependency objects within the pytest framework. There is a whole world of functionality that they provide (https://docs.pytest.org/en/6.2.x/fixture.html). For this guide, we will just explore some basic usage whereby we will define an object to be used across multiple tests.

A fixture is a function, appended with the fixture decorator

```
@pytest.fixture
```

The fixture function has a unique name and returns an object. We can pass the fixture into a test (using its name) and pytest will automatically run the fixture and make its return value available to the test. This negates the need to have additional setup logic in the test itself. The fixture can be called by any number of tests, providing repeated savings in setup logic. This is especially useful if you have some core objects that a lot of your logic is built around (e.g., a class with a lot of methods to be tested, you can use a fixture to build a baseline instantiation of the class).

You could encapsulate the same logic in a regular function (as both will return objects that you can use in your test). Whilst this is true, fixtures provide deeper functionality that will be of use in more comprehensive test suites. Our example here will be simple, leaving you to explore fixtures at the above link at your own leisure.

## Example

Add this new test to the bottom of your test file

```

@pytest.fixture(name="log")
def fix_log() -> dict[str, list[Union[int, str, float]]]:
    return {"5.1": [2, 3.1, "1"]}


def test_write_log_fixture(log: dict[str, list[Union[int, str, float]]]) -> None:
    """Test write_log function by generating the existing log directly"""

    log_path = Path("data/test_log.json")

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f)

    logger = app.Log(log_path)
    logger.write_log(3, [1, 1.0, "1"])

    with open(log_path, "r", encoding="utf=8") as f:
        actual_log = json.load(f)

    assert actual_log == {"5.1": [2, 3.1, "1"], "3": [1, 1.0, "1"]}

    log_path.unlink()

```

The test itself is unchanged (other than removing the parametrisation logic). The log fixture is automatically passed in to the test by pytest (as the names match) and we can use the returned value as usual.

The use of 'log' within the test is using the actual object returned, which means (in this case) you can perform any dictionary operations on it that you would be able to normally (similarly if the return value was a list, class, function, etc.,). This means you can alter the fixture contents within tests in order to provide more bespoke behaviour across test scenarios.

In order to achieve the same functionality as we had before, we need a way to parametrise the generation of the log object (using the regular parametrise functionality and altering the log after the fact would negate any value of the fixture). This is unfortunately not as simple as just using a regular function. You can see an example of this in the linked documentation about 80% of the way down under 'Factories as fixtures' and then some more sections on parametrisation.

The principle is that you can return a function from the fixture; that function itself takes parameters. You then call the function as normal in your test and pass in the arguments dynamically (which can be delivered from the parametrise decorator).

As mentioned above, it may be simpler to use regular functions for a lot of this behaviour unles you're going to dive into the deeper end of what fixtures can do.

# Testing wide setup and teardown (conftest)

When you run pytest, it automatically searches for a ‘conftest.py’ file when it sets up your tests. This is a file that lets you configure various aspects of pytest and define objects to be used across multiple test files. You can have one conftest file per directory, allowing you to define objects for use across files in one, or mutliple folders.

One common usage of the conftest files is to store fixtures. In this way, you can make the same fixture available to all test files in the same directory (or sub directories) without having to import anything into each file.

You can read more about fixtures in the conftest file here: https://docs.pytest.org/en/7.1.x/reference/fixtures.html

## Example

If you are working with the repo from github, you already have a conftest file. Go into it and uncomment the log fixture and delete the version of it from your test file.
If you have set up your own project, then create a conftest.py file in your tests folder. Then copy the log fixture to the conftest file and delete it from your test file.

Your conftest should look like this:

```

from pathlib import Path
from typing import Union

import pytest

@pytest.fixture()
def log() -> dict[str, list[Union[int, str, float]]]:
return {"5.1": [2, 3.1, "1"]}

```

Your tests will still run, picking up the log object from the conftest file, even though you haven't imported it.

There is a second function in the conftest file (if you are in your own project, paste in the below).

```

def pytest_unconfigure() -> None:
"""Function called by pytest automatically once all tests are run to clean up test artifacts"""

    if Path("data/test_log.json").is_file():
        Path("data/test_log.json").unlink()

```

This is an example of some of the magic that pytest can do. This is a function which pytest looks to see if it exists. If it does, it runs it, otherwise not. This particular function runs at the end of all of your tests (hence 'unconfigure') and can be used to provide definitive cleanup for your tests.

# Complex dependencies - patching (basic return values)

It is finally time for us to return to the third type of dependency for a unit test, which was: 'A function depending on the output or operation of one or more processes that it itself calls (e.g., process_results)'

Whilst we have looked at creating and passing in test objects to supplant some dependencies, this is not always straightforward:

1. The dependency might be one or more functions that the function we would like to test calls
   - These functions could be nested 2 or more layers deep under other function calls (all part of a more complex pipeline). Tests want to assess a single unit, if we are actually executing dozens of lines of code, we can't be certain of what we're testing or what causes a test to fail
   - The other functions require their own testing and you shouldn't rely on their succesful operation in determining if your target function is correct
   - The functions might be undertaking processing that is not practical to complete within a test (e.g., accessing internet, accessing real data, etc.,). You can't guarantee the same result every time, which makes your tests unpredictable.
   - The operations undertaken by these functions might be slow, which is miserable to sit through. Atlas has 557 tests which take less than 10 seconds to run
2. The dependency might be an object, function or class which has its own behaviours (including automatic behaviours, such as init methods or properties)
3. The dependency might be an object that is not relevant to the test in question and it is therefore a waste of time to replace it
4. The function we are testing might itself be buried in some processes or objects (e.g., a method of class) which has its own behaviours that are either cumbersome to replace or could affect the outcome of the test

We can make extensive use of the unittest library to patch out these objects. We can replace the object with nothing (for irrelevant items for the test) or we can impute our own logic (great for creating bespoke testing scenarios).

## Example:

We have some real problems with testing the process_results function - it ticks a lot of the above criteria. Not least, because the collect_result_1 function relies on a random selection. There is no way to define a fixed expected output that would pass every time.

To start, we will solve that problem and at least enable us to generate tests that pass consistently.

At the top of your test file, add these imports:

```
import pandas as pd
from unittest.mock import Mock, patch
```

Add this function to the bottom of the tests file:

```
@patch("app.application.collect_result_1")
def test_process_results(mock_result_1: Mock) -> None:

    mock_result_1.return_value = 1

    pd.testing.assert_frame_equal(
        app.process_results([1, 2, 3], "easy"),
        pd.DataFrame(
            data={
                "result_1": [1],
                "result_2": [23.8],
                "result_3": ["number_3"],
                "sum": [27],
            }
        ),
    )
```

The patch decorator takes in the path of the object to be patched and replaces it with a Mock object (which, at this point, is empty). As with parametrization, we have to pass that object in to the test as a parameter.

Within the test, we can manipulate the patched object. Here we have used the functionality to fix its return value. So even though we pass a list of 1, 2 and 3 to the (what was) random selection, it will always return the value we specify.

You can also specify the replacement value directly in the patch decorator, it is the second positional argument after the path to the object being patched.

We (will) test the collect_result_1 function separately. From the perspective of process_results, we don't care what the actual output from collect_result_1 is - we are testing that process_results calls the correct functions and handles the inputs and outputs correctly. The actual values are irrelevant.

# Complex dependencies - patching (basic side effects)

As previously discussed, we don't want to rely on dependencies being correct when validating a function, therefore we should also patch out the other functions called by process_results.

We will leave the Log for now. This is actually a problem case, because it is currently hardcoded to write the log to the main data/log.json file, which violates our separation of tests from the real data.

## Example

For now, update the process_results function to this:

```
@patch("app.application.validate_result_range")
@patch("app.application.validate_test_type")
@patch("app.application.collect_result_1")
@patch("app.application.collect_result_2")
@patch("app.application.combine_results")
def test_process_results(
    mock_combine: Mock,
    mock_result_2: Mock,
    mock_result_1: Mock,
    mock_test_type: Mock,
    mock_result_range: Mock,
) -> None:

    mock_result_1.return_value = "Not a valid int"
    mock_result_2.return_value = False

    mock_test_type.side_effect = None
    mock_result_range.side_effect = None

    mock_combine.return_value = 245

    pd.testing.assert_frame_equal(
        app.process_results([1, 2, 3], "easy"),
        pd.DataFrame(
            data={
                "result_1": ["Not a valid int"],
                "result_2": False,
                "result_3": ["number_3"],
                "sum": [245],
            }
        ),
    )

```

We have replaced the 5 other functions called by process_results. To demonstrate the power of the patching, we have deliberately returned invalid values for result 1 and 2. But we set the side_effect (i.e., what the function does) for the two validate functions to None - so they do nothing and don't flag the result as invalid. We then hardcode the output from combine_results and don't actually run the code at all, meaning that we can get a very malformed DataFrame which still passes the test.

Which of course is a little useless. As always, what are we testing here? Currently, only that a DataFrame is correctly generated from 4 given values. We have proved that our process_results function operates correctly as a control flow function.

# Patching order, 'with patch' and paths

## Patching order

Before expanding our use of patches, you should note that when you patch multiple objects and pass them into the test, the order in which you define the arguments is in reverse order to the list of decorators:

Here, validate_result_range is the first decorator, but is the last parameter (mock_result_range).

## With patch

You can also patch objects inside the test with the 'with' context manager:

```
with patch("app.application.validate_result_range") as mock_result_range:
```

This works exactly the same, then within the context manager you can assign return_values or side_effects as before. This simplifies your test signature, as you don't pass it in as an argument. You can chain multiple contexts within the same 'with' command, by commad separating them. However, this can become a little hard to decipher if you need to patch multiple objects.

## Patching paths

In a more complex project, you may have a file that defines some core functions (e.g., reading data, writing data, transforming values, etc.,) and then a second file which imports those functions to use in some processing functions (such as the process_results function).

If you wish to test the process_results function, but mock out one of the dependent functions that come from the second file, then you need to ‘mock the object at import, not definition’.

If we imagine that our collect_result_1 and collect_result_2 functions were in another file, then our application file would have an additional import:

```
from app.collect_funcs import collect_result_1, collect_result_2
```

When it comes to testing process_results and patching these functions, you would keep the same path as used in the above example (i.e., 'app.application.collect_result_1'). You would not patch the patch 'app.collect_funcs.collect_result_1.

This is because you are patching the version of the object used by process_results. Your main application file imports a copy of the function and therefore it is this version which needs to be patched.

# Complex dependencies - patching (complex side effects)

Up to now, we have not actually tested collect_result_1, as it relies on the randomise_result function. We now have the capability to bypass this dependency. We could patch it to have a fixed return value, but this is also an opportunity to show what can be done with side_effects.

## Example

Add the following to the bottom of the tests file:

```
@pytest.mark.parametrize(
    ["result_range", "exp_result"],
    [
        ([1, 2, 3, 4], 3),
        ([4, 5, 6, 7, 8, 9], 7),
    ],
)
@patch("app.application.randomise_result")
def test_collect_result_1(
    mock_random: Mock, result_range: list[int], exp_result: int
) -> None:
    def mock_random_func(length: int):
        return round(length / 2)

    mock_random.side_effect = mock_random_func

    assert app.collect_result_1(result_range) == exp_result
```

We can pass functions as the side effect for the patched function, effectively replacing its original behaviour with bespoke behaviour for the test. In order to create a stable output from randomise_result we have returned an index value equal to half of the length. We can then assert that collect_result_1 will return a specific value, based on the length and content of the list we pass in. This means we have tested collect_result_1 with no dependency on the actual behaviour of randomise_result.

# Complex dependencies - patching (call count and args)

At this point we have finally reached 100% code coverage, but our testing of process_results is not very robust. We have just patched out a bunch of functionality, continued to use the real write_log method and checked that the junk DataFrame looks like the one we told it to make.

When it comes to control flow functions, it is more useful to check whether the right functions have been called, in the right way. We can do this by interrograting which patches were called and the arguments they were called with.

## Example

This example will just apply the logic to the write_log method, to keep it simpler. The logic can be easily applied to the other patched functions.

Replace your test_process_results function with:

```
@patch("app.application.validate_result_range")
@patch("app.application.validate_test_type")
@patch("app.application.collect_result_1")
@patch("app.application.collect_result_2")
@patch("app.application.combine_results")
@patch("app.application.Log.write_log")
def test_process_results(
    mock_log: Mock,
    mock_combine: Mock,
    mock_result_2: Mock,
    mock_result_1: Mock,
    mock_test_type: Mock,
    mock_result_range: Mock,
) -> None:

    mock_result_1.return_value = "Not a valid int"
    mock_result_2.return_value = False

    mock_test_type.side_effect = None
    mock_result_range.side_effect = None

    mock_combine.return_value = 245

    pd.testing.assert_frame_equal(
        app.process_results([1, 2, 3], "easy"),
        pd.DataFrame(
            data={
                "result_1": ["Not a valid int"],
                "result_2": False,
                "result_3": ["number_3"],
                "sum": [245],
            }
        ),
    )
    assert mock_log.call_count == 1
    assert mock_log.call_args_list[0][0][0] == 245
    assert mock_log.call_args_list[0][0][1] == ["Not a valid int", False, "number_3"]
```

This adds a patch to the write_log method.
Note, that as a method of a class, the patch path goes via the Log class.
Also note that we don't assign a return value or side effect to the method - we are just blanking it own (we could assign a side effect if we wished).

We introduce two new asserts against patches. The first let's us query the number of times the patch was called (which proves it was run). We could apply the same logic to the other functions (this is quite useful if you conditional logic which will lead to different numbers of calls). There are various call related methods in the Mock library.

Whilst we don't care what the patched functions do (or would do), we do care what arguments they are called with, as this is evidence that the control flow is operating correctly. We can access every argument passed, for every call, to a patched function. It can take a bit of practice to get the correct indexing for each value you want to check.

When you consider the eventual complexity of this test (with similar asserts on all the functions), you might start thinking some of the thoughts that were discussed back at the beginning of this document - the signs that your functions are too complicated.

It is definitely the case that this process_results function would be better off as 2 or 3 individual functions.

# Final items (dicts, properties, inits, methods, 3rd party and built-ins)

## Dictionaries

Sometimes you will need to patch out dictionaries (e.g., if you're using them to map values to functionality). The default patch syntax does not work properly with dictionary items, instead you need to use:

```
@patch.dict("path.to.dict", [replacement_dict])
```

Here you can supply the new dictionary directly in the patch.

## properties

If you're making use of classes, you may also be defining some properties for that class. As these are automatically created and updated, it may be critical to the testing of a method of function to be able to manipulate that property.

You will need to import an additional item from unittest:

```
from unittest.mock import PropertyMock
```

Then in your patch you will set the path to the property being mocked and set the 'new_callable' argument to 'PropertyMock'

```
@patch("app.application.log.[property_name], new_callable=PropertyMock)
```

Then you need to set the side effect for this patch, as above. Whatever the return value of that side effect is, that will be the value of the property when the class is instantiated as part of the test.

## inits and methods

We have already mocked a method - which can be done by pathing through the class object. However, you may want to replace the behaviour with custom behaviour (a side effect function), which is especially useful for init/post_init methods, as they run automatically.

The issue is in the use of 'self' within class methods. When you define a class method, the first argument is always 'self' which relates to some python magic which automatically passes the class itself as a parameter to any of its class methods. You'll notice that our write_log method has a self argument, but when we call it in our code, we don't pass anything to it.

When you create your mock function to replace the method, if you add a self argument to it, Python will not recognise that function as replacing a Class method. Therefore it will think 'self' is a regular argument and expect a value to be passed to it. However, when you run the test, which runs your actual code, you won't pass an argument to it (because in reality, Python would handle that for you, as the real method is a Class method).

Essentially, there is a mismatch when patching a Class method, as Pytest and Python do not know that the replacement function is meant to be a class method.

All that is to say, when you create the patch for the method (that you want to assign a side effect to), then add 'autospec=True' to the patch definition after the path. This will make it inherit the original methods signature. Your mock function can then define self (it's type will be of the Class the method belongs to)

```
@patch("app.application.Log.write_log", autospec=True)
...
def mock_log(self: Log, output: int, results: list[Union[int, str, float]]) -> None:
...
```

## Built ins and third party libraries

You can patch out built-in and 3rd party objects. If you are importing Path from pathlib, then you can use:

```
@patch("app.application.pathlib.Path)
```

If you alias the object (e.g., pandas as pd), then it will be "app.application.pd"

Some functions are called 'built-ins', such as len(), abs(), open(). You can patch these too - look it up!
