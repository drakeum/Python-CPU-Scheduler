import scheduler
import os.path
import sys

# variable that represents the algorithm selected by the user
alg = None
# boolean for if an exception occurred
exc = None
# the "valid" values that alg can be
valid_values = [0, 1, 2]
filename = input("Welcome to Drakeum's CPU scheduler simulator. Please input the file name (including extension) that you want to pull process data from: ")
while not os.path.exists(filename):
    print("File name ", filename, " does not exist. Please ensure the file name was input correctly with its extension included and that the file is in the same folder as the program.")
    filename = input("Input a new file name: ")
print("Please input the scheduling algorithm you would like the scheduler to use.")
print("0 = FCFS, 1 = SJF, 2 = MLFQ (3 queues: Round-robin, Round-robin, FCFS)")
while alg not in valid_values:
    try:
        if alg not in valid_values and exc is False:
            print("Not a valid selection. Please enter only 0, 1, or 2 to select the associated algorithm.")
        exc = False
        alg = int(input("Selected algorithm: "))
    except:
        print("Non-integer entered. Please enter only 0, 1, or 2 to select the associated algorithm.")
        exc = True
        pass

# Runs scheduler with selected settings. restart functionality is not present when running the script from something like cmd prompt
scheduler.run_scheduler(filename, alg)
print("Thank you for using my program!")
close = input()

# This code is here to allow the program to restart when packaged as an executable
# It is commented out in the script as it is not needed when the program is not packaged as an executable
# while True:
#     answer = str(input("Run scheduler again? (y/n): "))
#     if answer in ("y", "n"):
#         break
#     print("Input invalid.")
# if answer == "y":
#     os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
# else:
#     print("Thank you for using my program! Input anything to close this window, or close it yourself.")
#     close = input()
