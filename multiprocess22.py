from multiprocessing.shared_memory import SharedMemory
import struct

n = 1000
size = n * 4

shm = SharedMemory(create=True, size=size)
buf = shm.buf

for i in range(n):
    struct.pack_into("i", buf, i*4, i)
    
print(struct.unpack_from("i", buf, 0)[0])
print(struct.unpack_from("i", buf, 4*499)[0])
print(struct.unpack_from("i", buf, 4*999)[0])

shm.close()
shm.unlink()