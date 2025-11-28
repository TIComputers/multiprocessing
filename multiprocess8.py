from multiprocessing import Process, Array
import time

def worker(shared_arr):
    for i in range(len(shared_arr)):
        with shared_arr.get_lock():
            shared_arr[i] += 1


if __name__ == "__main__":
    arr = Array("i", [i for i in range(5)])
    
    p1 = Process(target=worker, args=(arr,))
    p2 = Process(target=worker, args=(arr,))
    p3 = Process(target=worker, args=(arr,))
    
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()
    
    print("Final array: ", list(arr))