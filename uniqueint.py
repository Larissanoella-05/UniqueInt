#!/usr/bin/python3

import os
import time
import psutil  # For memory tracking
import sys

class UniqueInt:
    @staticmethod
    def processFile(input_file_path, output_file_path):
        """
        Reads all unique integers from the specified file path and stores
        the sorted result into the specified output file path.
        Returns tuple of (execution_time, memory_used)
        """
        start_time = time.time()
        start_memory = UniqueInt.get_memory_usage()
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                print(f"Error creating directory {output_dir}: {e}")
                return (0, 0)
        
        try:
            integers = UniqueInt.readUniqueIntegers(input_file_path)
            
            if integers is None:  # Error occurred during reading
                return (0, 0)
                
            UniqueInt.quicksort(integers, 0, len(integers) - 1)
            
            try:
                with open(output_file_path, 'w') as file:
                    for integer in integers:
                        file.write(str(integer) + "\n")
            except IOError as e:
                print(f"Error writing to output file {output_file_path}: {e}")
                return (0, 0)
                
        except Exception as e:
            print(f"Unexpected error processing file: {e}")
            return (0, 0)
            
        end_time = time.time()
        end_memory = UniqueInt.get_memory_usage()
        
        return (end_time - start_time, end_memory - start_memory)

    @staticmethod
    def readUniqueIntegers(file_path):
        """
        Reads all the unique integers from the specified file path
        Uses a hash-like structure for faster uniqueness checking
        """
        unique_dict = {}  # Using a dictionary for O(1) lookup time
        
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Process the current line
                    integer = UniqueInt.processLine(line)
                    if integer is not None:
                        unique_dict[integer] = True
                        
            # Convert dictionary keys back to list
            return list(unique_dict.keys())
            
        except IOError as e:
            print(f"Error reading input file {file_path}: {e}")
            return None
            
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
        This function kicks off the program by asking the user for an input
        file's path, loading the unique integers, sort them and then store them
        in the specified output file path
        """
        input_file_path = input("Enter the input file path: ")
        if not os.path.exists(input_file_path):
            print(f"Error: Input file '{input_file_path}' does not exist.")
            return

        output_file_path = input("Enter the output file path: ")

        time_taken, memory_used = UniqueInt.processFile(input_file_path, output_file_path)
        print(f"Processing completed in {time_taken:.4f} seconds")
        print(f"Memory used: {memory_used:.2f} bytes")

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
    def partition(arr, low, high):
        """
        Helper function for quicksort algorithm
        Takes last element as pivot and places it at its correct position
        Places all smaller elements to left and all greater elements to right
        """
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    @staticmethod
    def quicksort(arr, low, high):
        """
        Implementation of quicksort algorithm for better performance
        than the original bubble sort (O(n log n) vs O(n²))
        """
        if low < high:
            # Find the partition index
            pi = UniqueInt.partition(arr, low, high)
            
            # Sort elements before and after partition
            UniqueInt.quicksort(arr, low, pi - 1)
            UniqueInt.quicksort(arr, pi + 1, high)
            
        return arr

    @staticmethod
    def get_memory_usage():
        """
        Returns the current memory usage in bytes
        """
        process = psutil.Process(os.getpid())
        return process.memory_info().rss  # in bytes

if __name__ == "__main__":
    input_folder = "inputs"
    output_folder = "outputs"
    
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)
        
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except OSError as e:
            print(f"Error creating output directory '{output_folder}': {e}")
            sys.exit(1)
    
    overall_start_time = time.time()
    overall_start_memory = UniqueInt.get_memory_usage()
    
    total_files_processed = 0
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            # Remove the .txt extension
            basename = filename[:-4]

            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{basename}.txt_results.txt")

            # Measure performance for each file
            start_time = time.time()
            start_memory = UniqueInt.get_memory_usage()
            
            time_taken, _ = UniqueInt.processFile(input_path, output_path)
            
            end_time = time.time()
            end_memory = UniqueInt.get_memory_usage()
            
            memory_used = end_memory - start_memory
            
            print(f"Processed {filename}:")
            print(f"  Time: {end_time - start_time:.4f} seconds")
            print(f"  Memory: {memory_used} bytes")
            
            total_files_processed += 1

    overall_end_time = time.time()
    overall_end_memory = UniqueInt.get_memory_usage()
    
    print(f"\nProcessed {total_files_processed} files in {overall_end_time - overall_start_time:.4f} seconds")
    print(f"Total memory used: {overall_end_memory - overall_start_memory} bytes")