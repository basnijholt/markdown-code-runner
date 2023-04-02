# :rocket: Markdown Code Runner

`markdown-code-runner` is a Python package that automatically executes code blocks within a Markdown file and updates the output in-place. This package is particularly useful for maintaining Markdown files with embedded code snippets, ensuring that the output displayed is up-to-date and accurate.

The package is hosted on GitHub: [https://github.com/basnijholt/markdown-code-runner](https://github.com/basnijholt/markdown-code-runner)

## :question: Problem Statement

When creating Markdown files with code examples, it's essential to keep the output of these code snippets accurate and up-to-date. Manually updating the output can be time-consuming and error-prone, especially when working with large files or multiple collaborators.

`markdown-code-runner` solves this problem by automatically executing the code blocks within a Markdown file and updating the output in-place. This ensures that the displayed output is always in sync with the code.

## :books: Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [:rocket: Markdown Code Runner](#rocket-markdown-code-runner)
  - [:question: Problem Statement](#question-problem-statement)
  - [:books: Table of Contents](#books-table-of-contents)
  - [:computer: Installation](#computer-installation)
  - [:rocket: Quick Start](#rocket-quick-start)
  - [Usage](#usage)
  - [:book: Examples](#book-examples)
    - [:star: Example 1: Simple code block](#star-example-1-simple-code-block)
    - [:star: Example 2: Multiple code blocks](#star-example-2-multiple-code-blocks)
  - [:bulb: Usage Ideas](#bulb-usage-ideas)
    - [:bar\_chart: Generating Markdown Tables](#bar_chart-generating-markdown-tables)
    - [:art: Generating Visualizations](#art-generating-visualizations)
  - [:page\_with\_curl: License](#page_with_curl-license)
  - [:handshake: Contributing](#handshake-contributing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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

### :bar_chart: Generating Markdown Tables

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

| Column A | Column B | Column C |
| --- | --- | --- |
| 52 | 93 | 15 |
| 72 | 61 | 21 |
| 83 | 87 | 75 |
| 75 | 88 | 24 |
| 3 | 22 | 53 |

<!-- END_OUTPUT -->

### :art: Generating Visualizations

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
img_html = f'<img src="data:image/png;base64,{quote(data)}" alt="Sample Line Plot"/>'

print(img_html)
```

<!-- START_CODE -->
<!-- import matplotlib.pyplot as plt -->
<!-- import io -->
<!-- import base64 -->
<!-- from urllib.parse import quote -->

<!-- # Example data for the plot -->
<!-- x = [1, 2, 3, 4, 5] -->
<!-- y = [2, 4, 6, 8, 10] -->

<!-- # Create a simple line plot -->
<!-- plt.plot(x, y) -->
<!-- plt.xlabel("X-axis") -->
<!-- plt.ylabel("Y-axis") -->
<!-- plt.title("Sample Line Plot") -->

<!-- # Save the plot to a BytesIO buffer -->
<!-- buf = io.BytesIO() -->
<!-- plt.savefig(buf, format='png', dpi=30) -->
<!-- plt.close() -->

<!-- # Encode the buffer as a base64 string -->
<!-- data = base64.b64encode(buf.getvalue()).decode('utf-8') -->

<!-- # Create an inline HTML img tag with the base64 string -->
<!-- img_html = f'<img src="data:image/png;base64,{quote(data)}" alt="Sample Line Plot"/>' -->

<!-- print(img_html) -->

<!-- END_CODE -->
<!-- START_OUTPUT -->

<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMAAAACQCAYAAABeUmTwAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjYuMywgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/P9b71AAAACXBIWXMAAASdAAAEnQF8NGuhAAAPOUlEQVR4nO3de1hTd5oH8G8CJMg1iAgol4ogELTCYGcLI2Ntt2prdWprq04X252nz7Pb8WmnsnZtZ9puH6sdpy1TCqvY6sy2q61anLWrKDqtxUstY0HlJoJAjIRbkEtIIiTkcuYPGwqOYgjn5HLO%2B/kvJHnP%2ByS/N7/fSX6cV8QwDANCBErs6gQIcSUqACJoVABE0KgAiKBRARBBowIggkYFQASNCoAIGhUAETQqACJoVAAO%2BOyzz7Blyxbs379/XM9TKpXYt2/fbe/bunUrAKCnpwfl5eV3jbVx40Zs3boVO3fuHH6uPccho3m7OgFPpFarERsbi4cffhjNzc0oLi6G2WxGeno6jh49Cq1Wi5SUFJhMJkyePBnd3d3Q6/V47rnnAACFhYUwGAyIiorCU089NSq2TqdDc3Mz9u7di9TUVGg0GiQnJ%2BPChQvw8fFBTk4OACAkJASvvvoq3njjDfj7%2B6OlpQUfffQRGIbB4sWLcerUKWRlZWH69OnOfnk8Cs0ADsjJyUFaWhpycnIwMDAAiUSCK1euAACWL1%2BOqKgorFu3DkajEQCwbNkyyGQy9Pf3AwDOnTuHkJAQ9PX13fEYoaGhWLt2LQYGBnDixAmEh4dDr9cP36/RaLBt2zYsWrQIAFBWVobs7GxERUXB19cXCxYsoMFvByoABxw%2BfBglJSUIDw9HXV0d/P39hwe7t7c3vL29IRaLIRKJAAAHDhxAe3s7goODAQAZGRnQaDRITEwcjllTU4O8vDwMDAwAALy8vIbve%2Bihh9DZ2YmEhIThv8lkMqxbtw5ZWVkAgMzMTOzevRutra2Qy%2BU4e/YsVCoVty8ED4hoOzS3PvnkEyxZsgQRERGuToXcBqcFoNFooFAoIJVKuToEERij0Yi4uDjIZDJW4nG6BFIoFDQNE1apVCooFArW4nH6LZBUKkV8fDxSUlK4PAwhDqOTYCJoVABE0Ca8BCorK8O5c%2BcglUrh7%2B%2BPtWvXDt/X1NSE%2BPj4iR6CCAzDMLBYGXh7cf/5POEjZGRkQKfTYeHChTCbzWzkRASsf9CEDUXVqG3XOuV4Ey6A%2Bvp6dHV14fjx46N%2BvAFAn/5kXKpUGrxSVIUXHpiJ1GiZU4454SVQUlISCgoK2MiFCBTDMPjzWSVUvQPIX5MGXx%2Bvuz%2BJJXQSTFxKMzCE//iiCmGBUry1PMWpgx%2Bg3aDEhc5f68NHp5rx2qPJmDHF3yU5UAEQp7NaGew8o4Baa3T6kudWtAQiTtV7Ywjrv6hEzGQ/vLlM7tLBD9AMQJzo%2B6u9%2BNO3CvzuUTliQv1cnQ4AKgDiBFYrg8JTzegfNKFgzU8g8XafhQcVAOFUt96Itw5dwvK507Aoxf3%2BJ4IKgHDmu%2BZu/O931/D6Y8mICnGPJc%2BtWC2Ajz/%2BGGKxGEuXLkVkZCSboYkHsVgZ/Pc3TTCYLSj4ZRp8nLCnx1GsZpacnAyRSITq6moANzfDEWHp0hrw0t6LmBMVhI1Lktx68AMszwCBgYHQ6XSYN28em2GJhzjTeB2fn2vBm8vkiAye5Op07MJqAaSmpiI1NXX4Nm2GEwazxYr8E41gABSsSXPKNma20EkwmZCO/kG8XVyH1ffF4OezwlydzrhRARCHlTZ04UBFK/5rWQrCg3xdnY5DqADIuJksVnzw1RVIvb2QvyYNXmKRq1NyGBUAGZc2zSDePlyHtRmxyIyf4up0JowKgNjtqzo1/r%2ByDW8/Phthgfy42BkVALmrIbMV7/%2B1AcGTfJC/Og1iD17y3IoKgIxJ1TuAzUfq8KufzcA/xYW6Oh3WUQGQOzpW24GjNZ14Z8UchAbwY8lzKyoA8g%2BMZgvePdaAsEAp8lal8mrJcytWC2DXrl0Qi8V48MEHcc8997AZmjiJsvsG3jl6Gf%2B2IA7psZNdnQ7nWC0Aq9UKtVoNP7%2BbW1/pynCe5XBVO05cVuMPT96LEH%2BJq9NxClY3bVgsFsTGxqKjo4PNsIRjBpMFbx26BLXWgA9WpQpm8AMszwAvvPDCqNv06e/%2Bmq/rsbWkHusWxjvtamzuhE6CBezgxVacaezG%2B0/NRfAkH1en4xKes2%2BVsGZwyILXv6yBdtCMXAEPfoBmAMFpVOvw7vEGvPRgAuZEBbs6HZejAhAIhmFQdL4V5Vd78cen5yLQV7if%2BiPREkgAbhjN%2BO3BWpgsVry78l4a/CPQDMBzlzu0%2BONXV7D%2Bn2dBPi3I1em4HSoAnmIYBnu/V6G6VYMPVqUiQEpv9e3QEoiHdAYTXv1LDbzFIvz%2BiTk0%2BMdArwzP1Lb148MTjXhlcSJmhQe6Oh23x%2BoMUFFRgQ0bNqClpQUAXRjLmRiGwe4yJfZ%2B34IPV6fS4LcTqwUwb948xMbGIiYmhs2w5C60BhNeOVANf6k3tqyYAz8JTez2YvWVUqvVo64JSnuBuFel0mBbaRP%2Bc0kS4qcGuDodj8NqAYSHh2PlypVshiR3YOuseK3nhsvbDHky%2BhbIA9k6K04JkGDTL2bT4J8AWix6mAstfdhx0rWdFfmECsBDuFNnRT6hJZAHsHVWjHaTzop8QjOAmytX9mLXGffqrMgnds8ASqUSu3fv5jIXMoLVymBbaRO%2BqlMjf00aDX6O2F0A27dvh5cXTb3O0K034jf7K5EwNQC/fTQZUm963bli1xKovb0dWVlZVABOUNbcg0%2B/U7p1Z0U%2BsasAgoKCkJCQALPZPObjioqKIBaLsXjxYgQE0K%2BS42H5YckzaHL/zop8YterHBAQgCNHjqC0tHTMx1VUVMDX1xdGoxEAbYazV5fOgJf2XcTs6Z7RWZFP7P4WaNasWRgcHBzzMXK5HDqdDm1tbQgN5d%2BVhLnwbWM3Pv/%2BGt54zHM6K/KJ3QXQ19cHpVI55mOeffbZUbdpM9yd2TorWhkgf7VndVbkE7sLoL6%2BHnK5nMtcBKOz34BNxZew6r4YLPDAzop8YlcBNDU1Yf369WhoaOA6H9472dCFIg/vrMgndhWAQqFAZWUlTCYT5s%2Bfz3VOvGTrrCjxFnt8Z0U%2BsasAGhoa8Mwzz2D69Olc58NLbZpBbC6uQ/b9/OisyCd2FcCLL77IdR689XWdGl9WtmHTL/jTWZFPaDMcR4bMVuT%2BtQGBvt74cDUtedwVFQAHbJ0V//VnM3A/Dzsr8gkVAMuE0FmRT6gAWCKkzop8wurPj4WFhSguLhbcXiBl9w28%2BPlFPDI7Av%2B%2BYCYNfg/C6gwQHR0Ng8EAvV4PqVQY039xdTu%2BrhNWZ0U%2BYXUGiIyMhFqtRnt7OwB%2B7wWydVbs7BdeZ0U%2BYXUGSE9PR3p6Opsh3ZKts%2BKvH5iJtJgQV6dDJoBOgsfpy4ttOH3lOt5fORfBftRpxdNRAdhpcMiCd45exswwf%2BQ%2BPRciEZ3o8gEVgB2osyJ/UQHcRVGFCueu9iL36bkIouZyvEP/hnQHN4xmvPZ/NTCarXhv5b00%2BHmKZoDbqO/U4v3jV7D%2B4QSkTKMlD59RAYzAMAz2latQ2aJB3mrqrCgEtAT6gc5gwsa/VEMEYOuT1FlRKFgtAJPJhFWrVrEZ0ilq2/qxfn8VfjV/Blb/NIa%2B4hQQVj/miouLkZWVNXy7qanJrbdDMAyDPX%2B7hroOHfLXpFJzOQFidQbQ6XRobm6GWq1mMywntAYTNhRVw9fHC79/gjorCpWIYRiGq%2BCXLl0CAKSkpHB1CIdUqTQo%2BKYJG5ckIoH66XoUtseUoD72GIbB/5xVQtlzAwVr0jBJQle7FjrBfAukGRhCzhdVCP2hsyINfgIIZAa40NKHwpPNeO2RJMSF0WXbyY94XQBWK4Nd3yrQrjGggDorktvg7RLI1llxmmwS3lqeQoOf3BYvZ4ByZS92nlbgd0uTERtKzaTJnfGqAKxWBjtON6NXP4SCX6ZRczlyV7xZAnXrjXhp30XETQnA64/JafATu/BiBihr7sEn313F60vliJ5MnRWJ/VgtgPLycpw%2BfRrZ2dmYOnUqm6Fvy9ZZ8caQGQVrfgKJN28mNOIkrI6YxMREaLVaSCQ3r5HD5ZXhbJ0V5ZFBeO2RZBr8xCGszgC1tbUICQlBf38/ZDIZm6FH%2BbaxG3v%2Bdg1vLpNjmow6KxLHsVoAmZmZyMzMHL7N9lZos8WK/G%2BaYLFaqZk0YYXHnATbOis%2BPS8aDyRyf35BhMEjCuBkQxe%2BqFDhzcdSEBFMnRUJe9y6AGydFX28xNRMmnDCbQugXTOITYfr8C/3x2J%2BAnVWJNxwywL4uk6Ng5Vt2PR4CqYG0pKHcMetCsDWWTFA6o186qxInMBtCsDWWfG5zBnImEmdFYlzuEUBHKvtxJGaDmxZMQdTqLMicSKXFoCts2JogAQfUmdF4gKsfq9YVlaGvLw8dHZ2Ahh7L9C1npudFZfMjsCvH4inwU9cgtUCyMjIgEgkQlBQ0F0f29FvwB%2BevBf33TOZzRQIGRdWl0B5eXmQSqUYGhqCn5/fmHuB7o%2BjE13ieqwWwMsvv8xmOEI4R3sLiKBx%2Bi2Q0WiESqXi8hBEYJqamhAdHc1aPE4LIC4u7o732b4hmsj/DLhDDHfIQUgxoqOjxxxX48Xp1aEJcXd0DkAEzekFYPuxDAB27NiB/Px8WCwWh2Ns3rwZJ0%2BedDiPzs5OfPrpp9i%2BfTv6%2B/sdjpGbm4uSkpJxPb%2B8vBy5ubno6upyOIeRMRzJARjd2srR92RkDEffk8LCQhQXF8NoNDr8eoyX0wsgIyMDAQE3r9AskUiQkJCA69evOxwjJiYG3d3dDuVh%2B9HOYrFg4cKFuHz5ssMxYmJioNVqYTQa7X7%2ByKtoOJrDyBiO5ACMbm3l6HsyMoaj70l0dDQMBgP0er3Dr8d4Ob0A6uvrcf78eVRXV8NoNKKxsRFhYWEOx4iIiEBNTQ3MZvO4YuTl5UEikaC8vBxeXl4oLS1FUlKSwzEiIyNx9erVcX1i2a6iUVVV5XAOI2M4kgPwY2urU6dOOfyejIzh6HsSGRkJtVqN1tZWh1%2BP8aKTYCJodBJMBI0KgAiaW/xDjJAUFRVBJpOBYRgsWrToH%2B6vr6/nfN1LfkTnAE5mMBiwYsUKlJSU4NChQzhz5gyef/55HDt2DOHh4dDr9QgLC0NPTw%2Bys7Ph4%2BPj6pR5jZZATrZnzx689957OHjwIHQ6HWJjY6FQKCASiYa/vkxMTERjYyN6enpcnC3/0QxABI1mACJoVABE0KgAiKD9Hfoh4RhRXa13AAAAAElFTkSuQmCC" alt="Sample Line Plot"/>

<!-- END_OUTPUT -->

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
