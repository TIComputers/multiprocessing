from multiprocessing import Process
import time

def counter(num):
    count = 0
    while count < num:
        count += 1
        
def main():
    t1 = time.time()
    a = Process(target=counter, args=(1000000000,))
    b = Process(target=counter, args=(1000000000,))
    
    a.start()
    b.start()
    
    a.join()
    b.join()
    
    t2 = time.time()
    
    print(f"finished in: {t2-t1:.2f} seconds")
    
def main0():
    t1 = time.time()
    
    a = counter(1000000000)
    b = counter(1000000000)
    
    t2 = time.time()
    
    print(f"finished in: {t2-t1:.2f} seconds")
    

if __name__ == "__main__":
    a = Process(target=main)
    b = Process(target=main0)
    
    b.start()
    a.start()
    
    b.join()
    a.join()





































