# Developer Notes: Documentation Architecture

This document explains the documentation build system and why it's set up the way it is.

## The Recursion Problem

The documentation for `markdown-code-runner` uses `markdown-code-runner` itself to generate content. This creates a potential recursion problem:

1. The docs contain **examples** showing how to use the tool (CODE:START, OUTPUT:START markers, etc.)
2. If these examples were executed by the tool, their OUTPUT sections would be filled with actual output
3. This would make them useless as examples - users need to see the *template* syntax, not executed results

## How We Solve It

### 1. CODE:SKIP Directive

Use `<!-- CODE:SKIP -->` before example code blocks to prevent them from being executed:

```markdown
<!-- CODE:SKIP --> <!-- Prevents the next code block from running -->
```python
print("This is an example that won't be executed")
```
```

### 2. PLACEHOLDER Pattern for Templates

OUTPUT sections in the repository contain only placeholder text:

```markdown
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->
```

This placeholder gets replaced with actual content during CI builds, but the generated content is **never committed** back to the repository.

### 3. Nested HTML Comment Escaping

When writing code that references markdown-code-runner markers inside HTML comments, you must escape them to avoid breaking markdown parsing:

```python
# BAD - nested HTML comments break parsing:
<!-- content = re.sub(r"<!-- SECTION:START -->.*?<!-- SECTION:END -->", ...) -->

# GOOD - use string concatenation to escape:
<!-- start_marker = "<!-" + "- SECTION:START -" + "->" -->
<!-- end_marker = "<!-" + "- SECTION:END -" + "->" -->
<!-- content = re.sub(start_marker + ".*?" + end_marker, ...) -->
```

## Documentation Build Process

1. **Source files** in `docs/` contain CODE blocks that pull content from README.md
2. **CI runs** `docs/docs_gen.py` which executes `markdown-code-runner` on all doc files
3. **Generated output** is used to build the documentation site
4. **Generated content is NOT committed** - only the templates with PLACEHOLDERs exist in the repo

## File Structure

- `docs/docs_gen.py` - Script that processes all markdown files for documentation build
- `docs/*.md` - Documentation templates with CODE/OUTPUT blocks
- `README.md` - Source of truth for content (uses SECTION markers)

## Pre-commit Hook

The `Verify docs templates have placeholders` pre-commit hook ensures that OUTPUT sections contain PLACEHOLDER text, preventing accidental commits of generated content.

## Why Not Commit Generated Output?

1. **Copyability**: Users copying examples from the docs get clean templates, not filled-in output
2. **Recursion avoidance**: Examples remain as examples, not executed results
3. **Single source of truth**: README.md is the source; docs pull from it
4. **Cleaner diffs**: No noise from regenerated output in every commit
