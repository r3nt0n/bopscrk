#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - optimized transform functions module

import itertools
from multiprocessing import cpu_count, Pool
from alive_progress import alive_bar
from typing import List, Dict, Iterable
import sys

from . import Config
from .excluders import remove_duplicates_fast
from .auxiliars import append_wordlist_to_file

# OPTIMIZED: Pre-compute vowel set for faster lookup
VOWELS = frozenset("aeiou")


# EXTENSIVE: generates all case transforms possibilities (optimized)
def case_transforms_extensive(word: str) -> List[str]:
    """Optimized extensive case transforms using list comprehension"""
    word_lower = word.lower()
    # Pre-compute upper/lower pairs for better performance
    char_pairs = list(zip(word_lower.upper(), word_lower))
    return ["".join(combo) for combo in itertools.product(*char_pairs)]


# OPTIMIZED: BASIC case transforms with better string operations
def case_transforms_basic(word: str) -> List[str]:
    """Optimized basic case transforms"""
    word_lower = word.lower()
    word_upper = word_lower.upper()
    results = [word_lower, word_upper]

    # Pre-allocate set for O(1) duplicate checking
    seen = set(results)

    # Single character uppercase transforms
    for i, char in enumerate(word_lower):
        new_word = word_lower[:i] + char.upper() + word_lower[i + 1 :]
        if new_word not in seen:
            seen.add(new_word)
            results.append(new_word)

    # Even positions uppercase
    even_chars = [
        char.upper() if i % 2 == 0 else char for i, char in enumerate(word_lower)
    ]
    new_word = "".join(even_chars)
    if new_word not in seen:
        seen.add(new_word)
        results.append(new_word)

    # Odd positions uppercase
    odd_chars = [
        char.upper() if i % 2 != 0 else char for i, char in enumerate(word_lower)
    ]
    new_word = "".join(odd_chars)
    if new_word not in seen:
        seen.add(new_word)
        results.append(new_word)

    # Consonants uppercase (optimized with set lookup)
    consonant_chars = [
        char.upper() if char.lower() not in VOWELS else char for char in word_lower
    ]
    new_word = "".join(consonant_chars)
    if new_word not in seen:
        seen.add(new_word)
        results.append(new_word)

    # Vowels uppercase (optimized with set lookup)
    vowel_chars = [
        char.upper() if char.lower() in VOWELS else char for char in word_lower
    ]
    new_word = "".join(vowel_chars)
    if new_word not in seen:
        seen.add(new_word)
        results.append(new_word)

    return results


def case_transforms(word: str) -> List[str]:
    """Optimized case transforms dispatcher"""
    if Config.EXTENSIVE_CASE:
        return case_transforms_extensive(word)
    return case_transforms_basic(word)


# OPTIMIZED: Leet transforms with better data structures
def leet_transforms(word: str) -> List[str]:
    """Optimized leet transforms using dict lookup"""
    # Pre-build leet mapping dictionary for O(1) lookup
    leet_map = {}
    for mapping in Config.LEET_CHARSET:
        if ":" in mapping:
            original, leet = mapping.split(":", 1)
            if original and leet:
                leet_map[original.lower()] = leet

    new_words = []
    word_lower = word.lower()

    # Generate all possible single-character leet transforms
    for i, char in enumerate(word_lower):
        if char in leet_map:
            for leet_char in leet_map[char].split(","):
                new_word = word[:i] + leet_char + word[i + 1 :]
                if new_word not in new_words:
                    new_words.append(new_word)

    # Handle recursive leet if enabled
    if Config.RECURSIVE_LEET and new_words:
        original_size = len(new_words)
        for new_word in new_words[
            :
        ]:  # Use slice to avoid modification during iteration
            recursive_transforms = leet_transforms(new_word)
            for transform in recursive_transforms:
                if transform not in new_words:
                    new_words.append(transform)
            if len(new_words) == original_size:
                break

    return remove_duplicates_fast(new_words)


# OPTIMIZED: Take initials using list comprehension
def take_initials(word: str) -> str:
    """Optimized initials extraction"""
    return "".join([part[0] for part in word.split(" ") if part])


# OPTIMIZED: Artist space transforms with better string operations
def artist_space_transforms(word: str) -> List[str]:
    """Optimized artist space transforms"""
    if " " not in word:
        return []

    results = []

    # Split by word if enabled
    if Config.ARTIST_SPLIT_BY_WORD:
        results.extend(word.split(" "))

    # Remove spaces
    no_spaces = word.replace(" ", "")
    if no_spaces not in results:
        results.append(no_spaces)

    # Replace with charset
    if Config.ARTIST_SPACE_REPLACEMENT and Config.SPACE_REPLACEMENT_CHARSET:
        for char in Config.SPACE_REPLACEMENT_CHARSET:
            replaced = word.replace(" ", char)
            if replaced not in results:
                results.append(replaced)

    return results


