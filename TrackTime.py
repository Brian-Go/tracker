from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import tkinter as tk
from tkinter import ttk
import threading

'''TEST FOR USING GUI INSTEAD OF CMD NOT WORKING'''

class DisplayTime(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.timestamp = {}
        self.process_time = {}
        self.output = tk.StringVar()
        self.createOutput()

    def createOutput(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.text = tk.Text(self, height=20, width=100)
        self.text.grid(row=0,column=0)

        # self.textbox1 = ttk.Entry(self, textvariable=self.command).grid(row=1, column=0)
        # self.textbox2 = ttk.Entry(self, textvariable=self.scriptfile).grid(row=2, column=0)

        # self.button1 = ttk.Button(self, text="Send Command", command=self.handleCmd).grid(row=1, column=1)
        # self.button2 = ttk.Button(self, text="Run Scriptfile", command=self.runScript).grid(row=2, column=1)

    def changeOutput(self):
        self.output = ""
        for key, val in self.process_time:
            self.output += key + ": " + val + " minutes"
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, self.output)

    def run(self):
        while True:
            print(self.process_time)
            current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
            self.timestamp[current_app] = int(time.time())/60
            time.sleep(10)
            if current_app not in self.process_time.keys():
                self.process_time[current_app] = 0
            self.process_time[current_app] = self.process_time[current_app]+int(time.time())/60-self.timestamp[current_app]
            self.changeOutput()
        
    
    # def process_queue(self):
    #     self.changeOutput()
    #     self.master.after(10, self.process_queue)
        

def runUI():
    window = tk.Tk()
    window.title("Time Spent")
    notebook = ttk.Notebook(window)
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Time")
    Disp = DisplayTime(master=frame)
    notebook.grid()
    Disp.grid()
    window.mainloop()
    Disp.run()

if __name__ == "__main__":
    runUI()

class ThreadedTask(threading.Thread):
    def __init__(self, process_time, timestamp):
        threading.Thread.__init__(self)
        self.process_time = process_time
        self.timestamp = timestamp

    def run(self):
        while True:
            current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
            self.timestamp[current_app] = int(time.time())/60
            time.sleep(10)
            if current_app not in self.process_time.keys():
                self.process_time[current_app] = 0
            self.process_time[current_app] = self.process_time[current_app]+int(time.time())/60-self.timestamp[current_app]
            self.changeOutput()