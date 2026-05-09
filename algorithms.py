def srtf(processes):
    for p in processes:
        if p["arrival"] < 0 or p["burst"] < 0 or p["priority"] < 0:
            raise ValueError("Negative values are not allowed")

    n = len(processes)

    remaining = [p["burst"] for p in processes]
    arrival = [p["arrival"] for p in processes]

    waiting = [0] * n
    turnaround = [0] * n
    rt = [-1] * n

    complete = 0
    time = 0

    gantt = []

    while complete != n:
        min_bt = float('inf')
        min_index = -1

        for i in range(n):
            if arrival[i] <= time and remaining[i] > 0:
                if remaining[i] < min_bt:
                    min_bt = remaining[i]
                    min_index = i

                elif remaining[i] == min_bt:
                    if arrival[i] < arrival[min_index]:
                        min_index = i

        if min_index == -1:
            time += 1
            continue

        if rt[min_index] == -1:
            rt[min_index] = time - arrival[min_index]

        start = time

        remaining[min_index] -= 1
        time += 1

        gantt.append((f"P{min_index+1}", start, time))

        if remaining[min_index] == 0:
            complete += 1
            finish_time = time

            turnaround[min_index] = finish_time - arrival[min_index]
            waiting[min_index] = turnaround[min_index] - processes[min_index]["burst"]

    avg_wt = sum(waiting) / n
    avg_tat = sum(turnaround) / n
    avg_rt = sum(rt) / n

    return waiting, turnaround, rt, avg_wt, avg_tat, avg_rt, gantt
#--------------------------------------------------------------
def priority_preemptive(processes):
    for p in processes:
        if p["arrival"] < 0 or p["burst"] < 0 or p["priority"] < 0:
            raise ValueError("Negative values are not allowed")

    n = len(processes)

    remaining = [p["burst"] for p in processes]
    arrival = [p["arrival"] for p in processes]
    priority = [p["priority"] for p in processes]

    waiting = [0] * n
    turnaround = [0] * n
    rt = [-1] * n

    complete = 0
    time = 0

    gantt = []

    while complete != n:
        best = float('inf')
        index = -1

        for i in range(n):
            if arrival[i] <= time and remaining[i] > 0:
                if priority[i] < best:
                    best = priority[i]
                    index = i

                elif priority[i] == best:
                    if arrival[i] < arrival[index]:
                        index = i

        if index == -1:
            time += 1
            continue

        if rt[index] == -1:
            rt[index] = time - arrival[index]

        start = time

        remaining[index] -= 1
        time += 1

        gantt.append((f"P{index+1}", start, time))

        if remaining[index] == 0:
            complete += 1
            finish_time = time

            turnaround[index] = finish_time - arrival[index]
            waiting[index] = turnaround[index] - processes[index]["burst"]

    avg_wt = sum(waiting) / n
    avg_tat = sum(turnaround) / n
    avg_rt = sum(rt) / n

    return waiting, turnaround, rt, avg_wt, avg_tat, avg_rt, gantt