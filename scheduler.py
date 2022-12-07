# NOTE: For this program, all references to "burst", "burst time", or "bursts" always refer to CPU bursts
# I/O bursts will be referred to as "I/O time" or similar
from process import Process

# variables to hold each process 1-8
p1 = None
p2 = None
p3 = None
p4 = None
p5 = None
p6 = None
p7 = None
p8 = None
# an int to determine the type of algorithm to schedule with. 0 = FCFS, 1 = SJF, 2 = MLFQ
algorithm = 0
# the time quantum of MLFQ queue 1
tq_1 = 5
# the time quantum of MLFQ queue 2
tq_2 = 10
# counter for tq
tq_counter = -1
# list to hold all the processes
processes = []
# queue to hold processes that are ready and waiting to burst (used for FCFS and SJF)
ready_queue = []
# queue to hold the first priority processes (used for MLFQ, round-robin)
ready_queue_1 = []
# queue to hold the second priority processes (used for MLFQ, round-robin)
ready_queue_2 = []
# queue to hold the third priority processes (used for MLFQ, FCFS)
ready_queue_3 = []
# the current time unit the scheduler is on
current_time = -1
# the average waiting time for all processes
avg_wait_time = 0
# the average turnaround time for all processes
avg_tr_time = 0
# the average response time for all processes
avg_res_time = 0
# the CPU utilization
cpu_util = 0


# Loads processes and their burst/IO times from a data file and initializes Process objects with the information
def load_processes_file(filename):
    with open(filename, 'r') as f:
        for i, row in enumerate(f):
            unsliced_data_string = row.strip().split()
            unsliced_data = [int(num) for num in unsliced_data_string]
            burst_data = unsliced_data[::2]
            io_data = unsliced_data[1::2]
            vars()['p' + str(i + 1)] = Process('p' + str(i + 1), burst_data, io_data)
            processes.append(vars()['p' + str(i + 1)])
            # print(row.strip().split())


# Enqueues each process in to the ready queue for the first time, assuming all are activated at time 0.
# If FCFS (alg = 0), does nothing. If SJF (alg = 1), sorts the queue accordingly.
def first_time_enqueue(args, alg):
    # print("Loading processes into the initial ready queue")
    global algorithm
    if alg != 2:
        for arg in args:
            ready_queue.append(arg)
    if alg == 1:
        algorithm = 1
        sjf_sort_queue()
    if alg == 2:
        algorithm = 2
        for arg in args:
            ready_queue_1.append(arg)


# Checks if any process is currently bursting
def check_if_bursting():
    is_bursting = False
    for proc in processes:
        if proc.bursting:
            # print("There is a process bursting right now, is_bursting")
            is_bursting = True
    return is_bursting


# returns the length of the next burst a process will have
def return_next_burst_length(process):
    return process.bursts[process.burst_counter + 1]


# returns the remaining burst time a process has yet to complete for a burst
def return_remaining_burst_length(process):
    return process.current_burst_time_left


# sorts the ready queue according to the shortest job first
def sjf_sort_queue():
    ready_queue.sort(key=return_next_burst_length)


