---
tags: smart home, matter, thread, zephyr, esp32, esp-idf, espressif, clanguru
category: learning
date: 2026-01-25
title: Smarty - Matter on ESP32 with Zephyr - Part 2
---

# Smarty - Matter on ESP32 with Zephyr - Part 2


```{admonition} Disclaimer
:class: dropdown, warning

I am an engineer who knows his sh*t and prioritizes learning and innovation to getting certifications for tinkering with hardware. To follow along with the hardware portions of this guide, you should either:

- Be an engineer who also knows their sh*t.
- Accept that you are responsible for your own components and safety.
- Or just sit back and enjoy the read.

Reading is still learning, and you are more than welcome to just follow the code without touching a single wire. However, if you do decide to dive into the hardware and things go sideways, whether it's a fried ESP32, a tripped breaker, or a "spicy" encounter with mains power, I am not to be held accountable. I take no responsibility for your hardware, your home, or yourself. You are the captain of your own (hopefully well-insulated) ship.
```

In the [previous part](smarty_p1.md) we built the `Hello World` Zephyr sample project and analyzed the build environment, dependencies and generated artifacts.

Now I will setup a [yanga](https://github.com/cuinixam/yanga) project to build the same example. The goal is to configure in `yanga`:

- the two external dependencies `zephyr` and `hal_espressif`
- the toolchain `riscv64-zephyr-elf`
- the platform `esp32h2_devkitm`
- a `hello_world` component

One shall be able to clone the repository and build it using `yanga` on both Ubuntu and Windows by running a single command.
No extra steps to install toolchains or other dependencies.


## PART 2: Hello World on ESP32-H2 with Yanga

I followed the [yanga getting started guide](https://yanga.readthedocs.io/en/latest/getting_started/hello_yanga.html) to setup my project. This project has two variants, `English` and `German`, which greet the user in their language (e.g. "Hello World" or "Hallo Welt").

I pushed the code to github [cuinixam/smarty](https://github.com/cuinixam/smarty).

Next steps are to add a new [platform](https://yanga.readthedocs.io/en/latest/features/platform.html) for ESP32-H2 and Zephyr.

The new platform `esp32h2-zephyr` will:

- use the `riscv64-zephyr-elf` toolchain
- define two dependencies: `zephyr` and `hal_espressif`

To be continued...
