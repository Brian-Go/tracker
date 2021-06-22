from win32gui import GetForegroundWindow
import psutil
import time
import win32process
from datetime import datetime
import threading

process_time={}
cycle_sec = 10
start_time = datetime.now()

def get_time_info():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        time.sleep(cycle_sec)
        if current_app not in process_time.keys():
            process_time[current_app] = [datetime.now()]
        else:
            process_time[current_app].append(datetime.now())

def get_results(file_name):
    total_times = {}
    f = open(file_name, "a")

    #header
    header = "Program run from " +  str(start_time) + " to " + str(datetime.now()) + "\n"
    f.write(header)

    #get specific times per process
    for process, times in process_time.items():
        total_times[process] = len(times) * cycle_sec

        process_block = "Process name: " + process + "\n"
        f.write(process_block)
        for i in times:
            f.write(str(i)+ "\n")

    #get total time
    for process, total in total_times.items():
        total_str = "Total time for " + process + ": " + str(total) + " sec\n"
        f.write(total_str)

    f.write("\n")
    f.close()
        

def main():
    try: 
        t = threading.Thread(target=get_time_info)
        t.start()

        print("type exit to end process")
        stop_cmd = input()
        while stop_cmd != "exit":
            print("you typed", stop_cmd)
            print("to end process type: 'exit'")
            stop_cmd = input()
        t.do_run = False
        get_results("output/results.txt")
    except (KeyboardInterrupt, SystemExit):
        t.do_run = False
        get_results("output/results.txt")
        
if __name__ == '__main__':
    main()

