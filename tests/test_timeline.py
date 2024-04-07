from pathlib import Path

from jarvis.timeline import Timeline, TimelineEntry, TimelineWriter


def test_timeline(tmp_path: Path) -> None:
    timeline = Timeline(
        entries=[
            TimelineEntry(year=2021, title="First entry.", description="First description."),
            TimelineEntry(year=2022, title="Second entry.", description="Second description."),
        ]
    )

    input_json_file = tmp_path / "timeline.json"
    output_md_file = tmp_path / "timeline.md"

    timeline.to_json_file(input_json_file)

    writer = TimelineWriter(input_json_file, output_md_file)
    writer.write()

    assert output_md_file.exists()
    assert (
        output_md_file.read_text()
        == """\
`````{grid} 2
:class-container: timeline


````{grid-item-card}
:class-item: entry left
<!-- ------------------------------------------------------------------------- -->

**2021** First entry.
^^^

First description.

````


````{grid-item}
:class: right
````
````{grid-item}
:class: left
````
````{grid-item-card}
:class-item: entry right
<!-- ------------------------------------------------------------------------- -->

**2022** Second entry.
^^^

Second description.

````


````{grid-item}
:class: left
````
````{grid-item}
:class: right
````


`````"""
    )
