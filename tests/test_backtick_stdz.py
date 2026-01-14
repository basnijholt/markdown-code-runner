"""Test the standardization functionality of markdown-code-runner."""

from pathlib import Path

import pytest

from markdown_code_runner import (
    ProcessingState,
    _extract_backtick_options,
    process_markdown,
    standardize_code_fences,
    update_markdown_file,
)


def test_extract_backtick_options_without_markdown_code_runner() -> None:
    """Test _extract_backtick_options with basic language extraction."""
    # Test simple language extraction
    assert _extract_backtick_options("```python") == {"language": "python"}
    assert _extract_backtick_options("```javascript") == {"language": "javascript"}

    # Test with spaces and other content
    assert _extract_backtick_options("```python some other text") == {
        "language": "python",
    }
    assert _extract_backtick_options("```rust ") == {"language": "rust"}

    # Test invalid/empty cases
    assert _extract_backtick_options("```") == {}
    assert _extract_backtick_options("some random text") == {}


def test_extract_backtick_options_with_markdown_code_runner() -> None:
    """Test _extract_backtick_options with markdown-code-runner."""
    # Test with markdown-code-runner and options
    assert _extract_backtick_options(
        "```python markdown-code-runner filename=test.py",
    ) == {
        "language": "python",
        "filename": "test.py",
    }

    # Test with multiple options
    assert _extract_backtick_options(
        "```javascript markdown-code-runner filename=test.js debug=true",
    ) == {
        "language": "javascript",
        "filename": "test.js",
        "debug": "true",
    }


def test_process_markdown_standardization() -> None:
    """Test process_markdown with standardization enabled/disabled."""
    input_lines = [
        "# Test markdown",
        "```python markdown-code-runner filename=test.py",
        "print('hello')",
        "```",
        "Some text",
        "```javascript",
        "console.log('hi')",
        "```",
    ]

    # Test with standardization enabled (default)
    output = process_markdown(input_lines)
    assert output[1] == "```python"  # markdown-code-runner should be removed
    assert output[5] == "```javascript"  # unchanged

    # Test with standardization disabled
    output = process_markdown(input_lines, backtick_standardize=False)
    assert output[1] == "```python markdown-code-runner filename=test.py"  # preserved
    assert output[5] == "```javascript"  # unchanged


def test_process_markdown_mixed_blocks() -> None:
    """Test process_markdown with mixed block types."""
    input_lines = [
        "# Mixed blocks",
        "```python markdown-code-runner filename=test.py debug=true",
        "x = 1",
        "```",
        "Normal block:",
        "```python",
        "y = 2",
        "```",
        "Another runner block:",
        "```javascript markdown-code-runner filename=test.js",
        "let z = 3;",
        "```",
    ]

    # With standardization
    output = process_markdown(input_lines)
    assert output[1] == "```python"
    assert output[5] == "```python"
    assert output[9] == "```javascript"

    # Without standardization
    output = process_markdown(input_lines, backtick_standardize=False)
    assert output[1] == "```python markdown-code-runner filename=test.py debug=true"
    assert output[5] == "```python"
    assert output[9] == "```javascript markdown-code-runner filename=test.js"


def test_update_markdown_file_standardization(tmp_path: Path) -> None:
    """Test update_markdown_file with standardization options."""
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test_output.md"

    content = """# Test
```python markdown-code-runner filename=test.py
print('hello')
```
Some text
```javascript
console.log('hi')
```"""

    input_file.write_text(content)

    # Test with output file (standardization enabled by default)
    update_markdown_file(input_file, output_file)
    output_content = output_file.read_text()
    assert "markdown-code-runner" not in output_content
    assert "```python\n" in output_content

    # Test with output file (standardization disabled)
    update_markdown_file(input_file, output_file, backtick_standardize=False)
    output_content = output_file.read_text()
    assert "markdown-code-runner" in output_content

    # Test in-place editing (should not standardize by default)
    update_markdown_file(input_file, backtick_standardize=False)
    input_content = input_file.read_text()
    assert "markdown-code-runner" in input_content


def test_process_backticks_start() -> None:
    """Test the backtick standardization logic via _process_start_markers."""
    # Test with standardization enabled
    state = ProcessingState(backtick_standardize=True)

    # Should remove markdown-code-runner and options
    line = "```python markdown-code-runner filename=test.py"
    result = state._process_start_markers(line)
    assert result == "```python"

    # Should preserve non-markdown-code-runner content
    line = "```javascript some other content"
    result = state._process_start_markers(line)
    assert result is None  # Not a marker, so returns None

    # Test with standardization disabled
    state = ProcessingState(backtick_standardize=False)

    # Should preserve everything
    line = "```python markdown-code-runner filename=test.py"
    result = state._process_start_markers(line)
    assert result == line

    # Non-marker line should return None
    line = "```javascript some other content"
    result = state._process_start_markers(line)
    assert result is None


