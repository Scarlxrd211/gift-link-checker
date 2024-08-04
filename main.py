# Made by scarlxrd_1337
# https://github.com/Scarlxrd211/nitro-checker
# Please don't be a skid

import requests
from colorama import *
import time
from datetime import datetime
import os
import sys

# Define colors for print
G = Fore.GREEN
R = Fore.RED
W = Fore.WHITE
M = Fore.MAGENTA
T = Fore.LIGHTBLACK_EX
Y = Fore.YELLOW

# Define global variables
valids = 0
invalids = 0
claimed = 0

# List for rate limited requests (to recheck)
rate_limited = []

# Clear all output files function
def clear_files():
    choice = input(f"{M}[?] Do you want clear all old nitro checked files (yes/no) ?: ")
    if choice.lower() == 'yes' or choice.lower() == "y":
        with open('data/claimed.txt', 'w') as f:
            pass
        with open("data/invalids.txt", 'w') as f:
            pass
        with open('data/valids.txt', 'w') as f:
            pass
        return
    else:
        return 

# Clear command prompt
def clear():
    return os.system('cls') 

# Special print for time in line start
def sprint(text):
    return f"{T}[{W}{text}{T}]{W}"

# Get time now
def rntime():
    return datetime.now().strftime("%H:%M:%S")

# Save an element in file (1 element per line)
def save_in(file_path, element):
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(element + "\n")
        return True
    except Exception as e:
        print("err")

# Check if nitro are in input files
def load_nitro():
    with open('data/nitro.txt', 'r') as f:
        if len(f.read().splitlines()) == 0:
            print(f"{R}[!] There is any nitro links in file (data/nitro.txt)")
            return sys.exit(0)
        
# Check nitro main function
def check_nitro(link):
    global valids, invalids, claimed

    start = time.time()
    now_dt = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
    time_to_check = now_dt[:-2] + ':' + now_dt[-2:]
    
    # Rate limit Handler
    if rate_limited == []:
        code  = link[21:]
    elif rate_limited != []:
        code = rate_limited[0][21:]
        rate_limited.clear()
    
    # Requests to get nitro code informations
    req = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{code}")
    end = time.time()

    # Code: rate limited
    if req.status_code == 429:
        rate_limited.append(link)

    # Code with valid response (claimed, valid, expired)
    if req.status_code == 200:
        response = req.json()
        expires_at = response.get('expires_at')

        # Expired Nitro Code
        if expires_at and time_to_check > expires_at:
            save_in("data/invalids.txt", link)
            invalids += 1
            return_code = f"{T}[{R}INVALID{T}]{W}"
            print(f"{sprint(rntime())}{R}[X] Nitro Code: {W}{code} {return_code} {W}Time Taken: {end - start:.2f}")
            return
        
        # Claimed Nitro Code
        if response.get('uses') == response.get('max_uses'):
            save_in("data/claimed.txt", link)
            claimed += 1
            return_code = f"{T}[{Y}CLAIMED{T}]{W}"
            print(f"{sprint(rntime())}{Y}[!] Nitro Code: {W}{code} {return_code} {W}Time Taken: {end - start:.2f}")
            return
        
        # Claimed Nitro Code too
        if response.get('redeemed', True):
            save_in("data/claimed.txt", link)
            claimed += 1
            return_code = f"{T}[{Y}CLAIMED{T}]{W}"
            print(f"{sprint(rntime())}{Y}[!] Nitro Code: {W}{code} {return_code} {W}Time Taken: {end - start:.2f}")
            return
        
        # Valid and not claimed nitro code
        else:
            save_in("data/valids.txt", link)
            valids += 1
            return_code = f"{T}[{G}VALID{T}]{W}"
            print(f"{sprint(rntime())}{G}[+] Nitro Code: {W}{code} {return_code} {W}Time Taken: {end - start:.2f}")
            return
        
    # Nitro Code doesn't exist (Unknown code for api)
    elif req.status_code == 404:
        save_in("data/invalids.txt", link)
        invalids += 1
        return_code = f"{T}[{R}INVALID{T}]{W}"
        print(f"{sprint(rntime())}{R}[+] Nitro Code: {W}{code} {return_code} {W}Time Taken: {end - start:.2f}")

# Main Function
def main():
    global valids, claimed, invalids

    # Check Nitro in files and clear files
    clear()
    load_nitro()
    clear()
    clear_files()
    clear()

    # one-line to check all nitro in file
    [check_nitro(code) for code in open('data/nitro.txt', 'r').read().splitlines()]
    print(f"{M}[+] All Nitro Are Checked: {W}{valids}{G} Valids / {W}{claimed}{G} Claimed / {W}{invalids}{G} Invalids")

if __name__ == "__main__":
    main()