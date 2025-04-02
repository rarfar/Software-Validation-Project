import time
import psutil
import requests
import matplotlib.pyplot as plt
from faker import Faker

fake = Faker()
BASE_URL = 'http://localhost:4567/projects'

ITERATIONS = [1, 10, 100, 500, 1000, 2000]
times = []
cpu_usages = []
memory_usages = []

def create_project():
    payload = {
        "title": fake.sentence(nb_words=3),
        "description": fake.sentence(),
        "completed": False,
        "active": False
    }
    res = requests.post(BASE_URL, json=payload)
    assert res.status_code == 201
    return res.json()['id']

def update_project(project_id):
    new_data = {
        "title": fake.sentence(nb_words=4),
        "description": fake.sentence(),
        "completed": True,
        "active": True
    }
    res = requests.post(f"{BASE_URL}/{project_id}", json=new_data)
    assert res.status_code in [200, 201]

def test_change_project_performance():
    process = psutil.Process()

    for count in ITERATIONS:
        print(f"Updating {count} projects...")
        project_ids = [create_project() for _ in range(count)]

        start_time = time.time()
        start_memory = process.memory_info().rss
        start_cpu = process.cpu_percent(interval=None)

        for project_id in project_ids:
            update_project(project_id)

        end_time = time.time()
        end_memory = process.memory_info().rss
        end_cpu = process.cpu_percent(interval=None)

        total_time = end_time - start_time
        memory_used = (end_memory - start_memory) / 1024
        cpu_used = end_cpu - start_cpu

        times.append(total_time)
        memory_usages.append(memory_used)
        cpu_usages.append(cpu_used)

        print(f"{count} projects → Time: {total_time:.2f}s, CPU: {cpu_used:.2f}%, Memory: {memory_used:.2f} KB")

    # Plotting
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.plot(ITERATIONS, times, marker='o')
    plt.title("Update Time")
    plt.xlabel("Number of Projects")
    plt.ylabel("Time (s)")

    plt.subplot(1, 3, 2)
    plt.plot(ITERATIONS, memory_usages, marker='o')
    plt.title("Memory Usage")
    plt.xlabel("Number of Projects")
    plt.ylabel("Memory (KB)")

    plt.subplot(1, 3, 3)
    plt.plot(ITERATIONS, cpu_usages, marker='o')
    plt.title("CPU Usage")
    plt.xlabel("Number of Projects")
    plt.ylabel("CPU %")

    plt.tight_layout()
    plt.savefig("project_change_graph.png")
    plt.show()

if __name__ == "__main__":
    test_change_project_performance()
