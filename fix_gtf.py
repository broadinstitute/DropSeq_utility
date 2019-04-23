#!/usr/bin/env python

import argparse
import collections
import re

if __name__ == '__main__':
    SEMICOLON = re.compile(r'\s*;\s*')
    KEYVALUE = re.compile(r'(\s+|\s*=\s*)')

    parser = argparse.ArgumentParser(
        description='Fix gene and transcript names in a GTF file and optionally add a genome prefix.')
    parser.add_argument('--output', help='Output GTF file', required=True)
    parser.add_argument('--prefix', help='Comma delimitted genome prefixes')
    parser.add_argument('input', help='Input GTF file', nargs='+')
    args = parser.parse_args()
    gtf_files = args.input
    output_file = args.output

    prefix_list = None
    if args.prefix is not None and len(gtf_files) > 1:
        prefix_list = args.prefix.split(',')

    writer = open(output_file, 'w')
    for gtf_file_index in range(len(gtf_files)):
        prefix = prefix_list[gtf_file_index] if prefix_list is not None else None
        input_file = gtf_files[gtf_file_index]

        with open(input_file, 'r') as reader:
            for line in reader:
                if not line.startswith('#'):
                    values = line.rstrip().split('\t')
                    # last column contains key-value pairs
                    infos = [x for x in re.split(SEMICOLON, values[8]) if x.strip()]
                    key_vals = collections.OrderedDict()
                    for i, info in enumerate(infos, 1):
                        # It should be key="value".
                        try:
                            key, _, value = re.split(KEYVALUE, info, 1)
                        # But sometimes it is just "value".
                        except ValueError:
                            key = 'INFO{}'.format(i)
                            value = info
                        # Ignore the field if there is no value.
                        if value != '':
                            key_vals[key] = value
                    # use gene_id for gene_name and transcript_id for transcript_name
                    if key_vals.get('gene_name') is None:
                        gene_id = key_vals.get('gene_id')
                        if gene_id is None:
                            continue
                        key_vals['gene_name'] = gene_id
                    if key_vals.get('gene_id') is None:
                        key_vals['gene_id'] = key_vals.get('gene_name')

                    if key_vals.get('transcript_name') is None:
                        transcript_id = key_vals.get('transcript_id')
                        if transcript_id is None:
                            continue
                        key_vals['transcript_name'] = transcript_id
                    if key_vals.get('transcript_id') is None:
                        key_vals['transcript_id'] = key_vals.get('transcript_name')

                    if prefix is not None:
                        values[0] = prefix + '_' + values[0]
                    writer.write('\t'.join(values[0:8]))
                    writer.write('\t')
                    is_first_key = True
                    for k in key_vals:
                        if not is_first_key:
                            writer.write(' ')
                        info_val = key_vals[k]
                        if info_val[0] != '"':
                            info_val = '"' + info_val + '"'
                        if info_val[len(info_val) - 1] != ';':
                            info_val = info_val + ';'
                        writer.write(k + ' ' + info_val)
                        is_first_key = False

                else:  # comment
                    writer.write(line)
                writer.write('\n')
    writer.close()
