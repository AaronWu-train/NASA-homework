import signal

def alarm(second):
    def handler(signum, frame):
        print('\nHello...? Anyone there? Gotta leave!')
        exit()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(second)
