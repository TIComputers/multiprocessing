from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process
import struct

#====================================================================
# this code we have a race condition becuase result is not 400000   |
# and ever run this code result defrent befor result                |
#====================================================================

def worker(name):
    shm = SharedMemory(name=name)
    for _ in range(100000):
        value = struct.unpack_from("i", shm.buf, 0)[0]
        value += 1
        struct.pack_into("i", shm.buf, 0, value)
    shm.close()

if __name__ == "__main__":
    shm = SharedMemory(create=True, size=4)
    
    struct.pack_into("i", shm.buf, 0,0) 
    # "i"=int32, shm.buf=buffer, 0=offset, 0=value
    
    processes = [Process(target=worker, args=(shm.name,)) for _ in range(4)]
    for p in processes: p.start()
    for p in processes: p.join()
    
    print("Final:", struct.unpack_from("i", shm.buf, 0)[0])
    
    shm.close()
    shm.unlink()