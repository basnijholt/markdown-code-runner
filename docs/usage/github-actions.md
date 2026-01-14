---
icon: lucide/github
---

# GitHub Actions Integration

Automate your Markdown updates with CI/CD workflows.

## Continuous Integration with GitHub Actions

<!-- CODE:START -->
<!-- from docs_gen import readme_section -->
<!-- print(readme_section("github-actions")) -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

## Workflow Breakdown

### Trigger Events

The workflow triggers on:

- **Push to main**: Update documentation when changes are merged
- **Pull requests**: Validate documentation changes in PRs

### Key Steps

1. **Checkout**: Clone the repository with full history for proper git operations
2. **Python Setup**: Configure Python environment
3. **Install Dependencies**: Install `markdown-code-runner` and any packages used in your code blocks
4. **Run Processing**: Execute `markdown-code-runner` on your Markdown files
5. **Commit & Push**: Automatically commit any changes

## Advanced Configurations

### Processing Multiple Files

To process multiple Markdown files, create a helper script using [PEP 723](https://peps.python.org/pep-0723/) inline script dependencies:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown-code-runner"]
# ///
"""Update all markdown files that use markdown-code-runner."""
from pathlib import Path

from markdown_code_runner import update_markdown_file


def find_markdown_files(root: Path) -> list[Path]:
    """Find all markdown files containing code markers."""
    files = []
    for md_file in root.rglob("*.md"):
        content = md_file.read_text()
        if "<!-- CODE:START -->" in content:
            files.append(md_file)
    return sorted(files)


def main():
    root = Path(".")
    files = find_markdown_files(root / "docs")

    # Also check README
    readme = root / "README.md"
    if readme.exists() and "<!-- CODE:START -->" in readme.read_text():
        files.append(readme)

    for f in files:
        print(f"Processing {f}...")
        update_markdown_file(f)


if __name__ == "__main__":
    main()
```

Run it with `uv run update_docs.py` or make it executable and run directly.

### Only Run on Specific Files

Limit when the workflow runs:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'docs/**/*.md'
      - 'README.md'
      - '.github/workflows/docs.yml'
```

## Troubleshooting

### Import Errors

If your code blocks import local modules, ensure they're installed:

```yaml
- name: Install local package
  run: pip install -e .
```

### Permission Issues

Ensure the workflow has write permissions:

```yaml
permissions:
  contents: write
```

### Token Issues

For pushing to protected branches, you may need a Personal Access Token:

```yaml
- name: Push changes
  uses: ad-m/github-push-action@master
  with:
    github_token: ${{ secrets.PAT_TOKEN }}
    branch: ${{ github.ref }}
```
