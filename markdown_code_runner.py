# Copyright (c) 2023, Bas Nijholt
# All rights reserved.
"""Markdown Code Runner.

Automatically update Markdown files with code block output.

This script is part of the 'markdown-code-runner' package available on GitHub:
https://github.com/basnijholt/markdown-code-runner

Add code blocks between <!-- START_CODE --> and <!-- END_CODE --> in your Markdown file.
The output will be inserted between <!-- START_OUTPUT --> and <!-- END_OUTPUT -->.

Example:
-------
<!-- START_CODE -->
<!-- print('Hello, world!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
This will be replaced by the output of the code block above.

<!-- END_OUTPUT -->
```
Alternatively, you can add a <!-- SKIP --> comment to skip a code block.

Another way is to run code blocks in triple backticks:
```python markdown-code-runner
print('Hello, world!')
```
Which will print the output of the code block above below the code block.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import re
from pathlib import Path
from typing import Any

import pkg_resources

__version__ = pkg_resources.get_distribution("markdown-code-runner").version


def md_comment(text: str) -> str:
    """Format a string as a Markdown comment."""
    return f"<!-- {text} -->"


MARKERS = {
    "warning": md_comment(
        "⚠️ This content is auto-generated by `markdown-code-runner`.",
    ),
    "start_code": md_comment("START_CODE"),
    "end_code": md_comment("END_CODE"),
    "start_output": md_comment("START_OUTPUT"),
    "end_output": md_comment("END_OUTPUT"),
    "skip": md_comment("SKIP"),
}


def remove_md_comment(commented_text: str) -> str:
    """Remove Markdown comment tags from a string."""
    if not (commented_text.startswith("<!-- ") and commented_text.endswith(" -->")):
        msg = f"Invalid Markdown comment format: {commented_text}"
        raise ValueError(msg)
    return commented_text[5:-4]


def execute_code(
    code: list[str],
    context: dict[str, Any] | None = None,
    *,
    verbose: bool = False,
) -> list[str]:
    """Execute a code block and return its output as a list of strings."""
    if context is None:
        context = {}
    full_code = "\n".join(code)
    if verbose:
        print(_bold("\nExecuting code block:"))
        print(f"\n{full_code}\n")
    with io.StringIO() as f, contextlib.redirect_stdout(f):
        exec(full_code, context)  # noqa: S102
        output = f.getvalue().split("\n")
    if verbose:
        print(_bold("Output:"))
        print(f"\n{output}\n")
    return output


def is_marker(line: str, marker: str) -> bool:
    """Check if a line is a specific marker."""
    return line.startswith(MARKERS[marker])


def _bold(text: str) -> str:
    """Format a string as bold."""
    bold = "\033[1m"
    reset = "\033[0m"
    return f"{bold}{text}{reset}"


def process_markdown(  # noqa: PLR0912, PLR0915
    content: list[str],
    *,
    verbose: bool = False,
) -> list[str]:
    """Executes code blocks in a list of Markdown-formatted strings and returns the modified list.

    Parameters
    ----------
    content
        A list of Markdown-formatted strings.
    verbose
        If True, print every line that is processed.

    Returns
    -------
    list[str]
        A modified list of Markdown-formatted strings with code block output inserted.
    """
    assert isinstance(content, list), "Input must be a list"
    context: dict[str, Any] = {}
    new_lines = []
    code: list[str] = []
    original_output: list[str] = []
    in_md_code = in_backtick_code = in_output = skip_code_block = False
    output: list[str] | None = None

    triple_backtick_pattern = re.compile(r"^```python markdown-code-runner")
    # add empty line to process last code block (if at end of file)
    content = [
        *content,
        "",
    ]
    for i, line in enumerate(content):
        if verbose:
            nr = _bold(f"line {i:4d}")
            print(f"{nr}: {line}")

        if is_marker(line, "skip"):
            skip_code_block = True
        elif is_marker(line, "start_code"):
            in_md_code = True
        elif is_marker(line, "start_output"):
            in_output = True
            if not skip_code_block:
                assert isinstance(
                    output,
                    list,
                ), f"Output must be a list, not {type(output)}, line: {line}"
                new_lines.extend([line, MARKERS["warning"], *output])
                output = None
            else:
                original_output.append(line)
        elif is_marker(line, "end_output"):
            in_output = False
            if skip_code_block:
                new_lines.extend(original_output)
                skip_code_block = False
            original_output = []
        elif in_md_code:
            if is_marker(line, "end_code"):
                in_md_code = False
                if not skip_code_block:
                    output = execute_code(code, context, verbose=verbose)
                code = []
            else:
                code.append(remove_md_comment(line))
        elif in_output:
            original_output.append(line)
        elif in_backtick_code:
            if line.strip() == "```":
                in_backtick_code = False
                if not skip_code_block:
                    output = execute_code(code, context, verbose=verbose)
                code = []
            else:
                code.append(line)
        elif triple_backtick_pattern.match(line):
            in_backtick_code = True

        last_line = i == len(content) - 1
        if not in_output and not last_line:
            new_lines.append(line)
    return new_lines


def update_markdown_file(
    input_filepath: Path | str,
    output_filepath: Path | str | None = None,
    *,
    debug: bool = False,
) -> None:
    """Rewrite a Markdown file by executing and updating code blocks."""
    if isinstance(input_filepath, str):  # pragma: no cover
        input_filepath = Path(input_filepath)
    with input_filepath.open() as f:
        original_lines = [line.rstrip("\n") for line in f.readlines()]
    if debug:
        print(f"Processing input file: {input_filepath}")
    new_lines = process_markdown(original_lines, verbose=debug)
    updated_content = "\n".join(new_lines).rstrip() + "\n"
    if debug:
        print(f"Writing output to: {output_filepath}")
    output_filepath = (
        input_filepath if output_filepath is None else Path(output_filepath)
    )
    with output_filepath.open("w") as f:
        f.write(updated_content)
    if debug:
        print("Done!")


def main() -> None:
    """Parse command line arguments and run the script."""
    parser = argparse.ArgumentParser(
        description="Automatically update Markdown files with code block output.",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to the input Markdown file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output Markdown file. (default: overwrite input file)",
        default=None,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debugging mode (default: False)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    input_filepath = Path(args.input)
    output_filepath = Path(args.output) if args.output is not None else input_filepath
    update_markdown_file(input_filepath, output_filepath, debug=args.debug)


if __name__ == "__main__":
    main()
