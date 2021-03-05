"""Script to generate README suitable for PyPI.

- Replace Sphinx directives (like :class: and :attr:)
  with plain reST inline literals.
- Replace final line (which has internal link to tutorial)
  with external links for tutorial and full documentation
  in Apteco Help Hub.

"""

import re
from pathlib import Path

DOCS_SOURCE = Path(__file__).parent / "source"

README_SOURCE = DOCS_SOURCE / "getting_started.rst"
README_OUT = DOCS_SOURCE / "readme.rst"


def generate_readme():
    """Generate PyPI-friendly README from quickstart guide."""
    lines = read_quickstart_lines()
    edited_lines = replace_sphinx_directives(lines)
    edited_lines = replace_final_line(edited_lines)
    write_readme_lines(edited_lines)


def read_quickstart_lines():
    """Read lines from quickstart guide source file."""
    with open(README_SOURCE, encoding="utf8") as f:
        lines = f.readlines()
    return lines


def replace_sphinx_directives(lines):
    """Replace Sphinx directives with reST inline literals."""
    directive_pattern = re.compile(r":(class|func|attr|mod):`([A-z_]*)`")
    edited_lines = [directive_pattern.sub(r"``\2``", line) for line in lines]
    return edited_lines


def replace_final_line(edited_lines):
    """Replace final line internal tutorial link with external links."""
    expected_final_line = (
        "For a more thorough introduction,"
        " check out the :ref:`tutorial`.\n"
    )
    new_final_line = (
        "You can find the complete documentation"
        "\nincluding a more thorough"
        " `tutorial <https://help.apteco.com/python/tutorial.html>`_"
        "\non the `Apteco website <https://help.apteco.com/python/index.html>`_."
    )

    final_line = edited_lines[-1]
    if final_line != expected_final_line:
        raise ValueError("Final line was different from expected.")
    edited_lines[-1] = new_final_line
    return edited_lines


def write_readme_lines(edited_lines):
    """Write edited line to README file."""
    with open(README_OUT, "w", encoding="utf8") as f:
        f.writelines(edited_lines)


if __name__ == "__main__":
    generate_readme()
