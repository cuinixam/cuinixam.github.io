# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.1",
#     "numpy==2.2.4",
# ]
# ///

import marimo

app = marimo.App(width="medium")


@app.cell
def __():
    def get_function_latex(a3, a2, a1, a0):
        """Determine the function latex equation. Do not show the elements with coefficient 0."""
        result = ""
        if a3 != 0:
            result = f"{a3}x^3"
        if a2 != 0:
            if not result:
                result = f"{a2}x^2"
            else:
                result += f" + {a2}x^2" if a2 > 0 else f" {a2}x^2"
        if a1 != 0:
            if not result:
                result = f"{a1}x"
            else:
                result += f" + {a1}x" if a1 > 0 else f" {a1}x"
        if a0 != 0:
            if not result:
                result = f"{a0}"
            else:
                result += f" + {a0}" if a0 > 0 else f" {a0}"
        if not result:
            return "0"
        return result

    return get_function_latex


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

/// note | Definition

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

These operations — adding, subtracting, and multiplying by constants or by \\( x \\) — are the building blocks
for a very important class of functions called **polynomial functions**.
We will not discuss them here, but only the simplest ones, the **linear functions**.

"""
    )
    return


@app.cell(hide_code=True)
def __(mo, a3_slider, a2_slider, a1_slider, a0_slider):
    mo.vstack(
        [
            mo.md(
                rf"""
                ### Play Around: Explore Functions

                /// tip | Todo
                Use the sliders to adjust the coefficients of the function and observe how the graph changes.

                \[
                f(x) = a_3 x^3 + a_2 x^2 + a_1 x + a_0
                \]

                ///

                - {mo.as_html(a3_slider)} a3 (coefficient of x³)
                - {mo.as_html(a2_slider)} a2 (coefficient of x²)
                - {mo.as_html(a1_slider)} a1 (coefficient of x )
                - {mo.as_html(a0_slider)} a0 (constant)

                \[
                f(x) = {get_function_latex(a3_slider.value, a2_slider.value, a1_slider.value, a0_slider.value)}
                \]

                """  # noqa: F821
            ),
            construct_polynomial_function_plot(),  # noqa: F821
        ]
    )
    return


@app.cell(hide_code=True)
def __(mo):
    a3_slider = mo.ui.number(-0.1, 0.1, step=0.001, value=0.0)
    a2_slider = mo.ui.number(-1, 1, step=0.01, value=0)
    a1_slider = mo.ui.number(-10, 10, step=0.1, value=0)
    a0_slider = mo.ui.number(-100, 100, step=10, value=0)

    return a3_slider, a2_slider, a1_slider, a0_slider


@app.cell
def __(a3_slider, a2_slider, a1_slider, a0_slider):
    def construct_polynomial_function_plot():
        import matplotlib.pyplot as plt

        plt.axes()
        x = range(-100, 100)
        y = [a3_slider.value * (i**3) + a2_slider.value * (i**2) + a1_slider.value * i + a0_slider.value for i in x]
        plt.plot(x, y, label=f"f(x) = {a3_slider.value}x³ {a2_slider.value}x² + {a1_slider.value}x + {a0_slider.value}")
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

    return (construct_polynomial_function_plot,)


@app.cell
def __(mo):
    mo.vstack(
        [
            mo.md(
                """
## Linear Functions

Imagine you land a summer job at a cool local café. It's a pretty good deal:

- You get a fixed amount of €10 just for showing up each day (your base pay).
- Plus, you get an extra €2 bonus for every customer you personally help.

How much would you earn on a given day? Let's say you help ten customers.
You get €10 for showing up and another €20 for helping ten customers (2 x 10), in total €30.

So, for your café job, the function describing your earnings is:

\\[
\\text{Earnings} = 2 \\times (\\text{number of customers}) + 10
\\]

or using our standard notation:

\\[
f(x) = 2x + 10
\\]
"""
            ),
            construct_local_cafe_function_plot(),  # noqa: F821
            mo.md(
                """


/// note | Definition
A **linear function** is a function that can be expressed in the form \\( f(x) = mx + b \\), where:

- \\( m \\) is the slope (the rate of change),
- \\( b \\) is the y-intercept or offset (the value of the function when \\( x = 0 \\)).

///

