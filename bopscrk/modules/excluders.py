#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - optimized transform functions module

from multiprocessing import Pool, cpu_count
from collections import OrderedDict
from typing import List, Iterable, Set

from . import Config


def compare(word_to_exclude, word_in_wordlist):
    if word_in_wordlist is not word_to_exclude:
        return word_in_wordlist


# OPTIMIZED: Remove word to exclude from final_wordlist
def multithread_exclude(word_to_exclude, wordlist):
    exclude_word = word_to_exclude.strip()
    if not exclude_word:
        return wordlist

    # For single exclusion, list comprehension is faster than multiprocessing
    return [word for word in wordlist if word != exclude_word]


# OPTIMIZED: Using dict.fromkeys() - faster than OrderedDict in Python 3.7+
def remove_duplicates(wordlist):
    return list(dict.fromkeys(wordlist))


# OPTIMIZED: Memory-efficient duplicate removal using set
def remove_duplicates_fast(wordlist: Iterable) -> List[str]:
    """Fast duplicate removal using set for O(1) lookups"""
    seen: Set[str] = set()
    result = []
    for item in wordlist:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# OPTIMIZED: Helper function for parallel processing (fixes pickle issue)
def _remove_duplicates_chunk(chunk: List[str]) -> List[str]:
    """Helper function to remove duplicates from a chunk - picklable"""
    return list(dict.fromkeys(chunk))


# OPTIMIZED: Get physical CPU cores
def get_physical_cores() -> int:
    """Get the number of physical CPU cores"""
    try:
        import os

        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        from multiprocessing import cpu_count

        return cpu_count()


# OPTIMIZED: Ultra-fast duplicate remover using parallel processing
def parallel_remove_duplicates(wordlist: List[str]) -> List[str]:
    """Parallel duplicate removal for massive wordlists"""
    if not wordlist:
        return []

    # For smaller lists, use single-threaded approach
    if len(wordlist) < 50000:
        return list(dict.fromkeys(wordlist))

    physical_cores = min(get_physical_cores(), 8)  # Limit to 8 cores to avoid overhead

    # Split into chunks for parallel processing
    chunk_size = max(1000, len(wordlist) // physical_cores)
    chunks = [wordlist[i : i + chunk_size] for i in range(0, len(wordlist), chunk_size)]

    # Process chunks in parallel
    try:
        with Pool(processes=physical_cores) as pool:
            unique_chunks = pool.map(_remove_duplicates_chunk, chunks)
    except Exception as e:
        # Fallback to single-threaded if multiprocessing fails
        print(
            f"  {color.ORANGE}[!]{color.END} Parallel processing failed, using single-threaded: {e}"
        )
        return list(dict.fromkeys(wordlist))

    # Merge and remove duplicates across chunks efficiently
    seen = set()
    final_results = []

    # Pre-allocate list size for better performance
    estimated_size = len(wordlist) // 2  # Rough estimate
    final_results = []

    for chunk in unique_chunks:
        for item in chunk:
            if item not in seen:
                seen.add(item)
                final_results.append(item)

    return final_results


# OPTIMIZED: Using list comprehension and avoiding unnecessary str() calls
def remove_by_lengths(wordlist, min_length, max_length):
    """expect a list, return a new list with the values between min and max length provided"""
    min_len, max_len = min_length, max_length
    # List comprehension is faster than explicit loops
    return [word for word in wordlist if min_len <= len(word) <= max_len]


# OPTIMIZED: Memory-efficient length filtering
def remove_by_lengths_fast(
    wordlist: Iterable, min_length: int, max_length: int
) -> List[str]:
    """Memory-efficient length filtering using generator"""
    min_len, max_len = min_length, max_length
    return [str(word) for word in wordlist if min_len <= len(str(word)) <= max_len]
