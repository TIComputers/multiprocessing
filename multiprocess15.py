from multiprocessing import Process, Queue
from time import sleep
import random

def worker(id, q):
    for i in range(5):
        msg = f"Worker[{id}] -> message[{i}]"
        q.put(msg)
        sleep(random.uniform(0.2, 1.0))
    
    q.put(f"Worker[{id}] -> DONE")
        
        
if __name__ == "__main__":
    
    q = Queue()
    workers = []
    
    for wid in range(3):
        p = Process(target=worker, args=(wid, q))
        p.start()
        workers.append(p)
        
    finished = 0
    while finished < 3:
        try:
            msg = q.get(timeout=0.5)
            print("Parent Received: ", msg)
            
            if "DONE" in msg:
                finished += 1
        except:
            pass
        
    for p in workers:
        p.join()
    
    print("All wokers finished.")