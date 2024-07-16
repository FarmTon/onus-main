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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Newbie Airdrop {white}Onus Auto Claimer
        https://t.me/NewbieAirdropTool

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
    # Clear the terminal
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

        return response

    def get_balance(self, data):
        url = "https://bot-game.goonus.io/api/v1/points"

        headers = self.headers.copy()

        payload = json.dumps({"initData": f"{data}"})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def start_click(self, data, click_num):
        url = "https://bot-game.goonus.io/api/v1/claimClick"

        headers = self.headers.copy()

        payload = json.dumps({"initData": f"{data}", "click": click_num})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def start_farm(self, data):
        url = "https://bot-game.goonus.io/api/v1/startFarm"

        headers = self.headers.copy()

        payload = json.dumps({"initData": f"{data}"})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def claim_farm(self, data):
        url = "https://bot-game.goonus.io/api/v1/claimFarm"

        headers = self.headers.copy()

        payload = json.dumps({"initData": f"{data}"})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Get info and tap
                try:
                    self.log(f"{yellow}Getting user info...")
                    user_info = self.user_info(data=data).json()
                    user_name = user_info["firstName"]
                    click_left = user_info["clickNumberLeft"]
                    get_balance = self.get_balance(data=data).json()
                    balance_click = get_balance[0]["amount"]
                    balance_farm = get_balance[1]["amount"]
                    self.log(f"{green}User name: {white}{user_name}")
                    self.log(
                        f"{green}Total Balance: {white}{balance_click + balance_farm} (Click: {balance_click} - Farm: {balance_farm})"
                    )
                    while True:
                        if click_left > 0:
                            self.log(f"{yellow}Trying to tap...")
                            start_click = self.start_click(
                                data=data, click_num=click_left
                            ).json()
                            click_left = start_click["clickNumberLeft"]
                            get_balance = self.get_balance(data=data).json()
                            balance_click = get_balance[0]["amount"]
                            balance_farm = get_balance[1]["amount"]
                            self.log(
                                f"{green}Current Balance: {white}{balance_click + balance_farm} (Click: {balance_click} - Farm: {balance_farm})"
                            )
                        else:
                            self.log(f"{yellow}No tap available!")
                            break
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

                # Farming
                try:
                    self.log(f"{yellow}Trying to claim and farm...")
                    while True:
                        start_farm = self.start_farm(data=data).json()
                        if start_farm["success"]:
                            self.log(f"{green}Farm successful!")
                            break
                        else:
                            self.log(f"{yellow}Checking to claim...")
                            claim_farm = self.claim_farm(data=data).json()
                            if claim_farm["success"]:
                                self.log(f"{green}Claim successful!")
                            else:
                                self.log(f"{yellow}Not time to claim now!")
                                break
                except Exception as e:
                    self.log(f"{red}Farm error!!!")

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
