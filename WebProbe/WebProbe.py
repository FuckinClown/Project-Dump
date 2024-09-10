import argparse, threading
import Utils.threads as tds
import Utils.color as c

parser = argparse.ArgumentParser(description='Website Info')
parser.add_argument('--domain', dest='domain', type=str, help='Main website your tring to search')
parser.add_argument('--threads', dest='threads', type=int, help='Amount of threads to use (Default: 25)', default=25)
parser.add_argument('--period', dest='period', type=float, help='Time in between sending the requests so you dont get limited (Default: 0.35)', default=0.35)

args = parser.parse_args()
if args.threads == None or args.domain == None:
    print(f"{c.red}Missing arguments, please use {c.green}--help")
    exit(1)
print(f"{c.main}Starting search on: {c.data}{args.domain}{c.res}")
print(f"{c.main}With {c.data}{args.threads}{c.main} threads{c.res}")
print(f"{c.main}And waiting {c.data}{args.threads}{c.main} seconds between each request{c.res}")
print(f"{c.main}-"*25)

admin = open("data/All.txt").readlines()

try:
    for line in admin:
        tds.Cache_Threads(args.domain, line, args.threads)
    tds.Start(args.threads, args.period)
except Exception as ex:
    print(f"{c.red}Program has beem interupted: {ex}")
    exit(0)