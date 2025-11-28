from multiprocessing import Process, Value

# ===================================
# Value and Array have builtin lock
# ===================================

def worker(counter): 
    for i in range(100000):
        with counter.get_lock(): # lock builtin
            counter.value += 1


if __name__ == "__main__":
    counter = Value("i", 0)
    
    x = 4
    for _ in range(x):
        p = Process(target=worker, args=(counter,))
        p.start()
        
    for i in range(x):
        p.join()
        
    print("Final: ", counter.value)