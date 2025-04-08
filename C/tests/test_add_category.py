import time
import psutil
import requests
import matplotlib.pyplot as plt
from faker import Faker
import threading
import subprocess
session = requests.Session()

fake = Faker() # used to generate titles and descriptions for testing
BASE_URL = 'http://localhost:4567/categories'
ITERATIONS = [1, 10, 100, 500, 1000, 2000, 5000]

#Tracking
times = []
cpu_percentages = []
memory_usages = []

def start_api_server():
    print("Starting API server...")
    api_process = subprocess.Popen(["java", "-jar", "Application_Being_Tested/runTodoManagerRestAPI-1.5.5.jar"],
        stdout=subprocess.DEVNULL,  # Suppress standard output
        stderr=subprocess.DEVNULL   # Suppress standard error
        )
    time.sleep(5)  # Wait for the server to start
    return api_process

def stop_api_server(api_process):
    print("Stopping API server...")
    api_process.terminate()
    api_process.wait()

def create_category():
    return f"""
    <category>
        <title>{fake.sentence(nb_words=3)}</title>
        <description>{fake.sentence()}</description>
    </category>
    """

def monitor_cpu(process, interval, running, usage_log):
    while running["flag"]:
        usage_log.append(process.cpu_percent(interval=interval))
        time.sleep(interval)

def test_add_category_performance():
    process = psutil.Process()

    for count in ITERATIONS:
        print(f"Adding {count} categories...")
        start_memory = process.memory_info().rss
        start_time = time.time()

        cpu_usage_log = []
        running_flag = {"flag": True}
        monitor_thread = threading.Thread(target=monitor_cpu, args=(process, 0.5, running_flag, cpu_usage_log))
        monitor_thread.start()

        for _ in range(count):
            data = create_category()
            headers = {"Content-Type": "application/xml"}
            res = session.post(BASE_URL, data=data, headers=headers)
            assert res.status_code == 201

        end_time = time.time()
        running_flag["flag"] = False
        monitor_thread.join()

        end_memory = process.memory_info().rss
        total_time = end_time - start_time
        memory_used = end_memory / 1024
        avg_cpu = sum(cpu_usage_log) / len(cpu_usage_log) if cpu_usage_log else 0

        times.append(total_time)
        memory_usages.append(memory_used)
        cpu_percentages.append(avg_cpu)

        print(f"{count} Categories → Time: {total_time:.2f}s, CPU %: {avg_cpu:.2f}, Memory: {memory_used:.2f} KB")


    # Plotting
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.plot(ITERATIONS, times, marker='o')
    plt.title("Execution Time")
    plt.xlabel("Number of Categories")
    plt.ylabel("Time (s)")

    plt.subplot(1, 3, 2)
    plt.plot(ITERATIONS, memory_usages, marker='o')
    plt.title("Memory Usage")
    plt.xlabel("Number of Categories")
    plt.ylabel("Memory (KB)")

    plt.subplot(1, 3, 3)
    plt.plot(ITERATIONS, cpu_percentages, marker='o')
    plt.title("CPU Usage (%)")
    plt.xlabel("Number of Categories")
    plt.ylabel("CPU %")

    plt.tight_layout()
    plt.savefig("C/graphs/category_add_graph.png")
    plt.close()

if __name__ == "__main__":
    server = start_api_server()
    try:
        test_add_category_performance()
    finally:
        stop_api_server(server)
