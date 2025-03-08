---
tags: spl git post-build cmake
category: learning
date: 2024-10-01
title: Efficiently Embedding Git Information in C Projects
---

# Efficiently Embedding Git Information in C Projects

## Introduction

In software development, embedding Git metadata (like commit IDs, branches, and tags) into your binaries is useful for debugging and traceability. However, how you integrate this information can significantly impact your build times and workflow efficiency. This post explores the challenges of embedding Git information in C projects using CMake and proposes an optimized solution.

## Current Approaches

### Project One: Command-Line Defines

In the first project, Git information is passed directly as compiler command-line arguments using `add_compile_options` in CMake:

```{code-block} cmake
add_compile_options(
    -DGIT_CUR_COMMIT=\"${GIT_CUR_COMMIT}\"
    -DGIT_CUR_USER=\"${GIT_CUR_USER}\"
)
```

These defines are then used in the codebase to embed Git metadata:

```{code-block} c
const uint8 git_commit[] = GIT_CUR_COMMIT;
```

**Advantages**

- Simplicity: Easy to implement and understand.
- Direct Integration: Git information is directly available in the code via macros.

**Disadvantages**

- Inefficient Builds: Any change in the command-line arguments (e.g., a new commit ID) invalidates the build cache, forcing a full recompilation.
- Poor Incremental Build Support: Full builds slow down development, especially in large product with multiple variants.
- Inconsistent Updates: The file generation relies on the CMake configure step, which may not run if no CMake files have changed.

### Project Two: Generated Source File

The second project generates a C source file during the CMake configuration step:

```{code-block} cmake
set(GIT_INFO_TEMPLATE ${CMAKE_SOURCE_DIR}/src/git_info.c.in)
set(GIT_INFO_FILE_OUT ${CMAKE_BINARY_DIR}/Src/git_info.c)

add_custom_target(version_info COMMAND ${CMAKE_COMMAND}
    -DUPDATE_VERSION_INFORMATION_REQUESTED=1
    -DVERSION_INFORMATION_FILE=${GIT_INFO_TEMPLATE}
    -DVERSION_INFORMATION_FILE_OUT=${GIT_INFO_FILE_OUT}
    -DGIT_VARIANT=${VARIANT}
    -P ${CMAKE_SOURCE_DIR}/src/gitinfo.cmake
    BYPRODUCTS ${GIT_INFO_FILE_OUT}
)

spl_add_source(${GIT_INFO_FILE_OUT})
spl_create_component()
```

**Advantages**

- Selective Compilation: Only the generated file re-compiles when Git information changes.
- Improved Build Times: Reduces the need for full recompilations.

**Disadvantages**

- Inefficient Builds: The generated file is recompiled every time, even if the Git information hasn't changed.
- Complexity: Adds extra steps and dependencies in the build process.

## Proposed Solution: Embedding Git Information in the Binary

To overcome the problems of current methods, we propose embedding Git information directly into the binary (using Intel-HEX format) after the build process. This approach eliminates unnecessary recompilation and simplifies the build process by embedding Git metadata in a dedicated memory section.

### Create the git information source files

We need to have:

- global constants for the Git information
- compiler directives to place the constants in a specific memory section

_git_info.c_

```{code-block} c

#include "git_info.h"

#define GITINFO_START_SEC_CONST
#include "git_info_mem_map.h"

const unsigned char git_commit[GIT_COMMIT_LENGTH] = "0123456701234567";

#define GITINFO_STOP_SEC_CONST
#include "git_info_mem_map.h"

```

```{important}
The `git_info.c` file contains dummy Git information and is used only for a placeholder. The actual Git information will be updated after the build process.
```

_git_info_mem_map.h_

```{code-block} c

#if defined( GITINFO_START_SEC_CONST )
#pragma protect
#pragma section nearrom "GitInfoSection"
#pragma section farrom "GitInfoSection"
# undef GITINFO_START_SEC_CONST
# define START_SEC_CODE
#endif

#if defined( GITINFO_STOP_SEC_CONST )
#pragma endprotect
#pragma section nearrom restore
#pragma section farrom restore
# undef GITINFO_STOP_SEC_CONST
# define STOP_SEC_CODE
#endif

```

