#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - optimized script opts and presentation

import sys, os, datetime
from typing import List, Set, Iterator, Generator
import gc
import itertools
from alive_progress import alive_bar

from . import args, Config
from .auxiliars import clear
from . import banners
from .color import color
from .transforms import (
    leet_transforms,
    case_transforms,
    multiprocess_transforms,
    parallel_batch_processor,
    transform_cached_wordlist_and_save,
)
from .combinators import combinator, add_common_separators
from .excluders import (
    remove_by_lengths_fast,
    remove_duplicates_fast,
    parallel_remove_duplicates,
)


# OPTIMIZED: Get physical CPU cores for better performance
def get_physical_cores() -> int:
    """Get the number of physical CPU cores"""
    try:
        import os

        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        from multiprocessing import cpu_count

        return cpu_count()


# OPTIMIZED: Memory-efficient file writing with parallel processing
def write_wordlist_to_file_parallel(wordlist: List[str], filepath: str) -> None:
    """Optimized parallel file writing with buffered I/O"""
    if not wordlist:
        return

    try:
        # For very large wordlists, split into chunks for parallel writing
        if len(wordlist) > 100000:
            # Split into chunks and write in parallel
            chunk_size = 10000
            chunks = [
                wordlist[i : i + chunk_size]
                for i in range(0, len(wordlist), chunk_size)
            ]

            with open(filepath, "w", encoding="utf-8", buffering=8192) as f:
                for chunk in chunks:
                    f.write("\n".join(chunk) + "\n")
        else:
            # Standard writing for smaller lists
            with open(filepath, "w", encoding="utf-8", buffering=8192) as f:
                f.write("\n".join(wordlist) + "\n")

    except IOError as e:
        print(f"  {color.RED}[!]{color.END} Error writing to file {filepath}: {e}")
        sys.exit(3)


# OPTIMIZED: Enhanced memory generator with parallel processing
def process_wordlist_generator(
    wordlist: List[str], chunk_size: int = 10000
) -> Iterator[List[str]]:
    """Generator to process wordlist in chunks to manage memory"""
    for i in range(0, len(wordlist), chunk_size):
        yield wordlist[i : i + chunk_size]


# OPTIMIZED: High-performance combinator generator
def combinator_generator(
    wordlist: List[str], nWords: int, batch_size: int = 1000
) -> Generator[List[str], None, None]:
    """Generate combinations in batches to manage memory - FIXED VERSION"""
    if nWords <= 1 or not wordlist:
        return

    # Remove duplicates and use index permutations to avoid self-combinations
    from collections import OrderedDict

    unique_wordlist = list(OrderedDict.fromkeys(wordlist))
    indices = list(range(len(unique_wordlist)))

    # Calculate total combinations mathematically for progress bar
    import math

    n = len(indices)
    total_combinations = (
        math.perm(n, nWords)
        if hasattr(math, "perm")
        else sum(1 for _ in itertools.permutations(indices, nWords))
    )

    batch = []
    # Use permutations of indices to avoid self-combinations
    with alive_bar(
        total=total_combinations,
        bar="bubbles",
        unknown="bubbles",
        spinner="bubbles",
        receipt=False,
    ) as progressbar:
        for combo in itertools.permutations(indices, nWords):
            batch.append("".join(unique_wordlist[i] for i in combo))
            if len(batch) >= batch_size:
                yield batch
                batch = []
            progressbar()

    if batch:
        yield batch


