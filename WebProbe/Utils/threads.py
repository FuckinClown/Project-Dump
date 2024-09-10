import requests, threading
import Utils.color as c
import Utils.Agents as Agt
import time

total_Threads:list[threading.Thread] = []
active_Threads:list[threading.Thread] = []

KEYBOARD_STOP = False
global Period

def Thread_Func(Domain:str, ext:str):
    if KEYBOARD_STOP ==False:
        url = (Domain+ext).replace("\n", "")
        rq = requests.get(url, headers={'User-Agent':Agt.UserAgent()})
        if rq.status_code == 200:
            print(f"{c.data}{Domain} {c.green}[{rq.status_code}] {c.green}/{ext}")
        else:
            print(f"{c.data}{Domain} {c.red}[{rq.status_code}] {c.data}/{ext}")

    
def Cache_Threads(Domain:str, ext:str, max_threads:int):
    thrd = threading.Thread(target=Thread_Func, args=(Domain, ext))
    total_Threads.append(thrd)

def wait_until(max_threads, timeout, period=0.25):
  mustend = time.time() + timeout
  while time.time() < mustend:
    if active_Threads.__len__()<max_threads: return True
    ClearDead()
    time.sleep(period)
  return False

def Start(max_threads:int, waitTime:float):
    try:
        for thread in total_Threads:
            if active_Threads.__len__() < max_threads:
                time.sleep(waitTime)
                thread.start()
                active_Threads.append(thread)
            else:
                wait_until(max_threads, 2)#Waiting for a new thread to open up
                time.sleep(waitTime)
                thread.start()
                active_Threads.append(thread)
                

    except KeyboardInterrupt:
        global KEYBOARD_STOP
        KEYBOARD_STOP = True
        print(f"{c.red}Program has beem interupted:{c.yellow} User Input\n{c.main}Waiting for threads to stop...")

def ClearDead():
    for deadThread in active_Threads:
        if not deadThread.is_alive():
            active_Threads.remove(deadThread)