```{note}
The `GitInfoSection` memory section shall be defined in the linker script.
```

For other modules to access the Git information, we need to define the Git information in a header file:

_git_info.h_

```{code-block} c

#ifndef GIT_INFO_H
#define GIT_INFO_H

#define GIT_COMMIT_LENGTH 16
extern const unsigned char git_commit[GIT_COMMIT_LENGTH];

#endif

```

### Linker Script to Define the Git Information Memory Section

```
/* Start address to store the git information */
#define GITINFO_ADDRESS                         (0xABCD)

section_layout :vtc:linear
{
	group PFLASH0(fill = 0x00)
	{
		group GitInfoSectionGroup (ordered, run_addr=GITINFO_ADDRESS)
		{
			section "GitInfoSectionGroup_SEC" (fill, blocksize = 2, attributes = rx)
			{
					select "[.]rodata.GitInfoSection";
			}
		}
		"_GitInfoSectionGroup_START" = "_lc_gb_GitInfoSectionGroup";
		"_GitInfoSectionGroup_END" = ("_lc_ge_GitInfoSectionGroup" == 0) ? 0 : "_lc_ge_GitInfoSectionGroup" - 1;
		"_GitInfoSectionGroup_LIMIT" = "_lc_ge_GitInfoSectionGroup";
	}
}
```

This linker script defines a memory section `GitInfoSection` at the specified address `GITINFO_ADDRESS` to store the Git information.
The constants defined in `git_info.c` (`rodata`) will be placed in this memory section.

### CMake script to update the Git information

We need to define custom commands to create a `git_info.hex` file containing the Git information.

**Requirements**

- the `git_info.hex` file shall only be generated if the git commit has changed
- the command for checking the git commit shall always run, to make sure the `git_info.hex` file is up-to-date

```{important}
As you might have noticed, we need to **always** run the command for checking the git commit but **only** generate the `git_info.hex` file if the git commit has changed. This is a bit tricky to achieve with CMake, but it is possible.
```

#### Always Generate Git Commit Temporary File

- Purpose: Ensures the Git commit ID is updated every build.
- Mechanism: Uses a fictive output **git_commit_force_update** to force the command to run every time.

```{code-block} cmake
add_custom_command(
    OUTPUT __git_commit_force_update__
    BYPRODUCTS ${GIT_COMMIT_TMP_FILE}
    COMMAND git describe --always --dirty --exclude '*' --abbrev=8 > ${GIT_COMMIT_TMP_FILE}
    COMMENT "Generate the git commit tmp file"
    VERBATIM
)
```

#### Update Git Commit File if Changed

- Purpose: Copies the temporary commit ID file to the final file only if it has changed.
- Mechanism: Uses copy_if_different to avoid unnecessary updates.

```{code-block} cmake
add_custom_command(
    OUTPUT ${GIT_COMMIT_FILE}
    COMMAND ${CMAKE_COMMAND} -E copy_if_different ${GIT_COMMIT_TMP_FILE} ${GIT_COMMIT_FILE}
    COMMENT "Checking and updating git commit ID"
    DEPENDS __git_commit_force_update__ ${GIT_COMMIT_TMP_FILE}
    VERBATIM
)
```

#### Create Git Info Hex File

- Purpose: Converts the Git commit ID into a hex file at the specified address.
- Mechanism: Uses hextool to generate the hex file.

```{code-block} cmake
add_custom_command(
    OUTPUT ${GIT_INFO_HEX_FILE}
    COMMAND hextool create --input-binary ${GIT_COMMIT_FILE} --offset ${GITINFO_ADDRESS} --output ${GIT_INFO_HEX_FILE}
    DEPENDS ${GIT_COMMIT_FILE}
    COMMENT "Creating git info hex file"
    VERBATIM
)
```

```{note}
Please notice the `--input-binary` hextool option to read the git information as binary data directly from the file.
```

### Merge Git Info Hex File with the Binary

- Purpose: Combines the main output hex file with the Git info hex file.
- Output: Produces `link_out_with_git_info.hex` containing the embedded Git commit ID.

