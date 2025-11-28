from multiprocessing import Process, Queue
import time

def worker(q): # process child
    for i in range(50):
        q.put(f"Mwsasge {i} from worker")
        time.sleep(1)
    
        
if __name__ == "__main__":
    q = Queue()
    
    p = Process(target=worker, args=(q,))
    p.start()
    
    while True: # process parent
        msg = q.get()
        if msg == "Mwsasge 13 from worker":
            print(msg)
            break
        print("Main received: ", msg)
        time.sleep(1)
        
    
    q.close()
    p.join()