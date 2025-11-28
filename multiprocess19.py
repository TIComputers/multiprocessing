from multiprocessing.shared_memory import SharedMemory
import struct

shm = SharedMemory(name="sadegh", create=True, size=9)

# int=42(i) , float=3.14(f) , flag=1(b)
struct.pack_into("ifb", shm.buf, 0, 42, 3.14, 1)

print("Parent wrote:")
print(" int =", 42)
print(" float =", 3.14)
print(" flag =", 1)

input("\nPress Enter to exit and delete shared memory...")

# shm.close()


i, f, b = struct.unpack_from("ifb", shm.buf, 0)

print("Child read:")
print(" int  =", i)
print(" float=", f)
print(" flag =", b)

shm.close()