def test_standardize_code_fences() -> None:
    """Test the standardize_code_fences utility function."""
    # Basic case
    content = """# Example
```python markdown-code-runner
print('hello')
```
Some text
```javascript
console.log('hi')
```"""
    expected = """# Example
```python
print('hello')
```
Some text
```javascript
console.log('hi')
```"""
    assert standardize_code_fences(content) == expected

    # With options
    content = """```python markdown-code-runner filename=test.py debug=true
code here
```"""
    expected = """```python
code here
```"""
    assert standardize_code_fences(content) == expected

    # Multiple occurrences
    content = """```python markdown-code-runner
first
```
text
```bash markdown-code-runner
second
```
more text
```rust markdown-code-runner filename=test.rs
third
```"""
    expected = """```python
first
```
text
```bash
second
```
more text
```rust
third
```"""
    assert standardize_code_fences(content) == expected

    # Text references should be preserved
    content = """Using `markdown-code-runner` is easy.
```python markdown-code-runner
code
```"""
    expected = """Using `markdown-code-runner` is easy.
```python
code
```"""
    assert standardize_code_fences(content) == expected


def test_process_markdown_execute_flag() -> None:
    """Test process_markdown with execute=False."""
    input_lines = [
        "# Test",
        "```python markdown-code-runner",
        "print('hello')",
        "```",
        "<!-- OUTPUT:START -->",
        "old output",
        "<!-- OUTPUT:END -->",
    ]

    # With execute=False, content should pass through unchanged
    output = process_markdown(input_lines, execute=False)
    assert output == input_lines

    # With execute=True (default), code should be executed
    output = process_markdown(input_lines, execute=True, backtick_standardize=False)
    assert "hello" in "\n".join(output)
    assert "old output" not in "\n".join(output)


def test_update_markdown_file_execute_flag(tmp_path: Path) -> None:
    """Test update_markdown_file with execute=False."""
    input_file = tmp_path / "test.md"

    content = """# Test
```python markdown-code-runner
print('hello')
```
<!-- OUTPUT:START -->
old output
<!-- OUTPUT:END -->"""

    input_file.write_text(content)

    # Test with execute=False - content should be unchanged
    update_markdown_file(input_file, execute=False)
    result = input_file.read_text()
    assert "old output" in result  # Output not updated

    # Restore content
    input_file.write_text(content)

    # Test with execute=True (default) - code should run
    update_markdown_file(input_file, execute=True, backtick_standardize=False)
    result = input_file.read_text()
    assert "hello" in result
    assert "old output" not in result


def test_update_markdown_file_standardize_flag(tmp_path: Path) -> None:
    """Test update_markdown_file with standardize=True."""
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "output.md"

    # Content with code fence and text reference to markdown-code-runner
    content = """# Test
Using `markdown-code-runner` is great!
```python markdown-code-runner
print('hello')
```
<!-- OUTPUT:START -->
old output
<!-- OUTPUT:END -->
```bash markdown-code-runner
echo "test"
```
<!-- OUTPUT:START -->
old bash output
<!-- OUTPUT:END -->"""

    input_file.write_text(content)

    # Test with standardize=True - all code fences should be cleaned
    update_markdown_file(input_file, output_file, standardize=True)
    result = output_file.read_text()

    # Code fences should be standardized
    assert "```python\n" in result
    assert "```bash\n" in result
    assert "```python markdown-code-runner" not in result
    assert "```bash markdown-code-runner" not in result

    # Text references should be preserved
    assert "`markdown-code-runner`" in result

    # Code should have executed
    assert "hello" in result
    assert "test" in result
    assert "old output" not in result


def test_update_markdown_file_standardize_without_execute(tmp_path: Path) -> None:
    """Test update_markdown_file with standardize=True and execute=False."""
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "output.md"

    content = """# Test
```python markdown-code-runner
print('hello')
```
<!-- OUTPUT:START -->
old output
<!-- OUTPUT:END -->"""

    input_file.write_text(content)

    # Test with standardize=True and execute=False
    update_markdown_file(input_file, output_file, execute=False, standardize=True)
    result = output_file.read_text()

    # Code fences should be standardized
    assert "```python\n" in result
    assert "```python markdown-code-runner" not in result

    # Code should NOT have executed (execute=False)
    # The auto-generated warning should not appear
    assert "old output" in result
    assert "auto-generated" not in result


def test_update_markdown_file_standardize_verbose(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test update_markdown_file with standardize=True and verbose=True."""
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "output.md"

    content = """# Test
```python markdown-code-runner
print('hello')
```
<!-- OUTPUT:START -->
old output
<!-- OUTPUT:END -->"""

    input_file.write_text(content)

    # Test with standardize=True and verbose=True
    update_markdown_file(
        input_file,
        output_file,
        execute=False,
        standardize=True,
        verbose=True,
    )

    captured = capsys.readouterr()
    assert "Standardizing all code fences" in captured.out
