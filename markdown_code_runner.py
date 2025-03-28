# Copyright (c) 2023, Bas Nijholt
# All rights reserved.
"""Markdown Code Runner.

Automatically update Markdown files with code block output.

This script is part of the 'markdown-code-runner' package available on GitHub:
https://github.com/basnijholt/markdown-code-runner

Add code blocks between <!-- CODE:START --> and <!-- CODE:END --> in your Markdown file.
The output will be inserted between <!-- OUTPUT:START --> and <!-- OUTPUT:END -->.

Example:
-------
<!-- CODE:START -->
<!-- print('Hello, world!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
This will be replaced by the output of the code block above.
<!-- OUTPUT:END -->

Alternatively, you can add a <!-- CODE:SKIP --> comment above a code block to skip execution.

Another way is to run code blocks in triple backticks:
```python markdown-code-runner
print('Hello, world!')
```
Which will print the output of the code block between the output markers:
<!-- OUTPUT:START -->
This will be replaced by the output of the code block above.
<!-- OUTPUT:END -->

You can also run bash code blocks:
```bash markdown-code-runner
echo "Hello, world!"
```
Which will similarly print the output of the code block between next to the output markers.

"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import re
import subprocess
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Literal

try:
    __version__ = version("markdown-code-runner")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

DEBUG: bool = os.environ.get("DEBUG", "0") == "1"


def md_comment(text: str) -> str:
    """Format a string as a Markdown comment."""
    return f"<!-- {text} -->"


MARKERS = {
    "warning": md_comment(
        "⚠️ This content is auto-generated by `markdown-code-runner`.",
    ),
    "skip": md_comment("CODE:SKIP"),
    "code:comment:python:start": md_comment("CODE:START"),
    "code:comment:bash:start": md_comment("CODE:BASH:START"),
    "code:comment:end": md_comment("CODE:END"),
    "output:start": md_comment("OUTPUT:START"),
    "output:end": md_comment("OUTPUT:END"),
    "code:backticks:start": r"```(?P<language>\w+)\smarkdown-code-runner",
    "code:backticks:end": "```",
}


def markers_to_patterns() -> dict[str, re.Pattern]:
    """Convert the markers to regular expressions."""
    allow_spaces_before_text = r"^(?P<spaces>\s*)"
    patterns = {}
    for key, value in MARKERS.items():
        patterns[key] = re.compile(allow_spaces_before_text + value, re.MULTILINE)
    return patterns


PATTERNS = markers_to_patterns()


def is_marker(line: str, marker: str) -> re.Match | None:
    """Check if a line is a specific marker."""
    match = re.search(PATTERNS[marker], line)
    if DEBUG and match is not None:  # pragma: no cover
        print(f"Found marker {marker} in line {line}")
    return match


def remove_md_comment(commented_text: str) -> str:
    """Remove Markdown comment tags from a string."""
    commented_text = commented_text.strip()
    if not (commented_text.startswith("<!-- ") and commented_text.endswith(" -->")):
        msg = f"Invalid Markdown comment format: {commented_text}"
        raise ValueError(msg)
    return commented_text[5:-4]


def execute_code(
    code: list[str],
    context: dict[str, Any] | None = None,
    language: Literal["python", "bash"] | None = None,  # type: ignore[name-defined]
    *,
    output_file: str | Path | None = None,
    verbose: bool = False,
) -> list[str]:
    """Execute a code block and return its output as a list of strings."""
    if context is None:
        context = {}
    full_code = "\n".join(code)

    if verbose:
        print(_bold(f"\nExecuting code {language} block:"))
        print(f"\n{full_code}\n")

    if output_file is not None:
        output_file = Path(output_file)
        with output_file.open("w") as f:
            f.write(full_code)
        output = []
    elif language == "python":
        with io.StringIO() as string, contextlib.redirect_stdout(string):
            exec(full_code, context)  # noqa: S102
            output = string.getvalue().split("\n")
    elif language == "bash":
        result = subprocess.run(  # noqa: S602
            full_code,
            capture_output=True,
            text=True,
            shell=True,
            check=False,
        )
        output = result.stdout.split("\n")
    else:
        msg = "Specify 'output_file' for non-Python/Bash languages."
        raise ValueError(msg)

    if verbose:
        print(_bold("Output:"))
        print(f"\n{output}\n")

    return output


def _bold(text: str) -> str:
    """Format a string as bold."""
    bold = "\033[1m"
    reset = "\033[0m"
    return f"{bold}{text}{reset}"


def _extract_backtick_options(line: str) -> dict[str, str]:
    """Extract extra information from a line."""
    if "```" not in line:
        return {}
    language_pattern = r"```(?P<language>\w+) markdown-code-runner"
    extra_pattern = r"(?P<key>\w+)=(?P<value>\S+)"

    language_match = re.search(language_pattern, line)
    assert language_match is not None
    language = language_match.group("language")
    result = {"language": language}

    extra_str = line[language_match.end() :]
    extra_matches = re.finditer(extra_pattern, extra_str)

    for match in extra_matches:
        key, value = match.group("key"), match.group("value")
        result[key] = value

    return result


@dataclass
class ProcessingState:
    """State of the processing of a Markdown file."""

    section: Literal[
        "normal",
        "output",
        # code:comment stores language in `section`
        "code:comment:python",
        "code:comment:bash",
        # code:backticks store language in `backtick_options`
        "code:backticks",
    ] = "normal"
    code: list[str] = field(default_factory=list)
    original_output: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    skip_code_block: bool = False
    output: list[str] | None = None
    new_lines: list[str] = field(default_factory=list)
    backtick_options: dict[str, Any] = field(default_factory=dict)

    def process_line(self, line: str, *, verbose: bool = False) -> None:
        """Process a line of the Markdown file."""
        if is_marker(line, "skip"):
            self.skip_code_block = True
        elif is_marker(line, "output:start"):
            self._process_output_start(line)
        elif is_marker(line, "output:end"):
            self._process_output_end()
        elif self.section.startswith("code:comment"):
            self._process_comment_code(line, verbose=verbose)
        elif self.section.startswith("code:backticks"):
            self._process_backtick_code(line, verbose=verbose)
        elif self.section == "output":
            self.original_output.append(line)
        else:
            self._process_start_markers(line)

        if self.section != "output":
            self.new_lines.append(line)

    def _process_start_markers(self, line: str) -> None:
        for marker in MARKERS:
            if marker.endswith(":start") and is_marker(line, marker):
                # reset output in case previous output wasn't displayed
                self.output = None
                self.backtick_options = _extract_backtick_options(line)
                self.section, _ = marker.rsplit(":", 1)  # type: ignore[assignment]
                return

    def _process_output_start(self, line: str) -> None:
        self.section = "output"
        if not self.skip_code_block:
            assert isinstance(
                self.output,
                list,
            ), f"Output must be a list, not {type(self.output)}, line: {line}"
            self.new_lines.extend([line, MARKERS["warning"], *self.output])
        else:
            self.original_output.append(line)

    def _process_output_end(self) -> None:
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
        language: Literal["python", "bash"],
        *,
        remove_comment: bool = False,
        verbose: bool,
    ) -> None:
        if is_marker(line, end_marker):
            if not self.skip_code_block:
                self.output = execute_code(
                    self.code,
                    self.context,
                    language,
                    output_file=self.backtick_options.get("filename"),
                    verbose=verbose,
                )
            self.section = "normal"
            self.code = []
            self.backtick_options = {}
        else:
            self.code.append(remove_md_comment(line) if remove_comment else line)

    def _process_comment_code(self, line: str, *, verbose: bool) -> None:
        _, language = self.section.rsplit(":", 1)
        self._process_code(
            line,
            "code:comment:end",
            language,  # type: ignore[arg-type]
            remove_comment=True,
            verbose=verbose,
        )

    def _process_backtick_code(self, line: str, *, verbose: bool) -> None:
        # All end backticks markers are the same
        language = self.backtick_options["language"]
        self._process_code(line, "code:backticks:end", language, verbose=verbose)


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
    verbose: bool = False,
) -> None:
    """Rewrite a Markdown file by executing and updating code blocks."""
    if isinstance(input_filepath, str):  # pragma: no cover
        input_filepath = Path(input_filepath)
    with input_filepath.open() as f:
        original_lines = [line.rstrip("\n") for line in f.readlines()]
    if verbose:
        print(f"Processing input file: {input_filepath}")
    new_lines = process_markdown(original_lines, verbose=verbose)
    updated_content = "\n".join(new_lines).rstrip() + "\n"
    if verbose:
        print(f"Writing output to: {output_filepath}")
    output_filepath = (
        input_filepath if output_filepath is None else Path(output_filepath)
    )
    with output_filepath.open("w") as f:
        f.write(updated_content)
    if verbose:
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
        "--verbose",
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
    update_markdown_file(input_filepath, output_filepath, verbose=args.verbose)


if __name__ == "__main__":
    main()
