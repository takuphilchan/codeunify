import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def combine_files(input_dir, output_file, file_types=None, comment_format=None):
    """
    Combines all code files in the given directory and its subdirectories into a single file.
    Each section will be prefixed with a comment containing the original file's path, starting with the input folder name.
    
    Parameters:
    - input_dir (str): Directory containing the code files to combine.
    - output_file (str): Path where the combined code should be saved.
    - file_types (list): List of file extensions to include. Defaults to None (include all files).
    - comment_format (dict): Custom comment format. 
        Defaults to {"start": "# Start of {filepath}", "end": "# End of {filepath}"}.
    
    Raises:
    - FileNotFoundError: If the input directory is not found.
    - ValueError: If no valid code files are found.
    """
    if file_types is None:
        file_types = []  # Allow all file types by default
    if comment_format is None:
        comment_format = {"start": "# Start of {filepath}", "end": "# End of {filepath}"}
    
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
                with open(filepath, 'r', encoding='utf-8') as infile:
                    # Get the path relative to the input directory and prepend the input folder name
                    relative_path = os.path.relpath(filepath, abs_input_dir)
                    display_path = os.path.join(input_dir_name, relative_path)
                    
                    # Write a comment marking the start of the file content
                    start_comment = comment_format["start"].format(filepath=display_path)
                    outfile.write(f"{start_comment}\n")
                    
                    # Write the file's content
                    content = infile.read()
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
        combine_files(args.input_dir, args.output_file, args.file_types, comment_format)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
