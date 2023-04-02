# :rocket: Markdown Code Runner

`markdown-code-runner` is a Python package that automatically executes code blocks within a Markdown file and updates the output in-place. This package is particularly useful for maintaining Markdown files with embedded code snippets, ensuring that the output displayed is up-to-date and accurate.

The package is hosted on GitHub: [https://github.com/basnijholt/markdown-code-runner](https://github.com/basnijholt/markdown-code-runner)

## :books: Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [:question: Problem Statement](#question-problem-statement)
- [:computer: Installation](#computer-installation)
- [:rocket: Quick Start](#rocket-quick-start)
- [Usage](#usage)
- [:book: Examples](#book-examples)
  - [:star: Example 1: Simple code block](#star-example-1-simple-code-block)
  - [:star: Example 2: Multiple code blocks](#star-example-2-multiple-code-blocks)
- [:page_with_curl: License](#page_with_curl-license)
- [:handshake: Contributing](#handshake-contributing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## :question: Problem Statement

When creating Markdown files with code examples, it's essential to keep the output of these code snippets accurate and up-to-date. Manually updating the output can be time-consuming and error-prone, especially when working with large files or multiple collaborators.

`markdown-code-runner` solves this problem by automatically executing the code blocks within a Markdown file and updating the output in-place. This ensures that the displayed output is always in sync with the code.

## :computer: Installation

Install `markdown-code-runner` via pip:

```bash
pip install markdown-code-runner
```

## :rocket: Quick Start

To get started with `markdown-code-runner`, follow these steps:

1.  Add code blocks to your Markdown file between `<!-- START_CODE -->` and `<!-- END_CODE -->` markers.
2.  Place the output of the code blocks between `<!-- START_OUTPUT -->` and `<!-- END_OUTPUT -->` markers.

Example:

```markdown
This is an example code block:

<!-- START_CODE -->
<!-- print('Hello, world!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
This content will be replaced by the output of the code block above.
<!-- END_OUTPUT -->
```

3.  Run `markdown-code-runner` on your Markdown file:

```bash
markdown-code-runner /path/to/your/markdown_file.md
```

4.  The output of the code block will be automatically executed and inserted between the output markers.

Usage
-----

To use `markdown-code-runner`, simply import the `update_markdown_file` function from the package and call it with the path to your Markdown file:

```python
from markdown_code_runner import update_markdown_file
from pathlib import Path

update_markdown_file(Path("path/to/your/markdown_file.md"))
```

## :book: Examples

Here are a few examples demonstrating the usage of `markdown-code-runner`:

### :star: Example 1: Simple code block

```markdown
This is an example of a simple code block:

<!-- START_CODE -->
<!-- print('Hello, world!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
This content will be replaced by the output of the code block above.
<!-- END_OUTPUT -->
```

After running `markdown-code-runner`:

```markdown
This is an example of a simple code block:

<!-- START_CODE -->
<!-- print('Hello, world!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->
Hello, world!
<!-- END_OUTPUT -->
```

### :star: Example 2: Multiple code blocks

```markdown
Here are two code blocks:

First code block:

<!-- START_CODE -->
<!-- print('Hello, world!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
This content will be replaced by the output of the first code block.
<!-- END_OUTPUT -->

Second code block:

<!-- START_CODE -->
<!-- print('Hello again!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
This content will be replaced by the output of the second code block.
<!-- END_OUTPUT -->
```

After running `markdown-code-runner`:
```markdown
Here are two code blocks:

First code block:

<!-- START_CODE --> <!-- print('Hello, world!') --> <!-- END_CODE --> <!-- START_OUTPUT --> <!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->

Hello, world!

<!-- END_OUTPUT -->

Second code block:

<!-- START_CODE --> <!-- print('Hello again!') --> <!-- END_CODE --> <!-- START_OUTPUT --> <!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->

Hello again!

<!-- END_OUTPUT -->
```


## :page_with_curl: License

`markdown-code-runner` is released under the [MIT License](https://opensource.org/licenses/MIT). Please include the LICENSE file when using this package in your project, and cite the original source.

## :handshake: Contributing

Contributions are welcome! To contribute, please follow these steps:

1. Fork the repository on GitHub: [https://github.com/basnijholt/markdown-code-runner](https://github.com/basnijholt/markdown-code-runner)
2. Create a new branch for your changes.
3. Make your changes, ensuring that they adhere to the code style and guidelines.
4. Submit a pull request with a description of your changes.

Please report any issues or bugs on the GitHub issue tracker: [https://github.com/basnijholt/markdown-code-runner/issues](https://github.com/basnijholt/markdown-code-runner/issues)

Thank you for your interest in `markdown-code-runner`!