Let's try to understand the meaning of the slope and the offset.
"""
            ),
        ]
    )
    return


@app.cell
def __():
    def construct_local_cafe_function_plot():
        import matplotlib.pyplot as plt

        plt.axes()
        x = range(0, 10)
        y = [2 * i + 10 for i in x]
        plt.scatter(x, y, label="f(x) = 2x + 10", color="blue")
        plt.title("Café Earnings Function")
        plt.xlabel("Number of Customers")
        plt.ylabel("Earnings (€)")
        plt.grid()
        plt.xlim(0, 10)
        plt.ylim(0, 31)
        # Show increment of 1 on x-axis and 2 on y-axis
        plt.xticks(range(0, 11))
        plt.yticks(range(0, 31, 2))
        return plt.gca()

    return (construct_local_cafe_function_plot,)


@app.cell(hide_code=True)
def __(mo, lf_a1_slider, lf_a0_slider):
    mo.vstack(
        [
            mo.md(
                rf"""
                /// tip | Todo
                Use the sliders to adjust the slope *m* and offset *b* of the function and observe how the graph changes.

                \[
                f(x) = m x + b
                \]

                ///

                - {mo.as_html(lf_a1_slider)}
                - {mo.as_html(lf_a0_slider)}

                \[
                f(x) = {get_function_latex(0, 0, lf_a1_slider.value, lf_a0_slider.value)}
                \]

                """  # noqa: F821
            ),
            construct_linear_function_plot(),  # noqa: F821
            mo.md(
                """
                What happens when you change the slope \\( m \\)?

                - If \\( m \\) is positive, the function increases as \\( x \\) increases.
                - If \\( m \\) is negative, the function decreases as \\( x \\) increases.
                - If \\( m \\) is zero, the function is constant (a horizontal line).

                What happens when you change the offset \\( b \\)?

                - If \\( b \\) is positive, the function is shifted up.
                - If \\( b \\) is negative, the function is shifted down.

                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def __(mo):
    lf_a1_slider = mo.ui.number(-10, 10, step=0.1, value=0, label="Slope (m)")
    lf_a0_slider = mo.ui.number(-100, 100, step=10, value=0, label="Offset (b)")

    return lf_a1_slider, lf_a0_slider


@app.cell
def __(lf_a1_slider, lf_a0_slider):
    def construct_linear_function_plot():
        import matplotlib.pyplot as plt

        plt.axes()
        x = range(-100, 100)
        y = [lf_a1_slider.value * i + lf_a0_slider.value for i in x]
        plt.plot(x, y, label=f"f(x) = {lf_a1_slider.value}x + {lf_a0_slider.value}")
        plt.title("Function Plot")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid()
        # Keep the aspect ratio of the plot square
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)
        plt.axhline(0, color="black", lw=0.5, ls="--")
        plt.axvline(0, color="black", lw=0.5, ls="--")
        plt.xticks(range(-100, 100, 10))
        plt.yticks(range(-100, 100, 10))
        # Highlight the y-intercept point in red
        plt.scatter(0, lf_a0_slider.value, color="red", label=f"offset (b) = {lf_a0_slider.value}")
        plt.legend()
        return plt.gca()

    return (construct_linear_function_plot,)


