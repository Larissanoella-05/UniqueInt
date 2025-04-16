# DSA-HW01: UniqueInt

This projects provide a module `uniqueint.py` which will ask the user for a
specific input file. It will then read the unique integers on each line of the
file, then output them into a user-specified file.

## Features

- Reads the input file line-by-line
- Trims whitespace around each file
- Checks if each line of the file contains an integer (it may have an optional number sign prefix: -,+)
- Sorts the received integers
- Writes the output to a different file

## File structure

This program will read all `.txt` files from the `inputs` folder and write all
the output files in `outputs` folder.

## Usage

1. Place all  input files in the `inputs` folder
2. Run the script:

```sh
   python uniqueint.py
```
