---
tags: linker, section, memory, linker scripting language, lsl, gcc, tasking
category: learning
date: 2025-01-07
title: Allocate Code and Data to Specific Memory Sections
---

# Allocate Code and Data to Specific Memory Sections

## Introduction

There was a question in our support channel about the memory sections from an external library.
The colleague was trying to understand how the different sections were defined for the library and how they were placed in memory.
When checking the linker configuration file (`*.lsl`) the observation was that the memory sections for:

- all the objects for our code, the section pattern was `.<type>.<filename>.<symbol>`. For example, `select .text.component.main` or `select .data.component.my_var`.
- the library, the section pattern was `.<type>.<some_name>.<symbol`. For example, `.rodata.adjustable_parameters.my_param`.

The question was: how can we define the sections for the library in the linker script file and if they can use the same pattern as our code?

## Understanding the sections

### Why do we need to define different memory sections?

When integrating code with different safety levels or from external libraries, it is important to separate the memory sections to restrict the access to certain areas of the memory only to specific code.
This safety measure is important to avoid that a bug in one part of the code can corrupt the data of another part of the code.

### How are the sections defined?

The SW architecture describes the logical allocation of the components based on different abstraction levels and safety requirements.
Based on this and the memory map of the micro-controller, the sections are defined in the linker script file.

Here are some section types that are commonly used:

- `.text` - the code section
- `.data` - the initialized data section
- `.bss` - the uninitialized data section
- `.rodata` - the read-only data section

## How does my C code ends up in the sections?

By default, the compiler generates the sections based on the file name and the symbol name.
Let us consider the following code:

```{code-block} c
int my_var = 1;
void my_func(void) {
    my_var++;
}
```

The compiler will generate the following sections:

- `.text.my_file.my_func` - the code of the function `my_func`
- `.data.my_file.my_var` - the initialized data of the variable `my_var`

In the linker script file, we can `select` the sections to be placed in the memory map.

In the memory group where this component _code_ shall be placed, we can refer to it as:

```
select .text.my_file.*
```

This means that all the sections that start with `.text.my_file.` will be placed in this memory group.

## Renaming the sections

Let's say that one has some adjustable parameters which shall be allocated to a specific memory area.

```{code-block} c
const parameters_t my_parameters = {
    .param1 = 1,
    .param2 = 2,
};
```

By default the compiler will generate a section named `.rodata.my_file.my_parameters` for the read-only data of the variable `my_parameters`.

If one wants to give a specific name to this section, one can instruct the compiler to use a specific section name.
Depending on the compiler, there are different ways to do this.

When using the TASKING compiler, there is a special ´#pragma´ to define the section name.

```{code-block} c
#pragma section all "sw_constants" // define the section name
const parameters_t my_parameters = {
    .param1 = 1,
    .param2 = 2,
};
#pragma section restore all // restore the default section name
```

For more information see the TASKING User Guide, section 1.12.1 Rename Sections in the [](References).

When using the GCC compiler, there is a `__attribute__` that can be used to define the section name.

```{code-block} c
const parameters_t my_parameters __attribute__((section("sw_constants"))) = {
    .param1 = 1,
    .param2 = 2,
};
```

See more about the `__attribute__` in the [GCC documentation](https://gcc.gnu.org/onlinedocs/gcc/Common-Variable-Attributes.html#index-section-variable-attribute).

## Answering the question(s)

The linker configuration file (`*.lsl`) is used to define the memory layout, collect and group memory sections from objects and libraries.
The compiler generates the sections based on the file name and the symbol name and type. The user can rename the sections using compiler specific directives.

The memory sections defined for the objects inside the library have a different pattern because there were renamed using the compiler specific directives (`pragma` or `__attribute__ section`).
One can not change the section names after the compilation and therefore must rely on naming conventions to know which sections are present in the library.

(References)=

## References

- [TASKING User Guide](https://resources.tasking.com/sites/default/files/uberflip_docs/file_254.pdf)
- [GCC to TASKING Migration](https://resources.tasking.com/sites/default/files/uberflip_docs/file_847.pdf)
- [GCC documentation](https://gcc.gnu.org/onlinedocs/gcc/Common-Variable-Attributes.html#index-section-variable-attribute)
- [AUTOSAR Memory Mapping](https://www.autosar.org/fileadmin/standards/R24-11/CP/AUTOSAR_CP_SWS_MemoryMapping.pdf)