@app.cell
def __(mo):
    mo.md(
        """
### Determining a Function from Two Points

It is not hard to guess that one needs to know just two points to determine straight lines.
Ever wondered how to find the equation of a line when you know two points on it?

Let's explore a quick, real-world scenario to see how it works:

Imagine you're playing a popular online adventure game.

- You notice that buying 2 potions costs you 5 gold coins.
- Another time, buying 5 potions costs 11 gold coins.

You suspect the cost might follow a **linear function**, something like:

\\[
f(x) = m \\cdot x + b
\\]

where:

- \\( x \\) is the number of potions you buy.
- \\( f(x) \\) is the total cost.
- \\( m \\) is the cost *per potion* (the slope),
- \\( b \\) is the *base cost* even before buying any potions (the y-intercept).

**Question**: How do you figure out \\( m \\) and \\( b \\) just from these two data points?

#### The Slope

First, find the **slope** \\( m \\). This tells you how quickly the cost increases per additional potion. Mathematically, we often say:

\\[
\\text{slope} = m = \\frac{\\text{change in } y}{\\text{change in } x} = \\frac{y_2 - y_1}{x_2 - x_1}
\\]

In our potions example:

- the first information is that 2 potions cost 5 coins: \\( (x_1, y_1) = (2, 5) \\)
- the second information is the 5 potions cost 11 coins: \\( (x_2, y_2) = (5, 11) \\)

So,

\\[
m = \\frac{11 - 5}{5 - 2} = \\frac{6}{3} = 2.
\\]

In plain English, it means **each potion** adds 2 gold coins to the total cost.

#### The Intercept

Once we know \\( m \\), we can plug in either of our original points to solve for \\( b \\).
Using \\( (2,5) \\):

\\[
y_1 = m \\cdot x_1 + b \\quad \\Rightarrow \\quad 5 = 2 \\cdot 2 + b \\quad \\Rightarrow \\quad 5 = 4 + b \\quad \\Rightarrow \\quad b = 1.
\\]

So \\( b = 1 \\). This means there's a **base cost** of 1 coin even before you buy any potions.

#### Putting It All Together

Now we have:

\\[
f(x) = 2x + 1.
\\]

- \\( m = 2 \\) (slope, or 2 coins per potion)
- \\( b = 1 \\) (base cost, 1 coin)

So the next time you need to stock up on potions, you can **predict** your total cost: if you buy \\( x \\) potions, you pay \\( 2x + 1 \\) coins.

---

**In General**:

1. **Slope** \\( m = \\frac{y_2 - y_1}{x_2 - x_1} \\).
2. **Intercept** \\( b = y_1 - m \\cdot x_1 \\).
3. **Write** \\( f(x) = m x + b \\).

With just two points, you can always uncover the "rate of change" (slope) and the "starting value" (intercept) for a linear function.
This helps you connect the dots (literally!) in all sorts of situations, from in-game purchases to real-world pricing.
"""
    )
    return


@app.cell(hide_code=True)
def __(mo, end_portal_spot1, end_portal_drop1, end_portal_spot2, end_portal_drop2, end_portal_m1, end_portal_b1, end_portal_m2, end_portal_b2):
    mo.vstack(
        [
            mo.md(
                f"""
### Intersection of Two Lines

**Minecraft: Finding the End Portal**

In Minecraft, you can locate the End Portal (deep underground within a Stronghold) by using **Eyes of Ender**.
Throw an Eye of Ender, and it will fly in the direction of the nearest stronghold.

Usually, players do something like this:

- Walk in any direction, throw an Eye of Ender, watch where it flies, and then pick it up (if it doesn't break).
- Keep walking that way, throwing the Eye every so often, until you notice its flight path change or the Eye goes underground.
- Dig around that general area to find the Stronghold.

This method works, but it is very inefficient because you might have to throw a lot of Eyes of Ender to find the Stronghold.
Eyes of Ender are precious and hard to make (you need Blaze Powder and Ender Pearls), so you want to use them wisely.


Let's come up with a better plan using some math! 😎

/// tip | Idea

Throw two Eyes of Ender from two different (far away) locations, write down coordinates and find the intersection of the two lines they create.
Remember that the Eyes of Ender fly in a straight line towards the Stronghold.

///


#### Finding the End Portal

1. **First Spot**

  - Let's say you're hanging around coordinates \\({end_portal_spot1}\\).
  - You throw an Eye of Ender, and it tends to land around \\({end_portal_drop1}\\).
  - If you connect these points (where you stand and where the Eye drops), you get a rough line
  - We can calculate the slope and intercept of this first line: \\( f(x) = {end_portal_m1} x + {end_portal_b1} \\)

2. **Second Spot**

  - Next, you move to a different place, maybe around \\({end_portal_spot2}\\).
  - Throw the Eye of Ender again, and this time it drops near \\({end_portal_drop2}\\).
  - Connecting these new points gives you the second line:  \\( f(x) = {end_portal_m2} x + {end_portal_b2} \\)

3. **Where to Dig?**

  - These two lines will cross at a specific location.
  - That intersection is your best guess for where the Stronghold (and thus the End Portal) is waiting underground!
  - Next, we'll break down the math behind finding that intersection point.


---

#### The Math: Finding the Intersection

Let the two lines be:

\\[
\\begin{{cases}}
y = m_1 x + b_1
\\\\
y = m_2 x + b_2
\\end{{cases}}
\\]

To find the intersection:

1. **Set them equal** (because we expect them to meet at the same value of \\( y \\)):

\\[
m_1 x + b_1 = m_2 x + b_2.
\\]

2. **Solve for \\( x \\)**:

\\[
m_1 x - m_2 x = b_2 - b_1
\\quad\\Rightarrow\\quad
x(m_1 - m_2) = b_2 - b_1
\\quad\\Rightarrow\\quad
x = \\frac{{b_2 - b_1}}{{m_1 - m_2}}.
\\]

3. **Plug \\( x \\) back in** to get \\( y \\), for example into the first line:

\\[
y = m_1 \\left(\\frac{{b_2 - b_1}}{{m_1 - m_2}}\\right) + b_1.
\\]

The point \\((x,\\, y)\\) is where the two lines meet — or in **Minecraft** terms, where you should head to find the End Portal.


The lines you created with the two Eyes of Ender are shown in the graph below.

                """
            ),
            construct_minecraft_find_end_portal_function_plot(),  # noqa: F821
            mo.md(
                """
                #### Summary

                Finding where two lines cross isn't just an abstract math problem!
                As we saw with the Minecraft example, it can be a clever strategy for pinpointing a hidden location.

                Understanding linear functions and how to find their intersections provides a powerful tool for solving real-world (and game-world!) problems.
                Finding the End Portal is a great example of how math helps us navigate the world around us more effectively.
                """
            ),
        ]
    )
    return


