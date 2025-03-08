## Coding Dojo

Detect CI Context

---

## Objective 1

Detect whether your program runs on Jenkins or locally and determine the CI context based on the environment variables. <!-- .element: class="monospace" -->

---

## Expected Output Information

- The CI system name (e.g. Jenkins or Unknown).<!-- .element: class="fragment monospace" -->
- Is the build trigger a Pull Request. <!-- .element: class="fragment monospace" -->
- Name of the target branch (branch to merge into). <!-- .element: class="fragment monospace" -->
- Name of the current branch being built or tested. <!-- .element: class="fragment monospace" -->

---

## Jenkins Environment Variables

- Presence of JENKINS_HOME indicates Jenkins.<!-- .element: class="fragment monospace" -->
- If running a pull request (CHANGE_ID), CHANGE_TARGET is the target branch and CHANGE_BRANCH is the current branch.<!-- .element: class="fragment monospace" -->
- If not a pull request, BRANCH_NAME is the current branch.<!-- .element: class="fragment monospace" -->

---

## Schedule

- 5 minutes to discuss the problem and ask questions.<!-- .element: class="monospace" -->
- 30 minutes to implement the solution.<!-- .element: class="monospace" -->
- 10 minutes to discuss the solution.<!-- .element: class="monospace" -->

---

## Happy Coding! ⌨️

_30 minutes_

--

## Define API

```python
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

--

## Define API

```python
def detect_ci_context() -> CIContext:
    pass
```

--

## Test Cases

```python
@pytest.fixture
def mock_on_getenv():
    with patch("os.getenv") as mock_os_getenv:
        yield mock_os_getenv
```

--

## Test Cases

```python
def test_jenkins_branch_push(mock_on_getenv: MagicMock) -> None:
    # Setup
    mock_on_getenv.side_effect = lambda var, default=None: {
        "JENKINS_HOME": "/jenkins/home",
        "BRANCH_NAME": "main",
    }.get(var, default)
    # Run
    ci_context = detect_ci_context()
    # Check
    assert ci_context.name == "JENKINS"
    assert ci_context.is_pull_request is False
    assert ci_context.target_branch == "main"
    assert ci_context.current_branch == "main"
```

---

## Objective 2

Your program should be able to also detect the CI context when running on GitHub Actions. <!-- .element: class="monospace" -->

---

## GitHub Actions Environment Variables

- GITHUB_ACTIONS indicates GitHub Actions.<!-- .element: class="fragment monospace" -->
- If running a pull request (GITHUB_EVENT_NAME is "pull_request"), GITHUB_BASE_REF is the target branch and GITHUB_HEAD_REF is the current branch.<!-- .element: class="fragment monospace" -->
- If not a pull request, GITHUB_REF_NAME is the current branch.<!-- .element: class="fragment monospace" -->

---

## Happy Coding! ⌨️

_15 minutes_
