from multiprocessing import Process, Queue
from time import sleep
import random

def worker(worker_id, task_q, result_q):
    while True:
        task = task_q.get()

        if task is None:
            result_q.put((worker_id, "EXIT"))
            break


        job_id, value = task
        # sleep(random.uniform(0.3, 1.0))

        result = value * value  
        result_q.put((worker_id, job_id, result))


if __name__ == "__main__":
    num_workers = 3
    task_q = Queue()
    result_q = Queue()

    workers = []
    for wid in range(num_workers):
        p = Process(target=worker, args=(wid, task_q, result_q))
        p.start()
        workers.append(p)

    num_jobs = 10000
    for job_id in range(num_jobs):
        value = random.randint(1, 20)
        task_q.put((job_id, value))
        print(f"Parent → Job {job_id} with value {value} sent.")

    for _ in range(num_workers):
        task_q.put(None)

    finished_workers = 0
    results = {}

    while finished_workers < num_workers:
        data = result_q.get()

        if len(data) == 2:  
            wid, _ = data
            print(f"Worker {wid} exited.")
            finished_workers += 1
        else:
            wid, job_id, result = data
            print(f"Parent received: Worker {wid} → Job {job_id} = {result}")
            results[job_id] = result

    for p in workers:
        p.join()

    print("\nAll workers finished.")
    print("Final results:", results)
