from threading import Thread , Semaphore , current_thread, BoundedSemaphore
from time import sleep

num = 0
# lock = Semaphore(value=2)
lock = BoundedSemaphore(value=2)

def add():
    global num
    # with lock:
    lock.acquire()
    print(current_thread().getName())
    sleep(2)
    for _ in range(100000):
        num += 1
    # lock.release() # if we create release two time we could use BoundedSemphore
    lock.release()

t1 = Thread(target=add)
t2 = Thread(target=add)
t3 = Thread(target=add)
t4 = Thread(target=add)
t5 = Thread(target=add)
t6 = Thread(target=add)
t7 = Thread(target=add)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()


t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()


print(num)
print('done...')