---
tags: c, gtest, pointer, portability
category: learning
date: 2025-09-24
title: Why unit tests crashed on windows but worked on the microcontroller
---

# Why unit tests crashed on windows but worked on the microcontroller

When writing cross-platform code, it’s easy to forget that **pointers don’t always have the same size**.
This caused a segmentation fault in one of our unit tests.

## What happened

On the Aurix MCU, pointers are 32-bit.
In the code a pointer (memory address) was stored in a `uint32_t` variable.
That worked fine on the target.

But, when running the unit tests on the PC (Windows with GCC), pointers are **64-bit**.
Storing a 64-bit pointer into a 32-bit integer truncated the address.
The compiler only issued a warning and still compiled.

Later, when the truncated value was cast back to a pointer and dereferenced, it pointed to invalid memory and crashed with a **segmentation fault**.

## How to fix it and make the code portable

* 🚫 Never store a pointer in a fixed-width integer type (`uint32_t`, `uint64_t`, ...).
* ✅ Always use `uintptr_t` from `<stdint.h>` because it is guaranteed to be wide enough for a pointer on the current platform.


## Wrong vs Right

```{code-block} c
#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>

int main(void) {
    int value = 42;
    int *ptr = &value;

    // ❌ Wrong: pointer stored in fixed 32-bit type
    uint32_t wrong = (uint32_t)ptr;   // Works on 32-bit MCU, truncates on 64-bit host
    int *bad = (int *)wrong;          // may segfault
    printf("wrong addr = 0x%08" PRIx32 "\n", wrong);

    // ✅ Right: use uintptr_t (pointer-sized integer type)
    uintptr_t right = (uintptr_t)ptr;
    int *good = (int *)right;
    printf("right addr = 0x%" PRIxPTR ", *good = %d\n", right, *good);

    return 0;
}
```

Both `PRIx32` and `PRIxPTR` come from `<inttypes.h>`.
They expand to the correct `printf` format string for the given integer type:

* `PRIx32` - prints a 32-bit integer in hex.
* `PRIxPTR` - prints a `uintptr_t` (pointer-sized integer) in hex.

This ensures portable and correct logging across platforms.


## Final thought

Using `uintptr_t` instead of `uint32_t` to store pointers makes the code portable when running unit tests on a 64-bit host.
