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
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pkg_resources

if TYPE_CHECKING:
    try:
        from typing import Literal  # type: ignore[attr-defined]
    except ImportError:
        from typing_extensions import Literal


__version__ = pkg_resources.get_distribution("markdown-code-runner").version


def md_comment(text: str) -> str:
    """Format a string as a Markdown comment."""
    return f"<!-- {text} -->"


MARKERS = {
    "warning": md_comment(
        "⚠️ This content is auto-generated by `markdown-code-runner`.",
    ),
    "code:comment:start": md_comment("START_CODE"),
    "code:comment:end": md_comment("END_CODE"),
    "output:start": md_comment("START_OUTPUT"),
    "output:end": md_comment("END_OUTPUT"),
    "skip": md_comment("SKIP"),
    "code:backticks:start": "```python markdown-code-runner",
    "code:backticks:end": "```",
    "code:backticks:bash:start": "```bash markdown-code-runner",
    "code:backticks:bash:end": "```",
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
    language: Literal["python", "bash"] = "python",  # type: ignore[name-defined]
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

    if language == "python":
        with io.StringIO() as f, contextlib.redirect_stdout(f):
            exec(full_code, context)  # noqa: S102
            output = f.getvalue().split("\n")
    elif language == "bash":
        result = subprocess.run(
            full_code,
            capture_output=True,
            text=True,
            shell=True,
        )
        output = result.stdout.split("\n")

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


@dataclass
class ProcessingState:
    """State of the processing of a Markdown file."""

    section: Literal[
        "normal",
        "code:comment",
        "code:backtick",
        "code:backtick:bash",
        "output",
    ] = "normal"
    code: list[str] = field(default_factory=list)
    original_output: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    skip_code_block: bool = False
    output: list[str] | None = None
    new_lines: list[str] = field(default_factory=list)

    def process_line(self, line: str, *, verbose: bool = False) -> None:
        """Process a line of the Markdown file."""
        if is_marker(line, "skip"):
            self.skip_code_block = True
        elif is_marker(line, "code:comment:start"):
            self.section = "code:comment"
        elif is_marker(line, "code:backticks:start"):
            self.section = "code:backtick"
        elif is_marker(line, "code:backticks:bash:start"):
            self.section = "code:backtick:bash"
        elif is_marker(line, "output:start"):
            self._process_start_output(line)
        elif is_marker(line, "output:end"):
            self._process_end_output()
        elif self.section == "code:comment":
            self._process_comment_code(line, verbose=verbose)
        elif self.section.startswith("code:backtick"):
            self._process_backtick_code(line, verbose=verbose)
        elif self.section == "output":
            self.original_output.append(line)

        if self.section != "output":
            self.new_lines.append(line)

    def _process_start_output(self, line: str) -> None:
        self.section = "output"
        if not self.skip_code_block:
            assert isinstance(
                self.output,
                list,
            ), f"Output must be a list, not {type(self.output)}, line: {line}"
            self.new_lines.extend([line, MARKERS["warning"], *self.output])
        else:
            self.original_output.append(line)

    def _process_end_output(self) -> None:
        self.section = "normal"
        if self.skip_code_block:
            self.new_lines.extend(self.original_output)
            self.skip_code_block = False
        self.original_output = []
        self.output = None  # Reset output after processing end of the output section

    def _process_code(
        self,
        line: str,
        end_marker: str,
        *,
        remove_comment: bool = False,
        verbose: bool,
    ) -> None:
        if is_marker(line, end_marker):
            if not self.skip_code_block:
                language = "bash" if self.section == "code:backtick:bash" else "python"
                self.output = execute_code(
                    self.code,
                    self.context,
                    language,
                    verbose=verbose,
                )
            self.section = "normal"
            self.code = []
        else:
            self.code.append(remove_md_comment(line) if remove_comment else line)

    def _process_comment_code(self, line: str, *, verbose: bool) -> None:
        self._process_code(
            line,
            "code:comment:end",
            remove_comment=True,
            verbose=verbose,
        )

    def _process_backtick_code(self, line: str, *, verbose: bool) -> None:
        # All end backtick markers are the same
        self._process_code(line, "code:backticks:end", verbose=verbose)


def process_markdown(content: list[str], *, verbose: bool = False) -> list[str]:
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
    state = ProcessingState()

    for i, line in enumerate(content):
        if verbose:
            nr = _bold(f"line {i:4d}")
            print(f"{nr}: {line}")
        state.process_line(line, verbose=verbose)

    return state.new_lines


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
