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
