from multiprocessing import Process, Pipe
from time import sleep

def worker(con):
    for i in range(5):
        sleep(4)
        con.send(f"Message {i} from worker")

    con.send("done")
    con.close()

if __name__ == "__main__":
    p_con, c_con = Pipe()
    p = Process(target=worker, args=(c_con,))
    p.start()
    
    x = 0
    while True:
        if p_con.poll():
            x += 1
            msg = p_con.recv()
            print("\nReceived: ", msg)
            
            if msg == "done":
                break
            
        else:
            
            print(f"\rlistening Message [{x}]...", end="")
            sleep(1)
    
    p.join()
    print("Finished !")