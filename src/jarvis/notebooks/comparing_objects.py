# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.3",
# ]
# ///

import marimo

app = marimo.App(width="medium")


@app.cell
def __(mo):
    intro_text = mo.md(
        """
        # Comparing Objects: From Length to Surface Area and Beyond

        Since the dawn of civilization, humans have needed to compare objects. Whether it's for trade, construction, or daily life,
        we need a way to measure and understand the space that objects occupy.

        One needed to compare distances between cities, heights of castles, or the size of fields for farming.
        This notebook explores how we compare objects using mathematical concepts like **length**, **area**, and **volume**.
        """
    )
    return (intro_text,)


@app.cell
def __():
    class LengthExerciseData:
        def __init__(self, value: float, from_unit: str, to_unit: str, answer: float, step: float):
            self.value = value
            self.from_unit = from_unit
            self.to_unit = to_unit
            self.answer = answer
            self.step = step
            self.label = f"**{value:,} {from_unit}** is equal to"

    return LengthExerciseData


@app.cell
def __(mo):
    def create_ui_number_input(data):
        return mo.ui.number(label=data.label, step=data.step, value=0)

    return create_ui_number_input


@app.cell
def __(mo):
    def create_status_indicator(user_input, correct_answer):
        is_correct = user_input is not None and abs(user_input - correct_answer) < 1e-6
        return mo.md("✅" if is_correct else "❌")

    return create_status_indicator


@app.cell
def __(mo):
    def create_exercise_row(data, result, unit):
        return mo.hstack(
            [
                data,
                mo.md(f"**{unit}**"),
                result,
            ],
            justify="start",
            align="center",
            gap=1,
        )

    return create_exercise_row


@app.cell
def __(LengthExerciseData):
    length_exercise_data = [
        LengthExerciseData(value=2, from_unit="km", to_unit="m", answer=2000, step=1),
        LengthExerciseData(value=0.5, from_unit="m", to_unit="mm", answer=500, step=1),
        LengthExerciseData(value=150, from_unit="cm", to_unit="m", answer=1.5, step=0.1),
        LengthExerciseData(value=75, from_unit="mm", to_unit="cm", answer=7.5, step=0.1),
        LengthExerciseData(value=384000, from_unit="m", to_unit="km", answer=384, step=1),
    ]
    return (length_exercise_data,)


@app.cell
def __(create_ui_number_input, length_exercise_data):
    length_exercise_data_1 = create_ui_number_input(length_exercise_data[0])
    length_exercise_data_2 = create_ui_number_input(length_exercise_data[1])
    length_exercise_data_3 = create_ui_number_input(length_exercise_data[2])
    length_exercise_data_4 = create_ui_number_input(length_exercise_data[3])
    length_exercise_data_5 = create_ui_number_input(length_exercise_data[4])
    return (
        length_exercise_data_1,
        length_exercise_data_2,
        length_exercise_data_3,
        length_exercise_data_4,
        length_exercise_data_5,
    )


@app.cell
def __(
    create_status_indicator,
    length_exercise_data,
    length_exercise_data_1,
    length_exercise_data_2,
    length_exercise_data_3,
    length_exercise_data_4,
    length_exercise_data_5,
):
    length_exercise_result_1 = create_status_indicator(length_exercise_data_1.value, length_exercise_data[0].answer)
    length_exercise_result_2 = create_status_indicator(length_exercise_data_2.value, length_exercise_data[1].answer)
    length_exercise_result_3 = create_status_indicator(length_exercise_data_3.value, length_exercise_data[2].answer)
    length_exercise_result_4 = create_status_indicator(length_exercise_data_4.value, length_exercise_data[3].answer)
    length_exercise_result_5 = create_status_indicator(length_exercise_data_5.value, length_exercise_data[4].answer)
    return (
        length_exercise_result_1,
        length_exercise_result_2,
        length_exercise_result_3,
        length_exercise_result_4,
        length_exercise_result_5,
    )


