import requests, time, random, os, threading, re
from colorama import Fore

def TestToken(token : str):
    header={"Authorization" : token}
    User = requests.get("https://discord.com/api/v9/users/@me", headers=header, proxies={"http":Proxy()})
    if User.status_code == 401:
        print("Invalid Token")
        return False
    else:
        return True

def proxy_scrape(): 
    proxieslog = []
    #start timer
    startTime = time.time()
    #create temp dir
    temp = os.getenv("temp")+"\\Sproxies"
    print(f"{Fore.MAGENTA}No Proxies found, please wait...{Fore.RESET}")

    def fetchProxies(url, custom_regex):
        global proxylist
        try:
            proxylist = requests.get(url, timeout=5).text
        except Exception:
            pass
        finally:
            proxylist = proxylist.replace('null', '')
        #get the proxies from all the sites with the custom regex
        custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
        custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
        for proxy in re.findall(re.compile(custom_regex), proxylist):
            proxieslog.append(f"{proxy[0]}:{proxy[1]}")

    #all urls
    proxysources = [
        ["http://spys.me/proxy.txt","%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
        ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", '%ip%", "type": "http", "port": %port%'],
        ["https://www.us-proxy.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://free-proxy-list.net/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",']
    ]
    threads = [] 
    for url in proxysources:
        #send them out in threads
        t = threading.Thread(target=fetchProxies, args=(url[0], url[1]))
        threads.append(t)
    for t in threads:
        t.start()
        t.join()
    print("Got proxies, writing them to file")
    proxies = list(set(proxieslog))
    with open(temp, "w") as f:
        for proxy in proxies:
            #create the same proxy 7-10 times to avoid ratelimit when using other options
            for i in range(random.randint(7, 10)):
                print("Writing proxy")
                f.write(f"{proxy}\n")
                print("Wrote proxy")
    #get the time it took to scrape
    execution_time = (time.time() - startTime)
    print(f"{Fore.GREEN}Done! {Fore.MAGENTA}Scraped{len(proxies): >5}{Fore.GREEN} in total => {Fore.RED}{temp}{Fore.RESET} | {execution_time}ms")

def Proxy():#Writen by: Rdimo (Hazard Nuker)
    temp = os.getenv("temp")+"\\Sproxies"
    #if the file size is empty
    if os.stat(temp).st_size == 0:
        proxy_scrape()
    proxies = open(temp).read().split('\n')
    proxy = proxies[0]

    with open(temp, 'r+') as fp:
        #read all lines
        lines = fp.readlines()
        #get the first line
        fp.seek(0)
        #remove the proxy
        fp.truncate()
        fp.writelines(lines[1:])
    return proxy

def GetMembers(guildID, token):
    #time.sleep(1)
    rolesReq = requests.get(f"https://discord.com/api/v9/guilds/{guildID}/roles", headers={"Authorization" : token}, proxies={"http":Proxy()})
    RolesJson = rolesReq.json()
    listlist = []
    for obj in RolesJson:
        if obj['name'] == "@everyone":
            continue
        membersReq = requests.get(f"https://discord.com/api/v9/guilds/{guildID}/roles/{obj['id']}/member-ids", headers={"Authorization" : token}, proxies={"http":Proxy()})
        listlist.append(len(membersReq.json()))
        #time.sleep(2)
    if len(listlist) != 0:
        return max(listlist)
    else:
        return f"{Fore.RED}No Roles, Guessing:{Fore.YELLOW} 1{Fore.RESET}"#sorry, but I cant tell if there are no roles
                                                                          # Future me, I def could but didnt want to