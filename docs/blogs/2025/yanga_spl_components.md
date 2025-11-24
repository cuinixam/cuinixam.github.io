---
tags: spl, yanga, variant, component
category: design
date: 2025-10-15
title: SPL components in YANGA
---

# SPL components in [YANGA](https://github.com/cuinixam/yanga)

When building *software products*, you often need different *variants* for different purposes (like a basic vs. a pro version).
These variants consist of *components* that implement the features required for that particular variant.
Each variant might be built for different *platforms*, different hardware environments with their own constraints and capabilities.

When thinking about components, there are two main categories:

- Components which implement your product's features
- Components which provide the functionality for other components to run on a certain hardware platform

Sometimes you might hear these referred to as the application layer and drivers or low-level layer.

It seems natural to have two separate places to configure these components:

- One place for components that define what your product does
- Another place for components that every product needs when targeting a specific platform

Indeed in YANGA, one can configure variant components and platform components.

Example for a variant configuration:

```{code-block} yaml
variants:
- name: Spa
  description: The LED brightness pulsates and cycles through different colors
  components:
  - light_controller           # Light control algorithms
  - power_button               # Power button handling
  # ... and other core features
```

Example for a platform configuration:

```{code-block} yaml
platforms:
  - name: arduino_uno
    components:
      - arduino_core
      - digital_pins
    toolchain_file: arduino.cmake
```

I happen to find a third use case that doesn't fit neatly into either of these two categories: components that only some product variants need, and only on specific platforms.

I had a component that it only worked for Arduino, but I used it only for one of the four variants I was building. It didn't make sense to put it in the platform configuration, because not every product variant needed it. But it also didn't make sense to put it in the variant configuration, because it was platform specific.

## Three Places for Components

YANGA gives you three places to define components:

### 1. In Your Product Variant

For components that define what your product does, regardless of platform.

```{code-block} yaml
variants:
  - name: WeatherStation
    components:
      - sensor_reader
      - data_logger
      - weather_predictor
```

### 2. In Your Platform Configuration

For components that every product needs when targeting this platform.

```{code-block} yaml
platforms:
  - name: arduino_uno
    components:
      - arduino_core
      - digital_pins
    toolchain_file: arduino.cmake
```

### 3. In Your Variant's Platform-Specific Section

For components that only some products need, and only on specific platforms.

```{code-block} yaml
variants:
  - name: WeatherStation
    components:
      - sensor_reader
      - data_logger
    platforms:
      arduino_uno:
        components:
          - hc_sr04_ultrasonic  # Arduino-specific sensor
      raspberry_pi:
        components:
          - camera_module       # RPi-specific camera
```

Another use case for this third place is when you want to write integration tests. One can create components that combine together multiple components and only define them in the variant-platform section to be used only in that context.

```{code-block} yaml
:linenos:
:emphasize-lines: 9-11

variants:
- name: Disco
  description: The LED blinks and one can change the blinking frequency
  components:
  - spled
  - power_signal_processing
  - light_controller
  features_selection_file: variants/Disco/config.txt
  platforms:
    gtest:
      components: [test_integrations_spled]
```

## Conclusion

Three places to define components might seem like overkill, but they help keep a clear structure in your project configuration.
Each place has its purpose, and using them correctly can make your project easier to manage as it grows in complexity.

If you want to learn more about YANGA please check the [documentation](https://yanga.readthedocs.io/).

✌️