@app.cell
def __(
    mo,
    create_exercise_row,
    length_exercise_data,
    length_exercise_data_1,
    length_exercise_result_1,
    length_exercise_data_2,
    length_exercise_result_2,
    length_exercise_data_3,
    length_exercise_result_3,
    length_exercise_data_4,
    length_exercise_result_4,
    length_exercise_data_5,
    length_exercise_result_5,
):
    compare_by_length_exercises = mo.vstack(
        [
            create_exercise_row(length_exercise_data_1, length_exercise_result_1, length_exercise_data[0].to_unit),
            create_exercise_row(length_exercise_data_2, length_exercise_result_2, length_exercise_data[1].to_unit),
            create_exercise_row(length_exercise_data_3, length_exercise_result_3, length_exercise_data[2].to_unit),
            create_exercise_row(length_exercise_data_4, length_exercise_result_4, length_exercise_data[3].to_unit),
            create_exercise_row(length_exercise_data_5, length_exercise_result_5, length_exercise_data[4].to_unit),
        ],
        gap=1,
    )
    return compare_by_length_exercises


@app.cell
def __(mo):
    compare_by_length = mo.md(
        """
        ## Comparing by Length

        There is nothing simpler than comparing lengths, right? If you have two sticks, you can easily tell which one is longer
        by placing them side-by-side. But how about agreeing on what "longer" means without seeing them?
        One would need to ask someone to measure the length of each stick, get the numbers and compare them.

        In order to compare lengths, we need a standard unit of measurement which is used by everyone.
        Otherwise, we would have to say "this stick is twice as big as my hand" or "this rope is as long as my arm".
        Indeed, there was a time in history when kings and queens had their own units of measurement, like the "foot".
        Unfortunately, this made trade and communication difficult, especially when people from different regions
        tried to exchange goods.
        You can imagine what happened when a new king came to power and decided to change the length of the foot
        to be his own foot size. Suddenly, all the merchants had to adjust their measurements :O

        This is why we needed a unit of measurement independent of any person or ruler.
        This was a struggle that lasted for centuries, but eventually in the 18th century, the **metric system** was established.
        Since then, we have been using the **meter** as the standard unit of length.

        /// tip | Did you know?
        The meter was originally defined as one ten-millionth of the distance from the equator to the North Pole.
        The story of measuring and defining the meter is very interesting and I encourage you to read about it.
        ///

        Having the meter as a standard unit of length is great, but might not be enough to easily compare lengths.
        For example, how many meters does a matchstick have? Or how many meters are from earth to the moon?
        We could use meters, and say that a matchstick is 0.05 meters long and the distance to the moon is 384,400,000 meters.
        But this is not very practical. We need a way to express these lengths much more easily.

        That is why the metric system also introduced **prefixes** to express different orders of magnitude.
        For example:

        * **kilo-** means 1000, so 1 kilometer (km) is 1000 meters.
        * **deci-** means one tenth of a meter (dm), so 1 m = 10 dm.
        * **centi-** means one hundredth of a meter (cm), so 1 m = 100 cm.
        * **milli-** means one thousandth of a meter (mm), so 1 m = 1000 mm.

        Of course, converting between these units is easy, since they are all based on the meter.

        Let's do some quick exercises to practice converting between these units.


        ### Exercises

        /// tip | Todo
        Type the correct answer in the input fields below and press Enter to check your answer.

        Use `.` for decimal points, e.g. `1.5` for one and a half.
        ///

        """
    )
    return (compare_by_length,)


