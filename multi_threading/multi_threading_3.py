from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep


def show(name):
    print(f'starting {name} ... ')
    sleep(3)
    print(f'finishing {name} ... ')


with ThreadPoolExecutor(max_workers=2) as executer: # there is parenthesis
    names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']
    executer.map(show, names)

print('done...')