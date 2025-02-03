# >>>>> START: codeunify/README.md <<<<<

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
	# Start of app.py
	def main():
	    print("Hello, World!")
	# End of app.py
	
	# Start of utils.js
	function greet() {
	    console.log("Hello from JS!");
	}
	# End of utils.js
	
	# Start of index.html
	<html>
	    <body>
	        <h1>Welcome to my website</h1>
	    </body>
	</html>
	# End of index.html
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

# <<<<< END: codeunify/README.md >>>>>

# >>>>> START: codeunify/requirements.txt <<<<<

	numpy

# <<<<< END: codeunify/requirements.txt >>>>>

# >>>>> START: codeunify/__init__.py <<<<<



# <<<<< END: codeunify/__init__.py >>>>>

# >>>>> START: codeunify/core/combine.py <<<<<

	import os
	import logging
	import argparse
	import mimetypes
	
	# Set up logging
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
	logger = logging.getLogger(__name__)
	
	# List of metadata directories to exclude
	EXCLUDED_DIRS = {'.git', '__pycache__', '.idea', '.vscode'}
	
	# Set of common programming/text file extensions that we consider as text,
	# even if mimetypes.guess_type returns None or a non-text value.
	COMMON_TEXT_EXTENSIONS = {'.py', '.js', '.cpp', '.c', '.java', '.cu', '.h', '.hpp', '.cs', '.rb', '.php', '.go', '.rs', '.ts'}
	
	def get_default_comment_format(output_file):
	    """
	    Returns a default comment format dictionary based on the output file's extension.
	    For example, for .py files it returns markers using '#' and for languages like
	    .js, .cpp, .java, etc. it returns markers using '//'. For .txt files, a dashed style is used.
	    """
	    ext = os.path.splitext(output_file)[1].lower()
	    if ext in {'.py', '.sh', '.rb', '.pl'}:
	        comment_char = '#'
	    elif ext in {'.js', '.ts', '.c', '.cpp', '.java', '.cs', '.go', '.cu'}:
	        comment_char = '//'
	    elif ext in {'.txt'}:
	        comment_char = ''
	    else:
	        comment_char = '#'  # default fallback
	
	    if comment_char:
	        start = f"{comment_char} >>>>> START: {{filepath}} <<<<<"
	        end = f"{comment_char} <<<<< END: {{filepath}} >>>>>"
	    else:
	        start = f"----- START: {{filepath}} -----"
	        end = f"----- END: {{filepath}} -----"
	    return {"start": start, "end": end}
	
	def combine_files(input_dir, output_file, file_types=None, comment_format=None, block_indent="\t"):
	    """
	    Combines all code files in the given directory and its subdirectories into a single file.
	    Each section will be prefixed with a comment containing the original file's path, starting with the input folder name.
	    Optionally, the file content can be indented (block_indent) to visually separate it from the markers.
	    
	    Parameters:
	    - input_dir (str): Directory containing the code files to combine.
	    - output_file (str): Path where the combined code should be saved.
	    - file_types (list): List of file extensions to include. Defaults to None (include all files).
	    - comment_format (dict): Custom comment format. 
	        Defaults to one based on output_file extension.
	    - block_indent (str): String used to indent each line of file content. Default is "\t" (a tab).
	    
	    Raises:
	    - FileNotFoundError: If the input directory is not found.
	    - ValueError: If no valid code files are found.
	    """
	    if file_types is None:
	        file_types = []  # Allow all file types by default
	    if comment_format is None:
	        comment_format = get_default_comment_format(output_file)
	    
	    # Check if the input directory exists
	    if not os.path.exists(input_dir):
	        logger.error(f"The directory '{input_dir}' does not exist.")
	        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")
	    
	    # Convert input_dir to an absolute path and get its basename (e.g., examples_folder)
	    abs_input_dir = os.path.abspath(input_dir)
	    input_dir_name = os.path.basename(abs_input_dir)
	    
	    # Recursively collect files that match the file_types criteria (or all files if file_types is empty)
	    files_to_combine = []
	    for root, _, files in os.walk(abs_input_dir):
	        # Skip metadata directories
	        if any(excluded in root.split(os.sep) for excluded in EXCLUDED_DIRS):
	            continue
	        for filename in files:
	            if not file_types or any(filename.endswith(ext) for ext in file_types):
	                files_to_combine.append(os.path.join(root, filename))
	    
	    if not files_to_combine:
	        logger.error(f"No valid code files found in the directory '{input_dir}'.")
	        raise ValueError(f"No valid code files found in the directory '{input_dir}'.")
	    
	    logger.info(f"Found {len(files_to_combine)} files to combine.")
	    
	    # Write the combined content to the output file
	    with open(output_file, 'w', encoding='utf-8') as outfile:
	        for filepath in files_to_combine:
	            try:
	                # Determine the file extension in lowercase
	                ext = os.path.splitext(filepath)[1].lower()
	                # Attempt to guess the MIME type of the file
	                mime_type, _ = mimetypes.guess_type(filepath)
	                # If MIME type is not detected or doesn't indicate text, check if the extension is known
	                if (mime_type is None or not mime_type.startswith("text")) and ext not in COMMON_TEXT_EXTENSIONS:
	                    logger.warning(f"Skipping non-text (binary) file: {filepath}")
	                    continue
	
	                with open(filepath, 'r', encoding='utf-8') as infile:
	                    # Get the path relative to the input directory and prepend the input folder name
	                    relative_path = os.path.relpath(filepath, abs_input_dir)
	                    display_path = os.path.join(input_dir_name, relative_path)
	                    
	                    # Write a comment marking the start of the file content
	                    start_comment = comment_format["start"].format(filepath=display_path)
	                    outfile.write(f"{start_comment}\n\n")
	                    
	                    # Read the file's content and indent each line with block_indent
	                    content = infile.read()
	                    content = "\n".join(block_indent + line for line in content.splitlines())
	                    outfile.write(content)
	                    outfile.write("\n\n")  # Add spacing between files
	                    
	                    # Write a comment marking the end of the file content
	                    end_comment = comment_format["end"].format(filepath=display_path)
	                    outfile.write(f"{end_comment}\n\n")
	            except Exception as e:
	                logger.error(f"Error reading file {filepath}: {e}")
	                continue  # Skip files that cause errors
	
	    logger.info(f"All files have been successfully combined into '{output_file}'.")
	
	def parse_args():
	    """
	    Parses command line arguments.
	    """
	    parser = argparse.ArgumentParser(description="Combine code files into a single output file, preserving folder structure.")
	    parser.add_argument('input_dir', help="Directory containing the code files to combine")
	    parser.add_argument('output_file', help="Path where the combined code should be saved")
	    parser.add_argument('--file_types', nargs='*', default=[], 
	                        help="List of file extensions to include (e.g., .py .txt). Default is to include all files.")
	    parser.add_argument('--comment_format', type=str, default=None,
	                        help=("Custom comment format as a dictionary string. "
	                              "For example: \"{'start': '# Begin: {filepath}', 'end': '# Finish: {filepath}'}\""))
	    parser.add_argument('--block_indent', type=str, default="\t",
	                        help="String to prepend to each line of the file content (default is a tab).")
	    return parser.parse_args()
	
	def main():
	    args = parse_args()
	    
	    # If a custom comment format is provided, attempt to convert it into a dictionary
	    if args.comment_format:
	        try:
	            comment_format = eval(args.comment_format)
	            if not isinstance(comment_format, dict):
	                raise ValueError("comment_format must be a dictionary.")
	        except Exception as e:
	            logger.error(f"Error parsing comment_format: {e}")
	            return
	    else:
	        comment_format = None
	    
	    try:
	        combine_files(args.input_dir, args.output_file, args.file_types, comment_format, args.block_indent)
	    except Exception as e:
	        logger.error(f"An error occurred: {e}")
	
	if __name__ == "__main__":
	    main()