```{code-block} cmake
add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/link_out_with_git_info.hex
    COMMAND hextool merge --file ${CMAKE_BINARY_DIR}/link_out.hex --file ${GIT_INFO_HEX_FILE} --output ${CMAKE_BINARY_DIR}/link_out_with_git_info.hex
    COMMENT "Merging git info to the output hex file"
    DEPENDS ${GIT_INFO_HEX_FILE} ${CMAKE_BINARY_DIR}/link_out.hex
    VERBATIM
)
```

### Process Flow Diagram

```{mermaid}
flowchart TD
    A[Start Build] --> B[Generate git_commit_tmp.txt]
    B --> C{Has Commit ID Changed?}
    C -- Yes --> D[Update git_commit.txt]
    C -- No --> E[Skip Update]
    D & E --> F[Create git_info.hex]
    F --> G[Generate link_out.hex]
    G --> H[Merge git_info.hex with link_out.hex]
    H --> I[Produce link_out_with_git_info.hex]
```

### Alternative approach as POST_BUILD command

- Purpose: Merges `git_info.hex` directly into `link_out.hex` as a [POST_BUILD](https://cmake.org/cmake/help/latest/command/add_custom_command.html#examples-build-events) step, overwriting the original file.
- Mechanism:
  - Post-Build Command: Executes after the link target finishes building.
  - Force Relinking: Adds git_info.hex as a dependency to ensure that the linker runs again if the Git info changes.
- Output: The `link_out.hex` file now contains the embedded Git commit ID without creating a new file.

```{code-block} cmake
:linenos:
:emphasize-lines: 7

# Add post-build command to merge the git info to the link_out.hex.
add_custom_command(
    TARGET link
    POST_BUILD
    COMMAND hextool merge --file ${CMAKE_BINARY_DIR}/link_out.hex --file ${GIT_INFO_HEX_FILE} --output ${CMAKE_BINARY_DIR}/link_out.hex
    COMMENT "Merging git info to the output hex file"
    # (!) Adding DEPENDS has no effect on POST_BUILD commands. So next line is useless.
    DEPENDS ${GIT_INFO_HEX_FILE}
    VERBATIM
)

# (!) Force linking again if the git info hex has changed.
# This hack adds the git info hex file as a dependency to the src_git_info target. When the git info hex file changes, the src_git_info target will be considered out of date and will be rebuilt.
set_property(TARGET src_git_info PROPERTY INTERFACE_LINK_DEPENDS ${GIT_INFO_HEX_FILE})
```

```{mermaid}
flowchart TD
    A[Start Build] --> B[Generate git_commit_tmp.txt]
    B --> C{Has Commit ID Changed?}
    C -- Yes --> D[Update git_commit.txt]
    C -- No --> Z[End Build]
    D --> F[Create git_info.hex]
    F --> G{Has git_info.hex Changed?}
    G -- Yes --> H[Link link_out.hex]
    G -- No --> Z
    H --> K[Merging git_info.hex into link_out.hex - Post-Build]
    K --> L[Updated link_out.hex with Git info]
    L --> Z
```

**Advantages**

- Single Output File: Avoids creating an extra hex file; simplifies deployment.
- Always Updated: Ensures `link_out.hex` always contains the latest Git info.

**Disadvantages**

- Forced Relinking: Changes in git_info.hex cause the linker to run again, potentially increasing build times. Note: Only the linking step is rerun; source files are not recompiled.
- Overwriting Output: Original `link_out.hex` is modified, which may not be desirable in all workflows.

## Conclusion

We have explored the challenges of embedding Git information in C projects and proposed an optimized solution using CMake and Intel-HEX format.
This approach ensures that Git metadata is efficiently embedded in the firmware binary without unnecessary recompilations by:

- Extracting the current Git commit ID during each build.
- Updating the commit ID file only when changes occur to avoid unnecessary rebuilds.
- Embedding the commit ID into the hex file at a specific memory address.
- Merging the Git info hex file with the main output using one of the two approaches.

I hope this post is helpful in optimizing your build process.