# Starts the burst of the next process in the ready queue
def start_next_burst():
    global algorithm
    global tq_counter
    process_to_begin_burst = None
    if algorithm == 0 or algorithm == 1:
        # print("Popping next process ready to burst from ready queue")
        process_to_begin_burst = ready_queue.pop(0)
        # print("The next process ready to queue is ", process_to_begin_burst.name)
        if process_to_begin_burst.has_responded is False:
            # print("Process", process_to_begin_burst.name, " has not used the CPU yet. Setting has_responded to True.")
            process_to_begin_burst.has_responded = True
        # print("Changing process ", process_to_begin_burst.name, " to ready = False and bursting = True")
        process_to_begin_burst.ready = False
        process_to_begin_burst.bursting = True
        # print("Increasing process ", process_to_begin_burst.name, " burst counter")
        process_to_begin_burst.burst_counter += 1
        # print("Process ", process_to_begin_burst.name, " is on burst #", process_to_begin_burst.burst_counter,
        # ". Setting burst length to ", process_to_begin_burst.bursts[process_to_begin_burst.burst_counter],
        # " time units.")
        process_to_begin_burst.set_new_burst_time(process_to_begin_burst.bursts[process_to_begin_burst.burst_counter])
        print_context_switch(process_to_begin_burst)
    # Alternate way to start the next burst is MLFQ is used. also checks if a burst was preemted before and bursts it accordingly
    if algorithm == 2:
        if len(ready_queue_1) != 0:
            # print("Queue 1 not empty, starting next process from queue 1")
            process_to_begin_burst = ready_queue_1.pop(0)
            # print("The next process ready to queue is ", process_to_begin_burst.name)
        elif len(ready_queue_1) == 0 and len(ready_queue_2) != 0:
            # print("Queue 1 empty, queue 2 not empty, starting next process from queue 2")
            process_to_begin_burst = ready_queue_2.pop(0)
            # print("The next process ready to queue is ", process_to_begin_burst.name)
        else:
            # print("Queue 1 and 2 empty, starting next process from queue 3")
            process_to_begin_burst = ready_queue_3.pop(0)
            # print("The next process ready to queue is ", process_to_begin_burst.name)
        if process_to_begin_burst.has_responded is False:
            # print("Process", process_to_begin_burst.name, " has not used the CPU yet. Setting has_responded to True.")
            process_to_begin_burst.has_responded = True
        # print("Changing process ", process_to_begin_burst.name, " to ready = False and bursting = True")
        process_to_begin_burst.ready = False
        process_to_begin_burst.bursting = True
        if process_to_begin_burst.burst_paused is False:
            # print("Process ", process_to_begin_burst.name, " was not preemted before.")
            # print("Increasing process ", process_to_begin_burst.name, " burst counter")
            process_to_begin_burst.burst_counter += 1
            # print("Process ", process_to_begin_burst.name, " is on burst #", process_to_begin_burst.burst_counter + 1,
            #       ". Setting burst length to ", process_to_begin_burst.bursts[process_to_begin_burst.burst_counter],
            #       " time units.")
            process_to_begin_burst.set_new_burst_time(process_to_begin_burst.bursts[process_to_begin_burst.burst_counter])
            print_context_switch(process_to_begin_burst)
        elif process_to_begin_burst.burst_paused:
            # print("Process ", process_to_begin_burst.name,
            #       " was preemted before. Starting its next burst with a remaining burst time of ",
            #       process_to_begin_burst.current_burst_time_left)
            print_context_switch(process_to_begin_burst)
            process_to_begin_burst.burst_paused = False