# <<<<< END: codeunify/core/combine.py >>>>>

# >>>>> START: codeunify/core/__init__.py <<<<<



# <<<<< END: codeunify/core/__init__.py >>>>>

# >>>>> START: codeunify/examples/combined_output_example.py <<<<<

	# >>>>> START: codeunify/README.md <<<<<
	
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
		# Start of app.py
		def main():
		    print("Hello, World!")
		# End of app.py
		
		# Start of utils.js
		function greet() {
		    console.log("Hello from JS!");
		}
		# End of utils.js
		
		# Start of index.html
		<html>
		    <body>
		        <h1>Welcome to my website</h1>
		    </body>
		</html>
		# End of index.html
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
	
	# <<<<< END: codeunify/README.md >>>>>
	
	# >>>>> START: codeunify/requirements.txt <<<<<
	
		numpy
	
	# <<<<< END: codeunify/requirements.txt >>>>>
	
	# >>>>> START: codeunify/__init__.py <<<<<
	
	
	
	# <<<<< END: codeunify/__init__.py >>>>>
	
	# >>>>> START: codeunify/core/combine.py <<<<<
	
		import os
		import logging
		import argparse
		import mimetypes
		
		# Set up logging
		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
		logger = logging.getLogger(__name__)
		
		# List of metadata directories to exclude
		EXCLUDED_DIRS = {'.git', '__pycache__', '.idea', '.vscode'}
		
		# Set of common programming/text file extensions that we consider as text,
		# even if mimetypes.guess_type returns None or a non-text value.
		COMMON_TEXT_EXTENSIONS = {'.py', '.js', '.cpp', '.c', '.java', '.cu', '.h', '.hpp', '.cs', '.rb', '.php', '.go', '.rs', '.ts'}
		
		def get_default_comment_format(output_file):
		    """
		    Returns a default comment format dictionary based on the output file's extension.
		    For example, for .py files it returns markers using '#' and for languages like
		    .js, .cpp, .java, etc. it returns markers using '//'. For .txt files, a dashed style is used.
		    """
		    ext = os.path.splitext(output_file)[1].lower()
		    if ext in {'.py', '.sh', '.rb', '.pl'}:
		        comment_char = '#'
		    elif ext in {'.js', '.ts', '.c', '.cpp', '.java', '.cs', '.go', '.cu'}:
		        comment_char = '//'
		    elif ext in {'.txt'}:
		        comment_char = ''
		    else:
		        comment_char = '#'  # default fallback
		
		    if comment_char:
		        start = f"{comment_char} >>>>> START: {{filepath}} <<<<<"
		        end = f"{comment_char} <<<<< END: {{filepath}} >>>>>"
		    else:
		        start = f"----- START: {{filepath}} -----"
		        end = f"----- END: {{filepath}} -----"
		    return {"start": start, "end": end}
		
		def combine_files(input_dir, output_file, file_types=None, comment_format=None, block_indent="\t"):
		    """
		    Combines all code files in the given directory and its subdirectories into a single file.
		    Each section will be prefixed with a comment containing the original file's path, starting with the input folder name.
		    Optionally, the file content can be indented (block_indent) to visually separate it from the markers.
		    
		    Parameters:
		    - input_dir (str): Directory containing the code files to combine.
		    - output_file (str): Path where the combined code should be saved.
		    - file_types (list): List of file extensions to include. Defaults to None (include all files).
		    - comment_format (dict): Custom comment format. 
		        Defaults to one based on output_file extension.
		    - block_indent (str): String used to indent each line of file content. Default is "\t" (a tab).
		    
		    Raises:
		    - FileNotFoundError: If the input directory is not found.
		    - ValueError: If no valid code files are found.
		    """
		    if file_types is None:
		        file_types = []  # Allow all file types by default
		    if comment_format is None:
		        comment_format = get_default_comment_format(output_file)
		    
		    # Check if the input directory exists
		    if not os.path.exists(input_dir):
		        logger.error(f"The directory '{input_dir}' does not exist.")
		        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")
		    
		    # Convert input_dir to an absolute path and get its basename (e.g., examples_folder)
		    abs_input_dir = os.path.abspath(input_dir)
		    input_dir_name = os.path.basename(abs_input_dir)
		    
		    # Recursively collect files that match the file_types criteria (or all files if file_types is empty)
		    files_to_combine = []
		    for root, _, files in os.walk(abs_input_dir):
		        # Skip metadata directories
		        if any(excluded in root.split(os.sep) for excluded in EXCLUDED_DIRS):
		            continue
		        for filename in files:
		            if not file_types or any(filename.endswith(ext) for ext in file_types):
		                files_to_combine.append(os.path.join(root, filename))
		    
		    if not files_to_combine:
		        logger.error(f"No valid code files found in the directory '{input_dir}'.")
		        raise ValueError(f"No valid code files found in the directory '{input_dir}'.")
		    
		    logger.info(f"Found {len(files_to_combine)} files to combine.")
		    
		    # Write the combined content to the output file
		    with open(output_file, 'w', encoding='utf-8') as outfile:
		        for filepath in files_to_combine:
		            try:
		                # Determine the file extension in lowercase
		                ext = os.path.splitext(filepath)[1].lower()
		                # Attempt to guess the MIME type of the file
		                mime_type, _ = mimetypes.guess_type(filepath)
		                # If MIME type is not detected or doesn't indicate text, check if the extension is known
		                if (mime_type is None or not mime_type.startswith("text")) and ext not in COMMON_TEXT_EXTENSIONS:
		                    logger.warning(f"Skipping non-text (binary) file: {filepath}")
		                    continue
		
		                with open(filepath, 'r', encoding='utf-8') as infile:
		                    # Get the path relative to the input directory and prepend the input folder name
		                    relative_path = os.path.relpath(filepath, abs_input_dir)
		                    display_path = os.path.join(input_dir_name, relative_path)
		                    
		                    # Write a comment marking the start of the file content
		                    start_comment = comment_format["start"].format(filepath=display_path)
		                    outfile.write(f"{start_comment}\n\n")
		                    
		                    # Read the file's content and indent each line with block_indent
		                    content = infile.read()
		                    content = "\n".join(block_indent + line for line in content.splitlines())
		                    outfile.write(content)
		                    outfile.write("\n\n")  # Add spacing between files
		                    
		                    # Write a comment marking the end of the file content
		                    end_comment = comment_format["end"].format(filepath=display_path)
		                    outfile.write(f"{end_comment}\n\n")
		            except Exception as e:
		                logger.error(f"Error reading file {filepath}: {e}")
		                continue  # Skip files that cause errors
		
		    logger.info(f"All files have been successfully combined into '{output_file}'.")
		
		def parse_args():
		    """
		    Parses command line arguments.
		    """
		    parser = argparse.ArgumentParser(description="Combine code files into a single output file, preserving folder structure.")
		    parser.add_argument('input_dir', help="Directory containing the code files to combine")
		    parser.add_argument('output_file', help="Path where the combined code should be saved")
		    parser.add_argument('--file_types', nargs='*', default=[], 
		                        help="List of file extensions to include (e.g., .py .txt). Default is to include all files.")
		    parser.add_argument('--comment_format', type=str, default=None,
		                        help=("Custom comment format as a dictionary string. "
		                              "For example: \"{'start': '# Begin: {filepath}', 'end': '# Finish: {filepath}'}\""))
		    parser.add_argument('--block_indent', type=str, default="\t",
		                        help="String to prepend to each line of the file content (default is a tab).")
		    return parser.parse_args()
		
		def main():
		    args = parse_args()
		    
		    # If a custom comment format is provided, attempt to convert it into a dictionary
		    if args.comment_format:
		        try:
		            comment_format = eval(args.comment_format)
		            if not isinstance(comment_format, dict):
		                raise ValueError("comment_format must be a dictionary.")
		        except Exception as e:
		            logger.error(f"Error parsing comment_format: {e}")
		            return
		    else:
		        comment_format = None
		    
		    try:
		        combine_files(args.input_dir, args.output_file, args.file_types, comment_format, args.block_indent)
		    except Exception as e:
		        logger.error(f"An error occurred: {e}")
		
		if __name__ == "__main__":
		    main()
	
	# <<<<< END: codeunify/core/combine.py >>>>>
	
	# >>>>> START: codeunify/core/__init__.py <<<<<
	
	
	

