import multiprocessing
import time

start = time.perf_counter()

def do_something():
    print('sleeping 1 second...')
    time.sleep(1)
    print('done sleeping...')
    

processes = []

for _ in range(10):
    p = multiprocessing.Process(target=do_something)
    p.start()
    processes.append(p)

for process in processes:
    process.join()


finish = time.perf_counter()

print(f'finished in {round(finish-start , 2)}')