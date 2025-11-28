from multiprocessing import Pool, Manager
import time


def worker(x, shared_list):
    for i in range(3):
        shared_list.append(f"process[{x}], step[{i}]")
        time.sleep(0.5)
    return x*x


if __name__ == "__main__":
    shared_list = Manager().list()
    
    with Pool(processes=4) as pool:
        results = pool.starmap(worker, [[i, shared_list] for i in range(4)])
        
    print("Results:", results)
    print("Shared_List:", shared_list)        