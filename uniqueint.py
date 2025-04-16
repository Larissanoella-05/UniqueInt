#!/usr/bin/python3

import os
import time

class UniqueInt:
    @staticmethod
    def processFile(input_file_path, output_file_path):
        """
        Reads all unique integers from the specified file path and store
        the sorted result into the specified output file path
        """
        integers = UniqueInt.readUniqueIntegers(input_file_path)
        UniqueInt.sort(integers)

        with open(output_file_path, 'w') as file:
            for integer in integers:
                file.write(str(integer) + "\n")

    @staticmethod
    def readUniqueIntegers(file_path):
        """
        Reads all the unique integers from the specified file path
        """
        unique_integers = []
        with open(file_path, 'r') as file:
            for line in file:
                # Process the current line
                integer = UniqueInt.processLine(line)
                if integer is not None and not UniqueInt.contains(unique_integers, integer):
                    unique_integers.append(integer)
        return unique_integers

    @staticmethod
    def processLine(line):
        """
        Processes a line into an integer, by first removing all surrounding
        whitespace and returning an integer if the line contains a valid
        integer
        """
        stripped_line = UniqueInt.strip(line)

        # Skip empty lines
        if not stripped_line:
            return None

        # Try to convert the line to an integer
        if UniqueInt.is_integer(stripped_line):
            integer = int(stripped_line)
            # Check if the integer is within the acceptable range
            if integer >= -1023 and integer <= 1024:
                return integer

        return None

    @staticmethod
    def ask_user():
        """
        This function kicks of the program by asking the user for an input
        file's path, loading the unique integers, sort them and then store them
        in the specified output file path
        """
        input_file_path = input("Enter the input file path: ")

        output_file_path = input("Enter the output file path: ")

        UniqueInt.processFile(input_file_path, output_file_path)

    # Standard functions

    @staticmethod
    def is_integer(s):
        """
        This function checks whether a string (which may contain a number sign
        as prefix) is a valid integer
        """
        # may contain a number sign as prefix
        if s[0] in ('-', '+'):
            return s[1:].isdigit()

        return s.isdigit()

    @staticmethod
    def strip(s):
        """
        Remove all leading and trailing whitespace from a string
        """
        result = ""
        i = 0
        space_characters = (' ', '\t', '\n')
        # remove all leading whitespace characters
        while i < len(s) and (s[i] in space_characters):
            i += 1
        j = len(s) - 1
        # remove all trailing whitespace characterss
        while j >= 0 and (s[j] in space_characters):
            j -= 1
        for k in range(i, j + 1):
            result += s[k]
        return result

    @staticmethod
    def split(s):
        """
        Strip a string into multiple parts separated by a space or tab
        character
        """
        parts = []
        part = ""
        for char in s:
            if char == ' ' or char == '\t':
                if part:
                    parts.append(part)
                    part = ""
            else:
                part += char
        if part:
            parts.append(part)
        return parts

    @staticmethod
    def contains(arr, value):
        """
        Checks whether a given item is included in the array
        """
        for item in arr:
            if item == value:
                return True
        return False

    @staticmethod
    def sort(arr):
        """
        Sort an array using a simple bubble sort algorithm
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

if __name__ == "__main__":
    input_folder = "inputs"
    output_folder = "outputs"
    
    overall_start_time = time.time()

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            # Remove the .txt extension
            basename = filename[:-4]

            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{basename}.txt_results.txt")

            # Measure performance for each file for each file
            start_time = time.time()
            UniqueInt.processFile(input_path, output_path)
            end_time = time.time()

            print(f"Processed {filename} in {end_time - start_time:.4f} seconds")

    overall_end_time = time.time()
    print(f"Processed all files in {overall_end_time - overall_start_time:.4f} seconds")
