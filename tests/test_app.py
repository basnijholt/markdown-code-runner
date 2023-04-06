"""Test the markdown_code_runner app."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from unittest.mock import patch

import pytest

from markdown_code_runner import (
    MARKERS,
    PATTERNS,
    execute_code,
    extract_extra,
    main,
    markers_to_patterns,
    md_comment,
    process_markdown,
    remove_md_comment,
)

TEST_FOLDER = Path(__file__).parent


def assert_process(input_lines: list[str], expected_output: list[str]) -> None:
    """Assert that the process_markdown function returns the expected output."""
    output = process_markdown(input_lines, verbose=True)
    assert output == expected_output, f"Expected\n{expected_output}\ngot\n{output}"


def test_process_markdown() -> None:
    """Test the process_markdown function."""
    # Test case 1: Single code block
    input_lines = [
        "Some text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        "Which will procure the following output:",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = [
        "Some text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        "Which will procure the following output:",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test case 2: Two code blocks
    input_lines = [
        "Some text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello again!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello again!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello again!",
        "",
        MARKERS["output:end"],
    ]
    assert_process(input_lines, expected_output)

    # Test case 3: No code blocks
    input_lines = [
        "Some text",
        "More text",
    ]
    expected_output = [
        "Some text",
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test case 4: Single code block with skip marker
    input_lines = [
        "Some text",
        MARKERS["skip"],
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = input_lines
    assert_process(input_lines, expected_output)

    # Test case 5: Skip marker at first code block, execute second code block
    input_lines = [
        "Some text",
        MARKERS["skip"],
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello again!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        MARKERS["skip"],
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello again!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello again!",
        "",
        MARKERS["output:end"],
    ]
    assert_process(input_lines, expected_output)


def test_remove_md_comment() -> None:
    """Test the remove_md_comment function."""
    input_str = "<!-- This is a comment -->"
    output_str = remove_md_comment(input_str)
    assert (
        output_str == "This is a comment"
    ), f"Expected 'This is a comment', got '{output_str}'"

    input_str = "This is not a comment"
    with pytest.raises(ValueError, match="Invalid Markdown comment format"):
        output_str = remove_md_comment(input_str)


def test_execute_code_block() -> None:
    """Test the execute_code function."""
    code = ["print('Hello, world!')"]
    output = execute_code(code)
    expected_output = ["Hello, world!", ""]
    assert output == expected_output, f"Expected {expected_output}, got {output}"


def test_main_no_arguments(tmp_path: Path) -> None:
    """Test the main function with no arguments."""
    test_filepath = TEST_FOLDER / "test.md"
    output_filepath = tmp_path / "output.md"
    expected_output_filepath = TEST_FOLDER / "test_expected_output.md"

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            input=test_filepath,
            output=None,
            verbose=False,
        ),
    ):
        main()
        assert output_filepath.exists() is False
        with test_filepath.open() as f1, expected_output_filepath.open() as f2:
            assert f1.read() == f2.read()


def test_main_filepath_argument(tmp_path: Path) -> None:
    """Test the main function with a filepath argument."""
    test_filepath = TEST_FOLDER / "test.md"
    output_filepath = tmp_path / "output.md"
    expected_output_filepath = TEST_FOLDER / "test_expected_output.md"

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            input=test_filepath,
            output=str(output_filepath),
            verbose=False,
        ),
    ):
        main()
        assert output_filepath.exists()
        with output_filepath.open() as f1, expected_output_filepath.open() as f2:
            assert f1.read() == f2.read()


def test_main_debug_mode(capfd: pytest.CaptureFixture, tmp_path: Path) -> None:
    """Test the main function with verbose mode enabled."""
    test_filepath = TEST_FOLDER / "test.md"
    output_filepath = tmp_path / "output.md"
    expected_output_filepath = TEST_FOLDER / "test_expected_output.md"

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            input=test_filepath,
            output=str(output_filepath),
            verbose=True,
        ),
    ):
        main()
        assert output_filepath.exists()
        with output_filepath.open() as f1, expected_output_filepath.open() as f2:
            assert f1.read() == f2.read()
        captured = capfd.readouterr()
        assert f"Processing input file: {test_filepath}" in captured.out
        assert f"Writing output to: {output_filepath}" in captured.out
        assert "Done!" in captured.out


def test_triple_backticks() -> None:
    """Test the triple-backticks code block."""
    # Test case 1: Single code block
    input_lines = [
        "Some text",
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = [
        "Some text",
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test case 2: Two code blocks
    input_lines = [
        "Some text",
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        "```python markdown-code-runner",
        "print('Hello again!')",
        "```",
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
        "```python markdown-code-runner",
        "print('Hello again!')",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello again!",
        "",
        MARKERS["output:end"],
    ]
    assert_process(input_lines, expected_output)

    # Test case 3: No code blocks
    input_lines = [
        "Some text",
        "More text",
    ]
    expected_output = [
        "Some text",
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test case 4: Single code block with skip marker
    input_lines = [
        "Some text",
        MARKERS["skip"],
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = input_lines
    assert_process(input_lines, expected_output)

    # Test case 5: Skip marker at first code block, execute second code block
    input_lines = [
        "Some text",
        MARKERS["skip"],
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        "This content will not be replaced because of skip marker",
        MARKERS["output:end"],
        "More text",
        "```python markdown-code-runner",
        "print('Hello again!')",
        "```",
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        MARKERS["skip"],
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        "This content will not be replaced because of skip marker",
        MARKERS["output:end"],
        "More text",
        "```python markdown-code-runner",
        "print('Hello again!')",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello again!",
        "",
        MARKERS["output:end"],
    ]
    assert_process(input_lines, expected_output)


def test_mix_md_and_triple_backticks() -> None:
    """Test the mixing of markdown code blocks and triple backticks."""
    input_lines = [
        # ``` code block
        "Some text",
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        "Which will procure the following output:",
        MARKERS["output:start"],
        "This content will be replaced.",
        MARKERS["output:end"],
        "More text",
        # ``` code block
        "```python markdown-code-runner",
        "print('Hello again!')",
        "```",
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
        # ``` code block that is skipped
        "Some text",
        MARKERS["skip"],
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        "This content will not be replaced because of skip marker",
        MARKERS["output:end"],
        # Md code block
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = [
        # ``` code block
        "Some text",
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        "Which will procure the following output:",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
        # ``` code block
        "```python markdown-code-runner",
        "print('Hello again!')",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello again!",
        "",
        MARKERS["output:end"],
        # ``` code block that is skipped
        "Some text",
        MARKERS["skip"],
        "```python markdown-code-runner",
        "print('Hello, world!')",
        "```",
        MARKERS["output:start"],
        "This content will not be replaced because of skip marker",
        MARKERS["output:end"],
        # Md code block
        MARKERS["code:comment:python:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
    ]
    assert_process(input_lines, expected_output)


def test_preserve_variables_between_code_blocks() -> None:
    """Test that variables are preserved between code blocks."""
    input_lines = [
        "Some text",
        "```python markdown-code-runner",
        "a = 1",
        "print(a)",
        "```",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        "```python markdown-code-runner",
        "print(a)",
        "```",
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        "```python markdown-code-runner",
        "a = 1",
        "print(a)",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "1",
        "",
        MARKERS["output:end"],
        "More text",
        "```python markdown-code-runner",
        "print(a)",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "1",
        "",
        MARKERS["output:end"],
    ]
    assert_process(input_lines, expected_output)


def test_two_code_blocks_but_first_without_output() -> None:
    """Test that two code blocks are executed even if the first one has no output block."""
    input_lines = [
        "Some text",
        "```python markdown-code-runner",
        "a = 1",
        "print('this will not be printed')",
        "```",
        "No output block here",
        "```python markdown-code-runner",
        "print(a)",
        "```",
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        "```python markdown-code-runner",
        "a = 1",
        "print('this will not be printed')",
        "```",
        "No output block here",
        "```python markdown-code-runner",
        "print(a)",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "1",
        "",
        MARKERS["output:end"],
    ]
    assert_process(input_lines, expected_output)


def test_bash() -> None:
    """Test that bash code is executed."""
    # Test case 1 (backticks): Single code block
    input_lines = [
        "Some text",
        "```bash markdown-code-runner",
        'echo "Hello, world!"',
        "```",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = [
        "Some text",
        "```bash markdown-code-runner",
        'echo "Hello, world!"',
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test case 1 (hidden): Single code block
    input_lines = [
        "Some text",
        MARKERS["code:comment:bash:start"],
        md_comment('echo "Hello, world!"'),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = [
        "Some text",
        MARKERS["code:comment:bash:start"],
        md_comment('echo "Hello, world!"'),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
    ]
    assert_process(input_lines, expected_output)


def test_bash_variables() -> None:
    """Test that bash code is executed."""
    # Test case 1 (backticks): Single code block
    input_lines = [
        "Some text",
        "```bash markdown-code-runner",
        'MY_VAR="Hello, world!"',
        "echo $MY_VAR",
        "```",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = [
        "Some text",
        "```bash markdown-code-runner",
        'MY_VAR="Hello, world!"',
        "echo $MY_VAR",
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
    ]
    assert_process(input_lines, expected_output)


def test_marker_pattern() -> None:
    """Test that all marker patterns match the expected text."""
    patterns = markers_to_patterns()
    for marker_key, pattern in patterns.items():
        if marker_key == "code:backticks:file:start":
            continue
        for spaces in ["", "   "]:
            test_text = f"{spaces}{MARKERS[marker_key]}"
            match = re.search(pattern, test_text)
            assert match is not None, f"No match found for {marker_key}"

    marker_key = "code:backticks:file:start"
    pattern = patterns[marker_key]
    for spaces in ["", "   "]:
        test_text = f"{spaces}```somelanguage markdown-code-runner"
        match = re.search(pattern, test_text)
        assert match is not None, f"No match found for {marker_key}, {match}"


def test_write_to_file() -> None:
    """Test that bash code is executed."""
    print(PATTERNS)
    # Test case 1 (backticks): Single code block
    input_lines = [
        "Some text",
        "```rust markdown-code-runner filename=test.rs",
        "let a = 1;",
        'println!("a = {}", a);',
        "```",
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
    ]
    expected_output = [
        "Some text",
        "```rust markdown-code-runner filename=test.rs",
        "let a = 1;",
        'println!("a = {}", a);',
        "```",
        MARKERS["output:start"],
        MARKERS["warning"],
        MARKERS["output:end"],
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test case 2: test without output block
    input_lines = [
        "Some text",
        "```rust markdown-code-runner filename=test.rs",
        "let a = 1;",
        'println!("a = {}", a);',
        "```",
        "More text",
    ]
    expected_output = [
        "Some text",
        "```rust markdown-code-runner filename=test.rs",
        "let a = 1;",
        'println!("a = {}", a);',
        "```",
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test missing filename
    input_lines = [
        "Some text",
        "```rust markdown-code-runner",
        "let a = 1;",
        'println!("a = {}", a);',
        "```",
        "More text",
    ]
    with pytest.raises(ValueError, match="'output_file' must be specified"):
        process_markdown(input_lines, verbose=True)


def test_patterns() -> None:
    """Test that all marker patterns match the expected text."""
    p = re.compile(pattern=PATTERNS["code:backticks:file:start"])
    text = "```python markdown-code-runner"
    m = p.search(text)
    assert m is None
    text = "```javascript markdown-code-runner filename=test.js"
    m = p.search(text)
    assert m is not None
    text = "```rust markdown-code-runner"
    m = p.search(text)
    assert m is not None
    assert m.group("language") == "rust"


@pytest.mark.parametrize(
    ("line", "marker", "expected_result"),
    [
        (
            "```javascript markdown-code-runner filename=test.js",
            "code:backticks:file:start",
            {"filename": "test.js"},
        ),
        (
            "```python markdown-code-runner arg1=value1 arg2=value2",
            "code:backticks:python:start",
            {"arg1": "value1", "arg2": "value2"},
        ),
        (
            "```bash markdown-code-runner key1=value1 key2=value2",
            "code:backticks:bash:start",
            {"key1": "value1", "key2": "value2"},
        ),
        ("```python markdown-code-runner", "code:backticks:python:start", {}),
        ("This is a regular text line", "code:backticks:file:start", {}),
    ],
)
def test_extract_extra(line: str, marker: str, expected_result: str) -> None:
    """Test that the extract_extra function works as expected."""
    assert extract_extra(line, marker) == expected_result