@app.cell
def __():
    def visualize_rooms():
        import matplotlib.patches as patches
        import matplotlib.pyplot as plt

        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle("Visualizing Rooms", fontsize=16)

        # --- Room 1: 4x6 ---
        width1, length1 = 4, 6
        ax1.set_title("My Room")
        # Set plot limits
        ax1.set_xlim(-0.5, 6.5)
        ax1.set_ylim(-0.5, 6.5)
        # Draw the rectangle
        ax1.add_patch(patches.Rectangle((0, 0), length1, width1, facecolor="lightblue", edgecolor="black"))
        # Draw the grid lines (tiles)
        for x in range(length1 + 1):
            ax1.plot([x, x], [0, width1], color="white", linestyle="-")
        for y in range(width1 + 1):
            ax1.plot([0, length1], [y, y], color="white", linestyle="-")
        ax1.set_xlabel("Length (m)")
        ax1.set_ylabel("Width (m)")
        ax1.set_aspect("equal", adjustable="box")

        # --- Room 2: 5x5 ---
        width2, length2 = 5, 5
        ax2.set_title("Your Room")
        # Set plot limits
        ax2.set_xlim(-0.5, 6.5)
        ax2.set_ylim(-0.5, 6.5)
        # Draw the rectangle
        ax2.add_patch(patches.Rectangle((0, 0), length2, width2, facecolor="lightgreen", edgecolor="black"))
        # Draw the grid lines (tiles)
        for x in range(length2 + 1):
            ax2.plot([x, x], [0, width2], color="white", linestyle="-")
        for y in range(width2 + 1):
            ax2.plot([0, length2], [y, y], color="white", linestyle="-")
        ax2.set_xlabel("Length (m)")
        ax2.set_aspect("equal", adjustable="box")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        room_comparison_plot = plt.gcf()

        return room_comparison_plot

    return visualize_rooms


@app.cell
def __(LengthExerciseData):
    area_exercise_data = [
        LengthExerciseData(value=200, from_unit="cm²", to_unit="m²", answer=2, step=1),
        LengthExerciseData(value=2, from_unit="m²", to_unit="mm²", answer=2000000, step=1),
        LengthExerciseData(value=1.5, from_unit="m²", to_unit="cm²", answer=15000, step=1),
        LengthExerciseData(value=1, from_unit="ha", to_unit="dm²", answer=1000000, step=1),
        LengthExerciseData(value=15, from_unit="are", to_unit="m²", answer=1500, step=1),
    ]
    return (area_exercise_data,)


@app.cell
def __(create_ui_number_input, area_exercise_data):
    area_exercise_data_1 = create_ui_number_input(area_exercise_data[0])
    area_exercise_data_2 = create_ui_number_input(area_exercise_data[1])
    area_exercise_data_3 = create_ui_number_input(area_exercise_data[2])
    area_exercise_data_4 = create_ui_number_input(area_exercise_data[3])
    area_exercise_data_5 = create_ui_number_input(area_exercise_data[4])
    return (
        area_exercise_data_1,
        area_exercise_data_2,
        area_exercise_data_3,
        area_exercise_data_4,
        area_exercise_data_5,
    )


@app.cell
def __(
    create_status_indicator,
    area_exercise_data,
    area_exercise_data_1,
    area_exercise_data_2,
    area_exercise_data_3,
    area_exercise_data_4,
    area_exercise_data_5,
):
    area_exercise_result_1 = create_status_indicator(area_exercise_data_1.value, area_exercise_data[0].answer)
    area_exercise_result_2 = create_status_indicator(area_exercise_data_2.value, area_exercise_data[1].answer)
    area_exercise_result_3 = create_status_indicator(area_exercise_data_3.value, area_exercise_data[2].answer)
    area_exercise_result_4 = create_status_indicator(area_exercise_data_4.value, area_exercise_data[3].answer)
    area_exercise_result_5 = create_status_indicator(area_exercise_data_5.value, area_exercise_data[4].answer)
    return (
        area_exercise_result_1,
        area_exercise_result_2,
        area_exercise_result_3,
        area_exercise_result_4,
        area_exercise_result_5,
    )


