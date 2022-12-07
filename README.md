# Python-CPU-Scheduler
A representation of a CPU scheduler in Python. Scheduling algorithms include FCFS, SJF, and MLFQ (RR and FCFS). There is sample data provided to run this project in "data.txt"

## Requirements and running the program
This program requires that Python be installed on your computer. Any of the most recent versions should work.

To run the program, open a cmd prompt in the the root directory (where main.py is located) and type
`python main.py`

Alternatively, navigate to /dist and open the runnable .exe to start the program. Your OS may have a serious issue with opening an .exe comprised of scripts, and may detect
it as a virus/malware. This program is not one, and you can see the code for yourself, but if this makes you uncomfortable, simply run the program using the previous method.

## There are several assumptions made for the entire scheduler, these are as follows:
1. All processes activate at time 0

2. No process waits on I/O devices

3. Immediately after completing an I/O event, a process is put into the ready queue

4. A process accumulates waiting time while waiting in the ready queue

5. Turnaround time = waiting time + I/O time + CPU burst time

6. Response time = the time it takes for a process to CPU burst for the first time from time 0

## The MLFQ also has certain specifications listed here:

• Queue 1 will use round-robin scheduling with a time quantum (Tq) of 5

• Queue 2 will use round-robin scheduling with a time quantum (Tq) of 10

• Queue 3 will use FCFS scheduling

• All processes enter queue 1 first at activation time. If time quantum expires before a process’ CPU burst is complete, the process is downgraded to the next lower priority queue. 
  Processes will not be downgraded when preemted by a process of higher priority. A process will not be upgraded after it is downgraded.
 
## The program fetches process data from a text document (.txt). The document must be formatted as follows:

• Each line of the document indicates a different process. i.e., data in line 1 is data for process 1, data in line 2 is for data in process 2, etc.

• Data for each process must be formatted as a series of numbers only separated by a space. For example: 5 27 3 31 5 43 4 18 6 22 4 26 3 24 4

• Data for a process is interpreted as follows: CPU burst length, I/O time length, CPU burst length, I/O time length, etc.

• There must be an odd amount of numbers in the series. Processes must begin and end with a CPU burst.

For example:

5 27 3 31 **WRONG**

5 27 3 31 5 **CORRECT**

• The example data for this project has been formatted in the provided “data.txt” to abide by these rules.
