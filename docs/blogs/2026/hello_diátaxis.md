---
tags: technical documentation, diátaxis, ai, docs, sphinx
category: learning
date: 2026-01-25
title: Hello Diátaxis
---

# Hello [Diátaxis](https://diataxis.fr/start-here/)

As a software engineer, I tend to treat user documentation as something to be written late in the development when I think that someone might use my software.
I could improve this klingonian approach, but not today.

Anyway, this weekend I decided to spend 10 minutes and request my apprentice (aka AI Agent) to refactor the documentation I wrote for one of my python application.
I already had some documentation, but this was ... well, let's say not the best ;)

So I need to tell my apprentice what I want, but writing prompts takes also time, so I wrote a prompt to write me a prompt.

This was my request:

```
I have a python application and want to write the documentation
and publish it to readthedocs.
Please create a prompt for an ai agent to parse the code,
existing documentation and generate the documentation.
Look for best practices for writing documentation and include them in the prompt.
Remember that less is more.
```

In seconds I got this prompt:

```
The AI Agent Prompt

Role: You are an expert Technical Writer specializing in Python
and the Diátaxis framework.

Objective: Parse the provided codebase and existing notes to generate
a comprehensive documentation suite optimized for Read the Docs (MkDocs or Sphinx).

Guidelines:

- Clarity over Volume: Use the "less is more" principle. Avoid fluff; prioritize "Time to First Hello World."
- Standards: Ensure all docstrings follow PEP 257 (Google or NumPy style).
- Structure (Diátaxis): Organize content into four distinct categories:
  - Tutorials: Learning-oriented (Step-by-step for beginners).
  - How-to Guides: Problem-oriented (Solving specific tasks).
  - Reference: Information-oriented (API technical descriptions).
  - Explanation: Understanding-oriented (Concepts and architecture).

Task Requirements:

- README.md: Create a high-level overview including installation, a 5-line "Quick Start" code block, and links to the full docs.
- API Reference: Automatically generate documentation for all public classes and functions based on code logic and docstrings.
- Requirement File: Ensure requirements.txt or pyproject.toml is correctly reflected in the setup instructions.
- Configuration: Generate a basic .readthedocs.yaml and mkdocs.yml (or conf.py) file to ensure seamless deployment.

Output Format: Provide the documentation in Markdown (for MkDocs) or reStructuredText (for Sphinx).
```

Like a good master I am ;), I actually checked the prompt my apprentice wrote and immediately stopped at the `Diátaxis framework`.

At this point I was like, why does my apprentice invent words and frameworks again? :)

In the end, what should have been a 10 minutes task to let my apprentice generate the documentation and then me to review and approve it,
took me over one hour to understand what [Diátaxis](https://diataxis.fr/start-here/) is and why didn't I know about it before. :)

I had to adapt the prompt slightly for my project setup (Sphinx, Myst Parser, etc.).
The Sphinx theme and layout remained untouched but the chapters changed completely.
Here is the refactored documentation: [pypeline-runner.readthedocs.io](https://pypeline-runner.readthedocs.io/en/latest/).

I think I will use this "framework" for my future documentation projects and of course create an agentic [SKILL](https://agentskills.io/specification) to do this for me. ;)

Have fun and happy documenting!