# <<<<< END: codeunify/examples/combined_output_example.py >>>>>

# >>>>> START: codeunify/examples/example.py <<<<<

	from codeunify.core.combine import combine_files
	
	# Path to the examples directory and the desired output file name
	input_dir = '/mnt/d/programming/new_lib/codeunify/codeunify'
	output_file = '/mnt/d/programming/new_lib/codeunify/codeunify/examples/combined_output_example.py'
	
	# Combine the files in the examples directory
	combine_files(input_dir, output_file)

# <<<<< END: codeunify/examples/example.py >>>>>

# >>>>> START: codeunify/examples/example_files/file1.py <<<<<

	# This Python script processes a dataset and outputs basic statistics.
	
	import numpy as np
	
	# Dataset
	data = [12, 15, 17, 19, 24, 29, 33, 35, 39]
	
	# Calculate mean and standard deviation
	mean = np.mean(data)
	std_dev = np.std(data)
	
	# Output results
	print(f"Mean: {mean}")
	print(f"Standard Deviation: {std_dev}")

# <<<<< END: codeunify/examples/example_files/file1.py >>>>>

# >>>>> START: codeunify/examples/example_files/file2.js <<<<<

	// This JavaScript script validates a user's input on a form before submission.
	
	function validateForm(form) {
	    let isValid = true;
	    if (form.name.value === "") {
	        alert("Name must be filled out");
	        isValid = false;
	    }
	    if (form.email.value === "") {
	        alert("Email must be filled out");
	        isValid = false;
	    }
	    return isValid;
	}
	
	// Example usage of validation function
	let form = {
	    name: { value: "" },
	    email: { value: "test@example.com" },
	};
	console.log(validateForm(form));  // Should return false due to empty name field

