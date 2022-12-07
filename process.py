# NOTE: For this program, all references to "burst", "burst time", or "bursts" always refer to CPU bursts
# I/O bursts will be referred to as "I/O time" or similar
class Process:
    def __init__(self, name, bursts, ios):
        # the process' name
        self.name = name
        # array of the process' burst times throughout its lifespan
        self.bursts = bursts
        # array of the process' I/O times throughout its lifespan
        self.ios = ios
        # total time units for the processes' bursts
        self.total_burst_time = sum(bursts)
        # total time units for the processes' I/O times
        self.total_io_time = sum(ios)
        # boolean to check if process has completed all bursts in its lifespan
        self.is_done = False
        # boolean to check if the process is ready to burst
        self.ready = True
        # boolean to check if the process is currently bursting
        self.bursting = False
        # boolean to check if the process is in I/O time
        self.in_io = False
        # boolean to check if a process was preemted and has time left in its current burst (used for MLFQ)
        self.burst_paused = False
        # boolean to check if the process has burst for the first time
        self.has_responded = False
        # represents whether the process if in queue 1, 2, or 3 priority (used for MLFQ)
        self.queue_priority = 1
        # represents the burst a process is on (first, second, third, etc...)
        self.burst_counter = -1
        # represents the I/O time a process is on (first, second, third, etc...)
        self.io_counter = -1
        # represents time units of burst left for the process while it is bursting
        self.current_burst_time_left = 0
        # represents time units of I/O time left for the process while in I/O time
        self.current_io_time_left = 0
        # continuously represents time units a process has spent waiting ready to burst
        self.time_in_waiting_counter = 0
        # continuously represents the total time units a process waited from arrival at time 0 until the
        # first time it burst
        self.response_time_counter = 0
        # represents the final response time of a process at the end of its life
        self.final_response_time = 0
        # represents the final waiting time of a process at the end of its life
        self.final_waiting_time = 0
        # represents the final turnaround time of a process at the end of its life
        # turnaround time = (final waiting time) + (total CPU burst time) + (total I/O time)
        self.final_turnaround_time = 0

    # decrements the process' remaining burst time for a burst by 1
    def decrement_burst(self):
        self.current_burst_time_left -= 1

    # decrements the process' remaining io time by 1
    def decrement_IO(self):
        self.current_io_time_left -= 1

    # increments the process' time in waiting by 1
    def increment_wait_time(self):
        self.time_in_waiting_counter += 1

    # increments the process' response time by 1
    def increment_response_time(self):
        self.response_time_counter += 1

    # sets a new time for the process' burst to start at
    def set_new_burst_time(self, time):
        self.current_burst_time_left = time

    # sets a new io time for the process' io time to start at
    def set_new_io_time(self, time):
        self.current_io_time_left = time
