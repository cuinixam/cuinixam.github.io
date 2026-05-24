# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
from pathlib import Path

project_root_path = Path(__file__).parent.parent

for path in ["src", "tests"]:
    sys.path.insert(0, project_root_path.joinpath(path).as_posix())


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Alexandru Maxiniuc"
copyright = "2024, Alexandru Maxiniuc"
author = "Alexandru Maxiniuc"
release = "0.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

# https://github.com/executablebooks/sphinx-design
extensions.append("sphinx_design")

extensions.append("ablog")

# https://myst-parser.readthedocs.io/en/latest/intro.html
extensions.append("myst_parser")

myst_enable_extensions = ["colon_fence", "deflist", "html_admonition", "html_image", "attrs_inline"]

# mermaid config - @see https://pypi.org/project/sphinxcontrib-mermaid/
extensions.append("sphinxcontrib.mermaid")

# Configure extensions for include doc-strings from code
extensions.extend(
    [
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
    ]
)

# The suffix of source filenames.
source_suffix = [
    ".md",
]

templates_path = ["_templates"]
# about.md is the prose source for the jarvis-rendered about.html — Sphinx no longer renders it.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "presentations", "about.md"]

# copy button for code block
extensions.append("sphinx_copybutton")

extensions.append("sphinx_togglebutton")

# -- HTML output ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_logo = "_static/bio-photo-circle.png"
html_title = "Alexandru Maxiniuc"
# Filament theme: single dark palette, no light/dark switcher.
# `default_mode` belongs in html_context, not html_theme_options.
html_context = {"default_mode": "dark"}
html_theme_options = {
    "navbar_end": ["navbar-icon-links"],
    # Right sidebar (page TOC) only adds value on long-form blog posts.
    # Explicit page list avoids wildcard overlap warnings between ** and blogs/**.
    "secondary_sidebar_items": {
        "index": [],
        "timeline": [],
        "projects": [],
        "blogs/**": ["page-toc"],
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/cuinixam/",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/in/alexandru-maxiniuc-53604612",
            "icon": "fa-brands fa-linkedin",
        },
        {
            "name": "Blog RSS feed",
            "url": "https://maxiniuc.com/blogs/atom.xml",
            "icon": "fa-solid fa-rss",
        },
    ],
}

# Filament: warm-toned syntax highlighting for code blocks.
pygments_dark_style = "gruvbox-dark"
html_last_updated_fmt = ""
html_static_path = ["_static"]

html_sidebars = {
    "index": ["hello.html"],
    "projects": ["hello.html"],
    "blogs": ["ablog/categories.html"],
    "blogs/**": ["ablog/recentposts.html"],
}

# Presentations and notebooks are no longer copied by Sphinx — jarvis landing handles them.
html_extra_path = []

# -- ABlog ---------------------------------------------------

blog_baseurl = "https://maxiniuc.com"
blog_title = "Alexandru Maxiniuc"
blog_path = "blogs"
blog_post_pattern = "blogs/*/*"
blog_feed_fulltext = True
fontawesome_included = True
post_redirect_refresh = 1
post_auto_image = 1
post_auto_excerpt = 2


def setup(app):
    app.add_css_file("filament.css")
    app.add_css_file("custom.css")
    app.add_css_file("lessons.css")
