import os
import requests
from colorama import init, Fore
import utils
import time
os.system("cls")

if not os.path.exists(os.getenv("temp")+"\\Sproxies"):
    open(os.getenv("temp")+"\\Sproxies", "w").close()
    utils.proxy_scrape()

token = input("Token: ")
header={"Authorization" : token}
utils.TestToken(token)

guildsReq = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=header, proxies={"http":utils.Proxy()})
guildsJson = guildsReq.json()
relationsReq = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=header, proxies={"http":utils.Proxy()})
relationJson = relationsReq.json()

relationTypes = {
    1 : 'Friend',
    2 : 'Blocked',
    3 : 'Incoming friend request',
    4 : 'Outgoing friend request'
}

os.system("cls")
User = requests.get("https://discord.com/api/v9/users/@me", headers=header, proxies={"http":utils.Proxy()})
UserJson = User.json()
print(f"{Fore.MAGENTA}|--------------{Fore.GREEN}User{Fore.MAGENTA}--------------{Fore.RESET}")
print(f"{Fore.MAGENTA}|Username:     {Fore.YELLOW}{UserJson['username']}{Fore.RESET}")
print(f"{Fore.MAGENTA}|Display Name: {Fore.YELLOW}{UserJson['global_name']}{Fore.RESET}")
print(f"{Fore.MAGENTA}|ID:           {Fore.YELLOW}{UserJson['id']}{Fore.RESET}")
print(f"{Fore.MAGENTA}|Email:        {Fore.YELLOW}{UserJson['email']}{Fore.RESET}")
print(f"{Fore.MAGENTA}|Phone:        {Fore.YELLOW}{UserJson['phone']}{Fore.RESET}")
print(f"{Fore.MAGENTA}|Likes NSFW:   {Fore.YELLOW}{UserJson['nsfw_allowed']}{Fore.RESET}")
print(f"{Fore.MAGENTA}|BIO:\n{Fore.YELLOW}{UserJson['bio']}{Fore.RESET}")
print(f"{Fore.MAGENTA}|-------------{Fore.GREEN}Friends{Fore.MAGENTA}-------------{Fore.RESET}")
for user in relationJson:
    print(f"{Fore.MAGENTA}|Username: {Fore.YELLOW}{user['user']['username']} {Fore.MAGENTA}| Status: {Fore.YELLOW}{relationTypes[user['type']]}{Fore.RESET}")
print(f"{Fore.MAGENTA}|---------------------------------{Fore.RESET}")

print(f"\n{Fore.LIGHTRED_EX}    Checking servers and members...\n    This Could take a minute{Fore.RESET}\n")
time.sleep(1)
print(f"{Fore.MAGENTA}|-----------{Fore.GREEN}Owns Sever(s){Fore.MAGENTA}-----------{Fore.RESET}")
for obj in guildsJson:
    if obj['owner'] == True:
        print(f"{Fore.MAGENTA}|   Name:    {Fore.YELLOW}{obj['name']}{Fore.RESET}")
        MemberAmnt = utils.GetMembers(obj['id'], token)
        print(f"{Fore.MAGENTA}|   Member Count: {Fore.YELLOW}{MemberAmnt}{Fore.RESET}")
print(f"{Fore.MAGENTA}|----------------------------------{Fore.RESET}")