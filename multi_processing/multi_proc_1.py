import multiprocessing
import time

start = time.perf_counter()

def do_something():
    print('sleeping 1 second...')
    time.sleep(1)
    print('done sleeping...')
    

p1 = multiprocessing.Process(target=do_something)
p2 = multiprocessing.Process(target=do_something)

p1.start()
p2.start()

p1.join()
p2.join()

finish = time.perf_counter()

print(f'finished in {round(finish-start , 2)}')