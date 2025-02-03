# CodeUnify: Combine Multiple Code Files into One

## Introduction

**CodeUnify** is a Python library that helps developers combine multiple source code files from a directory into a single output file. This library can include files of any type (e.g., Python, JavaScript, Java, C, etc.) and provides the flexibility to specify which files should be included. The combined output will be organized with comments indicating the start and end of each file, preserving context for each file in the combined output.

This tool is useful for **AI-assisted development tools** that need access to multiple files and their content for understanding context, tracking errors, or facilitating debugging. By combining all relevant files into a single file with clear markers, AI tools can process all the code at once and provide better context-based suggestions and error resolutions.

## Features

- **Combine files of any type**: The tool can handle any source code files (e.g., `.py`, `.js`, `.java`, `.c`, `.txt`, etc.).
- **Customizable comment formatting**: Easily add custom comments at the start and end of each file for better context.
- **Command-line integration**: Combine files directly from the command line with flexible options for file type inclusion and comment formatting.
- **Error Context**: For AI tools, having all files in one place with clear markers makes it easier to analyze errors and provide solutions with full context of the files in the directory.
- **Improved AI Assistance**: By providing all the code in a single output file, AI systems can better understand relationships between files, making their suggestions and error tracking more accurate.

## Installation

To install **CodeUnify**, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/takuphilchan/codeunify.git
    cd codeunify
    ```

2. **Install dependencies**:
    If you are using `pip`, you can install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure Python 3.x is installed**: This library works with Python 3.x versions. You can check your Python version using:
    ```bash
    python --version
    ```

## Usage

### 1. Combine Files with Default Settings

To combine all code files from a directory into a single output file using default settings, run the following command:

```bash
python combine.py /path/to/code/files output_combined_file.txt
```

This will combine all files in the specified directory (`/path/to/code/files`) and save the result in `output_combined_file.txt`. Each file will be surrounded by comments indicating its start and end.

### 2. Combine Files with Specific File Types

If you want to specify which types of files to combine (e.g., only `.py` and `.js` files), use the `--file_types` flag followed by the extensions:

```bash
python combine.py /path/to/code/files output_combined_file.txt --file_types .py .js
```

This command will only combine files with `.py` and `.js` extensions from the specified directory.

### 3. Customize Comment Format

You can also customize the comment format using the `--comment_format` flag. The format must be a dictionary in the form of a string, where `{filename}` will be replaced with the actual filename.

Example:

```bash
python combine.py /path/to/code/files output_combined_file.txt --comment_format "{'start': '// Begin {filename}', 'end': '// End {filename}'}"
```

This will use `// Begin {filename}` and `// End {filename}` as comments around each file.

### 4. Importing and Using the Function in Your Own Code

If you'd like to use this library programmatically in your Python scripts, you can import the `combine_files` function and call it directly:

```python
from codeunify.core.combine import combine_files

combine_files('/path/to/code/files', 'output_combined_file.txt', file_types=['.py', '.js'])
```

### 5. Testing and Ensuring Accuracy

You can run the provided test cases to verify the functionality of the library. The tests ensure that files are correctly combined, and the comment markers are correctly placed.

To run the tests, use:

```bash
python -m unittest discover tests
```

## Example

Let’s say you have the following files in a folder (`/projects/code/`):

- `app.py`:
  ```python
  def main():
      print("Hello, World!")
  ```

- `utils.js`:
  ```javascript
  function greet() {
      console.log("Hello from JS!");
  }
  ```

- `index.html`:
  ```html
  <html>
      <body>
          <h1>Welcome to my website</h1>
      </body>
  </html>
  ```

You can run the following command to combine all these files into one:

```bash
python combine.py /projects/code/ combined_output.txt
```

The resulting `combined_output.txt` will look something like this:

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

----- START: index.html -----

	 <html>
	     <body>
	         <h1>Welcome to my website</h1>
	     </body>
	 </html>

----- END: index.html -----

```

## How It Aids AI Tools

Many AI tools and systems need context from multiple files when analyzing or debugging code. By combining all relevant files into one file with clear markers, **CodeUnify** makes it easier for AI systems to:

1. **Provide Accurate Error Analysis**: The AI tool has access to all files in a single context, allowing it to trace errors across multiple files and give better, more holistic suggestions.
   
2. **Support Code Completion**: Having access to multiple related files lets the AI tool provide better code completion suggestions by knowing the content of all relevant files.

3. **Enhance Code Understanding**: AI tools that need to understand how various files interact with each other can process the entire set of files in one go, leading to more context-aware and intelligent recommendations.

4. **Facilitate Debugging**: When working with multiple files, it's easy to miss context or overlook interactions between files. Combining them into one allows AI systems to quickly spot issues that may otherwise be difficult to detect.

## Contributing

We welcome contributions! If you would like to improve this library, please fork the repository, make your changes, and submit a pull request.

## License

This library is licensed under the MIT License.

---
