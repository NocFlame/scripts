#!/usr/bin/env python
#This version does not work too good yet,should probably just keep the other one
import concurrent
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
import subprocess
from os.path import exists
from os import remove, makedirs, getcwd
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found, please install with pip3 install google")
    print("google depends on beautifulsoup4 aswell so if you dont have it -> pip3 install beautifulsoup4")
    print("But if installing google then it should install beautifulsoap4 for you...")

cewl_path = "/git/CeWL/cewl.rb"

def check_for_target_folder(path):
    if exists(path) == False:
        makedirs(path)

def remove_file(filename):
    if exists(filename):
        remove(filename)

def merge_filelist(wordlist, filelist):
    for line in filelist:
        try:
            line_split = line.split(",")
            if line_split[0] in wordlist:
                value = int(wordlist[line_split[0]])
                new_value = value + int(line_split[1])
                wordlist[line_split[0]] = new_value
            else:
                wordlist[line_split[0]] = int(line_split[1])
        except IndexError:
            pass #Throw away invalid rows...

def cewl(url, filename, extended=False):
    print("Started CeWL on url:", url)
    if extended:
        if verbose:
            process = subprocess.Popen([cewl_path, "-d 1", "-m 1", "-g 5", "--with-numbers", "-e", "-c", "-a", "-v", "-w", filename+"_extended", url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            process = subprocess.Popen([cewl_path, "-d 1", "-m 1", "-g 5", "--with-numbers", "-e", "-c", "-a", "-w", filename+"_extended", url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        if verbose:
            process = subprocess.Popen([cewl_path, "-d 1", "-m 1", "-c", "--lowercase", "-v", "-w", filename, url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:    
            process = subprocess.Popen([cewl_path, "-d 1", "-m 4", "-c", "-w", filename, url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if verbose:
        print(process.stdout.read())
        print(process.stderr.read())

parser = argparse.ArgumentParser(description='Wordlistgenerator from top 10 google search results.')
parser.add_argument("query")
parser.add_argument('-e','--extended', help='Runs the extended version where metadata, email and groups are called with CeWL.', default=False, action="store_true", required=False)
parser.add_argument('-k', '--keep', help='keep all intermidiate generated files.', default=False, action="store_true", required=False)
parser.add_argument('-v','--verbose', help='verbose output from CeWL.', default=False, action="store_true", required=False)
parser.add_argument('-w','--path', help='path to where wordlist will be written. Default is current folder', default=getcwd()+"/", required=False)
args = parser.parse_args()

query = args.query
verbose = args.verbose
extended_search = args.extended
my_wordlist_path = args.path
keep_files = args.keep

t1 = time.perf_counter()
result = []
url_list = []
file_list = []
with concurrent.futures.ThreadPoolExecutor(1) as executor:
    fs = []
    #print("The following urls will be used as input for CeWL:")
    for index, url in enumerate(search(query, num=10, stop=10, pause=2)):
        #print(url)
        url_list.append(url)
        base_url = url.split("/")
        filename = query + "_" + str(index+1) + "_" + base_url[2]
        path = my_wordlist_path+query+"/"
        filename = path+filename
        file_list.append(filename)
        check_for_target_folder(path)
        remove_file(filename)
        fs.append(executor.submit(cewl, url, filename))
        if extended_search:
            filename_extended = query + "_" + str(index+1) + "_" + base_url[2] + "_extended"
            filename_extended = path+filename_extended
            file_list.append(filename_extended)
            check_for_target_folder(path)
            remove_file(filename_extended)
            fs.append(executor.map(cewl, url, filename_extended, extended_search))
    concurrent.futures.wait(fs) # wait for all threads
    for f in fs: result.append(f.result())

print ("All threads have been exited")

print("Starting aggregating data")
all_lines = []
all_extended_lines = []
all_basic_lines = []
for file in file_list:
    try:
        if "_extended" in file:
            with open(file) as fp:
                for line in fp:
                    all_extended_lines.append(line)
        else:
            with open(file) as fp:
                for line in fp:
                    all_basic_lines.append(line)
    except FileNotFoundError as e:
        print("Could not open file: ", e)
        pass

print("starting to sort the aggregated data")
if extended_search:
    all_lines = all_basic_lines + all_extended_lines
    print("lines to be sorted: ", len(all_lines))
    all_lines.sort()
else:
    print("lines to be sorted: ", len(all_basic_lines))
    all_basic_lines.sort()
print("sorting done")
print("merging all duplicates")
wordlist = {}
if extended_search:
    merge_filelist(wordlist, all_lines)
else:
    merge_filelist(wordlist, all_basic_lines)

#sort wordlist by value
wordlist_tmp = sorted(wordlist.items(), key=lambda x:x[1], reverse=True)
wordlist_sorted = dict(wordlist_tmp)

#write wordlist to file
with open(path + "wordlist.txt", 'w') as f: 
    for key, value in wordlist_sorted.items(): 
        #f.write('%s:%s\n' % (key, value))
        f.write('%s\n' % (key))

print("final wordlist written to disk: "+ path + "wordlist.txt")
print("Lines in wordlist is: ", len(wordlist))
if not keep_files:
    for file in file_list:
        remove_file(file)
print("Wordlist is sorted by frequency")

t2 = time.perf_counter()
print(f'MultiThreaded Code Took:{t2 - t1} seconds')
