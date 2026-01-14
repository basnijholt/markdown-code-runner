---
icon: lucide/terminal
---

# Command Line Interface

`markdown-code-runner` provides a command-line interface for processing Markdown files.

## Basic Usage

```bash
markdown-code-runner /path/to/your/markdown_file.md
```

This will process the file in-place, executing all code blocks and updating the output sections.

## Help Output

<!-- CODE:START -->
<!-- import subprocess -->
<!-- result = subprocess.run(["markdown-code-runner", "--help"], capture_output=True, text=True) -->
<!-- print("```") -->
<!-- print(result.stdout) -->
<!-- print("```") -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

## Options

### Input File (Required)

The path to the Markdown file to process.

```bash
markdown-code-runner README.md
```

### Output File (`-o`, `--output`)

Write the result to a different file instead of modifying in-place.

```bash
markdown-code-runner README.md -o README_updated.md
```

### Verbose Mode (`-d`, `--verbose`)

Enable verbose output to see each line being processed.

```bash
markdown-code-runner README.md --verbose
```

### Disable Backtick Standardization (`--no-backtick-standardize`)

By default, when writing to a separate output file, the `markdown-code-runner` tag is removed from backtick code blocks. Use this flag to disable that behavior.

```bash
markdown-code-runner README.md -o output.md --no-backtick-standardize
```

### Standardize All Code Fences (`-s`, `--standardize`)

Post-process the output to standardize ALL code fences, removing `markdown-code-runner` modifiers from language identifiers. This is useful for compatibility with markdown processors like mkdocs and pandoc that don't understand the `python markdown-code-runner` syntax.

```bash
markdown-code-runner README.md --standardize
```

This transforms code fences like:

````markdown
```python markdown-code-runner
print('hello')
```
````

Into standard code fences:

````markdown
```python
print('hello')
```
````

### Skip Code Execution (`-n`, `--no-execute`)

Skip code execution entirely. This is useful when you only want to standardize code fences without running any code.

```bash
markdown-code-runner README.md --no-execute --standardize
```

This combination is particularly useful for:

- Preparing files for external markdown processors
- Converting files without re-running code blocks
- Creating compatible output from existing processed files

### Version (`-v`, `--version`)

Display the installed version.

```bash
markdown-code-runner --version
```

## Examples

### Process a Single File

```bash
markdown-code-runner docs/index.md
```

### Process Multiple Files

```bash
for f in docs/*.md; do
    markdown-code-runner "$f"
done
```

### Process All Files in a Directory

```bash
find docs -name "*.md" -exec markdown-code-runner {} \;
```

### Process with Verbose Output

```bash
markdown-code-runner README.md --verbose
```
