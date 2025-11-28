from multiprocessing import Process, Pipe

def worker(conn):
    # if conn.poll() # check the revc do this emptye or no (you can use it)
    data = conn.recv()
    print("Worker received: ", data)
        
    conn.send(data.upper())
    conn.close()

if __name__ == "__main__":
    conn1 , conn2 = Pipe()
    
    p = Process(target=worker, args=(conn2,))
    p.start()
    
    # conn1.send("hello, im sadegh")
    print("parent send the message")
    
    reply = conn1.recv()
    print("Reply message: ", reply)
    
    p.join()
    
    