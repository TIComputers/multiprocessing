from multiprocessing import Process, Value, Lock

def worker(counter, lock): # with -> (context manager)
    for i in range(100000):
        with lock:
            counter.value += 1

def worker1(counter, lock): # without with (without context manager)
    for i in range(100000):
        lock.acquire()
        counter.value += 1
        lock.release()

if __name__ == "__main__":
    counter = Value("i", 0)
    lock    = Lock()
    lock.acquire()
    
    x = 4
    for i in range(x):
        p = Process(target=worker, args=(counter, lock))
        p.start()
        
    for j in range(x):
        p.join()
        
    print("Final: ", counter.value)