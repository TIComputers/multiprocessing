from multiprocessing import Process, Queue
import time

def long_task(q):
    for i in range(1, 6):
        q.put(f"Step {i}/5 running...")
        time.sleep(1)
        
    q.put("DONE")
    
    

if __name__ == "__main__":
    q = Queue()
    
    p = Process(target=long_task, args=(q,))
    p.start()
    
    while True:
        msg = q.get()
        print(msg)
        
        if msg == "DONE":
            break
        
    p.join()
    p.close()