# Increments the current time unit by one. Decrements burst and I/O times, increments waiting times,
# checks for burst completion, checks for process completion, and checks if all processes have completed
def increment_time():
    global current_time
    global algorithm
    global tq_counter
    # sorts the queue if SJF was selected
    if algorithm == 1:
        sjf_sort_queue()
    # Increments the current time unit by one
    # print("Incrementing time unit by 1")
    current_time += 1
    # Increments time quantum counter by one
    if algorithm == 2:
        tq_counter += 1
    # checks if all processes have completed.
    # If so, calculates final response, waiting, and turnaround times for each process
    if check_if_all_processes_done() is True:
        # print("All processes have completed, setting final response, waiting, and turnaround times")
        print_context_switch(1)
        for proc in processes:
            proc.final_response_time = proc.response_time_counter
            proc.final_waiting_time = proc.time_in_waiting_counter
            proc.final_turnaround_time = (proc.final_waiting_time + proc.total_burst_time + proc.total_io_time)
        return None
    # print("Current time unit is: ", current_time)
    # print("Current time quantum is: ", tq_counter)
    # print("Checking if there is a process currently bursting")

    # Checks if there is currently a process bursting.
    # If there is no process bursting, take the next process in the ready queue (if there is one) and start its burst
    if check_if_bursting() is False:
        # print("No process bursting, starting next process burst if there is one ready")
        if algorithm == 0 or algorithm == 1:
            if len(ready_queue) > 0:
                start_next_burst()
            # if len(ready_queue) == 0:
            # print_nothing_ready()
        elif algorithm == 2:
            if len(ready_queue_1) > 0 or len(ready_queue_2) > 0 or len(ready_queue_3) > 0:
                start_next_burst()
            else:
                print_nothing_ready()
                # print("There is no process ready in any of the three queues")
    # Checks if each process in the ready queue has used the CPU yet. If not, increments its response time
    # Also increments the time spent waiting of each process in the ready queue
    if algorithm == 0 or algorithm == 1:
        for proc in ready_queue:
            if proc.has_responded is False:
                # print("Process", proc.name, " has not used the CPU yet. Incrementing response time")
                proc.increment_response_time()
            # print("Incrementing wait times of processes in ready queue")
            proc.increment_wait_time()
    elif algorithm == 2:
        for proc in ready_queue_1:
            if proc.has_responded is False:
                # print("Process", proc.name, " has not used the CPU yet. Incrementing response time")
                proc.increment_response_time()
            # print("Incrementing wait times of processes in ready queue")
            proc.increment_wait_time()
        for proc in ready_queue_2:
            # print("Incrementing wait times of processes in ready queue")
            proc.increment_wait_time()
        for proc in ready_queue_3:
            # print("Incrementing wait times of processes in ready queue")
            proc.increment_wait_time()
    for proc in processes:
        # Checks if a process is currently in I/O time. If so, decrement its remaining I/O time
        if proc.in_io:
            # print("Decrementing I/O times of process ", proc.name, " in I/O time")
            proc.decrement_IO()
            # If a process has no I/O time left, add it to the ready queue (if MLFQ, add it to its current priority of queue)
            if algorithm == 0 or algorithm == 1:
                if proc.current_io_time_left == 0:
                    # print("Process ", proc.name, " has completed I/O time. Adding to ready queue to wait")
                    ready_queue.append(proc)
                    proc.in_io = False
            elif algorithm == 2:
                if proc.current_io_time_left == 0:
                    if proc.queue_priority == 1:
                        ready_queue_1.append(proc)
                    elif proc.queue_priority == 2:
                        ready_queue_2.append(proc)
                    elif proc.queue_priority == 3:
                        ready_queue_3.append(proc)
                    proc.in_io = False
        # Checks if a process is currently bursting. If so, decrement its remaining burst time
        if proc.bursting:
            # print("Decrementing burst time of the process that is bursting")
            proc.decrement_burst()
            if algorithm == 2:
                if tq_counter == 5 and proc.queue_priority == 1 and proc.current_burst_time_left > 0:
                    print("Process ", proc.name, " has been preemted at tq ", tq_counter)
                    # print("For ", proc.name, ": Setting bursting = False, burst_paused = True")
                    proc.bursting = False
                    proc.burst_paused = True
                    # print("Process was preemted from the first queue, downgrading it to queue 2. queue_priority = 2")
                    proc.queue_priority = 2
                    ready_queue_2.append(proc)
                    tq_counter = 0
                elif tq_counter == 10 and proc.queue_priority == 2 and proc.current_burst_time_left > 0:
                    print("Process ", proc.name, " has been preemted at tq ", tq_counter)
                    # print("For ", proc.name, ": Setting bursting = False, burst_paused = True")
                    proc.bursting = False
                    proc.burst_paused = True
                    if len(ready_queue_1) > 0:
                        # print("Process was preemted by a process in queue 1, not downgrading")
                        ready_queue_2.append(proc)
                    elif len(ready_queue_1) == 0:
                        # print("Process was preemted by a process in queue 2 or 3, downgrading it to queue 3")
                        proc.queue_priority = 3
                        ready_queue_3.append(proc)
                    tq_counter = 0
                elif proc.queue_priority == 3 and proc.current_burst_time_left > 0 and len(ready_queue_2) > 0:
                    print("Process ", proc.name, " has been preempted")
                    # print("For ", proc.name, ": Setting bursting = False, burst_paused = True")
                    proc.bursting = False
                    proc.burst_paused = True
                    # print("Process was preemted by a process arriving in queue 1 or 2. Keeping process in queue 3")
                    ready_queue_3.append(proc)
                    tq_counter = 0
            # Checks is a process is done bursting
            if proc.current_burst_time_left == 0:
                # print("Time left in ", proc.name, "'s burst time is 0")
                # Checks is a process has finished all bursts. If so, marks it as done
                if proc.burst_counter == (len(proc.bursts) - 1):
                    # print("Process ", proc.name, " has finished its final burst. Setting is_done = True")
                    proc.in_io = False
                    proc.bursting = False
                    proc.ready = False
                    proc.is_done = True
                # Checks if a process is done. If not, marks the current burst as complete and puts it into I/O time
                if proc.is_done is False:
                    # print("Process ", proc.name, " has completed a burst. Starting next I/O time")
                    # print("For ", proc.name,
                    # ": Setting bursting = False, incrementing I/O counter, in_io = True, setting I/O length to ",
                    # proc.ios[proc.io_counter], " time units")
                    proc.bursting = False
                    proc.io_counter += 1
                    proc.in_io = True
                    proc.set_new_io_time(proc.ios[proc.io_counter])
                    tq_counter = 0


# Checks if all processes have finished all their bursts
def check_if_all_processes_done():
    all_done = all(proc.is_done for proc in processes)
    return all_done


