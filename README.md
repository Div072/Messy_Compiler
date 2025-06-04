# Messy_Compiler

A learning-oriented C compiler project written in Python.  
The goal of this project is to build a compiler for a subset of the C language from scratch, to deepen understanding of compiler internals including lexing, parsing, semantic analysis, intermediate representation (IR), and x86 assembly code generation.

## Features

- **Lexical Analysis:** Tokenizes C-like source code into a stream of tokens.
- **Parsing:** Builds abstract syntax trees (ASTs) for function declarations, expressions, basic control flow (if/else), and variable declarations.
- **Semantic Analysis:** Resolves variable names, scopes, and checks for duplicate declarations.
- **Intermediate Representation (IR):** Converts high-level AST into an intermediate code structure for further processing.
- **Assembly Code Generation:** Generates x86 assembly instructions from IR.
- **Basic Error Handling:** Detects some syntax errors such as missing semicolons or parentheses.

## Getting Started

### Prerequisites

- Python 3.8 or newer

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Div072/Messy_Compiler.git
    cd Messy_Compiler
    ```
2. (Optional) Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

### Usage

Compile a simple C-like source file:

```sh
python main.py path/to/source_file.c
```

> **Note:** The input language is a C subset. See [Supported Features](#supported-features).

### Example

Given the following input code:
```c
int main() {
    int a = 5;
    int b = 10;
    return a + b;
}
```
The compiler will tokenize, parse, analyze, and generate corresponding (x86) assembly output.

## Supported Features

- Integer variables and literals
- Arithmetic expressions (`+`, `-`, `*`, `/`, `%`)
- Comparison operators (`<`, `<=`, `>`, `>=`, `==`, `!=`)
- Bitwise operators (`&`, `|`, `^`, `<<`, `>>`)
- Unary operators (`-`, `~`, `!`)
- If/Else statements
- Return statements
- Block scoping

## Project Structure

```
Messy_Compiler/
│
├── lexer.py           # Lexical analyzer
├── parser.py          # Parser and AST construction
├── Resolution.py      # Semantic analysis and scope resolution
├── IR_code.py         # Intermediate representation structures
├── Ass_Ast.py         # Assembly-level AST structures
├── ass_traverser.py   # Assembly code generation
├── main.py            # Entry point (if present)
├── README.md
└── LICENSE
```


## Roadmap

- [ ] Add support for more data types (floats, char)
- [ ] Implement arrays, structs, and pointers
- [ ] Improve error messages and reporting
- [ ] Add more comprehensive tests
- [ ] Expand code generation to support more target architectures

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

---

**Learning through building!**
