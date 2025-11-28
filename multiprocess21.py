from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process, Lock
import struct

#=============================================
# this code we have not race condition       |
# because we use the lock for shared_memory  |
#=============================================


def worker(name, lock):
    shm = SharedMemory(name=name)

    for _ in range(100000):
        with lock:
            value = struct.unpack_from("i", shm.buf, 0)[0]
            value += 1
            struct.pack_into("i", shm.buf, 0, value)
    shm.close()

if __name__ == "__main__":
    lock = Lock()

    shm = SharedMemory(create=True, size=4)
    struct.pack_into("i", shm.buf, 0, 0)

    procs = [Process(target=worker, args=(shm.name, lock)) for _ in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()

    print("Final:", struct.unpack_from("i", shm.buf, 0)[0])

    shm.close()
    shm.unlink()