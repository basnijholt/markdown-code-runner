#!/usr/bin/env python3
# ruff: noqa: T201, S603, S607
"""Documentation generation utilities for Markdown Code Runner.

Provides functions to extract sections from README.md and transform
content for the documentation site. Used by markdown-code-runner
to generate documentation pages from README content.

Run from repo root: uv run python docs/docs_gen.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# Path to README relative to this module (docs_gen.py is in docs/)
_MODULE_DIR = Path(__file__).parent
README_PATH = _MODULE_DIR.parent / "README.md"


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

    # Escape markers only OUTSIDE code fences to prevent re-execution
    # Markers inside code fences are examples meant to be copied by users
    return _escape_markers_outside_fences(content)


def _escape_markers_outside_fences(content: str) -> str:
    """Escape markdown-code-runner markers only outside of code fences.

    This ensures:
    - Examples inside ```markdown``` fences stay clean and copyable
    - Working demos outside fences get escaped to prevent re-execution

    Handles nested fences correctly (e.g., ```` containing ```).
    """
    # Markers to escape with zero-width space after "<!"
    marker_patterns = [
        ("<!-- CODE:START -->", "<!\u200b-- CODE:START -->"),
        ("<!-- CODE:END -->", "<!\u200b-- CODE:END -->"),
        ("<!-- CODE:BASH:START -->", "<!\u200b-- CODE:BASH:START -->"),
        ("<!-- CODE:SKIP -->", "<!\u200b-- CODE:SKIP -->"),
        ("<!-- OUTPUT:START -->", "<!\u200b-- OUTPUT:START -->"),
        ("<!-- OUTPUT:END -->", "<!\u200b-- OUTPUT:END -->"),
    ]

    # Pattern to match executable code blocks
    executable_block_pattern = re.compile(r"```(\w+)\s+markdown-code-runner")

    # Pattern to detect fence opening/closing (captures the fence characters)
    fence_pattern = re.compile(r"^(\s*)(`{3,}|~{3,})")

    lines = content.split("\n")
    result = []
    fence_delimiter: str | None = None  # Track the opening fence delimiter

    for line in lines:
        match = fence_pattern.match(line)
        if match:
            fence_chars = match.group(2)
            if fence_delimiter is None:
                # Opening a new fence - remember the delimiter
                fence_delimiter = fence_chars[0] * len(fence_chars)
                result.append(line)
                continue
            # Check if this closes the current fence (same char, at least same length)
            if fence_chars[0] == fence_delimiter[0] and len(fence_chars) >= len(
                fence_delimiter,
            ):
                # Closing the fence
                fence_delimiter = None
                result.append(line)
                continue
            # Otherwise it's a nested fence marker, treat as content
            result.append(line)
            continue

        if fence_delimiter is None:
            # Outside any fence - escape markers
            escaped_line = line
            for old, new in marker_patterns:
                escaped_line = escaped_line.replace(old, new)
            # Escape executable code block markers
            escaped_line = executable_block_pattern.sub(
                r"```\1 markdown-code-runner" + "\u200b",
                escaped_line,
            )
            result.append(escaped_line)
        else:
            # Inside a fence - keep content unchanged
            result.append(line)

    return "\n".join(result)


def _find_markdown_files_with_code_blocks(docs_dir: Path) -> list[Path]:
    """Find all markdown files containing markdown-code-runner markers."""
    files_with_code = []
    for md_file in docs_dir.rglob("*.md"):
        content = md_file.read_text()
        if "<!-- CODE:START -->" in content:
            files_with_code.append(md_file)
    return sorted(files_with_code)


def _run_markdown_code_runner(files: list[Path], repo_root: Path) -> bool:
    """Run markdown-code-runner on all files. Returns True if all succeeded."""
    if not files:
        print("No files with CODE:START markers found.")
        return True

    print(f"Found {len(files)} file(s) with auto-generated content:")
    for f in files:
        print(f"  - {f.relative_to(repo_root)}")
    print()

    # Set PYTHONPATH to include docs/ so this module is importable
    env = os.environ.copy()
    python_path = env.get("PYTHONPATH", "")
    docs_dir = str(repo_root / "docs")
    env["PYTHONPATH"] = f"{docs_dir}:{python_path}" if python_path else docs_dir

    all_success = True
    for file in files:
        rel_path = file.relative_to(repo_root)
        print(f"Updating {rel_path}...", end=" ", flush=True)
        result = subprocess.run(
            ["markdown-code-runner", str(file)],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode == 0:
            print("OK")
        else:
            print("FAILED")
            print(f"  Error: {result.stderr}")
            all_success = False

    return all_success


def main() -> int:
    """Main entry point for running markdown-code-runner on all docs."""
    repo_root = _MODULE_DIR.parent

    # Process docs/ files and README.md
    files = _find_markdown_files_with_code_blocks(repo_root / "docs")
    readme = repo_root / "README.md"
    if readme.exists() and "<!-- CODE:START -->" in readme.read_text():
        files.append(readme)

    success = _run_markdown_code_runner(files, repo_root)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