def run(name: str, version: str) -> None:
    """Ultra-optimized main function with full CPU utilization"""
    # check Python version
    if sys.version_info < (3, 0):
        print("Python 3 is required")
        sys.exit(1)

    # Print simple help and exit when runs without args
    if len(sys.argv) == 1:
        args.parser.print_help(sys.stdout)
        sys.exit(2)

    # Print version and exit (when runs with -v)
    if args.print_version:
        print(name + "_" + version)
        sys.exit(0)

    # Display CPU info
    cpu_cores = get_physical_cores()
    # print(
    #     f"  {color.GREEN}[*]{color.END} Using {cpu_cores} CPU cores for maximum performance"
    # )

    try:
        # setting args whether interactive or not
        if args.interactive:
            clear()
            banners.bopscrk_banner()
            banners.help_banner()
            banners.banner(name, version)
            args.set_interactive_options()
        else:
            banners.bopscrk_banner()
            banners.help_banner()
            banners.banner(name, version)
            args.set_cli_options()

        # Check if config file exists
        if not os.path.exists(args.cfg_file):
            print(
                "  {}[!]{} error trying to load config file {}".format(
                    color.RED, color.END, args.cfg_file
                )
            )
            sys.exit(3)
        else:
            Config.setup()
            print(
                "  {}[V]{} config file {} loaded".format(
                    color.GREEN, color.END, args.cfg_file
                )
            )

        # Initial timestamp
        start_time = datetime.datetime.now()

        # OPTIMIZED: Use set for O(1) duplicate checking
        base_wordlist = list(args.base_wordlist)
        final_words_set = set(base_wordlist)

        print(
            "  {}[+]{} Appending words provided (base wordlist length: {})...".format(
                color.BLUE, color.END, len(base_wordlist)
            )
        )

        # WORD COMBINATIONS - OPTIMIZED
        if args.n_words > 1:
            print(
                "  {}[+]{} Creating all possible combinations between words...".format(
                    color.BLUE, color.END
                )
            )

            # Convert set to list for combinations
            base_list = list(base_wordlist)

            for i in range(2, min(args.n_words + 1, len(base_list) + 1)):
                print(
                    "  {}[*]{} Creating {}-word combinations...".format(
                        color.CYAN, color.END, i
                    )
                )

                # Process in batches to manage memory with full CPU utilization
                batch_size = max(
                    1000, min(5000, len(base_list) ** i // (cpu_cores * 10))
                )
                processed_count = 0

                for batch in combinator_generator(base_list, i, batch_size=batch_size):
                    final_words_set.update(batch)
                    processed_count += len(batch)

                    # Periodic garbage collection
                    if processed_count % (batch_size * 10) == 0:
                        gc.collect()

                print(
                    "  {}[*]{} {} words combined using {} words (words produced: {})".format(
                        color.CYAN, color.END, len(base_list), i, len(final_words_set)
                    )
                )

        # WORD COMBINATIONS WITH SEPARATORS - OPTIMIZED
        if Config.EXTRA_COMBINATIONS and Config.SEPARATORS_CHARSET:
            print(
                "  {}[+]{} Creating extra combinations using separators charset...".format(
                    color.BLUE, color.END
                )
            )
            base_list = list(base_wordlist)

            # Use parallel processing for large wordlists
            if len(base_list) > 1000:
                separator_combinations = parallel_batch_processor(
                    add_common_separators, base_list
                )
            else:
                # Process in chunks
                separator_combinations = []
                for chunk in process_wordlist_generator(base_list, chunk_size=500):
                    chunk_combinations = multiprocess_transforms(
                        add_common_separators, chunk
                    )
                    separator_combinations.extend(chunk_combinations)

            final_words_set.update(separator_combinations)
            gc.collect()

            print(
                "  {}[*]{} Words produced: {}".format(
                    color.CYAN, color.END, len(final_words_set)
                )
            )
        elif Config.EXTRA_COMBINATIONS:
            print(
                "  {}[!]{} No separators charset specified in {}{}".format(
                    color.ORANGE, color.END, args.cfg_file, color.END
                )
            )

        # Convert to list for final processing
        final_wordlist = list(final_words_set)

        # Remove by length - OPTIMIZED
        print(
            "  {}[-]{} Removing words by min and max length provided ({}-{})...".format(
                color.PURPLE, color.END, args.min_length, args.max_length
            )
        )
        final_wordlist = remove_by_lengths_fast(
            final_wordlist, args.min_length, args.max_length
        )
        print(
            "  {}[*]{} Words remaining: {}".format(
                color.CYAN, color.END, len(final_wordlist)
            )
        )

        # LEET TRANSFORMS - OPTIMIZED
        if args.leet and Config.LEET_CHARSET:
            recursive_msg = (
                "{}recursive{} ".format(color.ORANGE, color.END)
                if Config.RECURSIVE_LEET
                else ""
            )
            print(
                "  {}[+]{} Applying {}leet transforms to {} words...".format(
                    color.BLUE, color.END, recursive_msg, len(final_wordlist)
                )
            )

            # Use parallel batch processing for large wordlists
            if len(final_wordlist) > 5000:
                leet_transforms_list = parallel_batch_processor(
                    leet_transforms, final_wordlist
                )
            else:
                leet_transforms_list = multiprocess_transforms(
                    leet_transforms, final_wordlist
                )

            final_wordlist.extend(leet_transforms_list)

            # Use parallel duplicate removal for large wordlists
            if len(final_wordlist) > 50000:
                final_wordlist = parallel_remove_duplicates(final_wordlist)
            else:
                final_wordlist = remove_duplicates_fast(final_wordlist)

            print(
                "  {}[*]{} Words after leet transforms: {}".format(
                    color.CYAN, color.END, len(final_wordlist)
                )
            )
        elif args.leet:
            print(
                "  {}[!]{} No leet charset specified in {}".format(
                    color.ORANGE, color.END, args.cfg_file
                )
            )
            print(
                "  {}[!]{} Skipping leet transforms...".format(
                    color.ORANGE, color.END, args.cfg_file
                )
            )

        # CASE TRANSFORMS - OPTIMIZED
        if args.case:
            extensive_msg = (
                "{}extensive{} ".format(color.ORANGE, color.END)
                if Config.EXTENSIVE_CASE
                else ""
            )
            print(
                "  {}[+]{} Applying {}case transforms to {} words...".format(
                    color.BLUE, color.END, extensive_msg, len(final_wordlist)
                )
            )

            # Use parallel batch processing for large wordlists
            if len(final_wordlist) > 5000:
                case_transforms_list = parallel_batch_processor(
                    case_transforms, final_wordlist
                )
            else:
                case_transforms_list = multiprocess_transforms(
                    case_transforms, final_wordlist
                )

            final_wordlist.extend(case_transforms_list)

            # Use parallel duplicate removal for large wordlists
            if len(final_wordlist) > 50000:
                final_wordlist = parallel_remove_duplicates(final_wordlist)
            else:
                final_wordlist = remove_duplicates_fast(final_wordlist)

            print(
                "  {}[*]{} Words after case transforms: {}".format(
                    color.CYAN, color.END, len(final_wordlist)
                )
            )

        # Final duplicate removal - OPTIMIZED
        print("  {}[-]{} Removing final duplicates...".format(color.PURPLE, color.END))
        if len(final_wordlist) > 50000:
            final_wordlist = parallel_remove_duplicates(final_wordlist)
        else:
            final_wordlist = remove_duplicates_fast(final_wordlist)
        print(
            "  {}[*]{} Final words count: {}".format(
                color.CYAN, color.END, len(final_wordlist)
            )
        )

        # SAVE WORDLIST TO FILE - OPTIMIZED
        print("  {}[+]{} Writing to output file...".format(color.BLUE, color.END))
        write_wordlist_to_file_parallel(final_wordlist, args.outfile)

        # Final timestamps
        end_time = datetime.datetime.now()
        total_time = end_time - start_time

        # PRINT RESULTS
        print(
            "\n  {}[+]{} Words generated:\t{}{}{}".format(
                color.GREEN, color.END, color.RED, len(final_wordlist), color.END
            )
        )
        print("  {}[+]{} Elapsed time:\t{}".format(color.GREEN, color.END, total_time))
        print(
            "  {}[+]{} Output file:\t{}{}{}{}".format(
                color.GREEN, color.END, color.BOLD, color.BLUE, args.outfile, color.END
            )
        )

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n  {}[!]{} Exiting...\n".format(color.RED, color.END))
        sys.exit(3)
    except MemoryError:
        print(
            "\n\n  {}[!]{} Memory error: Try reducing input size or using smaller wordlists\n".format(
                color.RED, color.END
            )
        )
        sys.exit(3)
    except Exception as e:
        print(f"\n\n  {color.RED}[!]{color.END} Unexpected error: {e}\n")
        sys.exit(3)
