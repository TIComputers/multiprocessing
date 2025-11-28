from multiprocessing import Process, Manager
import time


def worker(shared_list, x):
    for i in range(5):
        shared_list.append(f"Process[{x}]  step[{i}]")
        time.sleep(0.5)
        
if __name__ == "__main__":
    manger = Manager()
    shared_list = manger.list()
    
    Processes = []
    for i in range(3):
        p = Process(target=worker, args=(shared_list, i))
        p.start()
        Processes.append(p)
    
    print(Processes)
    for i in Processes:
        p.join()
        
    print("Shared_list:", shared_list)
    