# <<<<< END: codeunify/examples/example_files/file2.js >>>>>

# >>>>> START: codeunify/examples/example_files/file3.java <<<<<

	// This Java program reads from and writes to a file.
	
	import java.io.*;
	
	public class FileReaderWriter {
	    public static void main(String[] args) {
	        String filePath = "output.txt";
	
	        // Writing to a file
	        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
	            writer.write("Hello, this is a file handling example in Java!");
	            writer.newLine();
	            writer.write("Writing multiple lines to the file.");
	        } catch (IOException e) {
	            System.out.println("An error occurred while writing to the file.");
	        }
	
	        // Reading from a file
	        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
	            String line;
	            while ((line = reader.readLine()) != null) {
	                System.out.println(line);
	            }
	        } catch (IOException e) {
	            System.out.println("An error occurred while reading the file.");
	        }
	    }
	}

# <<<<< END: codeunify/examples/example_files/file3.java >>>>>

# >>>>> START: codeunify/examples/example_files/module/file1.py <<<<<

	# This Python script processes a dataset and outputs basic statistics.
	
	import numpy as np
	
	# Dataset
	data = [12, 15, 17, 19, 24, 29, 33, 35, 39]
	
	# Calculate mean and standard deviation
	mean = np.mean(data)
	std_dev = np.std(data)
	
	# Output results
	print(f"Mean: {mean}")
	print(f"Standard Deviation: {std_dev}")

