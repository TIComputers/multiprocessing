from multiprocessing import Process, Value
import time

def gtime(func):
    def wraper():  
        t1 = time.time()
        func()
        t2 = time.time()
        print(f"Time: {t2 - t1:.2f} sec")
    return wraper

def worker(counter):
    for _ in range(100000):
        counter.value += 1
        print(f"\r",counter.value, end="")

@gtime
def excute():
    counter = Value("i", 0)
    x = 4
    for _ in range(x):
        p = Process(target=worker, args=(counter,))
        p.start()
        
    for j in range(x):
        p.join()
            
    print("\rFinal value:", counter.value)


if __name__ == "__main__":
    excute()