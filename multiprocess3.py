from multiprocessing import Process, Queue
import time


def worker(commands):
    while True:
        cmd = commands.get()
        if cmd == "STOP":
            print("worker stopping...")
            break
        print("worker received:", cmd)
        
    
if __name__ == "__main__":
    q = Queue()
    p = Process(target=worker, args=(q,))
    p.start()
    
    q.put("Hello")
    q.put("Run step 2")
    time.sleep(1)
    q.put("sadegh working...")
    q.put("STOP")
    
    p.join()
        
        