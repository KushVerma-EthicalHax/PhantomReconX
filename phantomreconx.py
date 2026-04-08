import requests
import socket
import whois
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# =========================
# BANNER
# =========================
def banner():
    print(Fore.RED + """
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
        PhantomRecon X - Cyber Intelligence Tool
""" + Style.RESET_ALL)

# =========================
# IP INFO
# =========================
def ip_lookup(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = res.json()

        if data['status'] != 'success':
            print(Fore.RED + "[-] Invalid IP")
            return None

        print(Fore.GREEN + "\n[+] IP INFORMATION")
        print("-" * 40)
        print(f"IP Address   : {ip}")
        print(f"Country      : {data.get('country')}")
        print(f"Region       : {data.get('regionName')}")
        print(f"City         : {data.get('city')}")
        print(f"ISP          : {data.get('isp')}")
        print(f"Org          : {data.get('org')}")
        print(f"Timezone     : {data.get('timezone')}")

        return data

    except:
        print(Fore.RED + "[-] Network Error")
        return None

# =========================
# REVERSE DNS
# =========================
def reverse_dns(ip):
    print(Fore.CYAN + "\n[+] REVERSE DNS")
    try:
        host = socket.gethostbyaddr(ip)
        print(f"Hostname     : {host[0]}")
        return host[0]
    except:
        print("Hostname     : Not Found")
        return "Not Found"

# =========================
# WHOIS
# =========================
def whois_lookup(ip):
    print(Fore.YELLOW + "\n[+] WHOIS INFO")
    try:
        host = socket.gethostbyaddr(ip)[0]
        w = whois.whois(host)
        org = w.org if w.org else "N/A"
        print(f"Organization : {org}")
        return org
    except:
        print("WHOIS        : Failed")
        return "Failed"

# =========================
# PORT SCAN
# =========================
def port_scan(ip):
    print(Fore.MAGENTA + "\n[+] PORT SCAN (Top Ports)")
    os.system(f"nmap -Pn -F {ip}")

# =========================
# SAVE REPORT
# =========================
def save_report(ip, data, hostname, org):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/{ip}.txt"

    with open(filename, "w") as f:
        f.write(f"PhantomRecon X Report\n")
        f.write(f"Time: {datetime.now()}\n\n")

        if data:
            f.write(f"IP: {ip}\n")
            f.write(f"Country: {data.get('country')}\n")
            f.write(f"City: {data.get('city')}\n")
            f.write(f"ISP: {data.get('isp')}\n")

        f.write(f"Hostname: {hostname}\n")
        f.write(f"Organization: {org}\n")

    print(Fore.GREEN + f"\n[+] Report Saved: {filename}")

# =========================
# MAIN
# =========================
def main():
    banner()
    
    ip = input(Fore.WHITE + "Enter Target IP: ").strip()

    data = ip_lookup(ip)
    hostname = reverse_dns(ip)
    org = whois_lookup(ip)
    port_scan(ip)

    save_report(ip, data, hostname, org)

if __name__ == "__main__":
    main()
