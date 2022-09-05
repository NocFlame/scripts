#!/usr/bin/env python
from operator import contains
import subprocess
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

GOCRYPTSFS_CIPHER_FOLDER = "/path/to/cipher/folder/"
GOCRYPTSFS_PLAIN_FOLDER = "/path/to/plain/folder/"
WORDLIST= "/path/to/wordlist.txt"
#To unmount mounted crypto folder use: "fusermount -u /path/to/plain/folder/"

def check_pass(password):
    process = subprocess.Popen(["gocryptfs", GOCRYPTSFS_CIPHER_FOLDER, GOCRYPTSFS_PLAIN_FOLDER], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.stdin.write(password)
    process.stdin.close()
    #print(process.stdout.read())
    output = process.stdout.read()
    if "ready" in output:
        print("Password found: "+ password)
        return "Password found: "+ password

t1 = time.perf_counter()
result = []
with open(WORDLIST) as fp:
    Lines = fp.readlines()
    print("Number of lines in file:", len(Lines))
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        # result = executor.map(check_pass, Lines)
        # if len(result) > 0:
        #     executor.shutdown(wait=False, cancel_futures=True)

        futures = [executor.submit(check_pass, password) for password in Lines]
        for future in as_completed(futures):
            #if future.result() == "result found":
            res = future.result()
            if res != None:
                executor.shutdown(wait=False, cancel_futures=True)
                print("shutdown")
                for f in futures:
                    if not f.done():
                        f.cancel()
                break
print("about to exit")

t2 = time.perf_counter()
print(f'MultiThreaded Code Took:{t2 - t1} seconds')
    #counter = 0
    #for line in Lines:
        #if (counter % 100 == 0):
        #    print("on line number:", counter)
        #check_pass(line)
        #check_pass(line+"2022")
        #check_pass(line+"22")
