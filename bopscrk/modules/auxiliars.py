#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - optimized auxiliar functions module

import os
import datetime
from typing import List, Iterable, Set


def clear():
    """Clear the screen. Works on Windows and Linux."""
    os.system(["clear", "cls"][os.name == "nt"])


# OPTIMIZED: Simplified empty check
def is_empty(variable) -> bool:
    """Check if a variable is empty. Returns True or False"""
    return len(str(variable)) == 0


def is_valid_date(date_str: str) -> bool:
    """Check if a string corresponds to a valid date."""
    try:
        datetime.datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# OPTIMIZED: Buffered file writing for better performance
def append_wordlist_to_file(filepath: str, wordlist: List[str]) -> bool:
    """
    Optimized wordlist append with buffered I/O.
    :param filepath: path to file
    :param wordlist: list of words to save
    :return: True or False
    """
    if not wordlist:
        return True

    try:
        # Use buffered writing for better performance
        with open(filepath, "a", encoding="utf-8", buffering=8192) as f:
            # Join all words with newlines for faster writing
            f.write("\n".join(wordlist) + "\n")
        return True
    except (IOError, OSError):
        return False


# OPTIMIZED: Memory-efficient duplicate removal from file
def remove_duplicates_from_file(
    infile_path: str, outfile_path: str = "temp.000000000.bopscrk"
) -> bool:
    """
    Optimized duplicate removal from file using set for O(1) lookups.
    :param infile_path: input file path
    :param outfile_path: temporary output file path
    :return: True if successful, False otherwise
    """
    try:
        lines_seen: Set[str] = set()

        # Use buffered I/O for better performance
        with (
            open(infile_path, "r", encoding="utf-8", buffering=8192) as infile,
            open(outfile_path, "w", encoding="utf-8", buffering=8192) as outfile,
        ):
            # Process line by line to manage memory
            for line in infile:
                line = line.strip()
                if line and line not in lines_seen:
                    lines_seen.add(line)
                    outfile.write(line + "\n")

        # Atomic file replacement
        os.remove(infile_path)
        os.rename(outfile_path, infile_path)
        return True

    except (IOError, OSError):
        # Clean up temp file if it exists
        if os.path.exists(outfile_path):
            try:
                os.remove(outfile_path)
            except OSError:
                pass
        return False


# OPTIMIZED: Batch file writer for large wordlists
def write_wordlist_batch(
    filepath: str, wordlist: List[str], batch_size: int = 10000
) -> bool:
    """
    Write large wordlists in batches to manage memory.
    :param filepath: path to file
    :param wordlist: list of words to save
    :param batch_size: number of words to write at once
    :return: True if successful, False otherwise
    """
    if not wordlist:
        return True

    try:
        with open(filepath, "w", encoding="utf-8", buffering=8192) as f:
            for i in range(0, len(wordlist), batch_size):
                batch = wordlist[i : i + batch_size]
                f.write("\n".join(batch) + "\n")
        return True
    except (IOError, OSError):
        return False


# OPTIMIZED: Memory-efficient file reader
def read_wordlist_file(filepath: str, chunk_size: int = 10000) -> Iterable[str]:
    """
    Read wordlist file in chunks to manage memory.
    :param filepath: path to file
    :param chunk_size: number of lines to read at once
    :return: generator yielding words
    """
    try:
        with open(filepath, "r", encoding="utf-8", buffering=8192) as f:
            chunk = []
            for line in f:
                word = line.strip()
                if word:
                    chunk.append(word)
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []
            if chunk:
                yield chunk
    except (IOError, OSError):
        return


# OPTIMIZED: Safe file operations with error handling
def safe_file_operation(operation_func, *args, **kwargs):
    """
    Wrapper for safe file operations with error handling.
    :param operation_func: function to execute
    :param args: positional arguments
    :param kwargs: keyword arguments
    :return: result of operation or None if failed
    """
    try:
        return operation_func(*args, **kwargs)
    except (IOError, OSError) as e:
        print(f"File operation error: {e}")
        return None