@app.cell
def __(
    mo,
    create_exercise_row,
    area_exercise_data,
    area_exercise_data_1,
    area_exercise_result_1,
    area_exercise_data_2,
    area_exercise_result_2,
    area_exercise_data_3,
    area_exercise_result_3,
    area_exercise_data_4,
    area_exercise_result_4,
    area_exercise_data_5,
    area_exercise_result_5,
):
    compare_by_area_exercises = mo.vstack(
        [
            create_exercise_row(area_exercise_data_1, area_exercise_result_1, area_exercise_data[0].to_unit),
            create_exercise_row(area_exercise_data_2, area_exercise_result_2, area_exercise_data[1].to_unit),
            create_exercise_row(area_exercise_data_3, area_exercise_result_3, area_exercise_data[2].to_unit),
            create_exercise_row(area_exercise_data_4, area_exercise_result_4, area_exercise_data[3].to_unit),
            create_exercise_row(area_exercise_data_5, area_exercise_result_5, area_exercise_data[4].to_unit),
        ],
        gap=1,
    )
    return compare_by_area_exercises


@app.cell
def __():
    def visualize_my_room_3d():
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        # Create the 3D plot
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_title("My Room in 3D")

        # Room (4x6x3)
        x, y, z = 0, 0, 0
        dx, dy, dz = 4, 6, 3
        vertices = [[x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z], [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]]
        faces = [
            [vertices[j] for j in [0, 1, 2, 3]],
            [vertices[j] for j in [4, 5, 6, 7]],
            [vertices[j] for j in [0, 1, 5, 4]],
            [vertices[j] for j in [2, 3, 7, 6]],
            [vertices[j] for j in [1, 2, 6, 5]],
            [vertices[j] for j in [4, 7, 3, 0]],
        ]
        ax.add_collection3d(Poly3DCollection(faces, facecolors="lightblue", linewidths=1, edgecolors="black", alpha=0.2))

        # Reference cube (1x1x1)
        x, y, z = 0, 0, 0
        dx, dy, dz = 1, 1, 1
        vertices = [[x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z], [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]]
        faces = [
            [vertices[j] for j in [0, 1, 2, 3]],
            [vertices[j] for j in [4, 5, 6, 7]],
            [vertices[j] for j in [0, 1, 5, 4]],
            [vertices[j] for j in [2, 3, 7, 6]],
            [vertices[j] for j in [1, 2, 6, 5]],
            [vertices[j] for j in [4, 7, 3, 0]],
        ]
        ax.add_collection3d(Poly3DCollection(faces, facecolors="orange", linewidths=1, edgecolors="black", alpha=0.6))

        # Set limits, labels, and aspect
        ax.set_xlim([0, 4])
        ax.set_ylim([0, 6])
        ax.set_zlim([0, 3])
        ax.set_xlabel("Length (units)")
        ax.set_ylabel("Width (units)")
        ax.set_zlabel("Height (units)")
        ax.set_box_aspect([4, 6, 3])

        # Set the scale of the axes to be 1 and equal
        ax.set_xticks(range(0, 4, 1))
        ax.set_yticks(range(0, 6, 1))
        ax.set_zticks(range(0, 3, 1))

        # Make the plot tight
        plt.tight_layout()

        return plt.gcf()

    return visualize_my_room_3d