@app.cell
def __():
    end_portal_spot1 = (150, 80)  # first location
    end_portal_drop1 = (200, 70)  # where the Eye of Ender drops
    end_portal_spot2 = (350, 75)  # second location
    end_portal_drop2 = (300, 70)  # where the Eye of Ender drops

    # Calculate slope (m) and intercept (b) for Line 1
    end_portal_m1 = (end_portal_drop1[1] - end_portal_spot1[1]) / (end_portal_drop1[0] - end_portal_spot1[0])  # (z2 - z1) / (x2 - x1)
    end_portal_b1 = end_portal_spot1[1] - end_portal_m1 * end_portal_spot1[0]

    # Calculate slope and intercept for Line 2
    end_portal_m2 = (end_portal_drop2[1] - end_portal_spot2[1]) / (end_portal_drop2[0] - end_portal_spot2[0])
    end_portal_b2 = end_portal_spot2[1] - end_portal_m2 * end_portal_spot2[0]

    return (end_portal_spot1, end_portal_drop1, end_portal_spot2, end_portal_drop2, end_portal_m1, end_portal_b1, end_portal_m2, end_portal_b2)


@app.cell
def __(end_portal_spot1, end_portal_drop1, end_portal_spot2, end_portal_drop2, end_portal_m1, end_portal_b1, end_portal_m2, end_portal_b2):
    def construct_minecraft_find_end_portal_function_plot():
        import matplotlib.pyplot as plt
        import numpy as np

        # Find intersection (x_int, z_int) by setting m1*x + b1 = m2*x + b2
        x_int = (end_portal_b2 - end_portal_b1) / (end_portal_m1 - end_portal_m2)
        z_int = end_portal_m1 * x_int + end_portal_b1
        intersection_label = f"Intersection ~ ({x_int:.0f}, {z_int:.0f})"

        # Prepare data for plotting
        x_vals = np.linspace(100, 400, 300)
        z1_vals = end_portal_m1 * x_vals + end_portal_b1
        z2_vals = end_portal_m2 * x_vals + end_portal_b2

        plt.axes()

        # Plot the two lines
        plt.plot(x_vals, z1_vals, color="blue", linestyle="--")
        plt.plot(x_vals, z2_vals, color="purple", linestyle="--")

        # Mark vantage and drop points
        plt.scatter([end_portal_spot1[0]], [end_portal_spot1[1]], zorder=5, color="green", marker="x", label="First spot")
        plt.scatter([end_portal_spot2[0]], [end_portal_spot2[1]], zorder=5, color="green", marker="x", label="Second spot")
        plt.scatter([end_portal_drop1[0]], [end_portal_drop1[1]], zorder=5, color="orange", marker="o", label="First drop")
        plt.scatter([end_portal_drop2[0]], [end_portal_drop2[1]], zorder=5, color="orange", marker="o", label="Second drop")

        # Mark the intersection (if it exists)
        if x_int is not None and z_int is not None:
            plt.scatter([x_int], [z_int], color="red", zorder=5, label=intersection_label)

        plt.title("Minecraft - Locate the End Portal")
        plt.xlabel("x (East-West coordinate)")
        plt.ylabel("z (North-South coordinate)")
        plt.grid(True)
        plt.legend()

        return plt.gca()

    return (construct_minecraft_find_end_portal_function_plot,)


