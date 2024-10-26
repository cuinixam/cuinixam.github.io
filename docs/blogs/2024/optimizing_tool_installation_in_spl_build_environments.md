---
tags:
category: spl, yanga, build, optimization, tool, dependency
date: 2024-10-26
title: Optimizing Tool Installation in SPL Build Environments
---

# Optimizing Tool Installation in SPL Build Environments

I assume that the reader is familiar with the concept of software product lines (SPLs) and build environments. If not, as this is a blog post about optimizing tool installation in SPL build environments, I recommend you read up on these topics first.

## Introduction

In software product line (SPL) engineering, efficiently managing tool dependencies is essential for optimizing build environments and enhancing developer productivity. This blog post explores the thought process in addressing the challenge of optimizing tool installations in an SPL. We'll walk through the problem statement, initial ideas, the evolution of those ideas, and the final approach.

## The Problem: Inefficient Tool Installation

In our SPL build environments, all tools are being installed regardless of the specific needs of a developer or build target. This was not noticeable initially, but as the number of variants and use cases (e.g. different packaging formats, on target debugging, etc.) increased, the inefficiency became apparent.

Basically, there is an `install` step at the beginning of the build pipeline that installs all the tools required by all variants and all possible build targets.

Some use cases where this inefficiency is particularly noticeable include:

- A developer working on a specific variant needs only a subset of tools.
- A CI pipeline for running static analysis (e.g. Mathworks Polyspace) does not need to build or package the software.

The problem is more noticeable for developers spinning up a virtual machine (VM) to quickly test a change or for a developer setting up their environment for the first time.

On the other hand, when releasing a product, it is essential to ensure that all tools are available because we have to make sure that all variants are passing the defined quality gates.

## Brainstorming

### 💡 Categorizing Tools into Generic, Variant, and Build Target Sets

Let us categorize tools into three distinct sets:

1. **Generic Tools**: Tools required by all variants and build targets (e.g., CMake, Python).
2. **Variant-Specific Tools**: Tools required only for certain variants (e.g., specific compilers for microcontrollers).
3. **Build Target-Specific Tools**: Tools required for specific build targets (e.g., static analysis tools like Polyspace).

**Implementation Concept**

- **Separate Tool Dependency Files**:
  - **Generic Tool Dependencies File**: Contains tools common to all variants.
  - **Variant-Specific Tool Dependencies Files**: Contains tools specific to a variant or overrides for generic tools.
- **Merging Process**:
  - When building a variant, merge the generic and variant-specific tool files, with the variant-specific tools overriding any conflicts.
- **Handling Build Target-Specific Tools**:
  - Dynamically add tools based on the selected build target.

This means that the `install` step in the pipeline will install only the tools required for the specific variant and build target.

**Considerations**

While this idea provides a structured approach to managing tool dependencies, there are some challenges/limitations to consider:

- **Complexity in Linking Tools to Build Targets**: Tightly coupling tools to build targets might limit flexibility for other activities that require specific tools, such as generating reports or on-target debugging.
- **Aggregation of Tools for CI**: Collecting all tools from generic, variant, and build target files for CI builds might introduce complexity in managing tool versions and resolving conflicts.

### 💡 Introducing "Scopes" as an Abstraction Layer

One issue with the previous idea is the tight coupling of tools to build targets. The problem is that, in contrast to `variant`, a `build target` is not a domain term in SPL engineering. It is a technical term from the build system. This tight coupling might lead to confusion and make the system less flexible.

To address this limitation, we proposed introducing `scopes` as a higher-level abstraction.

```{admonition} Scopes
Scopes encompass a specific activity or domain within the development process, representing a set of tools, configurations and steps required for that activity.

Examples of scopes may include: `Build`, `StaticAnalysis`, `Debugging`, `Reporting`, and `Deployment`.
```

**Implementation Concept**

- **Scope-Specific Configuration Files**:
  - Each scope has its own configuration that lists the tools required for that scope.
  - It might also need to specify also what has to be done, which steps have to be executed.
- **Merging Tool Dependencies**:
  - **Hierarchy**: Generic tools < Variant Build Tools < Scope-specific tools.
  - When building, the script merges tools from these files, with later ones overriding earlier ones in case of conflicts.
  - There shall no be no variant specific tools anymore other than the toolchain for building the software.

**Considerations**

- **Complexity in Managing Scopes**: Managing a growing number of scopes might become complex.
- **User Awareness**: Developers need to understand which scopes are relevant for their tasks.
  - How are scopes related to build targets?

### 💡 Keep current solution and speed up installation of all tools

Another idea was to keep the current solution but speed up the installation process. This could be achieved by:

- CI jobs to install all tools on all agents
- Disable automatic installation of tools on developer machines. The developer can then install the required tools manually.

This idea is the least intrusive and requires the least amount of changes. However, it does not address the root cause of the problem. It is more of a workaround. 🙈

## Final Approach: Introducing Scopes

Introducing "scopes" as an abstraction layer offers a more flexible and domain-aligned solution for optimizing tool installation in an SPL build environment.

Scopes align with the development process, makes it easier for developers and platform engineers to understand and manage not only tool dependencies but also the steps required for a specific activity.

The final approach involves:

1. **Defining Scopes**: Identify and define scopes that represent activities or domains within the development process.
2. **Scope-Specific Configuration Files**: Create configuration files for each scope that list the tools required for that scope.
3. **Merging Tool Dependencies**: Merge tools from generic, variant build, and scope-specific files, with later ones overriding earlier ones in case of conflicts.
4. **Implementing Scope-Specific Steps**: Define and implement steps for each scope that specify what has to be done, which tools have to be installed, and which steps have to be executed.

This approach ensures that only the tools required for a specific activity are installed, optimizing the build environment and enhancing developer productivity.

There is one important aspect to consider: in the end one must be able insure a certain quality level for the software product as a whole. This means one needs to:

- define quality gates for the whole product and breaking them down to the individual variants
- map scopes to quality gates for each variant. Different variants might have different quality gates based on their maturity (e.g., prototype, beta, street ready).

The topics of quality gates and maturity levels, although related, deserve a separate blog post and I will not go into detail here.

## Conclusion

I hope this blog post has provided you with insights into the challenges of optimizing tool installation in SPL build environments and the thought process in addressing this challenge.

There will for sure be more questions to answer when actually implementing the solution but until then, keep fingers crossed and stay tuned for more updates on this topic.