@app.cell
def __(mo, visualize_rooms, visualize_my_room_3d, compare_by_area_exercises):
    compare_multiple_dimensions = mo.vstack(
        [
            mo.md(
                """
                ## Comparing Multiple Dimensions

                Comparing lengths is straightforward, but what about comparing objects that have more than one dimension?

                ### Comparing Room Sizes

                Let's say my living room is 4 meters wide and 6 meters long and yours is 5 meters wide and 5 meters long.

                *Which one is bigger?*

                It makes somehow sense to compare both lengths and widths.

                Shall we compare them one by one?

                * If we compare the lengths, my room is 6 meters long and yours is 5 meters long. *So my room is bigger.* 😍
                * If we compare the widths, my room is 4 meters wide and yours is 5 meters wide. *So your room is bigger.* 😢

                Shall we just add them? That would give us 10m for my room (6m + 4m) and 10 meters for yours (5m + 5m), *so they are equal*. 😐

                To make it easier to compare, let us visualize both rooms and show the length units for both sides.

                """
            ),
            visualize_rooms(),
            mo.md(
                """
                /// tip | Idea
                Now the rooms are made of same size parts, so we can easily compare them.
                We can count the number of parts in each room, and the room with more parts is bigger!
                ///

                Calculating how many parts each room has:

                * My room: \\( 4 + 4 + 4 + 4 + 4 + 4 = 4 \\times 6 = \\textbf{24 parts} \\)
                * Your room: \\( 5 + 5 + 5 + 5 + 5 = 5 \\times 5 = \\textbf{25 parts} \\)

                So your room is bigger! 🎉

                /// note | Definition

                What we've learned is that when comparing objects with two dimensions, we can just split them into smaller squared parts
                and count how many parts each object has. In mathematical terms, this is called the **area** of the object.

                For a rectangle, the **area** is calculated as:

                \\[
                \\text{Area} = \\text{Length} \\times \\text{Width}
                \\]

                The unit of area is the unit of length multiplied by itself. One calls it a **square unit**.
                For example, if the length and width are in meters, the area is in square meters (m²).

                ///

                """
            ),
            mo.md(
                """
                ## Converting Area Units

                Just like with lengths, we can use prefixes to express different orders of magnitude for areas.

                For example:

                * **kilo-** means 1,000, so 1 square kilometer (km²) is 1,000,000 square meters (m²).
                * **deci-** means one tenth of a square meter (dm²), so 1 m² = 100 dm².
                * **centi-** means one hundredth of a square meter (cm²), so 1 m² = 10,000 cm².
                * **milli-** means one thousandth of a square meter (mm²), so 1 m² = 1,000,000 mm².

                There are also special names for some common area units:

                * **hectare (ha)**: 1 hectare = 10,000 m² (used for measuring land). One hectare is a square with sides of 100 meters.
                * **are (a)**: 1 are = 100 m² (also used for measuring land). One are is a square with sides of 10 meters.

                /// tip | Todo

                Why is that one square kilometer is 1,000,000 square meters?
                Can you calculate it?

                Try to use the formula for area and the conversion between kilometers and meters.
                ///

                Let's us do it together:

                1 km = 1000 m, so:

                \\[
                1 \\text{ km}^2 = 1 \\text{ km} \\times 1 \\text{ km} = 1000 \\text{ m} \\times 1000 \\text{ m} = 1,000,000 \\text{ m}^2
                \\]

                """
            ),
            mo.md(
                """
                ### Exercises

                Let's practice calculating the area of some rectangles.

                /// tip | Todo
                Type the correct answer in the input fields below and press Enter to check your answer.
                Use `.` for decimal points, e.g. `1.5` for one and a half.
                ///

                """
            ),
            compare_by_area_exercises,
            mo.md(""),
            mo.md("---"),
            mo.md(""),
            mo.md(
                """
                ## How About Three Dimensions?

                /// tip | Todo
                Think about how you would compare objects that have three dimensions, like a box or your fridge.
                How would you compare their sizes?
                ///

                In the same way we went from one dimension (length) to two dimensions (area),
                we can go from two dimensions (area) to three dimensions (volume).

                /// note | Definition

                The **volume** of an object is the amount of space it occupies in three dimensions.
                For a rectangular box, the volume is calculated as:

                \\[
                \\text{Volume} = \\text{Length} \\times \\text{Width} \\times \\text{Height}
                \\]

                The unit of volume is the unit of length multiplied by itself three times. One calls it a **cubic unit**.
                For example, if the length, width, and height are in meters, the volume is in cubic meters (m³).
                ///

                """
            ),
            visualize_my_room_3d(),
            mo.md(
                """
                /// tip | Todo
                Can you calculate the volume of my room?
                Use the formula for volume and the dimensions of the room.
                ///

                The dimensions of my room are 4 meters wide, 6 meters long, and 3 meters high:

                \\[
                \\text{Volume} = 4 \\text{ m} \\times 6 \\text{ m} \\times 3 \\text{ m} = 72 \\text{ m}^3
                \\]

                So my room has a volume of 72 cubic meters (m³).

                """
            ),
        ]
    )
    return (compare_multiple_dimensions,)


