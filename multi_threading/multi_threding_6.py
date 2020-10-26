from threading import Timer


def show():
    print('how you doing?')


t = Timer(10, show)
t.start()
