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
