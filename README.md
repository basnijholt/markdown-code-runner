# :rocket: Markdown Code Runner

`markdown-code-runner` is a Python package that automatically executes code blocks within a Markdown file and updates the output in-place. This package is particularly useful for maintaining Markdown files with embedded code snippets, ensuring that the output displayed is up-to-date and accurate.

The package is hosted on GitHub: [https://github.com/basnijholt/markdown-code-runner](https://github.com/basnijholt/markdown-code-runner)

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
  - [:bar_chart: Idea 1: Generating Markdown Tables](#bar_chart-idea-1-generating-markdown-tables)
  - [:art: Idea 2: Generating Visualizations](#art-idea-2-generating-visualizations)
  - [:star: Idea 3: Generating a table from CSV data](#star-idea-3-generating-a-table-from-csv-data)
  - [:star: Idea 4: Displaying API data as a list](#star-idea-4-displaying-api-data-as-a-list)
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
<!-- SKIP -->
1.  Add code blocks to your Markdown file between `<!-- START_CODE -->` and `<!-- END_CODE -->` markers.
2.  Place the output of the code blocks between `<!-- START_OUTPUT -->` and `<!-- END_OUTPUT -->` markers.

Example:
<!-- SKIP -->
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
<!-- SKIP -->
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
<!-- SKIP -->
```markdown
Here are two code blocks:

First code block:

<!-- START_CODE -->
<!-- print('Hello, world!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
This content will be replaced by the output of the first code block.
<!-- END_OUTPUT -->
```

<!-- SKIP -->
```markdown
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

<!-- START_CODE -->
<!-- print('Hello, world!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->
Hello, world!

<!-- END_OUTPUT -->

Second code block:

<!-- START_CODE -->
<!-- print('Hello again!') -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->
Hello again!

<!-- END_OUTPUT -->
```

## :bulb: Usage Ideas

Markdown Code Runner can be used for various purposes, such as creating Markdown tables, generating visualizations, and showcasing code examples with live outputs. Here are some usage ideas to get you started:

### :bar_chart: Idea 1: Generating Markdown Tables

Use the `pandas` library to create a Markdown table from a DataFrame. The following example demonstrates how to create a table with random data:

```python
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

<!-- START_CODE -->
<!-- import pandas as pd -->
<!-- import numpy as np -->
<!-- # Generate random data -->
<!-- np.random.seed(42) -->
<!-- data = np.random.randint(1, 101, size=(5, 3)) -->
<!-- # Create a DataFrame and column names -->
<!-- df = pd.DataFrame(data, columns=["Column A", "Column B", "Column C"]) -->
<!-- # Convert the DataFrame to a Markdown table -->
<!-- print(df.to_markdown(index=False)) -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->
|   Column A |   Column B |   Column C |
|-----------:|-----------:|-----------:|
|         52 |         93 |         15 |
|         72 |         61 |         21 |
|         83 |         87 |         75 |
|         75 |         88 |        100 |
|         24 |          3 |         22 |

<!-- END_OUTPUT -->

### :art: Idea 2: Generating Visualizations

Create a visualization using the `matplotlib` library and save it as an image. Then, reference the image in your Markdown file. The following example demonstrates how to create a bar chart:

```python
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

<!-- START_CODE -->
<!-- import matplotlib.pyplot as plt -->
<!-- import io -->
<!-- import base64 -->
<!-- from urllib.parse import quote -->
<!--  -->
<!-- # Example data for the plot -->
<!-- x = [1, 2, 3, 4, 5] -->
<!-- y = [2, 4, 6, 8, 10] -->
<!--  -->
<!-- # Create a simple line plot -->
<!-- plt.plot(x, y) -->
<!-- plt.xlabel("X-axis") -->
<!-- plt.ylabel("Y-axis") -->
<!-- plt.title("Sample Line Plot") -->
<!--  -->
<!-- # Save the plot to a BytesIO buffer -->
<!-- buf = io.BytesIO() -->
<!-- plt.savefig(buf, format='png', dpi=30) -->
<!-- plt.close() -->
<!--  -->
<!-- # Encode the buffer as a base64 string -->
<!-- data = base64.b64encode(buf.getvalue()).decode('utf-8') -->
<!--  -->
<!-- # Create an inline HTML img tag with the base64 string -->
<!-- img_html = f'<img src="data:image/png;base64,{quote(data)}" alt="Sample Line Plot"/>' -->
<!--  -->
<!-- print(img_html) -->
<!--  -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->

<!-- END_OUTPUT -->

### :star: Idea 3: Generating a table from CSV data

Suppose you have a CSV file containing data that you want to display as a table in your Markdown file.
You can use `pandas` to read the CSV file, convert it to a DataFrame, and then output it as a Markdown table.
<!-- SKIP -->
```markdown
<!-- START_CODE -->
<!-- import pandas as pd -->
<!-- csv_data = "Name,Age,Score\nAlice,30,90\nBob,25,85\nCharlie,22,95" -->
<!-- with open("sample_data.csv", "w") as f: -->
<!--     f.write(csv_data) -->
<!-- df = pd.read_csv("sample_data.csv") -->
<!-- print(df.to_markdown(index=False)) --> -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->
| Name     |   Age |   Score |
|:---------|------:|--------:|
| Alice    |    30 |      90 |
| Bob      |    25 |      85 |
| Charlie  |    22 |      95 |
<!-- END_OUTPUT -->
```

<!-- START_CODE -->
<!-- import pandas as pd -->
<!-- csv_data = "Name,Age,Score\nAlice,30,90\nBob,25,85\nCharlie,22,95" -->
<!-- with open("sample_data.csv", "w") as f: -->
<!--     f.write(csv_data) -->
<!-- df = pd.read_csv("sample_data.csv") -->
<!-- print(df.to_markdown(index=False)) -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->
| Name    |   Age |   Score |
|:--------|------:|--------:|
| Alice   |    30 |      90 |
| Bob     |    25 |      85 |
| Charlie |    22 |      95 |

<!-- END_OUTPUT -->

### :star: Idea 4: Displaying API data as a list

You can use `markdown-code-runner` to make API calls and display the data as a list in your Markdown file.
In this example, we'll use the `requests` library to fetch data from an API and display the results as a list.
<!-- SKIP -->
```markdown
<!-- START_CODE -->
<!-- import requests -->
<!-- response = requests.get("https://jsonplaceholder.typicode.com/todos?_limit=5") -->
<!-- todos = response.json() -->
<!-- for todo in todos: -->
<!--     print(f"- {todo['title']} (User ID: {todo['userId']}, Completed: {todo['completed']})") -->
<!-- END_CODE -->
<!-- START_OUTPUT -->
<!-- THIS CONTENT IS AUTOMATICALLY GENERATED -->
- delectus aut autem (User ID: 1, Completed: False)
- quis ut nam facilis et officia qui (User ID: 1, Completed: False)
- fugiat veniam minus (User ID: 1, Completed: False)
- et porro tempora (User ID: 1, Completed: True)
- laboriosam mollitia et enim quasi adipisci quia provident illum (User ID: 1, Completed: False)
<!-- END_OUTPUT -->
```

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
