import threading
import time

status_lock = threading.Lock()
print_lock = threading.Lock()
isLooping = True


def background_job():
    while isLooping:
        with print_lock:
           print("still looping: " + str(isLooping))
           print(threading.current_thread().name)
        time.sleep(1)


for x in range(3):
    t = threading.Thread(target=background_job)
    t.daemon = True
    t.start()

while True:
    doLoop = input("1: stop, else cont")

    if int(doLoop) == 1:
        print("1 entered")
        isLooping = False







