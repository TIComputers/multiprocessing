from multiprocessing.shared_memory import SharedMemory

shm = SharedMemory(create=True, size=10) # 10 byts from memory reserved

buffer = shm.buf # we can really write on the memory with buffer

for i in range(10):
    buffer[i] = i + 1
    
print("Parent buffer:", list(buffer))
shm.close()  # disconnect process with memory
shm.unlink() # delete memory reserve from system