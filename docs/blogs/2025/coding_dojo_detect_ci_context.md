---
tags: python, coding-dojo, tdd, software-craftsmanship
category: coding-dojo
date: 2025-03-08
title: Coding Dojo - Detect CI Context
---

# Coding Dojo - Detect CI Context

## Introduction

Coding Dojos are a great way to practice and enhance your skills in Test-Driven Development (TDD), software craftsmanship, and incremental software design.
In this blog post, we’ll explore how to implement the [Detect CI Context](https://maxiniuc.com/coding_dojo_ci_context/presentation.html) coding example using Python.

You'll learn how to:

- Clearly define APIs and data structures.
- Translate the requirements to tests.
- Implement the solution incrementally using TDD.
- Refactor code for clarity, maintainability, and scalability.

## Understand the problem and define the API

The problem is to detect whether a program runs on Jenkins or locally.
The inputs are the specific environment variables that Jenkins sets when running a build.

The expected outputs are:

- The CI system name (e.g. Jenkins or Unknown).
- Is the build trigger a Pull Request.
- Name of the target branch (branch to merge into).
- Name of the current branch being built or tested.

Using our module should be as straightforward as calling a **method** that returns the required **data**.

In Python, our method signature could look like this:

```{code-block} python
def detect_ci_context() -> CIContext:
    pass
```

We can use a data class to represent the CI context:

```{code-block} python
@dataclass
class CIContext:
    #: CI system where the build is running
    name: str
    #: Whether the build is for a pull request
    is_pull_request: bool
    #: The branch to merge into
    target_branch: Optional[str]
    #: Branch being built
    current_branch: Optional[str]
```

## Implement the Solution Incrementally

The way to determine the CI context for Jenkins can be summarized as follows:

- Presence of `JENKINS_HOME` indicates Jenkins.
- If running a pull request (`CHANGE_ID`), `CHANGE_TARGET` is the target branch and `CHANGE_BRANCH` is the current branch.
- If not a pull request, `BRANCH_NAME` is the current branch.

### First requirement - Detect Jenkins

Let's start by writing a test that checks if the CI system is Jenkins.

Our test should:

- Set the `JENKINS_HOME` environment variable to a non-empty value.
- Call the `detect_ci_context` method.
- Check if the `name` is `JENKINS`.

The first issue we encounter is to be able to manipulate the environment variables.

In Python, we can mock the `os.getenv` function using the `unittest.mock` module:

```{code-block} python
@pytest.fixture
def mock_on_getenv():
    with patch("os.getenv") as mock_os_getenv:
        yield mock_os_getenv
```

What this fixture does is to replace the `os.getenv` function with a mock object that we can control.

Now we can write the test:

```{code-block} python
def test_jenkins_branch_push(mock_on_getenv: MagicMock) -> None:
    # Setup
    mock_on_getenv.side_effect = lambda var, default=None: {
        "JENKINS_HOME": "/jenkins/home"
    }.get(var, default)
    # Run
    ci_context = detect_ci_context()
    # Check
    assert ci_context.name == "JENKINS"
```

We override the `os.getenv` function with a [lambda](https://realpython.com/ref/keywords/lambda) that returns the value of the `JENKINS_HOME` environment variable. It has the same signature as the original function, taking two arguments: the variable name and a default value.

To fix the test, we need to implement the `detect_ci_context` method:

```{code-block} python
def detect_ci_context() -> CIContext:
    return CIContext(
        name="JENKINS",
        is_pull_request=False,
        target_branch=None,
        current_branch=None,
    )
```

```{note}
You might be surprised that we hardcoded the `name` to `JENKINS`.
This is one idea behind [TDD](https://en.wikipedia.org/wiki/Test-driven_development): write the simplest code that makes the test pass.
```

### Second requirement - Detect Unknown

Let's write a test that checks if the CI system is unknown:

```{code-block} python
def test_unknown_ci_system(mock_on_getenv: MagicMock) -> None:
    # Setup
    mock_on_getenv.side_effect = lambda var, default=None: {}
    # Run
    ci_context = detect_ci_context()
    # Check
    assert ci_context.name == "Unknown"
```

To fix the test and do not break the previous one, we can't just return a constant value but need to _check_ the environment variables:

```{code-block} python
def detect_ci_context() -> CIContext:
    return CIContext(
        name="JENKINS" if os.getenv("JENKINS_HOME", None) else "Unknown",
        is_pull_request=False,
        target_branch=None,
        current_branch=None,
    )
```

### Implement the rest of the requirements

We can continue implementing the rest of the requirements in the same way, writing tests and fixing them by implementing the `detect_ci_context` method.

```{code-block} python
def detect_ci_context() -> CIContext:
    ci_name = "UNKNOWN"
    is_pull_request = False
    target_branch = None
    current_branch = None
    if os.getenv("JENKINS_HOME", None) is not None:
        ci_name = "JENKINS"
        is_pull_request = os.getenv("CHANGE_ID", None) is not None
        if is_pull_request:
            target_branch = os.getenv("CHANGE_TARGET")
            current_branch = os.getenv("CHANGE_BRANCH")
        else:
            target_branch = os.getenv("BRANCH_NAME")
            current_branch = target_branch
    return CIContext(
        name=ci_name,
        is_pull_request=is_pull_request,
        target_branch=target_branch,
        current_branch=current_branch,
    )
```

## Refactor

First thing that looks odd is the `CIContext.name` variable type. Strings are too generic and can lead to errors. Imagine a typo in the string or different capitalization, `JENKINS` vs `Jenkins`.

We can use an enumeration to represent the CI system:

```{code-block} python
class CISystem(Enum):
    JENKINS = auto()
    UNKNOWN = auto()
```

and update the `CIContext` class:

```{code-block} python
@dataclass
class CIContext:
    #: CI system where the build is running
    ci_system: CISystem
    #: Whether the build is for a pull request
    is_pull_request: bool
    #: The branch to merge into
    target_branch: Optional[str]
    #: Branch being built
    current_branch: Optional[str]

    @property
    def name(self) -> str:
        return self.ci_system.name.upper()
```

```{note}
This refactoring caused no tests to fail nor did it change the API.
```

## New Feature Request

There is a new requirement to detect `GitHub Actions`.

The way to determine the CI context for `GitHub Actions` can be summarized as follows:

- `GITHUB_ACTIONS` indicates GitHub Actions.
- If running a pull request (`GITHUB_EVENT_NAME` is `pull_request`), `GITHUB_BASE_REF` is the target branch and `GITHUB_HEAD_REF` is the current branch.
- If not a pull request, `GITHUB_REF_NAME` is the current branch.

### First requirement - Detect Github Actions

We can write a test for this new requirement:

```{code-block} python
def test_github_actions_pull_request(mock_on_getenv: MagicMock) -> None:
    # Setup
    mock_on_getenv.side_effect = lambda var, default=None: {
        "GITHUB_ACTIONS": "true",
    }.get(var, default)
    # Run
    ci_context = detect_ci_context()
    # Check
    assert ci_context.name == "GITHUB_ACTIONS"
```

We can implement the new feature by extending the `detect_ci_context` method:

```{code-block} python
def detect_ci_context() -> CIContext:
    ci_system = CISystem.UNKNOWN
    is_pull_request = False
    target_branch = None
    current_branch = None
    if os.getenv("JENKINS_HOME", None) is not None:
        ci_system = CISystem.JENKINS
        is_pull_request = os.getenv("CHANGE_ID", None) is not None
        if is_pull_request:
            target_branch = os.getenv("CHANGE_TARGET")
            current_branch = os.getenv("CHANGE_BRANCH")
        else:
            target_branch = os.getenv("BRANCH_NAME")
            current_branch = target_branch
    elif os.getenv("GITHUB_ACTIONS", None) is not None:
        ci_system = CISystem.GITHUB_ACTIONS
    return CIContext(
        ci_system=cis_system,
        is_pull_request=is_pull_request,
        target_branch=target_branch,
        current_branch=current_branch,
    )
```

### Implement the rest of the requirements

We can continue implementing the rest of the requirements in the same way, writing tests and fixing them by implementing the `detect_ci_context` method.

```{code-block} python
def detect_ci_context() -> CIContext:
    ci_system = CISystem.UNKNOWN
    is_pull_request = False
    target_branch = None
    current_branch = None
    if os.getenv("JENKINS_HOME", None) is not None:
        ci_system = CISystem.JENKINS
        is_pull_request = os.getenv("CHANGE_ID", None) is not None
        if is_pull_request:
            target_branch = os.getenv("CHANGE_TARGET")
            current_branch = os.getenv("CHANGE_BRANCH")
        else:
            target_branch = os.getenv("BRANCH_NAME")
            current_branch = target_branch
    elif os.getenv("GITHUB_ACTIONS", None) is not None:
        ci_system = CISystem.GITHUB_ACTIONS
        is_pull_request = os.getenv("GITHUB_EVENT_NAME", None) == "pull_request"
        if is_pull_request:
            target_branch = os.getenv("GITHUB_BASE_REF")
            current_branch = os.getenv("GITHUB_HEAD_REF")
        else:
            current_branch = os.getenv("GITHUB_REF_NAME")
            target_branch = current_branch
    return CIContext(
        ci_system=ci_system,
        is_pull_request=is_pull_request,
        target_branch=target_branch,
        current_branch=current_branch,
    )
```

## Refactor

Is obvious that the `detect_ci_context` code smells. It does too many things and is not extensible.
Every time we add a new CI system, we need to modify this method. This is a violation of the [Open/Closed Principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle).

This translates to a new non-functional requirement: _Support more CI systems without modifying the `detect_ci_context` method._

To do this, "abstraction is the key". We can create a new class that will be responsible for detecting the CI system.

```{code-block} python
class CIDetector(ABC):
    @abstractmethod
    def detect(self) -> Optional[CIContext]:
        pass
```

We can now create a detector for every CI system and the `detect_ci_context` method will only iterate over the detectors and return the first result.

```{code-block} python
def detect_ci_context() -> CIContext:
    detectors = [
        JenkinsDetector(),
        GitHubActionsDetector(),
    ]
    for detector in detectors:
        ci_context = detector.detect()
        if ci_context is not None:
            return ci_context
    return CIContext(
        ci_system=CISystem.UNKNOWN,
        is_pull_request=False,
        target_branch=None,
        current_branch=None,
    )
```

Hmm, we still have to modify the `detect_ci_context` method every time we add a new CI system detector 😧 and the new value in the `CISystem` enumeration.

One solution could be to `link` the `CISystem` enumeration with the `CIDetector` class.

```{code-block} python
class CISystem(Enum):
    UNKNOWN = (auto(), None)  # Special case for unknown
    JENKINS = (auto(), JenkinsDetector)
    # Add new CI systems here:  MY_CI = (auto(), MyCIDetector)

    def __init__(self, _: Any, detector_class: Optional[Type[CIDetector]]):
        self._value_ = _  # Use auto() value, but ignore it in __init__
        self.detector_class = detector_class

    def get_detector(self) -> Optional[CIDetector]:
        return self.detector_class() if self.detector_class else None
```

Some of you might be surprised to see that one can add extra arguments to an enumeration member.

What we've done is to add a `detector_class` attribute to each enumeration member to link it with the detector class. This way, we can create a detector for each CI system and the `detect_ci_context` method will only iterate over the detectors and return the first result.

```{code-block} python
def detect_ci_context() -> CIContext:
    ci_context: Optional[CIContext] = None
    for ci_system in CISystem:
        detector = ci_system.get_detector()
        if detector:
            ci_context = detector.detect()
            if ci_context:
                break  # Stop at the first detected CI
    # If no CI system was detected, return unknown CIContext
    else:
        ci_context = CIContext(
            ci_system=CISystem.UNKNOWN,
            is_pull_request=False,
            target_branch=None,
            current_branch=None,
        )
    return ci_context
```

Now, to add a new CI system, we only need to create the new detector class and add the enumeration member. 😎

## Conclusion

In this blog post, we explored how to implement the [Detect CI Context](https://maxiniuc.com/coding_dojo_ci_context/presentation.html) coding example using Python.

We've learned how to:

- incrementally implement the solution using TDD, refactoring, and design patterns.
- learned how to use the Unittest `patch` method to manipulate the environment variables.
- learned how to add extra arguments to an enumeration.

I hope you enjoyed this coding dojo and learned something new.

Happy coding! ⌨️

## References

- [Detect CI Context Presentation](https://maxiniuc.com/coding_dojo_ci_context/presentation.html)
- [Source Code](https://github.com/cuinixam/HelloPython/blob/main/src/hello_python/ci_context.py)
