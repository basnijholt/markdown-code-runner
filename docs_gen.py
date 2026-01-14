"""Documentation generation utilities for Markdown Code Runner.

Provides functions to extract sections from README.md and transform
content for the documentation site. Used by markdown-code-runner
to generate documentation pages from README content.
"""

from __future__ import annotations

import re
from pathlib import Path

# Path to README relative to this module
_MODULE_DIR = Path(__file__).parent
README_PATH = _MODULE_DIR / "README.md"


def readme_section(section_name: str, *, strip_heading: bool = True) -> str:
    """Extract a marked section from README.md.

    Sections are marked with HTML comments:
    <!-- SECTION:section_name:START -->
    content
    <!-- SECTION:section_name:END -->

    Args:
        section_name: The name of the section to extract
        strip_heading: If True, remove the first heading from the section

    Returns:
        The content between the section markers

    Raises:
        ValueError: If the section is not found in README.md

    """
    content = README_PATH.read_text()

    start_marker = f"<!-- SECTION:{section_name}:START -->"
    end_marker = f"<!-- SECTION:{section_name}:END -->"

    start_idx = content.find(start_marker)
    if start_idx == -1:
        msg = f"Section '{section_name}' not found in README.md"
        raise ValueError(msg)

    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        msg = f"End marker for section '{section_name}' not found"
        raise ValueError(msg)

    section = content[start_idx + len(start_marker) : end_idx].strip()

    if strip_heading:
        # Remove first heading (# or ## or ###)
        section = re.sub(r"^#{1,3}\s+[^\n]+\n+", "", section, count=1)

    return _transform_readme_links(section)


def _transform_readme_links(content: str) -> str:
    """Transform README internal links to docs site links."""
    # Map README anchors to doc pages
    link_map = {
        "#computer-installation": "getting-started.md#installation",
        "#rocket-quick-start": "getting-started.md#quick-start",
        "#snake-python-api": "usage/python-api.md",
        "#book-examples": "examples.md",
        "#bulb-usage-ideas": "examples.md#usage-ideas",
        "#gear-idea-1-continuous-integration-with-github-actions": "usage/github-actions.md",
        "#page_with_curl-license": "index.md#license",
        "#handshake-contributing": "contributing.md",
        "#star-features": "index.md#features",
        "#question-problem-statement": "index.md#why-use-markdown-code-runner",
    }

    for old_link, new_link in link_map.items():
        content = content.replace(f"]({old_link})", f"]({new_link})")

    # Remove ToC link pattern [[ToC](#...)]
    content = re.sub(r"\[\[ToC\]\([^)]+\)\]", "", content)

    # Escape markdown-code-runner markers in extracted content to prevent re-execution
    # Add a zero-width space after "<!-" to break the marker pattern
    marker_patterns = [
        ("<!-- CODE:START -->", "<!\u200b-- CODE:START -->"),
        ("<!-- CODE:END -->", "<!\u200b-- CODE:END -->"),
        ("<!-- CODE:BASH:START -->", "<!\u200b-- CODE:BASH:START -->"),
        ("<!-- CODE:SKIP -->", "<!\u200b-- CODE:SKIP -->"),
        ("<!-- OUTPUT:START -->", "<!\u200b-- OUTPUT:START -->"),
        ("<!-- OUTPUT:END -->", "<!\u200b-- OUTPUT:END -->"),
    ]
    for old, new in marker_patterns:
        content = content.replace(old, new)

    # Also escape backtick code blocks that trigger execution
    # Replace "```python markdown-code-runner" with escaped version
    return re.sub(
        r"```(\w+)\s+markdown-code-runner",
        r"```\1 markdown-code-runner\u200b",  # Add zero-width space at end
        content,
    )
