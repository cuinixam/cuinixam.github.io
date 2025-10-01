---
tags: spl, yanga, spled, arduino, windows
category: learning
date: 2025-10-03
title: SPLED meets Arduino Uno
---

# SPLED meets Arduino Uno

For our Software Product Line Engineering (SPLE) training we use the [SPLED](https://github.com/avengineers/SPLed) repository,
which is a simple software product line for controlling an LED with different variants:

- Disco: the LED blinks and one can change the blinking frequency
- Sleep: the LED has a constant color and one can change the brightness
- Spa: the LED brigthness pulsates and can either have one color or cycle through different colors

The current implementation creates an executable which can be run in the terminal and uses ANSI escape codes to change the color of the text.

What I want to do is to port this example to an Arduino Uno, so that we can control an RGB LED with it.

I will not use the CMake build environment based on the [spl-core](https://github.com/avengineers/spl-core) CMake modules,
but instead use [YANGA](https://github.com/cuinixam/yanga) which is a software product line build environment written in Python.
YANGA uses `.yaml` configuration files and generates the CMake files for the actual build.

Although YANGA is platform independent, SPLED tools dependencies are only defined as [scoop](https://scoop.sh/) packages for Windows.
I am using a Windows 11 machine for this hacking session.

## Get the code

I forked SPLED and created the YANGA configuration files to build the different variants as with the original spl-core environment.

Clone the repository and setup the virtual environment to be able to run yanga:

```{code} powershell
git clone --branch arduino_platform --single-branch https://github.com/cuinixam/SPLed C:\temp\spled
cd C:\temp\spled
.\build.ps1 -install
```

We can check the SPL configuration with:

```{code} powershell
.\yanga.ps1 run --print
```

This should print the variants, components and supported platforms:

```
PS C:\temp\spled> .\yanga.ps1 run --print
START    | Starting run
INFO     | -----------------------------------------
INFO     | Project directory: C:\temp\spled
INFO     | Parsed 6 configuration file(s).
INFO     | Found 20 component(s).
INFO     | Found 5 variant(s):
INFO     |   - BlinkLed
INFO     |   - Base/Dev
INFO     |   - Disco
INFO     |   - Sleep
INFO     |   - Spa
INFO     | Found 4 platforms(s):
INFO     |   - win_exe
INFO     |   - gtest
INFO     |   - arduino_nano
INFO     |   - arduino_uno_r3
INFO     | Found pipeline config:
INFO     |     Group: install
INFO     |         CreateVEnv
INFO     |         ScoopInstall
INFO     |         WestInstall
INFO     |         GenerateEnvSetupScript
INFO     |     Group: gen
INFO     |         KConfigGen
INFO     |     Group: build
INFO     |         GenerateBuildSystemFiles
INFO     |         ExecuteBuild
INFO     | -----------------------------------------
STOP     | Finished run in 0.05s
PS C:\temp\spled>
```

Our focus will be to build the `Spa` variant for the `arduino_uno_r3` platform.

### Build the Spa variant for Arduino Uno R3

In order to build the Spa variant for the Arduino platform we have to make sure that the Windows executable (`win_exe` platform) specific components are not included when building for Arduino.
YANGA supports variant and platform specific components, so we can define that some components are only included for the `win_exe` platform.

```{code-block} yaml
- name: Spa
  description: The LED brigthness pulsates and can cycle through different colors
  components:
  - rte
  - spled
  - power_signal_processing
  - light_controller
  - power_button
  - main_control_knob
  - brightness_controller
  features_selection_file: variants/Spa/config.txt
  platforms:
    win_exe:
      components: 
      # Windows main
      - main
      # Simulates a period task using `usleep`
      - os
      # Prints to console using ANSI escape codes
      - console_interface
      # Reads key presses to detect `power on/off` and `up/down`
      - keyboard_interface
```

```{note}
The variant platform specific components should be used to defined components which are relevant for this specific variant when built for the given platform.
`main` and `os` components are needed actually by all variants when built for `win_exe`, so placing them in the variant platform specific section is not ideal.

For this, YANGA supports platform specific components at the platform level, which would be a better place to define these components.
```

```{code-block} yaml
