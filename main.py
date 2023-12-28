import requests
import time
import concurrent.futures
import os
import uuid
import ctypes
from random import choice
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class Counter:
    count = 0

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(message, color_code):
    print(f"{color_code}{message}\x1b[0m")

class PromoGenerator:
    def __init__(self, proxy=None):
        self.proxy = {'http': proxy, 'https': proxy} if proxy else None
        self.session = self.create_session()

    def create_session(self):
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session


    def generate_promo(self):
        url = "https://api.discord.gx.games/v1/direct-fulfillment"
        headers = {
            "Content-Type": "application/json",
            "Sec-Ch-Ua": '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
        }

        data = {"partnerUserId": str(uuid.uuid4())}

        try:
            response = self.session.post(url, json=data, headers=headers, proxies=self.proxy, timeout=5)

            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    self.print_promo_generated(token)
            elif response.status_code == 429:
                print_colored("You Are Being Rate-limited!", '\x1b[33m')  # Yellow color
            else:
                print_colored(f"Request failed : {response.status_code}", '\x1b[31m')  # Red color
        except Exception as e:
            print_colored(f"Request Failed : {e}", '\x1b[31m')  # Red color

    def print_promo_generated(self, token):
        Counter.count += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f"Nitro-gxGEN By Keniolez | Generated : {Counter.count}")
        link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
        with open("promos.txt", "a") as f:
            f.write(f"{link}\n")
        print_colored(f"Generated Promo Link : {link}", '\x1b[32m')  # Green color

class PromoManager:
    def __init__(self):
        self.num_threads = int(input(f"Enter Number Of Threads : "))
        with open("proxies.txt") as f:
            self.proxies = f.read().splitlines()

    def start_gen(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = {executor.submit(self.generate_promo): i for i in range(self.num_threads)}
            try:
                concurrent.futures.wait(futures)
            except KeyboardInterrupt:
                for future in concurrent.futures.as_completed(futures):
                    future.result()

    def generate_promo(self):
        proxy = choice(self.proxies) if self.proxies else None
        generator = PromoGenerator(proxy)
        while True:
            generator.generate_promo()

if __name__ == "__main__":
    manager = PromoManager()
    manager.start_gen()