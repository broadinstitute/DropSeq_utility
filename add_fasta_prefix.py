#!/usr/bin/env python

"""
Add genome prefix to a fasta file.
"""

import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add a prefix for multiple species experiments")
    parser.add_argument("--output", help="Output fasta", required=True)
    parser.add_argument("input", help="fasta file", nargs='+')
    args = parser.parse_args()
    with open(args.output, "w") as f:
        for fasta_file in args.input:
            prefix = os.path.basename(fasta_file)
            dot_index = prefix.rfind('.')
            prefix = prefix[0:dot_index]
            with open(fasta_file, "r") as reader:
                for line in reader:
                    line = line.strip()
                    if line.startswith('>'):
                        line = '>' + prefix + '_' + line[1:]
                    f.write(line + '\n')