@app.cell
def __(mo):
    triangle_peak = mo.ui.slider(label="Set the triangle peak position: ", start=0, stop=6, step=1, value=4)
    return (triangle_peak,)


@app.cell
def __(triangle_peak):
    def plot_triangle_and_rectangle():
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon, Rectangle

        base = 6
        height = 4
        fig, ax = plt.subplots(figsize=(6, 5))
        # Draw rectangle
        rect = Rectangle((0, 0), base, height, fill=True, color="lightblue", alpha=0.4)
        ax.add_patch(rect)
        # Draw the triangle
        triangle = Polygon([[0, 0], [base, 0], [triangle_peak.value, height]], closed=True, color="orange", alpha=0.4)
        ax.add_patch(triangle)
        # Draw base line
        ax.plot([0, base], [0, 0], color="black", lw=2)
        # Draw height line
        ax.plot([triangle_peak.value, triangle_peak.value], [0, height], color="red", lw=2)
        # Annotations
        ax.text(base / 2, -0.5, "base = 6", ha="center", va="top", fontsize=12)
        ax.text(triangle_peak.value, height / 2, "height = 4", ha="right", va="center", fontsize=12, rotation=90, color="red")
        # Set limits and aspect
        ax.set_xlim(-1, base + 1)
        ax.set_ylim(-1, height + 1)
        ax.set_aspect("equal")
        ax.axis("off")

        # Make the plot tight
        plt.tight_layout()

        return plt.gcf()

    return plot_triangle_and_rectangle


@app.cell
def __(mo, plot_triangle_and_rectangle, triangle_peak):
    calculate_are_of_a_triangle = mo.vstack(
        [
            mo.md("""
            ## Area of a Triangle

            Let's take a look at how to calculate the area of a triangle using what we have learned so far.

            We know how to calculate the area of a rectangle, so we can try to put our triangle inside a rectangle.
            See below how the triangle fits inside the rectangle.

            /// note | Todo
            You can use the slider to change the position of the triangle peak.
            ///

            """),
            mo.vstack(
                [
                    triangle_peak,
                    plot_triangle_and_rectangle(),
                ],
                gap=0,
                justify="center",
            ),
            mo.md("""

            /// tip | Todo

            * How much of the rectangle is orange?
            * Does it change if you move the triangle peak?

            ///

            You can split the figure in left and right parts of the height.
            On the left side rectangle, half of it is orange and on the right side rectangle, half of it is orange.

            This means that half of the rectangle is orange, so the area of the triangle is half the area of the rectangle.
            This is true for any triangle, regardless of where the peak is located!

            /// note | Formula
            The area of a triangle is always half the area of a rectangle with the same base and height:

            \\[
            \\text{Area}_{\\text{triangle}} = \\frac{1}{2} \\times \\text{base} \\times \\text{height}
            \\]

            ///
            """),
        ]
    )
    return (calculate_are_of_a_triangle,)


@app.cell
def __(mo, intro_text, compare_by_length, compare_by_length_exercises, compare_multiple_dimensions, calculate_are_of_a_triangle):
    mo.vstack(
        [
            intro_text,
            compare_by_length,
            compare_by_length_exercises,
            mo.md(""),
            mo.md("---"),
            mo.md(""),
            compare_multiple_dimensions,
            calculate_are_of_a_triangle,
        ],
        gap=1,
    )


@app.cell
def __():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
