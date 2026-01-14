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

## Usage Ideas

<!-- CODE:START -->
<!-- from docs_gen import readme_section -->
<!-- content = readme_section("usage-ideas", strip_heading=True) -->
<!-- # Remove the github-actions section since it's on its own page -->
<!-- import re -->
<!-- # Find where github-actions section starts and ends -->
<!-- content = re.sub(r"<!-- SECTION:github-actions:START -->.*?<!-- SECTION:github-actions:END -->", "", content, flags=re.DOTALL) -->
<!-- print(content) -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

## More Ideas

Here are additional creative uses for `markdown-code-runner`:

### Auto-Generate Package Statistics

```python markdown-code-runner
# Fetch package download statistics
import requests

url = "https://api.pepy.tech/api/v2/projects/markdown-code-runner"
# Note: This would require an API key in practice
print("Download statistics would appear here!")
```

### Document Your API

```python markdown-code-runner
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

```python markdown-code-runner
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

```python markdown-code-runner
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
