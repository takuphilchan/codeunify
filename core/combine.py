import os
import logging
import argparse
import mimetypes

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List of metadata directories to exclude
EXCLUDED_DIRS = {'.git', '__pycache__', '.idea', '.vscode'}

# Set of common programming/text file extensions to include, even if MIME detection fails
COMMON_TEXT_EXTENSIONS = {'.py', '.js', '.cpp', '.c', '.java', '.cu', '.h', '.hpp', '.cs', '.rb', '.php', '.go', '.rs', '.ts'}

# Comment formats based on file extension
COMMENT_STYLES = {
    "hash": {"ext": {'.py', '.sh', '.rb', '.pl'}, "start": "# >>>>> START: {filepath} <<<<<", "end": "# <<<<< END: {filepath} >>>>>"},
    "slash": {"ext": {'.js', '.ts', '.c', '.cpp', '.java', '.cs', '.go', '.cu'}, "start": "// >>>>> START: {filepath} <<<<<", "end": "// <<<<< END: {filepath} >>>>>"},
    "html": {"ext": {'.html', '.xml'}, "start": "<!-- >>>>> START: {filepath} <<<<< -->", "end": "<!-- <<<<< END: {filepath} >>>>> -->"},
    "dash": {"ext": {'.txt', '.md'}, "start": "----- START: {filepath} -----", "end": "----- END: {filepath} -----"},
}

def get_comment_format(file_path):
    """
    Determines the correct comment format based on the input file's extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    for style in COMMENT_STYLES.values():
        if ext in style["ext"]:
            return {"start": style["start"].format(filepath=file_path), "end": style["end"].format(filepath=file_path)}
    
    # Default fallback (hash-style comments)
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
    for root, _, files in os.walk(abs_input_dir):
        if any(excluded in root.split(os.sep) for excluded in EXCLUDED_DIRS):
            continue
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
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(description="Combine code files into a single output file, preserving folder structure.")
    parser.add_argument('input_dir', help="Directory containing the code files to combine")
    parser.add_argument('output_file', help="Path where the combined code should be saved")
    parser.add_argument('--file_types', nargs='*', default=[], help="List of file extensions to include (e.g., .py .txt). Default is to include all files.")
    parser.add_argument('--block_indent', type=str, default="\t", help="String to prepend to each line of file content (default is a tab).")
    return parser.parse_args()

def main():
    args = parse_args()
    
    try:
        combine_files(args.input_dir, args.output_file, args.file_types, args.block_indent)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
