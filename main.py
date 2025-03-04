import re
import requests
import threading
import os
import time

w = '\033[38;2;255;255;255m'
c = '\033[38;2;245;174;187m'

url = "https://minecraft-mp.com/servers/random/"

def clean():
    print(f'{c}[{w}*{c}]{w} Cleaning ips.txt & raw.txt')
    with open('ips.txt', 'w') as i:
        i.write(fr'''
 __         ______     ______     ______    
/\ \       /\  __ \   /\  ___\   /\  ___\   
\ \ \____  \ \ \/\ \  \ \ \__ \  \ \___  \  
 \ \_____\  \ \_____\  \ \_____\  \/\_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/ 
       Raccoon Logs | Made by crxelty''')
        print(f'{c}[{w}+{c}]{w} Cleaned ips.txt successfully!')
        print(f'-')
    with open('raw.txt', 'w') as z:
        z.write('')
        print(f'{c}[{w}+{c}]{w} Cleaned raw.txt successfully!')

def check_protection(server):
    res = requests.get(f'https://networkcalc.com/api/dns/lookup/{server}').text.lower()
    if 'cloudflare' in res: return True, 'cloudflare'
    elif 'tcpshield' in res: return True, 'tcpshield'
    elif 'neoprotect' in res: return True, 'neoprotect'
    else: return False, ''

def main():
    while True:
        r = requests.get(url)
        servers = re.findall(r'<strong>(.*?)</strong></button>', r.text)
        for ip in servers:
            try:
                server = requests.get(f'https://api.mcstatus.io/v2/status/java/{ip}').json()
                raw = server['ip_address']
                players = f"{server['players']['online']}/{server['players']['max']}"
                ver = server['version']['name_raw']
                protected, protype = check_protection(ip)

                if server['players']['online'] and raw not in open('ips.txt').read() and 'velocity' not in ver.lower():
                    info = (
                        f"{c}[{w}+{c}] {w}Found Server! │ "
                        f"{c}IP:{w} {str(raw).ljust(15)} │ "
                        f"{c}Players:{w} {str(players[:13]).ljust(13)} │ "
                        f"{c}Protected?:{w} {str(protected).ljust(5)} ({str(protype + ')' if protype != '' else raw + ')').ljust(17)} │ "
                        f"{c}Version: {w}({ver[:20]})"
                    )
                    print(info)
                    if not protected:
                        with open('ips.txt', 'a+', encoding='utf-8') as i: 
                            i.write(f'\n─────────────────────────────────────────\nDomain: {ip}\nIP: {raw}\nPlayers: {players}\nProtected?: {protected} ({protype if protype != "" else raw})\nVersion: ({ver[:20]})')
                        with open('raw.txt', 'a+', encoding='utf-8') as gg: 
                            gg.write(f'{raw}\n')
            
            except Exception as e:
                pass

if __name__ == '__main__':
    clean()
    os.system('cls')
    print(f'{w}raccoon scanner {c}v3')
    threads = []
    for i in range(50):
        t = threading.Thread(target=main)
        t.start()
        threads.append(t)
