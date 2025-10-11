#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - optimized combinators functions module

import itertools
from typing import List, Set, Generator
from alive_progress import alive_bar

from . import Config
from .excluders import remove_duplicates_fast


# OPTIMIZED: Add common separators with better data structures
def add_common_separators(wordlist: List[str]) -> List[str]:
    """Optimized separator combinations using set for O(1) lookups"""
    if not wordlist or not Config.SEPARATORS_CHARSET:
        return []

    results = []
    seen = set()

    # Pre-generate all separator variations
    separator_prefixes = []
    separator_suffixes = []

    for word in wordlist:
        for separator in Config.SEPARATORS_CHARSET:
            # Prefix and suffix variations
            prefix = separator + word
            suffix = word + separator

            if prefix not in seen:
                seen.add(prefix)
                separator_prefixes.append(prefix)
            if suffix not in seen:
                seen.add(suffix)
                separator_suffixes.append(suffix)

    results.extend(separator_prefixes)
    results.extend(separator_suffixes)

    # Combine with original words
    base_with_seps = separator_prefixes + separator_suffixes

    with alive_bar(
        total=len(wordlist),
        bar="bubbles",
        unknown="bubbles",
        spinner="bubbles",
        receipt=False,
    ) as progressbar:
        for word in wordlist:
            for sep_word in base_with_seps:
                if word not in sep_word:  # Avoid redundant combinations
                    combo1 = sep_word + word
                    combo2 = word + sep_word

                    if combo1 not in seen:
                        seen.add(combo1)
                        results.append(combo1)
                    if combo2 not in seen:
                        seen.add(combo2)
                        results.append(combo2)
            progressbar()

    return list(seen)  # Convert set back to list


# OPTIMIZED: Fixed combinator generator
def combinator_generator(wordlist: List[str], nWords: int, batch_size: int = 1000):
    """Generate combinations in batches to manage memory - FIXED VERSION"""
    if nWords <= 1 or not wordlist:
        return

    # Remove duplicates and use index permutations to avoid self-combinations
    from collections import OrderedDict

    unique_wordlist = list(OrderedDict.fromkeys(wordlist))
    indices = list(range(len(unique_wordlist)))

    batch = []
    # Use permutations of indices to avoid self-combinations
    for combo in itertools.permutations(indices, nWords):
        batch.append("".join(unique_wordlist[i] for i in combo))
        if len(batch) >= batch_size:
            yield batch
            batch = []

    if batch:
        yield batch


# OPTIMIZED: Fixed combinator - exact original behavior
def combinator(wordlist: List[str], nWords: int) -> List[str]:
    """Exact original combinator behavior - excludes self-combinations"""
    if nWords <= 1 or not wordlist:
        return wordlist[:]

    # Remove duplicates first to match original behavior
    from collections import OrderedDict

    unique_wordlist = list(OrderedDict.fromkeys(wordlist))
    indices = list(range(len(unique_wordlist)))

    new_wordlist = unique_wordlist[:]
    wlist_combined = itertools.permutations(indices, nWords)
    wlist_combined = [
        "".join(unique_wordlist[i] for i in combo) for combo in wlist_combined
    ]

    # Use the original logic exactly
    with alive_bar(
        total=len(wlist_combined),
        bar="bubbles",
        unknown="bubbles",
        spinner="bubbles",
        receipt=False,
    ) as progressbar:
        for combination in wlist_combined:
            word = "".join(combination)
            if word not in new_wordlist:
                new_wordlist.append(word)
            progressbar()

    # Original duplicate removal
    return list(OrderedDict.fromkeys(new_wordlist))


# OPTIMIZED: Simple batch combinator for cleanup
def combinator_batch(wordlist: List[str], nWords: int, batch_size: int = 1000):
    """Simple batch combinator for cleanup"""
    if nWords <= 1 or not wordlist:
        return

    seen = set(wordlist)
    batch = []

    for combination in itertools.permutations(wordlist, nWords):
        word = "".join(combination)
        if word not in seen:
            seen.add(word)
            batch.append(word)

        if len(batch) >= batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

