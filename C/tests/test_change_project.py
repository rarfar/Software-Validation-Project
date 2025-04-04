import time
import psutil
import requests
import matplotlib.pyplot as plt
from faker import Faker
import threading

fake = Faker()
BASE_URL = "http://localhost:4567/projects"
ITERATIONS = [1, 10, 100, 500, 1000, 2000, 5000]

# Tracking
times = []
cpu_percentages = []
memory_usages = []

def create_project():
    response = requests.post(BASE_URL, json={
        "title": fake.word(),
        "description": fake.sentence()
    })
    return response.json().get("id")

def monitor_cpu(process, interval, running, usage_log):
    while running["flag"]:
        usage_log.append(process.cpu_percent(interval=interval))
        time.sleep(interval)

def test_project_change_performance():
    process = psutil.Process()

    for count in ITERATIONS:
        print(f"Modifying {count} projects...")
        ids = [create_project() for _ in range(count)]

        start_memory = psutil.virtual_memory().used
        start_time = time.time()

        cpu_usage_log = []
        running_flag = {"flag": True}
        monitor_thread = threading.Thread(target=monitor_cpu, args=(process, 0.1, running_flag, cpu_usage_log))
        monitor_thread.start()

        for pid in ids:
            new_data = {"title": fake.word(), "description": fake.sentence()}
            requests.post(f"{BASE_URL}/{pid}", json=new_data)

        end_time = time.time()
        running_flag["flag"] = False
        monitor_thread.join()

        end_memory = psutil.virtual_memory().used
        total_time = end_time - start_time
        memory_used = abs(end_memory - start_memory) / 1024
        avg_cpu = sum(cpu_usage_log) / len(cpu_usage_log) if cpu_usage_log else 0

        times.append(total_time)
        memory_usages.append(memory_used)
        cpu_percentages.append(avg_cpu)

        print(f"{count} changes → Time: {total_time:.2f}s, CPU %: {avg_cpu:.2f}, Memory: {memory_used:.2f} KB")

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.plot(ITERATIONS, times, marker='o')
    plt.title("Change Time")
    plt.xlabel("Projects")
    plt.ylabel("Time (s)")

    plt.subplot(1, 3, 2)
    plt.plot(ITERATIONS, memory_usages, marker='o')
    plt.title("Change Memory Usage")
    plt.xlabel("Projects")
    plt.ylabel("Memory (KB)")

    plt.subplot(1, 3, 3)
    plt.plot(ITERATIONS, cpu_percentages, marker='o')
    plt.title("Change CPU Usage")
    plt.xlabel("Projects")
    plt.ylabel("CPU (%)")

    plt.tight_layout()
    plt.savefig("project_change_graph.png")
    plt.close()

if __name__ == "__main__":
    test_project_change_performance()
