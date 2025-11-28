from multiprocessing import Process, Pipe
import time
import random

def worker(conn, wid):
    for i in range(5):
        time.sleep(random.uniform(0.3, 1.2))
        conn.send((wid, f"step {i} done"))

    conn.send((wid, "finished"))
    conn.close()


if __name__ == "__main__":
    pipes = []
    workers = []

    for wid in range(3):
        parent_conn, child_conn = Pipe() # nodes to connect for ever process 
        p = Process(target=worker, args=(child_conn, wid))
        p.start()
        pipes.append((wid, parent_conn))
        workers.append(p)

    print("Parent started monitoring...\n")

    active_pipes = set(range(3)) 

    while active_pipes:

        for wid, conn in list(pipes):

            if wid not in active_pipes:
                continue

            if conn.poll():
                w, msg = conn.recv()
                print(f"[Worker {w}] → {msg}")

                if msg == "finished":
                    active_pipes.remove(w) 
        else:
            print("Parent: no new messages...")
            time.sleep(0.2)

    for p in workers:
        p.join()

    print("\nAll workers finished.")