# <<<<< END: codeunify/examples/example_files/module/file1.py >>>>>

# >>>>> START: codeunify/examples/example_files/module/file2.js <<<<<

	// This JavaScript script validates a user's input on a form before submission.
	
	function validateForm(form) {
	    let isValid = true;
	    if (form.name.value === "") {
	        alert("Name must be filled out");
	        isValid = false;
	    }
	    if (form.email.value === "") {
	        alert("Email must be filled out");
	        isValid = false;
	    }
	    return isValid;
	}
	
	// Example usage of validation function
	let form = {
	    name: { value: "" },
	    email: { value: "test@example.com" },
	};
	console.log(validateForm(form));  // Should return false due to empty name field

# <<<<< END: codeunify/examples/example_files/module/file2.js >>>>>

# >>>>> START: codeunify/examples/example_files/module/file3.java <<<<<

	// This Java program reads from and writes to a file.
	
	import java.io.*;
	
	public class FileReaderWriter {
	    public static void main(String[] args) {
	        String filePath = "output.txt";
	
	        // Writing to a file
	        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
	            writer.write("Hello, this is a file handling example in Java!");
	            writer.newLine();
	            writer.write("Writing multiple lines to the file.");
	        } catch (IOException e) {
	            System.out.println("An error occurred while writing to the file.");
	        }
	
	        // Reading from a file
	        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
	            String line;
	            while ((line = reader.readLine()) != null) {
	                System.out.println(line);
	            }
	        } catch (IOException e) {
	            System.out.println("An error occurred while reading the file.");
	        }
	    }
	}

# <<<<< END: codeunify/examples/example_files/module/file3.java >>>>>

# >>>>> START: codeunify/examples/example_files/module2/file1.py <<<<<

	# This Python script processes a dataset and outputs basic statistics.
	
	import numpy as np
	
	# Dataset
	data = [12, 15, 17, 19, 24, 29, 33, 35, 39]
	
	# Calculate mean and standard deviation
	mean = np.mean(data)
	std_dev = np.std(data)
	
	# Output results
	print(f"Mean: {mean}")
	print(f"Standard Deviation: {std_dev}")

# <<<<< END: codeunify/examples/example_files/module2/file1.py >>>>>

# >>>>> START: codeunify/examples/example_files/module2/file2.js <<<<<

	// This JavaScript script validates a user's input on a form before submission.
	
	function validateForm(form) {
	    let isValid = true;
	    if (form.name.value === "") {
	        alert("Name must be filled out");
	        isValid = false;
	    }
	    if (form.email.value === "") {
	        alert("Email must be filled out");
	        isValid = false;
	    }
	    return isValid;
	}
	
	// Example usage of validation function
	let form = {
	    name: { value: "" },
	    email: { value: "test@example.com" },
	};
	console.log(validateForm(form));  // Should return false due to empty name field

