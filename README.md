# :rocket: Markdown Code Runner

`markdown-code-runner` is a Python package that automatically executes code blocks within a Markdown file and updates the output in-place. This package is particularly useful for maintaining Markdown files with embedded code snippets, ensuring that the output displayed is up-to-date and accurate.

The package is hosted on GitHub: [https://github.com/basnijholt/markdown-code-runner](https://github.com/basnijholt/markdown-code-runner)

## :star: Features
-  :rocket: Automatically execute code blocks within a Markdown file
-  :eyes: Allows hidden code blocks (i.e. code blocks that are not displayed in the Markdown file)
-  :snake: :shell: Works with Python and Bash code blocks
-  :white_check_mark: Keeps the output of the code blocks up-to-date
-  :octocat: Easily integrates with GitHub Actions

## :question: Problem Statement

When creating Markdown files with code examples, it's essential to keep the output of these code snippets accurate and up-to-date. Manually updating the output can be time-consuming and error-prone, especially when working with large files or multiple collaborators.

`markdown-code-runner` solves this problem by automatically executing the code blocks within a Markdown file and updating the output in-place. This ensures that the displayed output is always in sync with the code.

## :books: Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [:computer: Installation](#computer-installation)
- [:rocket: Quick Start](#rocket-quick-start)
- [Usage](#usage)
- [:book: Examples](#book-examples)
  - [:star: Example 1: Simple code block](#star-example-1-simple-code-block)
  - [:star: Example 2: Multiple code blocks](#star-example-2-multiple-code-blocks)
- [:bulb: Usage Ideas](#bulb-usage-ideas)
  - [:gear: Idea 1: Continuous Integration with GitHub Actions](#gear-idea-1-continuous-integration-with-github-actions)
  - [:computer: Idea 2: Show command-line output](#computer-idea-2-show-command-line-output)
  - [:bar_chart: Idea 3: Generating Markdown Tables](#bar_chart-idea-3-generating-markdown-tables)
  - [:art: Idea 4: Generating Visualizations](#art-idea-4-generating-visualizations)
  - [:star: Idea 5: Generating a table from CSV data](#star-idea-5-generating-a-table-from-csv-data)
  - [:star: Idea 5: Displaying API data as a list](#star-idea-5-displaying-api-data-as-a-list)
- [:page_with_curl: License](#page_with_curl-license)
- [:handshake: Contributing](#handshake-contributing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## :computer: Installation

Install `markdown-code-runner` via pip:

```bash
pip install markdown-code-runner
```

## :rocket: Quick Start

To get started with `markdown-code-runner`, follow these steps:

1.  Add code blocks to your Markdown file using either of the following methods:

    **Method 1 (*show your code*):** Use a triple backtick code block with the language specifier `python markdown-code-runner`.

    Example:

    ````markdown
    ```python markdown-code-runner
    print('Hello, world!')
    ```
    (Optionally, you can place some text between the code block and the output markers)
    <!-- OUTPUT:START -->
    This content will be replaced by the output of the code block above.
    <!-- OUTPUT:END -->
    ````

    or for Bash:

    ````markdown
    ```bash markdown-code-runner
    echo 'Hello, world!'
    ```
    (Optionally, you can place some text between the code block and the output markers)
    <!-- OUTPUT:START -->
    This content will be replaced by the output of the code block above.
    <!-- OUTPUT:END -->
    ````

    **Method 2 *(hide your code)*:** Place the code between `<!-- CODE:START -->` and `<!-- CODE:END -->` markers. Add the output markers `<!-- OUTPUT:START -->` and `<!-- OUTPUT:END -->` where you want the output to be displayed.

    Example:

    ```markdown
    This is an example code block:

    <!-- CODE:START -->
    <!-- print('Hello, world!') -->
    <!-- CODE:END -->
    <!-- OUTPUT:START -->
    This content will be replaced by the output of the code block above.
    <!-- OUTPUT:END -->
    ```

2.  Run `markdown-code-runner` on your Markdown file:

    ```bash
    markdown-code-runner /path/to/your/markdown_file.md
    ```

3.  The output of the code block will be automatically executed and inserted between the output markers.

## Usage

To use `markdown-code-runner`, simply import the `update_markdown_file` function from the package and call it with the path to your Markdown file:

```python
from markdown_code_runner import update_markdown_file
from pathlib import Path

update_markdown_file(Path("path/to/your/markdown_file.md"))
```

## :book: Examples

Here are a few examples demonstrating the usage of `markdown-code-runner`:

### :star: Example 1: Simple code block
<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed -->
```markdown
This is an example of a simple hidden code block:

<!-- CODE:START -->
<!-- print('Hello, world!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
This content will be replaced by the output of the code block above.
<!-- OUTPUT:END -->
```

After running `markdown-code-runner`:
```markdown
This is an example of a simple code block:

<!-- CODE:START -->
<!-- print('Hello, world!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
Hello, world!

<!-- OUTPUT:END -->
```

### :star: Example 2: Multiple code blocks
<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed -->
```markdown
Here are two code blocks:

First code block:

<!-- CODE:START -->
<!-- print('Hello, world!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
This content will be replaced by the output of the first code block.
<!-- OUTPUT:END -->
```

<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed --> <!-- This is here otherwise the next example gets executed -->
```markdown
Second code block:

<!-- CODE:START -->
<!-- print('Hello again!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
This content will be replaced by the output of the second code block.
<!-- OUTPUT:END -->
```

After running `markdown-code-runner`:

```markdown
Here are two code blocks:

First code block:

<!-- CODE:START -->
<!-- print('Hello, world!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
Hello, world!

<!-- OUTPUT:END -->

Second code block:

<!-- CODE:START -->
<!-- print('Hello again!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
Hello again!

<!-- OUTPUT:END -->
```

## :bulb: Usage Ideas

Markdown Code Runner can be used for various purposes, such as creating Markdown tables, generating visualizations, and showcasing code examples with live outputs. Here are some usage ideas to get you started:

### :gear: Idea 1: Continuous Integration with GitHub Actions

You can use `markdown-code-runner` to automatically update your Markdown files in a CI environment.
The following example demonstrates how to configure a GitHub Actions workflow that updates your `README.md` whenever changes are pushed to the `main` branch.

1. Create a new workflow file in your repository at `.github/workflows/markdown-code-runner.yml`.

2. Add the following content to the workflow file:

<!-- CODE:START -->
<!-- print("```yaml") -->
<!-- with open(".github/workflows/markdown-code-runner.yml") as f: -->
<!--   print(f.read().replace("pip install .", "pip install markdown-code-runner")) -->
<!-- print("```") -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
```yaml
name: Update README.md

on:
  push:
    branches:
      - main

jobs:
  update_readme:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          persist-credentials: false
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.x'

      - name: Install markdown-code-runner
        run: |
          python -m pip install --upgrade pip
          pip install markdown-code-runner

      # Install dependencies you're using in your README.md
      - name: Install other Python dependencies
        run: |
          pip install pandas tabulate pytest matplotlib requests

      - name: Run update-readme.py
        run: markdown-code-runner README.md

      - name: Commit updated README.md
        id: commit
        run: |
          git add README.md
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          if git diff --quiet && git diff --staged --quiet; then
            echo "No changes in README.md, skipping commit."
            echo "commit_status=skipped" >> $GITHUB_ENV
          else
            git commit -m "Update README.md"
            echo "commit_status=committed" >> $GITHUB_ENV
          fi

      - name: Push changes
        if: env.commit_status == 'committed'
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.head_ref }}

```

<!-- OUTPUT:END -->

3.  Commit and push the workflow file to your repository. The workflow will now automatically run whenever you push changes to the `main` branch, updating your `README.md` with the latest outputs from your code blocks.

For more information on configuring GitHub Actions, check out the [official documentation](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions).

### :computer: Idea 2: Show command-line output

Use `markdown-code-runner` to display the output of a command-line program. For example, the following Markdown file shows the helper options of this package.

Using a hidden code block:
<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed -->
```markdown
<!-- CODE:START -->
<!-- import subprocess -->
<!-- out = subprocess.run(["markdown-code-runner", "--help"], capture_output=True, text=True) -->
<!-- print(f"```bash\n{out.stdout}\n```") -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- OUTPUT:END -->
```

Which is rendered as:

<!-- CODE:START -->
<!-- import subprocess -->
<!-- out = subprocess.run(["markdown-code-runner", "--help"], capture_output=True, text=True) -->
<!-- print(f"```bash\n{out.stdout}\n```") -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
```bash
usage: markdown-code-runner [-h] [-o OUTPUT] [-d] [-v] input

Automatically update Markdown files with code block output.

positional arguments:
  input                 Path to the input Markdown file.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to the output Markdown file. (default: overwrite
                        input file)
  -d, --debug           Enable debugging mode (default: False)
  -v, --version         show program's version number and exit

```

<!-- OUTPUT:END -->

### :bar_chart: Idea 3: Generating Markdown Tables

Use the `pandas` library to create a Markdown table from a DataFrame. The following example demonstrates how to create a table with random data:

```python markdown-code-runner
import pandas as pd
import numpy as np

# Generate random data
np.random.seed(42)
data = np.random.randint(1, 101, size=(5, 3))

# Create a DataFrame and column names
df = pd.DataFrame(data, columns=["Column A", "Column B", "Column C"])

# Convert the DataFrame to a Markdown table
print(df.to_markdown(index=False))
```

Which is rendered as:

<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
|   Column A |   Column B |   Column C |
|-----------:|-----------:|-----------:|
|         52 |         93 |         15 |
|         72 |         61 |         21 |
|         83 |         87 |         75 |
|         75 |         88 |        100 |
|         24 |          3 |         22 |

<!-- OUTPUT:END -->

### :art: Idea 4: Generating Visualizations

Create a visualization using the `matplotlib` library and save it as an image. Then, reference the image in your Markdown file. The following example demonstrates how to create a bar chart.

Using a triple-backtick code block:

<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed -->
```python markdown-code-runner
import matplotlib.pyplot as plt
import io
import base64
from urllib.parse import quote

# Example data for the plot
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Create a simple line plot
plt.plot(x, y)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Sample Line Plot")

# Save the plot to a BytesIO buffer
buf = io.BytesIO()
plt.savefig(buf, format='png')
plt.close()

# Encode the buffer as a base64 string
data = base64.b64encode(buf.getvalue()).decode('utf-8')

# Create an inline HTML img tag with the base64 string
from urllib.parse import quote
img_html = f'<img src="data:image/png;base64,{quote(data)}" alt="Sample Line Plot"/>'

print(img_html)
```
<!-- OUTPUT:START -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED BY markdown-code-runner -->

<!-- OUTPUT:END -->

### :star: Idea 5: Generating a table from CSV data

Suppose you have a CSV file containing data that you want to display as a table in your Markdown file.
You can use `pandas` to read the CSV file, convert it to a DataFrame, and then output it as a Markdown table.

Using a triple-backtick code block:

```python markdown-code-runner
import pandas as pd
csv_data = "Name,Age,Score\nAlice,30,90\nBob,25,85\nCharlie,22,95"
with open("sample_data.csv", "w") as f:
    f.write(csv_data)
df = pd.read_csv("sample_data.csv")
print(df.to_markdown(index=False))
```

Which is rendered as:

<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
| Name    |   Age |   Score |
|:--------|------:|--------:|
| Alice   |    30 |      90 |
| Bob     |    25 |      85 |
| Charlie |    22 |      95 |

<!-- OUTPUT:END -->

### :star: Idea 5: Displaying API data as a list

You can use `markdown-code-runner` to make API calls and display the data as a list in your Markdown file.
In this example, we'll use the `requests` library to fetch data from an API and display the results as a list.

Using a hidden code block:

<!-- CODE:SKIP --> <!-- This prevents the example below from getting executed -->
```markdown
<!-- CODE:START -->
<!-- import requests -->
<!-- response = requests.get("https://jsonplaceholder.typicode.com/todos?_limit=5") -->
<!-- todos = response.json() -->
<!-- for todo in todos: -->
<!--     print(f"- {todo['title']} (User ID: {todo['userId']}, Completed: {todo['completed']})") -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
Output will appear here.
<!-- OUTPUT:END -->
```
Which is rendered as:

<!-- CODE:START -->
<!-- import requests -->
<!-- response = requests.get("https://jsonplaceholder.typicode.com/todos?_limit=5") -->
<!-- todos = response.json() -->
<!-- for todo in todos: -->
<!--     print(f"- {todo['title']} (User ID: {todo['userId']}, Completed: {todo['completed']})") -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- ⚠️ This content is auto-generated by `markdown-code-runner`. -->
- delectus aut autem (User ID: 1, Completed: False)
- quis ut nam facilis et officia qui (User ID: 1, Completed: False)
- fugiat veniam minus (User ID: 1, Completed: False)
- et porro tempora (User ID: 1, Completed: True)
- laboriosam mollitia et enim quasi adipisci quia provident illum (User ID: 1, Completed: False)

<!-- OUTPUT:END -->

These are just a few examples of how you can use Markdown Code Runner to enhance your Markdown documents with dynamic content. The possibilities are endless!

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
