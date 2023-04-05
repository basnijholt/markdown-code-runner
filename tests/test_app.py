"""Test the markdown_code_runner app."""
from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import patch

import pytest

from markdown_code_runner import (
    MARKERS,
    execute_code,
    main,
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
        MARKERS["code:comment:start"],
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
        MARKERS["code:comment:start"],
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
        MARKERS["code:comment:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:start"],
        md_comment("print('Hello again!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        MARKERS["code:comment:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:start"],
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
        MARKERS["code:comment:start"],
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
        MARKERS["code:comment:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:start"],
        md_comment("print('Hello again!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will also be replaced",
        MARKERS["output:end"],
    ]
    expected_output = [
        "Some text",
        MARKERS["skip"],
        MARKERS["code:comment:start"],
        md_comment("print('Hello, world!')"),
        MARKERS["code:comment:end"],
        MARKERS["output:start"],
        "This content will be replaced",
        MARKERS["output:end"],
        "More text",
        MARKERS["code:comment:start"],
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
        return_value=argparse.Namespace(input=test_filepath, output=None, debug=False),
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
            debug=False,
        ),
    ):
        main()
        assert output_filepath.exists()
        with output_filepath.open() as f1, expected_output_filepath.open() as f2:
            assert f1.read() == f2.read()


def test_main_debug_mode(capfd: pytest.CaptureFixture, tmp_path: Path) -> None:
    """Test the main function with debug mode enabled."""
    test_filepath = TEST_FOLDER / "test.md"
    output_filepath = tmp_path / "output.md"
    expected_output_filepath = TEST_FOLDER / "test_expected_output.md"

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            input=test_filepath,
            output=str(output_filepath),
            debug=True,
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
        MARKERS["code:comment:start"],
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
        MARKERS["code:comment:start"],
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
