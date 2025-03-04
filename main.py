import re
import requests
import threading
import os


w = '\033[38;2;255;255;255m'
c = '\033[38;2;245;174;187m'

url = "https://minecraft-mp.com/servers/random/"

def clean():
    print(f'{c}[{w}*{c}]{w} Cleaning ips.txt')
    with open('ips.txt', 'w') as i :
        i.write(fr'''
 __         ______     ______     ______    
/\ \       /\  __ \   /\  ___\   /\  ___\   
\ \ \____  \ \ \/\ \  \ \ \__ \  \ \___  \  
 \ \_____\  \ \_____\  \ \_____\  \/\_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/ 
       Raccoon Logs | Made by crxelty''')
        print(f'{c}[{w}+{c}]{w} Cleaned ips.txt successfully!')
        print(f'-')

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
                with open('ips.txt', 'a+') as i:
                    server = requests.get(f'https://api.mcstatus.io/v2/status/java/{ip}').json()
                    raw = server['ip_address']
                    players = f'{server['players']['online']}/{server['players']['max']}'
                    protected, protype = check_protection(ip)
                    if server['players']['online'] and raw not in i.read():
                        print(f'{c}[{w}+{c}] {w}Found Server! │ {c}IP:{w} {str(raw).ljust(15)} {w}│ {c}Players:{w} {str(players).ljust(9)} {w}│ {c}Protected?:{w} {'True ' if protected == True else 'False'} ({protype if protype != '' else raw})')
                        i.write(f'\n=============================================\nDomain: {ip}\nIP: {raw} | Players: {players} | {c}Protected?: {protected} ({protype if protype != '' else raw})')

            except: pass

if __name__ == '__main__':
    clean()
    os.system('cls')
    print(f'{w}raccoon scanner {c}v3')
    threads = []
    for i in range(30):
        t = threading.Thread(target=main)
        t.start()
        threads.append(t)