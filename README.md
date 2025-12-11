# Developer Horoscope Generator 🪐

This is a small, playful static-analysis tool that reads a Python file and generates a "developer horoscope" based on simple code metrics.

Under the humor, it demonstrates how to:

- Parse Python code using the built-in `ast` module
- Collect basic code-quality metrics (lines, comments, TODOs, functions, average function length)
- Turn metrics into human-readable feedback

## Features

- Counts total lines of code
- Counts comment lines and `TODO` markers
- Detects number of functions using the AST
- Estimates average function length
- Generates a playful "horoscope" with messages about your coding style

## Usage

```bash
python3 main.py path/to/your_file.py