# OPTIMIZED: Lyric space transforms
def lyric_space_transforms(word: str) -> List[str]:
    """Optimized lyric space transforms"""
    if " " not in word:
        return []

    results = []

    # Split by word if enabled
    if Config.LYRIC_SPLIT_BY_WORD:
        results.extend(word.split(" "))

    # Remove spaces
    no_spaces = word.replace(" ", "")
    if no_spaces not in results:
        results.append(no_spaces)

    # Replace with charset
    if Config.LYRIC_SPACE_REPLACEMENT and Config.SPACE_REPLACEMENT_CHARSET:
        for char in Config.SPACE_REPLACEMENT_CHARSET:
            replaced = word.replace(" ", char)
            if replaced not in results:
                results.append(replaced)

    return results


# OPTIMIZED: Get physical CPU cores for better performance
def get_physical_cores() -> int:
    """Get the number of physical CPU cores"""
    try:
        import os

        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return cpu_count()


# OPTIMIZED: Parallel batch processor for massive wordlists
def parallel_batch_processor(
    transform_type, wordlist: List[str], batch_size: int = 50000
) -> List[str]:
    """Process massive wordlists in parallel batches to utilize all CPU cores"""
    if not wordlist:
        return []

    physical_cores = get_physical_cores()
    results = []

    # Process in parallel batches
    with Pool(processes=physical_cores) as pool:
        # Split wordlist into batches
        batches = [
            wordlist[i : i + batch_size] for i in range(0, len(wordlist), batch_size)
        ]

        # Process batches in parallel
        with alive_bar(
            total=len(batches),
            bar="smooth",
            spinner="dots",
            title=f"Batch processing on {physical_cores} cores",
            receipt=False,
        ) as progress:
            for i, batch in enumerate(batches):
                batch_results = pool.map(transform_type, batch)
                for sublist in batch_results:
                    results.extend(sublist)
                progress()

    return results


# OPTIMIZED: Enhanced multiprocessing with full CPU utilization
def multiprocess_transforms_optimized(transform_type, wordlist: List[str]) -> List[str]:
    """Ultra-optimized multiprocessing with full CPU utilization and intelligent load balancing"""
    if not wordlist:
        return []

    # If small list, don't bother with multiprocessing overhead
    if len(wordlist) < 100:
        return [item for word in wordlist for item in transform_type(word)]

    # Get actual CPU count
    physical_cores = get_physical_cores()

    # Dynamic chunking based on workload size and CPU count
    total_words = len(wordlist)
    optimal_chunk_size = max(10, min(1000, total_words // (physical_cores * 2)))

    results = []

    # Use process pool with optimized settings
    with Pool(processes=physical_cores) as pool:
        try:
            # Process with progress tracking
            with alive_bar(
                total=total_words,
                bar="smooth",
                spinner="dots",
                title=f"Processing on {physical_cores} cores",
                receipt=False,
            ) as progress:
                # Process in chunks with better load balancing
                wordlists = pool.map(
                    transform_type, wordlist, chunksize=optimal_chunk_size
                )

                # Efficiently flatten results
                for sublist in wordlists:
                    if sublist:
                        results.extend(sublist)
                    progress()

        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            raise
        except Exception as e:
            pool.terminate()
            pool.join()
            raise e

    return results


# OPTIMIZED: Enhanced multiprocessing with better chunking
def multiprocess_transforms(transform_type, wordlist: List[str]) -> List[str]:
    """Enhanced multiprocessing with automatic CPU utilization"""
    return multiprocess_transforms_optimized(transform_type, wordlist)


# OPTIMIZED: Batch processing for cached wordlist
def transform_cached_wordlist_and_save(transform_type, filepath: str):
    """Optimized cached wordlist processing with better I/O"""
    CHUNK_SIZE = 8000
    last_position = 0

    while True:
        cached_wordlist = []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                f.seek(last_position)

                # Read in chunks for better performance
                for _ in range(CHUNK_SIZE):
                    line = f.readline()
                    if not line:
                        break
                    word = line.strip()
                    if word and word not in cached_wordlist:
                        cached_wordlist.append(word)

                last_position = f.tell()

                if not cached_wordlist:
                    break

                # Process and save in batch
                new_wordlist = multiprocess_transforms(transform_type, cached_wordlist)
                append_wordlist_to_file(filepath, new_wordlist)

        except (IOError, OSError) as e:
            print(f"Error processing file: {e}")
            break
