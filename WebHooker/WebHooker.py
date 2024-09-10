from colorama import Fore, init
import requests, json
init(True)

hookURL = input(f"{Fore.MAGENTA}[?] Webhook url? {Fore.YELLOW}")
try:
    hookInfo = requests.get(hookURL)
    hookJson = hookInfo.json()
except:
    quit(f"{Fore.RED}[!] Not a webhook")
try:
    if hookJson["message"] == "Unknown Webhook" or hookJson["message"] == "Invalid Webhook Token":
        exit(f"{Fore.RED}[!] Invalid Webhook")
except Exception as e:
    print(f"{Fore.GREEN}[!] Webook is valid")
hookTypes = {
    1 : "Normal",
    2 : "Channel Follower",
    3 : "Application"
}

print(f"""
{Fore.MAGENTA}--------WEBHOOK-INFO---------{Fore.RESET}
Name:         {Fore.GREEN}{hookJson['name']}{Fore.RESET}
ID:           {Fore.GREEN}{hookJson['id']}{Fore.RESET}
Avatar:       {Fore.GREEN}{hookJson['avatar']}{Fore.RESET}
Channel ID:   {Fore.GREEN}{hookJson['channel_id']}{Fore.RESET}
Server ID:    {Fore.GREEN}{hookJson['guild_id']}{Fore.RESET}
Webhook type: {Fore.GREEN}{hookTypes[hookJson['type']]}{Fore.RESET}
{Fore.MAGENTA}-----------------------------{Fore.RESET}
""")

scare = input(f"{Fore.MAGENTA}[?] (y/n) Fake Warning and delete? ")
if scare.lower() == "n":
    customAvatar = input(f"{Fore.MAGENTA}[?] (Leave blank for default) Avatar URL: ")
    customName = input(f"{Fore.MAGENTA}[?] (Leave blank for default) Custom name: ")
customAvatar = ''
customName = ''
Avatar = False
Name = False

if customAvatar != '':
    Avatar = True
if customName != '':
    Name = True

try:
    if scare.lower() == "y":
        data = {"content":"""
Hello,

Discord is focused on maintaining a safe and secure environment for our community, and this webhook was reported of illegal activities by one of its members.

This server is currently under investigation. Everyone in the server will receive a notice via email. If you do not respond to the email, your account will be terminated.

Your actions are in violation of our Community Guidelines and are issuing you this warning. If the behavior continues, we may take further action on this server, up to and including account and/or server termination.
             
Sincerely, Discord Trust & Safety Team
""","username":"Dіscord","avatar_url":"https://static.vecteezy.com/system/resources/previews/006/892/625/non_2x/discord-logo-icon-editorial-free-vector.jpg"}#cant use "Discord" as name, so I used an ascii look alike
        msg = requests.post(hookURL, json=data)
        if msg.status_code == 204:
            print(f"{Fore.GREEN}[+] Sent message, deleting webhook...")
            delete = requests.delete(hookURL)
            if delete.status_code == 204:
                print(f"{Fore.GREEN}[+] Gone!{Fore.RESET}")
            else:
                print(f"\n{Fore.RED}[!] ERROR!!\nCode:      {msg.status_code}\nError msg: {msg.text}{Fore.RESET}\n")
                exit()
        else:
            print(f"\n{Fore.RED}[!] ERROR!!\nCode:      {msg.status_code}\nError msg: {msg.text}{Fore.RESET}\n")
        exit()
    else:
        print(f"{Fore.YELLOW}[.] Ctrl + C to stop")
    while True:
        speech = input(f"{Fore.RESET}Message: {Fore.YELLOW}")

        if Name == True and Avatar == True:
            data = {"content":speech,"username":customName,"avatar_url":customAvatar}
        elif Name == False and Avatar == True:
            data = {"content":speech,"avatar_url":customAvatar}
        elif Name == True and Avatar == False:
            data = {"content":speech,"username":customName}
        elif Name == False and Avatar == False:
            data = {"content":speech}
        else:
            data = {"content":speech}

        msg = requests.post(hookURL, json=data)
        if msg.status_code == 204:
            print(f"{Fore.GREEN}Sent")
        else:
            print(f"\n{Fore.RED}[!] ERROR!!\nCode:      {msg.status_code}\nError msg: {msg.text}{Fore.RESET}\n")
            exit()
except KeyboardInterrupt:
    print(f"{Fore.RESET}\n\nBye Bye!")
    exit()
except Exception as e:
    print(f"\n{Fore.RED}[!] ERROR: {e}{Fore.RESET}\n")