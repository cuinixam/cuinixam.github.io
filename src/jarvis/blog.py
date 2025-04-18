import textwrap
from datetime import datetime
from pathlib import Path


class BlogWritter:
    def __init__(self, output_dir: Path, title: str, category: str | None = None, tags: list[str] | None = None) -> None:
        self.output_dir = output_dir
        self.title = title
        self.category = category or "uncategorized"
        self.tags = tags or []

    @property
    def blog_filename(self) -> str:
        return f"{self.title.lower().replace(' ', '_')}.md"

    @property
    def blog_file(self) -> Path:
        """output_dir / <year> / blog_filename."""
        return self.output_dir / datetime.now().strftime("%Y") / self.blog_filename

    def write(self) -> None:
        """
        Create a new blog post with the given title.

        The name of the file is derived from the title.
        The content of the file is empty.
        """
        self.blog_file.parent.mkdir(parents=True, exist_ok=True)
        self.blog_file.write_text(self.new_blog_content())

    def new_blog_content(self) -> str:
        """Return the content of a new blog post with the given title."""
        return textwrap.dedent(f"""\
            ---
            tags: {", ".join(self.tags)}
            category: {self.category}
            date: {datetime.now().strftime("%Y-%m-%d")}
            title: {self.title}
            ---

            # {self.title}

            ## Introduction

            Start writing your blog post here.
            """)
