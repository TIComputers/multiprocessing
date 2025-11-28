from multiprocessing import Pool
import time

def worker(x):
    for i in range(x):
        print(f"\rprocess[{x}]: loop[{i}]")
 
def gtime(func):
    def wraper():  
        t1 = time.time()
        func()
        t2 = time.time()
        print(f"Time: {t2 - t1:.2f}")
    return wraper

@gtime        
def excute():
    with Pool(processes=8) as pool: 
        pool.map(worker, range(16))    

    


if __name__ == "__main__":
    excute()
    