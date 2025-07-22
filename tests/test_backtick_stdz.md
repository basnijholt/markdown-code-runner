# Backtick Standardization Test

This file tests various backtick code block scenarios.

## Basic Code Block
A simple Python code block with markdown-code-runner:
Currently no options are supported for backtick code blocks. May be used in the future.

```python markdown-code-runner filename=test1.py
print("Basic test")
```

## Code Block with Multiple Options
Testing multiple options in the backtick header:

```javascript markdown-code-runner filename=test2.js debug=true skip=false
console.log("Multiple options test")
```

## Language-only Block
This block should remain unchanged during standardization:

```rust
fn main() {
    println!("No markdown-code-runner");
}
```

## Complex Options Block
Testing complex options and spacing:

```python   markdown-code-runner    filename=test3.py   debug=true   skip=false
print("Testing spaces in options")
```

## Empty Language Block
Testing block with no language:

```markdown-code-runner filename=test4.txt
Just some plain text
```

## Mixed Content Block
Testing with additional content after options:

```python markdown-code-runner filename=test5.py some random text here
print("Mixed content test")
```
