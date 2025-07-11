# Backtick Standardization Test

This file tests various backtick code block scenarios.

## Basic Code Block
A simple Python code block with markdown-code-runner:

```python
print("Basic test")
```

## Code Block with Multiple Options
Testing multiple options in the backtick header:

```javascript
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

```python
print("Testing spaces in options")
```

## Empty Language Block
Testing block with no language:

```
Just some plain text
```

## Mixed Content Block
Testing with additional content after options:

```python
print("Mixed content test")
```
