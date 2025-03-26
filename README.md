# CodeUnify: Combine Multiple Code Files into One

## Introduction

**CodeUnify** is a Python library that helps developers combine multiple source code files from a directory into a single output file. It supports various programming languages and preserves the structure by marking the **start** and **end** of each file with appropriate comment styles.

This tool is particularly useful for **AI-assisted development tools**, enabling better **context-aware debugging, analysis, and assistance** by providing a unified file containing all necessary code components with clear section markers.

## Features

- **Combines files from multiple languages**: Supports `.py`, `.js`, `.cpp`, `.c`, `.java`, `.ts`, `.go`, `.cs`, `.html`, `.xml`, `.txt`, and more.
- **Per-file comment styles**: Each file retains its **own** comment style (`#`, `//`, `<!-- -->`, etc.), ensuring readability.
- **Indentation for clarity**: The contents of each file are indented under its respective section headers for easy visual distinction.
- **Command-line integration**: Run directly from the terminal with flexible options.
- **Excludes metadata and binary files**: Ignores `.git`, `__pycache__`, `.idea`, `.vscode`, and skips non-text files.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/takuphilchan/codeunify.git
    cd codeunify
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure Python 3.x is installed**:
    ```bash
    python --version
    ```

## Usage

# Installing the library via pip 
    ```bash
        pip install codeunify
    ```

### 1. Combine Files with Default Settings

To combine all code files from a directory into a single output file, run:

```bash
codeunify /path/to/code/files output_combined.txt
```

### 2. Combine Specific File Types

To only include certain file extensions (e.g., `.py` and `.js`):

```bash
codeunify /path/to/code/files output_combined.txt --file_types .py .js
```

### 3. Customize Indentation

The `--block_indent` flag allows adjusting how much each file's content is indented:

```bash
codeunify /path/to/code/files output_combined.txt --block_indent "    "
```

(Default indentation is a **tab** `\t`.)

## Example

### Given Input Files:

#### `app.py`:
```python
def main():
    print("Hello, World!")
```

#### `utils.js`:
```javascript
function greet() {
    console.log("Hello from JS!");
}
```

#### `index.html`:
```html
<html>
    <body>
        <h1>Welcome to my website</h1>
    </body>
</html>
```

### Running:
```bash
python combine.py /projects/code/ combined_output.txt
```

### **Correct Output:**
```txt
# >>>>> START: app.py <<<<<

	 def main():
	     print("Hello, World!")

# <<<<< END: app.py >>>>>

// >>>>> START: utils.js <<<<<

	 function greet() {
	     console.log("Hello from JS!");
	 }

// <<<<< END: utils.js >>>>>

<!-- >>>>> START: index.html <<<<< -->

	 <html>
	     <body>
	         <h1>Welcome to my website</h1>
	     </body>
	 </html>

<!-- <<<<< END: index.html >>>>> -->
```

## How It Helps AI-Assisted Development

- **Improved Code Context**: AI tools can analyze code **with clear section markers** instead of handling separate files.
- **Enhanced Debugging**: AI-powered debugging can **trace issues across multiple files** more effectively.
- **Better Code Completions**: By knowing the entire project's structure, AI can provide **better auto-suggestions**.

## Contributing

We welcome contributions! Feel free to fork the repository, make changes, and submit a pull request.

## License

This library is licensed under the MIT License.

