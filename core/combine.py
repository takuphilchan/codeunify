import os
import logging
import argparse
import mimetypes

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# List of metadata directories to exclude
EXCLUDED_DIRS = {
    '.git', '.svn', '.hg', '.bzr', '__pycache__', '.mypy_cache', '.pytest_cache', '.tox', '.venv', 'env', 'venv',  
    '.idea', '.vscode', '.vs', '.classpath', '.project', '.settings', 'node_modules', 'bower_components',  
    '.gradle', '.mvn', 'target', 'out', 'bin', 'target', 'build', 'cmake-build-debug', 'cmake-build-release',  
    'pkg', '.docker', '.circleci', '.github', '.gitlab', 'dist', 'output', 'logs', 'cache', '__MACOSX'
}

# Set of common programming/text file extensions to include
COMMON_TEXT_EXTENSIONS = {
    '.py', '.js', '.ts', '.c', '.cpp', '.h', '.hpp', '.java', '.cs', '.go', '.rs', '.rb', '.php', '.lua', '.m', '.swift', 
    '.kt', '.dart', '.r', '.pl', '.sh', '.ps1', '.bat', '.ex', '.exs', '.clj', '.cljs', '.erl', '.hrl', '.ml', '.mli', 
    '.fs', '.fsi', '.fsx', '.fsscript', '.v', '.vh', '.sv', '.svi', '.sc', '.scala', '.groovy', '.jl', '.adb', '.ads', 
    '.html', '.xml', '.ui', '.xsl', '.xsd', '.css', '.qss','.scss', '.sass', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.csv', 
    '.sql', '.db', '.dbt', '.makefile', '.mk', '.gradle', '.dockerfile', '.bash', '.zsh', '.fish', '.ksh', '.vhd', '.vhdl', 
    '.sdc', '.ipynb', '.mat', '.m', '.nb', '.wl', '.cmake', '.ninja', '.build', '.bazel', '.bzl', '.buck', '.ebuild', 
    '.lisp', '.cl', '.el', '.scm', '.rkt', '.tsx', '.jsx', '.astro', '.svelte'
}

# Comment formats based on file extension
COMMENT_STYLES = {
    "hash": {"ext": {'.py', '.sh', '.rb', '.pl', '.r', '.ps1', '.bash', '.zsh', '.ksh', '.fish'},
              "start": "# >>>>> START: {filepath} <<<<<", "end": "# <<<<< END: {filepath} >>>>>"},
    "slash": {"ext": {'.js', '.ts', '.c', '.cpp', '.java', '.cs', '.go', '.cu', '.rs', '.swift', '.kt', '.dart', '.scala'},
               "start": "// >>>>> START: {filepath} <<<<<", "end": "// <<<<< END: {filepath} >>>>>"},
    "css": {"ext": {'.css','.qss','.scss', '.sass'},
             "start": "/* >>>>> START: {filepath} <<<<< */", "end": "/* <<<<< END: {filepath} >>>>> */"},
    "html": {"ext": {'.html', '.xml', '.ui', '.xsl', '.xsd', '.jsx', '.tsx'},
              "start": "<!-- >>>>> START: {filepath} <<<<< -->", "end": "<!-- <<<<< END: {filepath} >>>>> -->"},
    "dash": {"ext": {'.txt', '.md', '.rst'},
              "start": "----- START: {filepath} -----", "end": "----- END: {filepath} -----"},
    "semicolon": {"ext": {'.lisp', '.clj', '.cljs', '.scm', '.rkt'},
                   "start": ";; >>>>> START: {filepath} <<<<<", "end": ";; <<<<< END: {filepath} >>>>>"},
    "percent": {"ext": {'.tex', '.sty', '.cls'},
                 "start": "% >>>>> START: {filepath} <<<<<", "end": "% <<<<< END: {filepath} >>>>>"},
    "sql": {"ext": {'.sql'},
             "start": "-- >>>>> START: {filepath} <<<<<", "end": "-- <<<<< END: {filepath} >>>>>"},
    "verilog": {"ext": {'.v', '.vh', '.sv', '.svi', '.vhd', '.vhdl'},
                 "start": "-- >>>>> START: {filepath} <<<<<", "end": "-- <<<<< END: {filepath} >>>>>"},
}

def get_comment_format(file_path):
    """
    Determines the correct comment format based on the input file's extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    for style in COMMENT_STYLES.values():
        if ext in style["ext"]:
            return {"start": style["start"].format(filepath=file_path), "end": style["end"].format(filepath=file_path)}
    
    return {"start": "# >>>>> START: {filepath} <<<<<".format(filepath=file_path), "end": "# <<<<< END: {filepath} >>>>>".format(filepath=file_path)}

def combine_files(input_dir, output_file, file_types=None, block_indent="\t"):
    """
    Combines all code files in the given directory and its subdirectories into a single file.
    Each section will be prefixed with a comment containing the original file's path.
    File content is indented for clarity.
    """
    if file_types is None:
        file_types = []  # Allow all file types by default
    
    if not os.path.exists(input_dir):
        logger.error(f"The directory '{input_dir}' does not exist.")
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")

    abs_input_dir = os.path.abspath(input_dir)
    input_dir_name = os.path.basename(abs_input_dir)
    
    files_to_combine = []
    for root, dirs, files in os.walk(abs_input_dir):
        # Exclude directories listed in EXCLUDED_DIRS
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for filename in files:
            if not file_types or any(filename.endswith(ext) for ext in file_types):
                files_to_combine.append(os.path.join(root, filename))
    
    if not files_to_combine:
        logger.error(f"No valid code files found in the directory '{input_dir}'.")
        raise ValueError(f"No valid code files found in the directory '{input_dir}'.")
    
    logger.info(f"Found {len(files_to_combine)} files to combine.")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filepath in files_to_combine:
            try:
                ext = os.path.splitext(filepath)[1].lower()
                mime_type, _ = mimetypes.guess_type(filepath)
                if (mime_type is None or not mime_type.startswith("text")) and ext not in COMMON_TEXT_EXTENSIONS:
                    logger.warning(f"Skipping non-text (binary) file: {filepath}")
                    continue

                comment_format = get_comment_format(filepath)
                relative_path = os.path.relpath(filepath, abs_input_dir)
                display_path = os.path.join(input_dir_name, relative_path)

                start_comment = comment_format["start"].replace("{filepath}", display_path)
                end_comment = comment_format["end"].replace("{filepath}", display_path)

                outfile.write(f"{start_comment}\n\n")
                
                with open(filepath, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    content = "\n".join(block_indent + line if line.strip() else line for line in content.splitlines())
                    outfile.write(content)
                    outfile.write("\n\n")

                outfile.write(f"{end_comment}\n\n")
            except Exception as e:
                logger.error(f"Error reading file {filepath}: {e}")
                continue

    logger.info(f"All files have been successfully combined into '{output_file}'.")

def parse_args():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="Combine code files into a single output file.")
    parser.add_argument("input_dir", help="Directory containing the code files to combine")
    parser.add_argument("output_file", help="Path to save the combined file")
    parser.add_argument("--file_types", nargs="*", default=[], help="List of file extensions to include")
    parser.add_argument("--block_indent", type=str, default="\t", help="Indentation string (default: tab)")
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        combine_files(args.input_dir, args.output_file, args.file_types, args.block_indent)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
