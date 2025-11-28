from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process, Lock
import struct
import time
import random

buffer_size = 10
n_items     = 20


def producer(shm_name, head_index, lock):
    shm = SharedMemory(name=shm_name)
    buf = shm.buf
    
    for i in range(n_items):
        with lock:
            struct.pack_into("i", buf, head_index[0]*4, i)
            print(f"Produced: {i} at {head_index[0]}")
            head_index[0] = (head_index[0] + 1) % buffer_size
    shm.close()


def consumer(shm_name, tail_index, lock):
    shm = SharedMemory(name=shm_name)
    buf = shm.buf
    for i in range(n_items):
        with lock:
            value = struct.unpack_from("i", buf, tail_index[0]*4)[0]
            print(f"consumed: {value} from {tail_index[0]}")
            tail_index[0] = (tail_index[0] + 1) % buffer_size
    shm.close()    
        

if __name__ == "__main__":
    lock = Lock()
    shm  = SharedMemory(create=True, size=buffer_size*4)
    buf  = shm.buf
    
    head_index = [0]
    tail_index = [0]

    p = Process(target=producer, args=(shm.name, head_index, lock))
    c = Process(target=consumer, args=(shm.name, tail_index, lock))
    
    p.start()
    c.start()
    
    p.join()
    c.join()
    
    shm.close()
    shm.unlink()

