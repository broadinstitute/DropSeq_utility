#!/usr/bin/env python

"""
Add genome prefix to a fasta file.
"""

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add a prefix for multiple species experiments")
    parser.add_argument("--output", help="Output basename", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("input", help="fasta file", nargs='+')
    args = parser.parse_args()
    fasta_files = args.input
    prefix_list = args.prefix.split(',')
    with open(args.output + '.fasta', "w") as f:
        for i in range(len(fasta_files)):
            fasta_file = fasta_files[i]
            prefix = prefix_list[i]
            with open(fasta_file, "r") as reader:
                for line in reader:
                    line = line.strip()
                    if line.startswith('>'):
                        line = '>' + prefix + '_' + line[1:]
                    f.write(line + '\n')
