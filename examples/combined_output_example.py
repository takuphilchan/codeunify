# Start of file1.py
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


# End of file1.py

# Start of file2.js
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


# End of file2.js

# Start of file3.java
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


# End of file3.java

