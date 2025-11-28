from multiprocessing import Process, Semaphore
from multiprocessing.shared_memory import SharedMemory
import time
import struct


def worker(p2w_name, w2p_name, sem_p2w, sem_w2p):
    shm_recv = SharedMemory(name=p2w_name)
    shm_send = SharedMemory(name=w2p_name)
    
    while True:
        sem_p2w.acquire()
        msg = shm_recv.buf[:4]
        num = struct.unpack_from("i", msg)[0]
        print(f"[Worker] received: {num}")
        result = num * 2
        struct.pack_into("i", shm_send.buf, 0, result)
        sem_w2p.release()



if __name__ == "__main__":
    shm_p2w = SharedMemory(create=True, size=4)
    shm_w2p = SharedMemory(create=True, size=4)
    
    sem_p2w = Semaphore(0)
    sem_w2p = Semaphore(0)
    
    p = Process(target=worker, args=(
        shm_p2w.name, shm_w2p.name,
        sem_p2w, sem_w2p
    ))
    p.start()
    
    for i in range(5):
        struct.pack_into("i", shm_p2w.buf, 0, i)
        print(f"[Parent] sended: {i}")
        
        sem_p2w.release()
        sem_w2p.acquire()
        
        msg = shm_w2p.buf[:4]
        result = struct.unpack("i", msg)[0]
        print(f"[Parent] conclutoin: {result}")
        
        time.sleep(0.4)
        
    shm_p2w.close()
    shm_w2p.close()
    
    shm_p2w.unlink()
    shm_w2p.unlink()