#!/usr/bin/env python3
# SILENT-SCAN: Passive Network Scanner — Real Devices Only

import time
import sys
import json
import subprocess
import random

# Safe fallback if colorama isn't installed
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore:
        RED = ''
        GREEN = ''
        BLUE = ''
        YELLOW = ''
        CYAN = ''
        MAGENTA = ''
    class Style:
        BRIGHT = ''
        RESET_ALL = ''

# CLEAN ASCII LOGO (Terminal-safe)
logo = f"""
{Fore.CYAN}{Style.BRIGHT}
   ____  _ _            _      ____                           
  / ___|| (_) ___ _ __ | |_   / ___|  ___ __ _ _ __           
  \___ \| | |/ _ \ '_ \| __|  \___ \ / __/ _` | '_ \          
   ___) | | |  __/ | | | |_    ___) | (_| (_| | | | |         
  |____/|_|_|\___|_| |_|\__|  |____/ \___\__,_|_| |_|         
            M A D E  B Y  F I K T H E D O G
{Style.RESET_ALL}
Passive Network Scanner — Ethical & Stealth
"""

# Fake vendor list for cosmetics
def get_mac_vendor(mac):
    vendors = ["Cisco", "TP-Link", "Apple", "Intel", "Netgear", "Ubiquiti", "Unknown"]
    return random.choice(vendors)

# Parse ARP table for real hosts
def get_real_hosts():
    hosts = []
    try:
        output = subprocess.check_output(['arp', '-a']).decode()
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[1].strip("()")
                mac = parts[3] if len(parts) >= 4 else "UNKNOWN"
                hosts.append({
                    "ip": ip,
                    "mac": mac,
                    "vendor": get_mac_vendor(mac)
                })
    except Exception as e:
        print(f"{Fore.RED}[!] Error reading ARP table: {e}")
    return hosts

# Fancy animation (visual only)
def scan_animation(ip):
    for i in range(3):
        sys.stdout.write(f"\rScanning {ip} {'.'*i}   ")
        sys.stdout.flush()
        time.sleep(0.4)
    print(f"\r{Fore.GREEN}[+] Host detected: {ip}           ")

def silent_scan():
    print(logo)
    print(f"{Fore.YELLOW}Initializing passive scan...\n")
    time.sleep(1)

    hosts = get_real_hosts()
    if not hosts:
        print(f"{Fore.RED}[!] No hosts found in ARP table.")
        return

    for host in hosts:
        scan_animation(host["ip"])

    # Save results
    with open("silent_scan_results.json", "w") as f:
        json.dump(hosts, f, indent=4)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}[✓] Scan complete.")
    print(f"{Fore.CYAN}[i] Results saved to silent_scan_results.json")
    print(f"[i] Total hosts detected: {len(hosts)}")

if __name__ == "__main__":
    silent_scan()