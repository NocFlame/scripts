#!/usr/bin/env python
# -*- coding: utf-8 -*-

#CPF - Create Passwords Files (success.txt and failures.txt) from two input files (one potfile and one hashfile)
#Current inputformat (hashfile) is resultfile from responder
# file hashes is the file with suitable inputformat for hashcat, file two is the potfile.
#example hashfile:
#domain.com\UserOne1:12345:aad3b435b51404eeaad3b435b51404ee:668fc9fb3deadbeaffffdeadbeefa403:::
#file 2:
#668fc9fb3deadbeaffffdeadbeefa403:FakePwd
#success file will have output format like $user:$hash:$password example:
#domain.com\UserOne1:668fc9fb3deadbeaffffdeadbeefa403:FakePwd

from pathlib import Path

potfilepath = "hashcat.potfile"
hashfilepath = "dc_synced.ntlm"

dict_from_potfile = {}
dict_from_hashfile = {}
dict_cracked_accounts = {}

with open(potfilepath, encoding="utf8") as potfile:
        for line in potfile:
            pothash = line.split(':')[0].strip()
            potpwd = line.split(':')[1]
            dict_from_potfile[pothash] = potpwd

with open(hashfilepath, encoding="utf8") as hashfile:
        for line in hashfile:
            try:
                raw_hash = line.split(":")
                username = raw_hash[0]
                hash = raw_hash[3]
                dict_from_hashfile[hash] = username
            except IndexError as identifier:
                pass

for hash in dict_from_potfile:
    if hash in dict_from_hashfile:
        username = dict_from_hashfile[hash]
        password = dict_from_potfile[hash].strip()
        hashinfo = {"username":username, "password":password}
        dict_cracked_accounts[hash] = hashinfo
        #print(''.join( (username,":",hash,":",password) ))
        #print(dict_cracked_accounts[hash])
        dict_from_hashfile.pop(hash)

def print_to_file_success():
    try:
        with open(Path(hashfilepath).parent / 'success.txt', 'w') as success_file:
            for x,y in dict_cracked_accounts.items():
                success_file.write(''.join( (y['username'],":",hash,":",y['password'],"\n") ))
        success_file.close()
        print("Created file: success.txt")
    except Exception as identifier:
        print(identifier)

def print_to_file_failed():
    try:
        with open(Path(hashfilepath).parent / 'failures.txt', 'w') as failure_file:
            for x,y in dict_from_hashfile.items():
                failure_file.write(''.join( (y,":",x,"\n") ))
        failure_file.close()
        print("Created file: failures.txt")
    except Exception as identifier:
        print(identifier)

def print_all_success_to_console():
    #print all elements of success
    for x,y in dict_cracked_accounts.items():
        print(''.join( (y['username'],":",hash,":",y['password']) ))

#prints some stats here
print("Accounts cracked: ", len(dict_cracked_accounts))
print("Accounts not cracked:", len(dict_from_hashfile))

#print results to files on disk here
print_to_file_success()
print_to_file_failed()
