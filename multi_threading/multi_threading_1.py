from time import sleep, perf_counter
from threading import Thread

start = perf_counter()


def show(name):
    print(f'starting {name} ... ')
    sleep(3)
    print(f'finishing {name} ... ')


t1 = Thread(target=show, args=('one',))
t2 = Thread(target=show, args=('two',))

# start the threading proccess
t1.start()
t2.start()

# if we dont write this line program goes to continue the execution...we say wait and do this and then continue
t1.join()
t2.join()

end = perf_counter()
print(round(end - start))
