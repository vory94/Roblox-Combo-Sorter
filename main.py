import os
import requests
from colorama import Fore, Style, init

init(autoreset=True)

SEND_TO_WEBHOOK = True  # Set to False to disable sending
WEBHOOK_URL = ""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("╔═════════════════════════════════════════════════════╗")
    print("║             🔷 Roblox Combo Sorter 🔷               ║")
    print("║                    Made by vory94                  ║")
    print("╚═════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)

def send_file_to_discord():
    if not SEND_TO_WEBHOOK:
        return

    if not WEBHOOK_URL or "your_webhook_here" in WEBHOOK_URL:
        print(f"{Fore.RED}❌ Webhook URL not set. Skipping webhook.")
        return

    if not os.path.exists("output.txt"):
        print(f"{Fore.RED}❌ No output.txt file to send.")
        return

    try:
        with open("output.txt", "rb") as file:
            files = {"file": ("output.txt", file)}
            response = requests.post(WEBHOOK_URL, files=files)

        if response.status_code in (200, 204):
            print(f"{Fore.GREEN}✅ Output file successfully sent to Discord webhook.")
        else:
            print(f"{Fore.RED}❌ Failed to send file. Status: {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}❌ Webhook Error: {e}")

# Main logic
def main():
    clear_screen()
    print_banner()

    print(f"{Fore.CYAN}{Style.BRIGHT}Select an extraction option:\n")
    print(f"{Fore.YELLOW}[1]{Fore.WHITE} Extract {Fore.CYAN}user:pass")
    print(f"{Fore.YELLOW}[2]{Fore.WHITE} Extract {Fore.CYAN}user only")
    print(f"{Fore.YELLOW}[3]{Fore.WHITE} Extract {Fore.CYAN}pass only")
    print(f"{Fore.YELLOW}[4]{Fore.WHITE} Extract {Fore.CYAN}cookie only\n")

    option = input(f"{Fore.CYAN}Enter your choice (1/2/3/4): {Fore.WHITE}")

    if option not in ["1", "2", "3", "4"]:
        print(f"{Fore.RED}❌ Invalid option selected. Exiting.")
        return

    try:
        with open("input.txt", "r", encoding="utf-8") as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Error: 'input.txt' not found in the current directory.")
        return

    output_lines = []
    skipped_lines = []

    for line in lines:
        line = line.strip()
        parts = line.split(":", 2)
        if len(parts) == 3:
            user, passwd, cookie = parts
            if option == "1":
                output_lines.append(f"{user}:{passwd}")
            elif option == "2":
                output_lines.append(user)
            elif option == "3":
                output_lines.append(passwd)
            elif option == "4":
                output_lines.append(cookie)
        else:
            print(f"{Fore.YELLOW}⚠️ Skipped invalid line: {line}")
            skipped_lines.append(line)

    if output_lines:
        with open("output.txt", "w", encoding="utf-8") as outfile:
            outfile.write("\n".join(output_lines))
        print(f"\n{Fore.GREEN}✅ Output successfully written to 'output.txt'.")
    else:
        print(f"\n{Fore.RED}❌ No valid combos found to write.")

    if skipped_lines:
        with open("skipped.txt", "w", encoding="utf-8") as skipped_file:
            skipped_file.write("\n".join(skipped_lines))
        print(f"{Fore.YELLOW}⚠️ {len(skipped_lines)} invalid lines written to 'skipped.txt'.")

    send_file_to_discord()

    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}🔷 Process complete — Roblox Combo Sorter by vory94 🔷\n")

if __name__ == "__main__":
    main()
