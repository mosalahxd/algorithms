import tkinter as tk
from tkinter import messagebox
from algorithms import srtf, priority_preemptive

def reset():
    global rows

    for label, row_entries in rows:
        label.destroy()
        for e in row_entries:
            e.destroy()

    rows.clear()

    result_label.config(text="")

root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("750x550")

rows = []

# -------------------- Add Process --------------------

def add_process():
    i = len(rows)

    label = tk.Label(root, text=f"P{i+1}")
    label.grid(row=i+2, column=0)

    row_entries = []

    for j in range(3):
        e = tk.Entry(root, width=10)
        e.grid(row=i+2, column=j+1)
        row_entries.append(e)

    rows.append((label, row_entries))


# -------------------- Remove Process --------------------

def remove_process():
    if not rows:
        return

    label, row_entries = rows.pop()

    label.destroy()

    for e in row_entries:
        e.destroy()

    for i, (lbl, _) in enumerate(rows):
        lbl.config(text=f"P{i+1}")


# -------------------- Get Processes --------------------

def get_processes():
    processes = []

    try:
        for i, (label, row) in enumerate(rows):
            arrival = int(row[0].get())
            burst = int(row[1].get())
            priority = int(row[2].get())

            if arrival < 0 or burst <= 0 or priority < 0:
                messagebox.showerror("Error", "Invalid values")
                return None

            processes.append({
                "id": i + 1,
                "arrival": arrival,
                "burst": burst,
                "priority": priority
            })

    except:
        messagebox.showerror("Error", "Please enter valid numbers")
        return None

    return processes


# -------------------- FORMAT GANTT --------------------

def format_gantt(gantt):
    return " | ".join([f"{p[0]}({p[1]}-{p[2]})" for p in gantt])


def extract_time(gantt):
    if not gantt:
        return []
    times = [gantt[0][1]]
    for g in gantt:
        times.append(g[2])
    return times


# -------------------- Run SRTF --------------------

def run_srtf():
    processes = get_processes()
    if not processes:
        return

    wt, tat, rt, avg_wt, avg_tat, avg_rt, gantt = srtf(processes)

    result_label.config(
        text=f"SRTF\n\n"
             f"Avg WT: {avg_wt}\n"
             f"Avg TAT: {avg_tat}\n"
             f"Avg RT: {avg_rt}\n\n"
             f"Gantt:\n{format_gantt(gantt)}\n"
             f"Time: {extract_time(gantt)}"
    )


# -------------------- Run Priority --------------------

def run_priority():
    processes = get_processes()
    if not processes:
        return

    wt, tat, rt, avg_wt, avg_tat, avg_rt, gantt = priority_preemptive(processes)

    result_label.config(
        text=f"PRIORITY\n\n"
             f"Avg WT: {avg_wt}\n"
             f"Avg TAT: {avg_tat}\n"
             f"Avg RT: {avg_rt}\n\n"
             f"Gantt:\n{format_gantt(gantt)}\n"
             f"Time: {extract_time(gantt)}"
    )


# -------------------- COMPARE --------------------

def compare():
    processes = get_processes()
    if not processes:
        return

    s_wt, s_tat, s_rt, s_awt, s_atat, s_art, s_gantt = srtf(processes)
    p_wt, p_tat, p_rt, p_awt, p_atat, p_art, p_gantt = priority_preemptive(processes)

    result_label.config(
        text="COMPARISON\n\n"
             f"SRTF -> WT: {s_awt} | TAT: {s_atat} | RT: {s_art}\n"
             f"PRIORITY -> WT: {p_awt} | TAT: {p_atat} | RT: {p_art}\n\n"
             f"SRTF Gantt:\n{format_gantt(s_gantt)}\n"
             f"Time: {extract_time(s_gantt)}\n\n"
             f"PRIORITY Gantt:\n{format_gantt(p_gantt)}\n"
             f"Time: {extract_time(p_gantt)}"
    )


# -------------------- UI --------------------

tk.Button(root, text="Add Process", command=add_process).grid(row=0, column=0)
tk.Button(root, text="Remove Process", command=remove_process).grid(row=0, column=1)

tk.Button(root, text="Run SRTF", command=run_srtf).grid(row=0, column=2)
tk.Button(root, text="Run Priority", command=run_priority).grid(row=0, column=3)

tk.Button(root, text="COMPARE", command=compare).grid(row=0, column=4)

tk.Button(root, text="Reset", command=reset).grid(row=0, column=5)
# Table Headers
tk.Label(root, text="Process").grid(row=1, column=0)
tk.Label(root, text="Arrival").grid(row=1, column=1)
tk.Label(root, text="Burst").grid(row=1, column=2)
tk.Label(root, text="Priority").grid(row=1, column=3)

# Result Output
result_label = tk.Label(root, text="", justify="left")
result_label.grid(row=100, column=0, columnspan=5)

root.mainloop()