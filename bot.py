import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import json

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")

class ONUS:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Origin": "https://onx.goonus.io",
            "Referer": "https://onx.goonus.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
        }

        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Lagged {white}ASF BRO
        https://t.me/SancPelocho

        """

    def countdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            hrs, mins = divmod(mins, 60)
            print(
                f"{white}Time left: {hrs:02d}:{mins:02d}:{secs:02d} ",
                flush=True,
                end="\r",
            )
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def user_info(self, data):
        url = "https://bot-game.goonus.io/api/v1/me"
        headers = self.headers.copy()
        payload = json.dumps({"initData": f"{data}"})
        response = requests.post(url=url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()

    def get_balance(self, data):
        url = "https://bot-game.goonus.io/api/v1/points"
        headers = self.headers.copy()
        payload = json.dumps({"initData": f"{data}"})
        response = requests.post(url=url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()

    def start_click(self, data, click_num, max_clicks_per_request=100):
        url = "https://bot-game.goonus.io/api/v1/claimClick"
        headers = self.headers.copy()
        total_clicks_done = 0

        while click_num > 0:
            clicks_to_send = min(click_num, max_clicks_per_request)
            payload = json.dumps({"initData": f"{data}", "click": clicks_to_send})
            response = requests.post(url=url, headers=headers, data=payload)
            response.raise_for_status()
            response_json = response.json()
            total_clicks_done += clicks_to_send
            click_num = response_json.get("clickNumberLeft", 0)

            if click_num == 0 or not response_json.get("success", False):
                break

            time.sleep(1)  # Adding a small delay to prevent overwhelming the server

        return response_json

    def start_farm(self, data):
        url = "https://bot-game.goonus.io/api/v1/startFarm"
        headers = self.headers.copy()
        payload = json.dumps({"initData": f"{data}"})
        response = requests.post(url=url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()

    def claim_farm(self, data):
        url = "https://bot-game.goonus.io/api/v1/claimFarm"
        headers = self.headers.copy()
        payload = json.dumps({"initData": f"{data}"})
        response = requests.post(url=url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        while True:  # Outer loop for infinite iteration
            self.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Number of accounts: {white}{num_acc}")
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                try:
                    self.log(f"{yellow}Getting user info...")
                    user_info = self.user_info(data=data)
                    user_name = user_info.get("firstName", "Unknown")
                    click_left = user_info.get("clickNumberLeft", 0)
                    get_balance = self.get_balance(data=data)

                    # Ensure we have at least two balances to avoid index errors
                    balance_click = get_balance[0].get("amount", 0) if len(get_balance) > 0 else 0
                    balance_farm = get_balance[1].get("amount", 0) if len(get_balance) > 1 else 0
                    
                    self.log(f"{green}User name: {white}{user_name}")
                    self.log(
                        f"{green}Total Balance: {white}{balance_click + balance_farm} (Click: {balance_click} - Farm: {balance_farm})"
                    )
                    while True:
                        if click_left > 0:
                            self.log(f"{yellow}Trying to tap...")
                            start_click = self.start_click(data=data, click_num=click_left)
                            click_left = start_click.get("clickNumberLeft", 0)
                            get_balance = self.get_balance(data=data)
                            balance_click = get_balance[0].get("amount", 0) if len(get_balance) > 0 else 0
                            balance_farm = get_balance[1].get("amount", 0) if len(get_balance) > 1 else 0
                            self.log(
                                f"{green}Current Balance: {white}{balance_click + balance_farm} (Click: {balance_click} - Farm: {balance_farm})"
                            )
                        else:
                            self.log(f"{yellow}No tap available!")
                            break
                except requests.exceptions.HTTPError as http_err:
                    self.log(f"{red}HTTP error occurred: {http_err}")
                except requests.exceptions.ConnectionError as conn_err:
                    self.log(f"{red}Connection error occurred: {conn_err}")
                except requests.exceptions.Timeout as timeout_err:
                    self.log(f"{red}Timeout error occurred: {timeout_err}")
                except requests.exceptions.RequestException as req_err:
                    self.log(f"{red}Request error occurred: {req_err}")
                except Exception as e:
                    self.log(f"{red}Get user info error: {e}")

                try:
                    self.log(f"{yellow}Trying to claim and farm...")
                    while True:
                        start_farm = self.start_farm(data=data)
                        if start_farm.get("success"):
                            self.log(f"{green}Farm successful!")
                            break
                        else:
                            self.log(f"{yellow}Checking to claim...")
                            claim_farm = self.claim_farm(data=data)
                            if claim_farm.get("success"):
                                self.log(f"{green}Claim successful!")
                            else:
                                self.log(f"{yellow}Not time to claim now!")
                                break
                except requests.exceptions.HTTPError as http_err:
                    self.log(f"{red}HTTP error occurred: {http_err}")
                except requests.exceptions.ConnectionError as conn_err:
                    self.log(f"{red}Connection error occurred: {conn_err}")
                except requests.exceptions.Timeout as timeout_err:
                    self.log(f"{red}Timeout error occurred: {timeout_err}")
                except requests.exceptions.RequestException as req_err:
                    self.log(f"{red}Request error occurred: {req_err}")
                except Exception as e:
                    self.log(f"{red}Farm error: {e}")

            print()
            wait_time = 30 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            self.countdown(wait_time)

if __name__ == "__main__":
    try:
        onus = ONUS()
        onus.main()
    except KeyboardInterrupt:
        sys.exit()
