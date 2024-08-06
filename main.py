# Made by scarlxrd_1337 and usagi
# https://github.com/Scarlxrd211/nitro-checker
# Please don't be a skid

import requests
from colorama import Fore, init
import time
from datetime import datetime
import os
import sys

# Initialize colorama
init(autoreset=True)

# Define colors for print
G = Fore.GREEN
R = Fore.RED
W = Fore.WHITE
M = Fore.MAGENTA
T = Fore.LIGHTBLACK_EX
Y = Fore.YELLOW

# Define global variables
valids, invalids, claimed = 0, 0, 0

# List for rate limited requests (to recheck)
rate_limited = []

class Manage:
    def __init__(self, nitros_path):
        self.nitros_path = nitros_path
        self.clear()
        self.load_nitro()
        self.clear()
        self.clear_files()
        self.clear()

    def clear(self):
        return os.system('cls' if os.name == 'nt' else 'clear')

    # Special print for time in line start
    @staticmethod
    def sprint(text):
        return f"{T}[{W}{text}{T}]{W}"

    # Get time now
    @staticmethod
    def rntime():
        return datetime.now().strftime("%H:%M:%S")

    # Save an element in file (1 element per line)
    @staticmethod
    def save_in(file_path, element):
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(element + "\n")
            return True
        except Exception as e:
            print(f"Error saving to file {file_path}: {e}")
            return False

    def clear_files(self):
        choice = input(f"{M}[?] Do you want to clear all old nitro checked files (yes/no)? ")
        if choice.lower() in ['yes', 'y']:
            for file in ['data/claimed.txt', 'data/invalids.txt', 'data/valids.txt']:
                with open(file, 'w') as f:
                    pass

    def load_nitro(self):
        with open(self.nitros_path, 'r') as f:
            if len(f.read().splitlines()) == 0:
                print(f"{R}[!] There are no nitro links in file ({self.nitros_path})")
                sys.exit(0)

class NitroChecker:
    def __init__(self):
        pass
    # Check nitro main function
    def check_nitro(self, link):
        global valids, invalids, claimed

        start = time.time()
        now_dt = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        time_to_check = now_dt[:-2] + ':' + now_dt[-2:]

        # Rate limit Handler
        if not rate_limited:
            code = link[21:]
        else:
            code = rate_limited.pop(0)[21:]

        # Requests to get nitro code information
        req = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{code}")
        end = time.time()

        # Code: rate limited
        if req.status_code == 429:
            rate_limited.append(link)
            print(f"{Manage.sprint(Manage.rntime())}{Y}[!] Rate limited, will retry later")

        # Code with valid response (claimed, valid, expired)
        elif req.status_code == 200:
            response = req.json()
            nitro_type = response.get('store_listing', {}).get('sku', {}).get('slug', 'unknown')
            expires_at = response.get('expires_at')
            nitro_type = "NITRO BASIC" if nitro_type == "nitro-basic" else "NITRO BOOST" if nitro_type == "nitro" else nitro_type

            # Expired Nitro Code
            if expires_at and time_to_check > expires_at:
                Manage.save_in("data/invalids.txt", link)
                invalids += 1
                return_code = f"{T}[{R}INVALID{T}]{W}"
                print(f"{Manage.sprint(Manage.rntime())}{R}[X] Nitro Code: {W}{code} {return_code} {W}[{M}{nitro_type}{T}]{W} Time Taken: {end - start:.2f}s")
                return

            # Claimed Nitro Code
            if response.get('uses') == response.get('max_uses') or response.get('redeemed', True):
                Manage.save_in("data/claimed.txt", link)
                claimed += 1
                return_code = f"{T}[{Y}CLAIMED{T}]{W}"
                print(f"{Manage.sprint(Manage.rntime())}{Y}[!] Nitro Code: {W}{code} {return_code} {W}[{M}{nitro_type}{T}]{W} Time Taken: {end - start:.2f}s")
                return

            # Valid and not claimed nitro code
            else:
                Manage.save_in("data/valids.txt", link)
                valids += 1
                return_code = f"{T}[{G}VALID{T}]{W}"
                print(f"{Manage.sprint(Manage.rntime())}{G}[+] Nitro Code: {W}{code} {return_code} {W}[{M}{nitro_type}{T}]{W} Time Taken: {end - start:.2f}s")
                return

        # Nitro Code doesn't exist (Unknown code for API)
        elif req.status_code == 404:
            Manage.save_in("data/invalids.txt", link)
            invalids += 1
            return_code = f"{T}[{R}INVALID{T}]{W}"
            print(f"{Manage.sprint(Manage.rntime())}{R}[+] Nitro Code: {W}{code} {return_code} {W} Time Taken: {end - start:.2f}s")

if __name__ == "__main__":
    nitros_path = input("Nitro file: ")
    with open(nitros_path, 'r') as f:
        links = f.read().splitlines()

    manager = Manage(nitros_path)
    checker = NitroChecker()

    for link in links:
        checker.check_nitro(link)
    print(f"\n{M}[+] All Nitro Are Checked: {W}{valids}{G} Valids / {W}{claimed}{G} Claimed / {W}{invalids}{G} Invalids")

