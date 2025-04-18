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
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "presentations"]

# copy button for code block
extensions.append("sphinx_copybutton")

# -- HTML output ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_logo = "_static/bio-photo-circle.png"
html_title = "Alexandru Maxiniuc"
html_theme_options = {
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
html_last_updated_fmt = ""
html_static_path = ["_static"]

html_sidebars = {
    "index": ["hello.html"],
    "about": ["hello.html"],
    "presentations": ["hello.html"],
    "teaching": ["hello.html"],
    "projects": ["hello.html"],
    "blogs": ["ablog/categories.html", "ablog/tagcloud.html", "ablog/archives.html"],
    "blogs/**": [
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/archives.html",
    ],
}

html_extra_path = ["presentations", "notebooks"]

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
    app.add_css_file("custom.css")
