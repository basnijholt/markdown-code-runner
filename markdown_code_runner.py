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
"""
from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path


def md_comment(text: str) -> str:
    """Format a string as a Markdown comment."""
    return f"<!-- {text} -->"


MARKERS = {
    "warning": md_comment("THIS CONTENT IS AUTOMATICALLY GENERATED"),
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


def execute_code_block(code: list[str]) -> list[str]:
    """Execute a code block and return its output as a list of strings."""
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        exec("\n".join(code))  # noqa: S102
    return f.getvalue().split("\n")


def process_markdown(content: list[str]) -> list[str]:  # noqa: PLR0912
    """Executes code blocks in a list of Markdown-formatted strings and returns the modified list.

    Parameters
    ----------
    content
        A list of Markdown-formatted strings.

    Returns
    -------
    list[str]
        A modified list of Markdown-formatted strings with code block output inserted.
    """
    assert isinstance(content, list), "Input must be a list"
    new_lines = []
    code: list[str] = []
    original_output: list[str] = []
    in_code_block = in_output_block = skip_code_block = False
    output: list[str] | None = None

    for line in content:
        if MARKERS["skip"] in line:
            skip_code_block = True
        elif MARKERS["start_code"] in line:
            in_code_block = True
        elif MARKERS["start_output"] in line:
            in_output_block = True
            if not skip_code_block:
                assert isinstance(
                    output,
                    list,
                ), f"Output must be a list, not {type(output)}, line: {line}"
                new_lines.extend([line, MARKERS["warning"], *output])
                output = None
            else:
                original_output.append(line)
        elif MARKERS["end_output"] in line:
            in_output_block = False
            if skip_code_block:
                new_lines.extend(original_output)
                skip_code_block = False
            original_output = []
        elif in_code_block:
            if MARKERS["end_code"] in line:
                in_code_block = False
                if not skip_code_block:
                    output = execute_code_block(code)
                code = []
            else:
                code.append(remove_md_comment(line))
        elif in_output_block:
            original_output.append(line)

        if not in_output_block:
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
    new_lines = process_markdown(original_lines)
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

    args = parser.parse_args()

    input_filepath = Path(args.input)
    output_filepath = Path(args.output) if args.output is not None else input_filepath
    update_markdown_file(input_filepath, output_filepath, debug=args.debug)


if __name__ == "__main__":
    main()
