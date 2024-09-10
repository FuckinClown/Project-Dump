import requests, string
from colorama import init, Fore
init(True)

available = []
for one in string.ascii_uppercase:
    for two in string.ascii_uppercase:
        platename = one + two
        plate_url = f"https://bmvonline.dps.ohio.gov/bmvonline/oplates/PlatePreview?plateNumber={platename}&vehicleClass=PC&organizationCode=0"
        content = requests.get(plate_url).content.decode()
        if "Please fix the following errors" in content:
            print(f"{Fore.RED}{platename}")
        else:
            print(f"{Fore.GREEN}{platename}")
            available.append(platename+"\n")

open("available.txt","w").write(available)