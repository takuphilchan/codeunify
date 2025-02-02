import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def combine_files(input_dir, output_file, file_types=None, comment_format=None):
    """
    Combines all code files in the given directory into a single file.
    Each section will be prefixed with a comment containing the original file's name.

    Parameters:
    - input_dir (str): Directory containing the code files to combine.
    - output_file (str): Path where the combined code should be saved.
    - file_types (list): List of file extensions to include. Defaults to None (include all files).
    - comment_format (dict): Custom comment format. Defaults to {"start": "# Start of {filename}", "end": "# End of {filename}"}.

    Raises:
    - FileNotFoundError: If the input directory is not found.
    - ValueError: If no code files are found.
    """
    if file_types is None:
        file_types = []  # Allow all file types by default
    if comment_format is None:
        comment_format = {"start": "# Start of {filename}", "end": "# End of {filename}"}  # Default comment format
    
    # Check if directory exists
    if not os.path.exists(input_dir):
        logger.error(f"The directory '{input_dir}' does not exist.")
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")
    
    # Get the list of files to combine
    files_to_combine = []
    for filename in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, filename)):
            # If file_types is empty, include all files
            if not file_types or any(filename.endswith(ext) for ext in file_types):
                files_to_combine.append(filename)

    # Raise an error if no valid code files are found
    if not files_to_combine:
        logger.error(f"No valid code files found in the directory '{input_dir}'.")
        raise ValueError(f"No valid code files found in the directory '{input_dir}'.")
    
    logger.info(f"Found {len(files_to_combine)} files to combine: {', '.join(files_to_combine)}")
    
    # Combine the files
    with open(output_file, 'w') as outfile:
        for filename in files_to_combine:
            filepath = os.path.join(input_dir, filename)
            try:
                with open(filepath, 'r') as infile:
                    # Write start comment with the file name
                    start_comment = comment_format["start"].format(filename=filename)
                    outfile.write(f"{start_comment}\n")
                    
                    # Write the content of the file
                    outfile.write(infile.read())
                    outfile.write("\n\n")  # Add spacing between files
                    
                    # Write end comment with the file name
                    end_comment = comment_format["end"].format(filename=filename)
                    outfile.write(f"{end_comment}\n\n")
            
            except Exception as e:
                logger.error(f"Error reading file {filename}: {e}")
                continue  # Skip any problematic file

    logger.info(f"All files have been successfully combined into '{output_file}'")

def parse_args():
    parser = argparse.ArgumentParser(description="Combine code files into a single output file.")
    parser.add_argument('input_dir', help="Directory containing the code files to combine")
    parser.add_argument('output_file', help="Path where the combined code should be saved")
    parser.add_argument('--file_types', nargs='*', default=[], 
                        help="List of file extensions to include (default: include all files)")
    parser.add_argument('--comment_format', type=str, default=None,
                        help="Custom comment format (e.g., '{'start': '# Start of {filename}', 'end': '# End of {filename}'}')")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # If the comment format is provided, parse it as a dictionary
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
