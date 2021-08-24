# coding=utf8
#usage -> my_wordlist_cleaner -i input_file -o output_file
#if no output file is specified stdout is given
import re
import os.path as path
import argparse

parser = argparse.ArgumentParser(description='Wordlist cleaner with umlat support')
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-o','--output',help='Output file name', required=False)
args = parser.parse_args()

input_file = args.input
output_file = args.output

data = []

regex = re.compile('([\w\u00C0-\u00ff]+.{1}[\w\u00C0-\u00ff]+)|([\w\u00C0-\u00ff]+)')

if path.exists(input_file):
    with open(input_file) as f:
        for line in f:
            result = regex.search(line)
            if result:
                data.append(result.group()+'\n')
    
    if output_file:
        with open(output_file, 'w') as file_out:
            file_out.writelines(data)
    else:
        #Write to console
        for line in data:
            print(line.strip())
else:
    print('Input file does not exist')
    exit('1')
