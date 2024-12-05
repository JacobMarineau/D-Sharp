## 🎵 D# - A Musical Programming Language

Welcome to D# (D-Sharp), an experimental musical programming language where code becomes melody. This project aims to blend programming concepts with musical expression, allowing users to compose music programmatically.

### 🚀 Features

Dynamic Music Composition: Define notes, melodies, and chords with intuitive syntax.
Custom Notations: Create reusable musical patterns.
Advanced Musical Expressions: Supports operations like base + 2 for note intervals.
Loops and Repeats: Iterate over musical elements with ease.
Extensibility: Add your custom parsing or musical logic.
📂 Project Structure

```bash
D-Sharp/
├── lexer.py         # Tokenizer for the language
├── parsers.py       # Parses the tokens and constructs the AST
├── program.ds       # Sample D# program
├── tests/           # Unit tests for the lexer and parser
└── README.md        # This file!
```

### 🛠️ Getting Started

#### Prerequisites
Python 3.9+: Ensure you have Python installed.
pip: Python's package manager (optional, for additional dependencies).

### Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/D-Sharp.git
cd D-Sharp
```

Run the sample program:

```bash
python3 parsers.py
```

### Usage
Create your own .ds files using the D# syntax. For example:

```ds
note tonic = "C";
play tonic;

note scale = ["C", "D", "E", "F", "G", "A", "B"];
repeat 4 times {
    play scale;
}

notation arpeggio(note base) {
    play base;
    play base + 2;
    play base + 4;
}

arpeggio("C");
```
Save it and modify parsers.py to parse your program file.

### 👩‍💻 How to Contribute

Fork the Repository: Make a copy under your own GitHub account.
Create a Branch: Add your feature or fix.

```bash
git checkout -b feature/new-idea
```

Write Tests: Ensure new features are covered.

Submit a Pull Request: Describe your changes and await feedback.

### Contributions Needed

Bug Fixes: Help identify and fix parsing issues.

Feature Enhancements: Add more syntax constructs or musical features.
Testing: Improve coverage for edge cases.

Documentation: Make this README even better!

### 📝 Current Challenges
play Parsing Issue: We’re currently debugging an issue where the parser misinterprets some play statements.

Expression Parsing: Handling base + 2 and similar expressions.

### 🌐 Community
Join the discussion on GitHub Issues. Share your ideas or report bugs!

### 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

### 🎶 Let’s Make Music!
Get coding and bring your musical ideas to life with D#. Feel free to reach out for help or to collaborate on new features. Happy coding! 👾🎼

