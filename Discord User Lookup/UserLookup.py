import requests, argparse, os, json
from colorama import Fore, init; init(autoreset=True)
q = f"{Fore.LIGHTMAGENTA_EX}[?] " # question
e = f"{Fore.RED}[!] "             # error
v = f"{Fore.LIGHTBLACK_EX}[*] "   # verbose
m = f"{Fore.YELLOW}[.] "          # main

parser = argparse.ArgumentParser()
parser.add_argument("userID", help="The userid to search")
parser.add_argument("-v", "--verbose", required=False, action="store_true", help="Shows everything thats happening behind the scenes")
args = parser.parse_args()

def verbose(msg):
    if args.verbose:
        print(v+msg)

def checkToken(token):
    if token == "":
        exit(f"{e}No token found in token.txt!")
    headers = {"authorization": token}
    info = requests.get("https://canary.discord.com/api/v9/users/@me", headers=headers)
    return info.status_code == 200

os.system('cls' if os.name == 'nt' else 'clear')
verbose("Reading token.txt")
TOKEN = ""
if os.path.exists("token.txt"):
    token = open("token.txt", "r").read()
    if checkToken(token):
        verbose("Token is valid")
        TOKEN = token
    else:
        exit(f"{e}Invalid token in token.txt!")
else:
    open("token.txt", "w").close()
    exit(f"{e}Please provide a token to token.txt!")

verbose(f"Sending get user request...")

headers = {"authorization": token}
info = requests.get(f"https://canary.discord.com/api/v9/users/{args.userID}", headers=headers)
infoJson = info.json()
#print(json.dumps(infoJson, indent=4))

try:
    if infoJson['message'] == "Unknown User":
        exit(f"{e}Unkown user")
except:
    verbose(f"{Fore.GREEN}Valid User!{Fore.LIGHTBLACK_EX} Dumping info...")
    pass # Valid user, move on

clanJson = ''
if infoJson["clan"]:
    verbose("They are in a clan, getting info...")
    clan = requests.get(f"https://discord.com/api/v9/discovery/{infoJson['clan']['identity_guild_id']}/clan", headers=headers)
    clanJson = clan.json()
    #exit(json.dumps(clanJson, indent=4))

pfpURL = f"https://cdn.discordapp.com/avatars/{args.userID}/{infoJson['avatar']}.webp"
bnrURL = f"https://cdn.discordapp.com/banners/{args.userID}/{infoJson['banner']}.png"
print(f"""
{Fore.YELLOW}╔═════╦═════════{Fore.LIGHTMAGENTA_EX}INFO{Fore.YELLOW}═══════════╦═════╗
{Fore.YELLOW}║{Fore.MAGENTA}┌{Fore.WHITE} User:  {Fore.LIGHTBLUE_EX}{infoJson['username']}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Nickname:  {Fore.LIGHTBLUE_EX}{infoJson['global_name']}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Profile Picture: 
{Fore.YELLOW}║{Fore.MAGENTA}╞═{Fore.LIGHTBLUE_EX} {pfpURL}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Banner: 
{Fore.YELLOW}║{Fore.MAGENTA}╞═{Fore.LIGHTBLUE_EX} {bnrURL}""")

if infoJson['avatar_decoration_data']:
    DecoURL = f"https://cdn.discordapp.com/avatar-decoration-presets/{infoJson['avatar_decoration_data']['asset']}.png"
    print(f"{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Decoration:\n{Fore.YELLOW}║{Fore.MAGENTA}╞{Fore.LIGHTBLUE_EX} {DecoURL}")

if infoJson["clan"]:
    clanURL = f"https://cdn.discordapp.com/clan-badges/{infoJson['clan']['identity_guild_id']}/{infoJson['clan']['badge']}.png"
    iconURL = f"https://cdn.discordapp.com/icons/{clanJson['id']}/{clanJson['icon_hash']}.webp"

    print(f"""{Fore.YELLOW}╠═════╦═════════{Fore.LIGHTMAGENTA_EX}CLAN{Fore.YELLOW}═══════════╦═════╗
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Clan Tag: {Fore.LIGHTBLUE_EX}{infoJson['clan']['tag']}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Guild ID: {Fore.LIGHTBLUE_EX}{infoJson['clan']['identity_guild_id']}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Server Name: {Fore.LIGHTBLUE_EX}{clanJson['name']}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Members: {Fore.LIGHTBLUE_EX}{clanJson['member_count']}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Description: {Fore.LIGHTBLUE_EX}{clanJson['description'].strip("\n")}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Search Terms: {Fore.LIGHTBLUE_EX}{', '.join(clanJson['search_terms'])}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Descriptors: {Fore.LIGHTBLUE_EX}{', '.join(clanJson['wildcard_descriptors'])}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Badge Icon: 
{Fore.YELLOW}║{Fore.MAGENTA}╞═{Fore.LIGHTBLUE_EX} {clanURL}
{Fore.YELLOW}║{Fore.MAGENTA}├{Fore.WHITE} Server Icon: 
{Fore.YELLOW}║{Fore.MAGENTA}╞═{Fore.LIGHTBLUE_EX} {iconURL}""")

print(f"{Fore.YELLOW}╚══════╩═══════════════════════╩══════╝")