@app.cell(hide_code=True)
def __(mo, exercise_a1_slider, exercise_a0_slider, run_button):
    mo.vstack(
        [
            mo.md(
                rf"""
                ---

                ## Test Your Understanding of Linear Functions

                /// tip | Todo
                Use the sliders to adjust the slope *m* and offset *b* of the function to match the two given points.
                When you are correct, the line will turn green. Press the "Generate Points" button to get new points.

                ///

                {run_button}

                {mo.as_html(exercise_a1_slider)}

                {mo.as_html(exercise_a0_slider)}

                \[
                f(x) = {get_function_latex(0, 0, exercise_a1_slider.value, exercise_a0_slider.value)}
                \]

                """  # noqa: F821
            ),
            construct_exercise_function_plot(),  # noqa: F821
        ]
    )
    return


@app.cell(hide_code=True)
def __(mo):
    exercise_a1_slider = mo.ui.number(-10, 10, step=0.1, value=0, label="Slope (m)")
    exercise_a0_slider = mo.ui.number(-100, 100, step=10, value=0, label="Offset (b)")

    return exercise_a1_slider, exercise_a0_slider


@app.cell(hide_code=True)
def _(mo):
    run_button = mo.ui.run_button(label="Generate Points")
    return (run_button,)


@app.cell(hide_code=True)
def __(run_button):
    import random

    _ = run_button

    # Generate a random slope and offset
    slope = random.randint(-30, 30) / 10  # noqa: S311
    offset = random.randint(-6, 6) * 10  # noqa: S311

    # Create two points on the line for x = -1 and x = 1
    exercise_x1 = -10
    exercise_y1 = slope * exercise_x1 + offset
    exercise_x2 = 10
    exercise_y2 = slope * exercise_x2 + offset

    return (exercise_x1, exercise_y1, exercise_x2, exercise_y2)


@app.cell
def __(exercise_a1_slider, exercise_a0_slider, exercise_x1, exercise_y1, exercise_x2, exercise_y2):
    def construct_exercise_function_plot():
        import matplotlib.pyplot as plt

        a1 = exercise_a1_slider.value
        a0 = exercise_a0_slider.value

        # Check if the line goes through both points
        passes_point1 = exercise_y1 == a1 * exercise_x1 + a0
        passes_point2 = exercise_y2 == a1 * exercise_x2 + a0

        # Use green if both points lie on the line, else use default color
        line_color = "green" if passes_point1 and passes_point2 else "blue"

        plt.axes()
        x = range(-100, 100)
        y = [a1 * i + a0 for i in x]
        plt.plot(x, y, color=line_color, label=f"f(x) = {a1}x + {a0}")
        plt.title("Function Plot")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid()
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)
        plt.axhline(0, color="black", lw=0.5, ls="--")
        plt.axvline(0, color="black", lw=0.5, ls="--")
        plt.xticks(range(-100, 100, 10))
        plt.yticks(range(-100, 100, 10))
        plt.scatter([exercise_x1, exercise_x2], [exercise_y1, exercise_y2], color="red", label="Points")
        plt.legend()
        return plt.gca()

    return (construct_exercise_function_plot,)


@app.cell
def __(mo):
    mo.md(
        """
---

## Summary

1. A function is a rule pairing each input to exactly one output.
2. Functions are indispensable for predicting and analyzing real-world relationships.
3. The "one output per input" rule is what sets functions apart from other types of relationships.
4. Representations include **equations**, **tables**, **graphs**, and **verbal descriptions**.

### Reflect

Think of something you do daily (like adjusting oven temperature, measuring how many steps you walk,
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
