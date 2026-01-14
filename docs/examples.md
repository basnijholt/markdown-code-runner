---
icon: lucide/book-open
---

# Examples

Real-world examples demonstrating the power and flexibility of `markdown-code-runner`.

<!-- CODE:START -->
<!-- from docs_gen import readme_section -->
<!-- print(readme_section("examples")) -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->
```

After running `markdown-code-runner`:
```markdown
This is an example of a simple code block:

<!-- CODE:START -->
<!-- print('Hello, world!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->
```

### Example 2: Multiple code blocks
<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed -->
```markdown
Here are two code blocks:

First code block:

<!-- CODE:START -->
<!-- print('Hello, world!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->
```

<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed --> <!-- This is here otherwise the next example gets executed -->
```markdown
Second code block:

<!-- CODE:START -->
<!-- print('Hello again!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
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
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

Second code block:

<!-- CODE:START -->
<!-- print('Hello again!') -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->
```

<!-- OUTPUT:END -->

## Usage Ideas

<!-- CODE:START -->
<!-- from docs_gen import readme_section -->
<!-- content = readme_section("usage-ideas", strip_heading=True) -->
<!-- # Remove the github-actions section since it's on its own page -->
<!-- import re -->
<!-- # Find where github-actions section starts and ends -->
<!-- start_marker = "<!-" + "- SECTION:github-actions:START -" + "->" -->
<!-- end_marker = "<!-" + "- SECTION:github-actions:END -" + "->" -->
<!-- pattern = start_marker + ".*?" + end_marker -->
<!-- content = re.sub(pattern, "", content, flags=re.DOTALL) -->
<!-- print(content) -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

### Idea 3: Generating Markdown Tables

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

Which is rendered as:

<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

### Idea 4: Generating Visualizations

Create a visualization using the `matplotlib` library and save it as an image. Then, reference the image in your Markdown file. The following example demonstrates how to create a bar chart.

Using a triple-backtick code block:

<!-- CODE:SKIP --> <!-- This is here otherwise the next example gets executed -->
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
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

> **NOTE**: This output is disabled here because GitHub Markdown doesn't support inline image HTML. This will work on other Markdown renderers.

### Idea 5: Generating a table from CSV data

Suppose you have a CSV file containing data that you want to display as a table in your Markdown file.
You can use `pandas` to read the CSV file, convert it to a DataFrame, and then output it as a Markdown table.

Using a triple-backtick code block:

```python
import pandas as pd
csv_data = "Name,Age,Score\nAlice,30,90\nBob,25,85\nCharlie,22,95"
with open("sample_data.csv", "w") as f:
    f.write(csv_data)
df = pd.read_csv("sample_data.csv")
print(df.to_markdown(index=False))
```

Which is rendered as:

<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

### Idea 6: Displaying API data as a list

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
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->


### Idea 7: Run a Rust program

We can use `markdown-code-runner` to write Rust code to a file and then a hidden bash code block to run the code and display the output.

The code below *is actually executed*, check out the [`README.md` in plain text](https://github.com/basnijholt/markdown-code-runner/blob/main/README.md?plain=1) to see how this works.

```rust
fn main() {
    println!("Hello, world!");
}
```

Which when executed produces:

<!-- CODE:BASH:START -->
<!-- echo '```' -->
<!-- rustc main.rs && ./main -->
<!-- echo '```' -->
<!-- CODE:END -->

<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

These are just a few examples of how you can use Markdown Code Runner to enhance your Markdown documents with dynamic content. The possibilities are endless!

<!-- OUTPUT:END -->

## More Ideas

Here are additional creative uses for `markdown-code-runner`:

### Auto-Generate Package Statistics

```python
# Fetch package download statistics
import requests

url = "https://api.pepy.tech/api/v2/projects/markdown-code-runner"
# Note: This would require an API key in practice
print("Download statistics would appear here!")
```

### Document Your API

```python
# Auto-generate API documentation from docstrings
import inspect
from markdown_code_runner import update_markdown_file

# Get function signature
sig = inspect.signature(update_markdown_file)
print(f"**Signature:** `update_markdown_file{sig}`")
print()

# Get docstring
doc = update_markdown_file.__doc__
if doc:
    print(doc)
```

### Include Test Results

```python
# Show test coverage or test results
import subprocess
result = subprocess.run(
    ["python", "-c", "print('All tests passed!')"],
    capture_output=True,
    text=True
)
print(result.stdout)
```

### Dynamic Configuration Examples

```python
# Generate configuration examples from actual defaults
print("Default markers used by markdown-code-runner:")
print()
print("| Marker | Purpose |")
print("|--------|---------|")
print("| `<!-- CODE:START -->` | Start of hidden Python code |")
print("| `<!-- CODE:END -->` | End of hidden code block |")
print("| `<!-- CODE:BASH:START -->` | Start of hidden Bash code |")
print("| `<!-- OUTPUT:START -->` | Start of output section |")
print("| `<!-- OUTPUT:END -->` | End of output section |")
print("| `<!-- CODE:SKIP -->` | Skip the next code block |")
```
