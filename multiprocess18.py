from multiprocessing.shared_memory import SharedMemory
import struct

number = 1234

shm = SharedMemory(create=True, size=4)

packet = struct.pack("i", number)

shm.buf[:4] = packet

print("Raw bytes: ", list(shm.buf))

rnumber = struct.unpack("i", shm.buf[:4])[0]

print("Read number: ", rnumber)

shm.close()
shm.unlink()