# <<<<< END: codeunify/examples/example_files/module2/file2.js >>>>>

# >>>>> START: codeunify/examples/example_files/module2/file3.java <<<<<

	// This Java program reads from and writes to a file.
	
	import java.io.*;
	
	public class FileReaderWriter {
	    public static void main(String[] args) {
	        String filePath = "output.txt";
	
	        // Writing to a file
	        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
	            writer.write("Hello, this is a file handling example in Java!");
	            writer.newLine();
	            writer.write("Writing multiple lines to the file.");
	        } catch (IOException e) {
	            System.out.println("An error occurred while writing to the file.");
	        }
	
	        // Reading from a file
	        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
	            String line;
	            while ((line = reader.readLine()) != null) {
	                System.out.println(line);
	            }
	        } catch (IOException e) {
	            System.out.println("An error occurred while reading the file.");
	        }
	    }
	}

# <<<<< END: codeunify/examples/example_files/module2/file3.java >>>>>

# >>>>> START: codeunify/tests/test_combine.py <<<<<

	import unittest
	import os
	from codeunify.core.combine import combine_files
	
	class TestCombineFiles(unittest.TestCase):
	
	    def setUp(self):
	        """Setup test files and directories."""
	        self.test_dir = "test_files"
	        self.output_file = "combined_output.txt"
	        
	        # Create a test directory and files
	        if not os.path.exists(self.test_dir):
	            os.makedirs(self.test_dir)
	        
	        # Files with different extensions
	        self.files = [
	            ("test1.py", "print('Hello from test1')"),
	            ("test2.js", "console.log('Hello from test2')"),
	            ("test3.java", "System.out.println('Hello from test3');"),
	            ("test4.txt", "Just a regular text file content."),
	            ("test5.c", "printf('Hello from C');")
	        ]
	        
	        # Create test files
	        for filename, content in self.files:
	            with open(os.path.join(self.test_dir, filename), "w") as f:
	                f.write(content)
	
	    def test_combine_files(self):
	        """Test combining files into one output."""
	        combine_files(self.test_dir, self.output_file)
	        
	        # Ensure output file is created
	        self.assertTrue(os.path.exists(self.output_file))
	        
	        # Read combined file content
	        with open(self.output_file, 'r') as f:
	            combined_content = f.read()
	
	        # Check if the comments are present in the combined content
	        for filename, _ in self.files:
	            self.assertIn(f"# Start of {filename}", combined_content)
	            self.assertIn(f"# End of {filename}", combined_content)
	
	            # Check if file content is present in the combined file
	            with open(os.path.join(self.test_dir, filename), 'r') as f:
	                file_content = f.read()
	                self.assertIn(file_content, combined_content)
	    
	    def test_combine_with_specified_file_types(self):
	        """Test combining files with specified file types."""
	        combine_files(self.test_dir, self.output_file, file_types=['.py', '.js'])
	        
	        # Ensure output file is created
	        self.assertTrue(os.path.exists(self.output_file))
	        
	        # Read combined file content
	        with open(self.output_file, 'r') as f:
	            combined_content = f.read()
	
	        # Check if the comments are present for specific file types
	        for filename, _ in self.files:
	            if filename.endswith('.py') or filename.endswith('.js'):
	                self.assertIn(f"# Start of {filename}", combined_content)
	                self.assertIn(f"# End of {filename}", combined_content)
	
	                # Check if file content is present in the combined file
	                with open(os.path.join(self.test_dir, filename), 'r') as f:
	                    file_content = f.read()
	                    self.assertIn(file_content, combined_content)
	            else:
	                # Ensure files that do not match the specified file types are not included
	                self.assertNotIn(f"# Start of {filename}", combined_content)
	                self.assertNotIn(f"# End of {filename}", combined_content)
	    
	    def tearDown(self):
	        """Clean up test files and output."""
	        for filename, _ in self.files:
	            os.remove(os.path.join(self.test_dir, filename))
	        os.rmdir(self.test_dir)
	        if os.path.exists(self.output_file):
	            os.remove(self.output_file)
	
	if __name__ == "__main__":
	    unittest.main()

# <<<<< END: codeunify/tests/test_combine.py >>>>>

# >>>>> START: codeunify/tests/__init__.py <<<<<



# <<<<< END: codeunify/tests/__init__.py >>>>>

