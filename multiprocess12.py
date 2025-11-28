from multiprocessing import Process, Pipe
import time

# =========================================================================
# General concept is: you sned the command and listening to recive result |
# after you can send command and again listening to recive result         |
# =========================================================================

def worker(con, wid):
    while True:
        cmd = con.recv()    
        
        if cmd == "stop":
            con.send(f"W[{wid}] stopped")
            break
        
        result = f"W[{wid}] processed: {cmd}"
        time.sleep(0.5)
        con.send(result)
    con.close()
    

if __name__ == "__main__":
    workers = []
    pipes   = []
    
    for i in range(3):
        p_con, c_con = Pipe()
        p = Process(target=worker, args=(c_con, i))
        p.start()
        
        workers.append(p)
        pipes.append(p_con)
        
    for i, con in enumerate(pipes):
        con.send(f"task {i}")
        
    for con in pipes:
        print(con.recv())
        
    print("Sending stop signals...")
    
    for con in pipes:
        con.send("stop")
    
    for conn in pipes:
        print(conn.recv())
    
    for p in workers:
        p.join()    
        
    print("DONE !")