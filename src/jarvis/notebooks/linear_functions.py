# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "matplotlib>=3.10",
# ]
# ///

import marimo

app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        """
# Lesson: Understanding (Linear) Functions

## Motivation: Why Do We Need "Functions"?

Think about everyday situations where one change predictably leads to another.
For instance, the more steps you take, the greater distance you walk.
Or if you keep increasing the side of a square, its area grows in a regular, predictable way.
Over time, people recognized these cause-and-effect relationships in nature and daily life.

We needed a systematic way to show how changing one quantity (like the side of a square
or the number of steps) would determine another (like area or total distance).

This is how the concept of a *function* came about: a reliable method to represent
how one variable depends on another in a clear, predictable manner.

## The Core Idea

A **function** is a specific type of relationship that:

- Takes an **input** (often represented by \\( x \\)).
- Produces **exactly one output** (often represented by \\( y \\) or \\( f(x) \\)).

The keyword is **exactly one**. If a rule or relationship can give more than one result
for the same input, it fails to meet the definition of a function.

**Example**: Multiply by 3.

- If you input 2, you *always* get 6.
- If you input 10, you *always* get 30.

No matter how many times or ways you feed in the same input, you get a single output.

**Non-Example**: Output a number whose square is the input.

- For an input of 9, you could get 3 *or* \\(-3\\).

The same input (9) can lead to more than one possible output. Hence, it is **not** a function.

/// admonition | Definition

In mathematics, a **function** is a relation between a set of inputs and a set of possible outputs
where each input is related to exactly one output. This means that for each value in the set of inputs,
there is a unique corresponding value in the set of possible outputs.

///


## How to Represent a Function

- **Verbal Description** - You might say, "Take any number, multiply by 2, then subtract 1."
- **Algebraic Expression** - This can be written as \\( f(x) = 2x - 1 \\).
- **Table** - Listing pairs of (input, output).

    \\[
    \\begin{array}{c|cccc}
    x & 0 & 1 & 2 & 3 \\\\
    f(x) & -1 & 1 & 3 & 5 \\\\
    \\end{array}
    \\]

- **Graph** - Plot points \\((x, f(x))\\) on a coordinate plane. For many standard functions, this forms a line or a curve.


## Constructing Functions

We've learned what a function is but how do we actually **build** one?
Let's see how simple operations on the input \\( x \\) can combine to form functions.

### Basic Operations

- **Addition and Subtraction**
  We can add or subtract a constant number. For example, "take \\( x \\) and add 3" means \\( f(x) = x + 3 \\).
  Similarly, "take \\( x \\) and subtract 2" means \\( g(x) = x - 2 \\).
- **Multiplying by a Number**
  We can multiply \\( x \\) by a constant, like 5. That gives us \\( h(x) = 5x \\).
- **Multiplying \\( x \\) by Itself**
  We can square \\( x \\), giving \\( x^2 \\), or take higher powers like \\( x^3 \\), \\( x^4 \\), and so on.

These operations—adding, subtracting, and multiplying by constants or by \\( x \\)—are the building blocks for a very important class of functions.

"""
    )
    return


@app.cell(hide_code=True)
def __(mo, a2_slider, a1_slider, a0_slider):
    # Determine the function latex equation. Do not show the elements with coefficient 0.
    def get_function_latex(a2, a1, a0):
        function_parts = []
        if a2 != 0:
            function_parts.append(f"{a2}x^2")
        if a1 != 0:
            function_parts.append(f"{a1}x")
        if a0 != 0:
            function_parts.append(f"{a0}")
        if len(function_parts) == 0:
            return "0"
        return " + ".join(function_parts)

    mo.vstack(
        [
            mo.md(
                rf"""
                ### Practice: Build Your Own Functions

                {mo.as_html([a2_slider, a1_slider, a0_slider])}

                \[
                f(x) = {get_function_latex(a2_slider.value, a1_slider.value, a0_slider.value)}
                \]

                """
            ),
            construct_function_plot(),  # noqa: F821
        ]
    )
    return


@app.cell(hide_code=True)
def __(mo):
    a2_slider = mo.ui.slider(label="a2 (coefficient of x²)", start=-1, stop=1, step=0.01, value=0)
    a1_slider = mo.ui.slider(label="a1 (coefficient of x )", start=-10, stop=10, step=0.1, value=0)
    a0_slider = mo.ui.slider(label="a0 (constant         )", start=-100, stop=100, step=10, value=0)

    return a2_slider, a1_slider, a0_slider


@app.cell
def __(a2_slider, a1_slider, a0_slider):
    def construct_function_plot():
        import matplotlib.pyplot as plt

        plt.axes()
        # Plot the a2*x² + a1*x + a0 function for x in range(-10, 10)
        x = range(-100, 100)
        y = [a2_slider.value * (i**2) + a1_slider.value * i + a0_slider.value for i in x]
        plt.plot(x, y, label=f"f(x) = {a2_slider.value}x² + {a1_slider.value}x + {a0_slider.value}")
        plt.title("Function Plot")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid()
        # Keep the aspect ratio of the plot square
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)
        plt.axhline(0, color="black", lw=0.5, ls="--")
        plt.axvline(0, color="black", lw=0.5, ls="--")
        return plt.gca()

    return (construct_function_plot,)


@app.cell
def __(mo):
    mo.md(
        """
## Linear Functions

Now that you see what makes something a function, the next big topic is **linear functions**,
functions where the output changes at a **constant rate** as the input increases.
Formally, linear functions have the form:

\\[
f(x) = mx + b,
\\]

where \\(m\\) is the "slope" (how steep the rate of change is) and \\(b\\) is the "y-intercept" (the output value when \\(x = 0\\)).

These functions come up everywhere: wages (hourly pay), distance (speed \\(\\times\\) time), and so on.
Exploring them will give you a solid foundation for much of algebra and beyond.

---

### Summary

1. A function is a rule pairing each input to exactly one output.
2. Functions are indispensable for predicting and analyzing real-world relationships.
3. The "one output per input" rule is what sets functions apart from other types of relationships.
4. Representations include **equations**, **tables**, **graphs**, and **verbal descriptions**.

---

## Bonus: Reflective Question

- **Reflect**: Think of something you do daily (like adjusting oven temperature, measuring how many steps you walk,
or reading a thermometer). How might a function describe this relationship between an input and an output?

Keeping these ideas in mind will help you recognize functions all around you and prepare you for the formal study of **linear functions** next!

"""
    )
    return


@app.cell
def __():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
