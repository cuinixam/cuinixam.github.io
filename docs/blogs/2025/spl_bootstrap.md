---
tags: python, bootstrap, venv
category: review
date: 2025-11-24
title: SPL Bootstrap - Handle Python Version
---

## SPL Bootstrap - Handle Python Version

### Introduction

The pipeline implementation for our Software Product Line (SPL) repositories uses the [pypeline](https://github.com/cuinixam/pypeline) Python application.
In order to start the `pypeline` application, we need to install Python (with a specified version) and create the Python virtual environment.
This step we call `bootstrap` and it is implemented [here](https://github.com/avengineers/bootstrap).

```{note}
Currently bootstrap supports only Windows for installing Python.
```

### Workflow

The bootstrap process is managed by two main scripts: a PowerShell script (`bootstrap.ps1`) for environment setup and a Python script (`bootstrap.py`) for dependency management. The diagram below shows the high-level workflow.

```{mermaid}
flowchart TD
    A[bootstrap.ps1] --> B{Python installed?};
    B -- No --> C[Install Python w/ Scoop 1️⃣];
    B -- Yes --> D;
    C --> D[Execute bootstrap.py];

    D --> E{Dependencies changed?};
    E -- No --> F[End];
    E -- Yes --> G[Create/Update .venv 2️⃣];
    G --> H[Install Dependencies];
    H --> F;
```

1. This step will first install the `scoop` windows package manager and then call `scoop` to install the configured python version.
2. The python virtual environment is updated in multiple steps:
    - create an empty virtual environment with python `venv.create`
    - install the package manager (e.g., poetry, uv, etc.) and `pip-system-certs` for using the system SSL certificates
    - run the package manager to install the python dependencies

#### bootstrap.ps1

- Scoop configuration and installation
- Python version detection and installation
- Delegates to `bootstrap.py` for virtual environment setup

#### bootstrap.py

- OS-agnostic virtual environment creation (Windows/Unix)
- Smart caching with hash-based dependency tracking. Only runs if dependencies have been updated.
- Package manager support: Poetry, UV, Pipenv
- Automatic pip configuration for custom PyPI sources

#### bootstrap.json Configuration

```json
{
    "python_version": "3.11",
    "python_package_manager": "poetry>=2.1.0",
    "scoop_ignore_scoopfile": true
}
```

### Things to Improve

#### Python Version Management

Currently the bootstrap process installs a fixed Python version as specified in the `bootstrap.json` configuration file.
When checking if python is installed, it only verifies that the major and minor version match (e.g., `3.11`),
but does not check for patch versions (e.g., `3.11.4` vs `3.11.5`).
This can lead to situations that on different machines, slightly different patch versions of Python are installed.

```{note}
This might not be a big issue in most cases, but it can lead to inconsistencies in our particular case,
because we use the python `venv` module to create the initial virtual environment,
which will include the standard library of the installed Python version.
```

The solution could be:

- to find all installed python versions in path and check if the exact version is already installed
- it might be that python versions installed with scoop are not available in path, so we need to query scoop for installed versions
- if the exact version is not installed, install it with scoop
- the `bootstrap.py` shall fail if the python interpreter version does not match exactly the configured version.
  This can happen if the user runs the `pypeline` including the `CreateVEnv` step which calls directly the `bootstrap.py` script.

#### Virtual Environment Management

As mention above, the virtual environment is created in three steps:

1. create an empty virtual environment with python `venv.create`
1. install the package manager (e.g., poetry, uv, etc.) and `pip-system-certs` for using the system SSL certificates
1. run the package manager to install the python dependencies

There is a problem with the second step: the package manager and pip-system certs are installed with pip.
These packages have their own dependencies, which are not tracked by pip because pip has no support for `.lock` files.

When step three is executed, the package manager might need to upgrade/downgrade some packages which were implicitly installed in step two
and this can cause crashes due to dependency conflicts.

#### Solution 1: User-defined Initial Packages

One way to solve this is to let the user define the list of package to install in step two in the `bootstrap.json` configuration file.
For example:

```{code-block} json
{
    "python_version": "3.11.4",
    "venv_initial_packages": [
        "poetry==2.1.0",
        "pip-system-certs==2.2.1",
        "wrapt==1.14.0"
    ],
}
```

In case there is a conflict between the initial packages and the packages defined in the package manager lock file,
the user can adjust the versions in the configuration file accordingly.

#### Solution 2: Install Package Manager with Scoop

Another way could be to install both python and the package manager with scoop in the `bootstrap.ps1` script,
so that pip is not involved at all in step two. This means that package manager will install exactly the version specified in the `.lock` file
and therefore always have a consistent set of dependencies.

The problem with this approach is that `pip-system-certs` is not available as a scoop package
and package installation will fail when ran against an on-premise PyPI server with self-signed certificates.

#### Package manager command

Currently the command to install dependencies with the package manager is hardcoded in the `bootstrap.py` script
with extra arguments being supported via the `bootstrap.json` configuration file.

```{code-block} json
{
    "python_package_manager_args": "--clean"
}
```

We added the feature to support extra arguments because we needed for some projects to pass the `--clean` to `pipenv`
to remove unused packages already existing in the virtual environment.

A better approach would be to let the user define the full command to install dependencies with the package manager.
For example:

```{code-block} json
{
    "venv_install_command": "poetry install --no-dev --clean"
}
```

This would give the user full control over how dependencies are installed.

## Conclusion

If all these improvements are implemented, the bootstrap process will be more reliable and flexible, ensuring consistent Python environments.

The configuration will allow users to tailor the bootstrap process to their specific needs.

```{code-block} json
{
    "python_version": "3.11.4",
    "venv_initial_packages": [
        "poetry==2.1.0",
        "pip-system-certs==2.2.1"
    ],
    "venv_install_command": "poetry install --no-dev --clean"
}
```

This configuration will ensure that:

- Python 3.11.4 is installed
- The package manager and pip-system-certs are installed with the specified versions
- Dependencies are installed with the specified command

Have fun bootstrapping! ✌️
