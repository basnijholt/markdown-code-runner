---
icon: lucide/code
---

# Python API

<!-- CODE:START -->
<!-- from docs_gen import readme_section -->
<!-- print(readme_section("python-api")) -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

## Function Reference

### `update_markdown_file`

The main function for processing Markdown files.

```python
def update_markdown_file(
    input_filepath: Path | str,
    output_filepath: Path | str | None = None,
    *,
    verbose: bool = False,
    backtick_standardize: bool = True,
    execute: bool = True,
    standardize: bool = False,
) -> None:
    """Rewrite a Markdown file by executing and updating code blocks.

    Parameters
    ----------
    input_filepath : Path | str
        Path to the input Markdown file.
    output_filepath : Path | str | None
        Path to the output Markdown file. If None, overwrites input file.
    verbose : bool
        If True, print every line that is processed.
    backtick_standardize : bool
        If True, clean up markdown-code-runner string from executed backtick code blocks.
    execute : bool
        If True, execute code blocks and update output sections.
        If False, skip code execution (useful with standardize=True).
    standardize : bool
        If True, post-process to standardize ALL code fences in the output,
        removing 'markdown-code-runner' modifiers. This is useful for
        compatibility with markdown processors like mkdocs and pandoc.
    """
```

### `process_markdown`

Lower-level function for processing Markdown content as a list of strings.

```python
def process_markdown(
    content: list[str],
    *,
    verbose: bool = False,
    backtick_standardize: bool = True,
    execute: bool = True,
) -> list[str]:
    """Execute code blocks in a list of Markdown-formatted strings.

    Parameters
    ----------
    content
        A list of Markdown-formatted strings.
    verbose
        If True, print every line that is processed.
    backtick_standardize
        If True, clean up markdown-code-runner string from executed backtick code blocks.
    execute
        If True, execute code blocks and update output sections.
        If False, return content unchanged.

    Returns
    -------
    list[str]
        A modified list of Markdown-formatted strings with code block output inserted.
    """
```

### `standardize_code_fences`

Utility function to strip `markdown-code-runner` modifiers from code fence language identifiers.

```python
def standardize_code_fences(content: str) -> str:
    """Strip markdown-code-runner modifiers from all code fence language identifiers.

    This is useful for making markdown files compatible with standard markdown
    processors like mkdocs and pandoc.

    Parameters
    ----------
    content
        The markdown content as a string.

    Returns
    -------
    str
        The content with all code fence modifiers stripped.
    """
```

## Examples

### Basic Usage

```python
from markdown_code_runner import update_markdown_file

# Update a Markdown file in-place
update_markdown_file("README.md")

# Write to a different file
update_markdown_file("README.md", "README_updated.md")

# Enable verbose output
update_markdown_file("README.md", verbose=True)
```

### Processing Content Directly

```python
from markdown_code_runner import process_markdown

content = [
    "<!-- CODE:START -->",
    "<!-- print('Hello, world!') -->",
    "<!-- CODE:END -->",
    "<!-- OUTPUT:START -->",
    "This will be replaced.",
    "<!-- OUTPUT:END -->",
]

result = process_markdown(content)
print("\n".join(result))
```

### Batch Processing Multiple Files

```python
from pathlib import Path
from markdown_code_runner import update_markdown_file

docs_dir = Path("docs")
for md_file in docs_dir.rglob("*.md"):
    if "<!-- CODE:START -->" in md_file.read_text():
        print(f"Processing {md_file}...")
        update_markdown_file(md_file)
```

### Standardizing Code Fences for External Processors

```python
from markdown_code_runner import update_markdown_file

# Execute code AND standardize all code fences
update_markdown_file("README.md", "docs/README.md", standardize=True)

# Only standardize without executing code
update_markdown_file("README.md", "docs/README.md", execute=False, standardize=True)
```

### Using the Standardize Function Directly

```python
from markdown_code_runner import standardize_code_fences

content = """
```python markdown-code-runner
print('hello')
```
"""

# Remove markdown-code-runner modifiers
clean_content = standardize_code_fences(content)
print(clean_content)
# Output:
# ```python
# print('hello')
# ```
```