# Prints status of scheduler. To be used when there are no processes currently in the ready queue
def print_nothing_ready():
    print("Current execution time is ", current_time)
    print("There is no program ready and waiting to run. CPU is not being utilized.")
    print("Processes in I/O: Process      Remaining time in I/O")
    for proc in processes:
        if proc.in_io:
            print("                  ", proc.name, "        ", proc.current_io_time_left)
    print("############################################################################")


# Prints status of scheduler. To be used whenever a context switch happens (a new burst is started)
def print_context_switch(process):
    global current_time
    global tq_counter
    global algorithm
    completed = []
    if process == 1:
        for proc in processes:
            if proc.is_done:
                completed.append(proc.name)
        print("All processes have completed: ", completed)
        return None
    print("Current execution time is ", current_time)
    if process.burst_paused:
        print("Now running process: ", process.name, " for a burst time of ", process.current_burst_time_left)
    else:
        print("Now running process: ", process.name, " for a burst time of ", process.bursts[process.burst_counter])
    print("-----------------------------------------------------")
    if algorithm == 0 or algorithm == 1:
        print("Ready Queue:      Process      Burst time")
        for proc in ready_queue:
            print("                  ", proc.name, "        ", proc.bursts[proc.burst_counter + 1])
        if len(ready_queue) == 0:
            print("                  none        N/A")
    if algorithm == 2:
        print("Ready Queue 1:      Process      Burst time")
        for proc in ready_queue_1:
            print("                    ", proc.name, "        ", proc.bursts[proc.burst_counter + 1])
        if len(ready_queue_1) == 0:
            print("                    none        N/A")
        print("Ready Queue 2:      Process      Burst time")
        for proc in ready_queue_2:
            if proc.burst_paused:
                print("                    ", proc.name, "        ", proc.current_burst_time_left)
            else:
                print("                    ", proc.name, "        ", proc.bursts[proc.burst_counter + 1])
        if len(ready_queue_2) == 0:
            print("                    none        N/A")
        print("Ready Queue 3:      Process      Burst time")
        for proc in ready_queue_3:
            if proc.burst_paused:
                print("                    ", proc.name, "        ", proc.current_burst_time_left)
            else:
                print("                    ", proc.name, "        ", proc.bursts[proc.burst_counter + 1])
        if len(ready_queue_3) == 0:
            print("                    none        N/A")
    print("-----------------------------------------------------")
    print("Processes in I/O: Process      Remaining time in I/O")
    for proc in processes:
        if proc.in_io:
            print("                  ", proc.name, "        ", proc.current_io_time_left)
    if all(not proc.in_io for proc in processes):
        print("                  none        N/A")
    print("-----------------------------------------------------")
    for proc in processes:
        if proc.is_done:
            completed.append(proc.name)
    print("Processes Completed: ", completed)
    print("############################################################################")


# runs the scheduler. pulls process data from filename and determines what scheduling algorithm to use with alg
def run_scheduler(filename, alg):
    load_processes_file(filename)
    first_time_enqueue(processes, alg)
    w = False
    while w is False:
        increment_time()
        w = check_if_all_processes_done()
    increment_time()
    print_results()


# prints the final results of the scheduler
def print_results():
    global cpu_util
    global avg_tr_time
    global avg_wait_time
    global avg_res_time
    global processes
    print("Total time needed to complete all ", len(processes), " processes: ", current_time)
    for proc in processes:
        cpu_util += proc.total_burst_time
    cpu_util = (cpu_util / current_time)
    print("CPU utilization: ", "{:.2%}".format(cpu_util))
    print("----------------------------------------------------------------------------------------------------")
    print("Wait time for each process:       Process   Wait time")
    for proc in processes:
        avg_wait_time += proc.final_waiting_time
        print("                                  ", proc.name, "        ", proc.final_waiting_time)
    avg_wait_time = (avg_wait_time / len(processes))
    print("Average wait time: ", avg_wait_time)
    print("----------------------------------------------------------------------------------------------------")
    print("Turnaround time for each process: Process   Turnaround time")
    for proc in processes:
        avg_tr_time += proc.final_turnaround_time
        print("                                  ", proc.name, "        ", proc.final_turnaround_time)
    avg_tr_time = (avg_tr_time / len(processes))
    print("Average turnaround time: ", avg_tr_time)
    print("----------------------------------------------------------------------------------------------------")
    print("Response time for each process:    Process   Response time")
    for proc in processes:
        avg_res_time += proc.final_response_time
        print("                                  ", proc.name, "        ", proc.final_response_time)
    avg_res_time = (avg_res_time / len(processes))
    print("Average response time: ", avg_res_time)
