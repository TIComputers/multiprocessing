from multiprocessing import Process, Queue, cpu_count
import subprocess
import ipaddress
import time


def producer(ip_range, task_queue):
    """Generate IPs and put into queue."""
    for ip in ipaddress.ip_network(ip_range, strict=False):
        task_queue.put(str(ip))

    for _ in range(cpu_count()):
        task_queue.put("STOP")


def worker(task_queue, result_queue):
    """Ping each IP and send result."""
    while True:
        ip = task_queue.get()
        if ip == "STOP":
            break

        cmd = ["ping", "-n" if is_windows else "-c", "1", "-w", "1", ip]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL)

        if res.returncode == 0:
            result_queue.put(ip)


def collector(result_queue):
    """Collect alive hosts and print them."""
    alive = []
    while True:
        ip = result_queue.get()
        if ip == "STOP":
            break
        alive.append(ip)
        print(f"[+] Host alive: {ip}")

    print("\n=== SUMMARY ===")
    print(f"Alive hosts ({len(alive)}):")
    for ip in alive:
        print("  -", ip)


def is_windows():
    import platform
    return platform.system().lower() == "windows"


if __name__ == "__main__":

    task_queue = Queue()
    result_queue = Queue()

    ip_input = input("Enter range ip: ")
    
    prod = Process(target=producer, args=(ip_input, task_queue))
    workers = [Process(target=worker, args=(task_queue, result_queue)) for _ in range(cpu_count())]
    collect = Process(target=collector, args=(result_queue,))

    start = time.time()
    prod.start()
    collect.start()
    for w in workers:
        w.start()
        
    prod.join()
    for w in workers:
        w.join()

    result_queue.put("STOP")
    collect.join()

    print(f"\nDone in {time.time() - start:.2f} sec")
