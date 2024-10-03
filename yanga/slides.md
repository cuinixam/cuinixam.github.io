## What is YANGA?

<!-- .slide: data-transition="none" -->

--

## What is YANGA?

<!-- .slide: data-transition="none" -->

It is a Python application.

--

## What is it for?

<!-- .slide: data-transition="none" -->

Note:

Why are we talking about a Line? A Product Line? A Software Product Line?

--

## Line

<!-- .slide: data-transition="none" -->

--

## Product Line

<!-- .slide: data-transition="none" -->

--

## Software Product Line

<!-- .slide: data-transition="none" -->

--

## <span class="highlighted-green">Engineering</span> <span class="monospacesmall">a Software Product Line</span>

<!-- .slide: data-transition="none" -->

--

## Domain

Terminology <!-- .element: class="monospacesmall" -->

- Product <!-- .element: class="fragment" -->
- Variant <!-- .element: class="fragment" -->
- Component <!-- .element: class="fragment" -->
- Platform <!-- .element: class="fragment" -->
- Assembly line <!-- .element: class="fragment" -->

Note:

May I see how to you do this?

---

## <span class="highlighted-yellow-transparent-background">Pipeline</span>

<!-- .slide: data-background-image="images/conveyor_isometric.jpg" -->

<div class="bottom-aligned-text">
<a href="http://www.freepik.com">Designed by macrovector / Freepik</a> <!-- .element: class="highlighted-yellow-transparent-background-small" -->
</div>

--

## Pipeline

<img src="images/conveyor_isometric.jpg" height="150" class="rounded-corners">
<!-- .element: style="width: 30%" -->

```yaml [1-10]
pipeline:
  - install:
      - step: RunScoop
  - gen:
      - step: FeatureModel
  - build:
      - step: Configure
      - step: Build
```

<!-- .element: style="float: right; width: 50%" -->

--

## Extend

yanga.yaml <!-- .element: class="monospacesmall" -->

```yaml [9-10]
pipeline:
  - install:
      - step: RunScoop
  - gen:
      - step: FeatureModel
  - build:
      - step: Configure
      - step: Build
  - publish:
      - step: Artifactory
```

--

## Replace

yanga.yaml <!-- .element: class="monospacesmall" -->

```yaml [8-8]
pipeline:
  - install:
      - step: RunScoop
  - gen:
      - step: FeatureModel
  - build:
      - step: Configure
      - step: MyNewBuild
  - publish:
      - step: Artifactory
```

--

## Execution

```yaml [1-10]
pipeline:
  - install:
      - step: RunScoop
  - gen:
      - step: FeatureModel
  - build:
      - step: Configure
      - step: Build
```

<!-- .element: style="float: left; width: 40%" -->

<div class="big-container">
  <!-- Assuming your list is here -->
  <ul>
    <li class="fragment">execution context</li>
    <li class="fragment">dependency management</li>
    <li class="fragment">single step execution</li>
  </ul>
</div> <!-- .element: style="float: right; width: 55%" -->

---

## <span class="highlighted-yellow-transparent-background">Platform</span>

<!-- .slide: data-background-image="images/futuristic_cpu.png" -->

--

## Platform

<div class="content-container">
  <div class="small-container">
    <img src="images/futuristic_cpu.png" height="235" class="rounded-corners">
  </div>
  <div class="big-container">
    <!-- Assuming your list is here -->
    <ul>
      <li>Where shall the software run?</li>
      <li>How to build it?</li>
    </ul>
  </div>
</div>

--

## Platform

yanga.yaml <!-- .element: class="monospacesmall" -->

```yaml [1-3,9-10|4-6,11-13|7,14]
platforms:
  - name: win_exe
    description: Build Windows executable
    cmake_generators:
      - step: CMakeGenerator
        module: yanga.cmake.executable
    toolchain_file: clang.cmake
    is_default: true
  - name: gtest
    description: Build GTest tests
    cmake_generators:
      - step: GTestCMakeGenerator
        module: yanga.cmake.gtest
    toolchain_file: gcc.cmake
```

---

## <span class="highlighted-red-transparent-background">Product Variants</span>

<!-- .slide: data-background-image="images/software_variants_hologram.png" -->

--

## Product Variants

yanga.yaml <!-- .element: class="monospacesmall" -->

```yaml [1-3,8-9|4-7,10-13|14]
variants:
  - name: EnglishVariant
    description: Say hello in English.
    bom:
      components:
        - main
        - greeter
  - name: GermanVariant
    description: Say hello in German.
    bom:
      components:
        - main
        - greeter
    config_file: "config_de.txt"
```

--

## Components

yanga.yaml <!-- .element: class="monospacesmall" -->

```yaml [1-3,6-7|4-5,8-11]
components:
  - name: main
    type: component
    sources:
      - main.c
  - name: greeter
    type: component
    sources:
      - greeter.c
    test_sources:
      - greeter_test.cc
```

---

## Next steps

--

## Multi-pipeline

|       | Build | Run | Release |
| ----- | ----- | --- | ------- |
| exe   | ✅    | ✅  |         |
| gtest | ✅    | ✅  |         |
| hil   | ✅    | ✅  |         |
| ecu   | ✅    |     | ✅💰    |

---

## <img src="images/yanga.png" class="inline-image"> <a href="https://github.com/cuinixam/yanga">YANGA</a>

<!-- .slide: data-background-iframe="https://yanga.readthedocs.io/en/latest/project_info.html" -->

---

## ❕Thank you❕
