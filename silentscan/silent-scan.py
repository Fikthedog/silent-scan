#!/usr/bin/env python3

import subprocess
import os
import time
import json
import socket
from datetime import datetime

# ---------------------------
#  MAC Vendor Lookup
# ---------------------------
def lookup_mac_vendor(mac):
    try:
        import requests
        url = f"https://api.macvendors.com/{mac}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.text.strip()
    except:
        pass
    return "Unknown Vendor"

# ---------------------------
#  Silent Scan Tool
# ---------------------------
def silent_scan():
    print("\n=== Silent Scan ===")
    output = subprocess.check_output(["arp", "-a"]).decode()

    devices = []
    for line in output.splitlines():
        if "(" in line and ")" in line and " at " in line:
            try:
                name = line.split(" ")[0]
                ip = line.split("(")[1].split(")")[0]
                mac = line.split(" at ")[1].split(" ")[0]

                vendor = lookup_mac_vendor(mac)

                devices.append((name, ip, mac, vendor))
            except:
                pass

    print("\nDiscovered Devices:")
    for d in devices:
        print(f"{d[0]:15}  {d[1]:16}  {d[2]:20}  {d[3]}")
    print("")

# ---------------------------
#  Port Peek (SYN Scanner)
# ---------------------------
def port_peek():
    import scapy.all as scapy
    target = input("Target IP: ")

    ports = [22, 80, 443, 8080, 3306, 53]
    print("\nScanning...")

    for port in ports:
        pkt = scapy.IP(dst=target)/scapy.TCP(dport=port, flags="S")
        resp = scapy.sr1(pkt, timeout=0.5, verbose=0)
        if resp and resp.haslayer(scapy.TCP) and resp.getlayer(scapy.TCP).flags == 0x12:
            print(f"OPEN → {port}")
        else:
            print(f"CLOSED → {port}")

# ---------------------------
#  Wi-fi Scan (macOS)
# ---------------------------
def wifi_scan():
    print("\n=== Wi-Fi Scanner ===")
    try:
        airport = subprocess.check_output(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"]
        ).decode()
        print(airport)
    except:
        print("Wi-Fi scan not supported on this system.")

# ---------------------------
#  Live Device Monitor
# ---------------------------
def live_monitor():
    print("\nMonitoring devices (Ctrl+C to stop)…")
    seen = set()

    while True:
        output = subprocess.check_output(["arp", "-a"]).decode()
        for line in output.splitlines():
            if "(" in line and ")" in line and " at " in line:
                mac = line.split(" at ")[1].split(" ")[0]
                if mac not in seen:
                    seen.add(mac)
                    print(f"[NEW DEVICE] {mac}  ({lookup_mac_vendor(mac)})")

        time.sleep(5)

# ---------------------------
#  Main Menu
# ---------------------------
def main():
    while True:
        print("""
╔════════════════════════════╗
║        Silent Scan         ║
║        Multi-Tool          ║
╠════════════════════════════╣
║ 1) Silent Scan             ║
║ 2) Port Peek (SYN scan)    ║
║ 3) Device Fingerprinter    ║
║ 4) Wi-Fi Signal Mapper     ║
║ 5) Live Device Monitor     ║
║ 6) Exit                    ║
╚════════════════════════════╝
""")
        choice = input("Select tool: ")

        if choice == "1":
            silent_scan()
        elif choice == "2":
            port_peek()
        elif choice == "3":
            device_fingerprinter()
        elif choice == "4":
            wifi_scan()
        elif choice == "5":
            live_monitor()
        elif choice == "6":
            break
        else:
            print("Invalid option.")

# ---------------------------
#  Entry
# ---------------------------
if __name__ == "__main__":
    main()
