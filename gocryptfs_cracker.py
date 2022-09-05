#!/usr/bin/env python
import subprocess

GOCRYPTSFS_CIPHER_FOLDER = "/path/to/cipher/folder/"
GOCRYPTSFS_PLAIN_FOLDER = "/path/to/plain/folder/"
WORDLIST= "/path/to/wordlist.txt"

def check_pass(password):
    process = subprocess.Popen(["gocryptfs", GOCRYPTFS_CIPHER_FOLDER , GOCRYPTFS_PLAIN_FOLDER], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.stdin.write(password)
    process.stdin.close()
    #print(process.stdout.read())
    output = process.stdout.read()
    if "ready" in output:
        print("Password found: "+ password)
        exit(1)

with open(WORDLIST) as fp:
    Lines = fp.readlines()
    print("Number of lines in file:", len(Lines))
    counter = 0
    for line in Lines:
        counter += 1
        if (counter % 100 == 0):
            print("on line number:", counter)
        check_pass(line)
        #check_pass(line+"2022")
        #check_pass(line+"22")
