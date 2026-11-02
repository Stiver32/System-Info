from tkinter import *
import tkinter as tk
import psutil
import time
from tkinter import messagebox
from functools import partial
import sys

class BaseMonitorWindow(tk.Toplevel):
    def __init__(self, parent, title="Monitor", update_interval_ms=1000):
        super().__init__(parent)
        self.parent = parent 
        self.update_interval_ms = update_interval_ms
        
        self.title(title)
        self.geometry("300x200+10+10")
        
        # shared close behavior
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # maybe a common close button
        close_button = tk.Button(self, text="Close", fg="red", command=self.on_close)
        close_button.pack(side="bottom", pady=10)
        
        
    def schedule_update(self):
        # call child-defined update method, then schedule next run
        self.update_data()
        self.after(self.update_interval_ms, self.schedule_update)
        
        
    def update_data(self):
        #override 
        raise NotImplementedError("Subclasses must implement update_data")
        
        
    def on_close(self):
        self.destroy()
        
        
class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        
        # show CPU stats button
        cpu_button = tk.Button(parent, text="cpu stats",command=self.open_cpu)
        cpu_button.grid(row=0,column=0,padx=10,pady=10)
        
        # show MEMORY stats button
        mem_button = tk.Button(parent, text="mem stats",command=self.open_memory)
        mem_button.grid(row=0, column=1, padx=10, pady=10)
        
        # show NETWORK stats button
        network_button = tk.Button(parent, text= "network stats", command=self.open_network)
        network_button.grid(row=0, column=2, padx=10, pady=10)  
        
        
              
        
        #  Close app button
        close_btn = tk.Button(parent, text="Close App", fg="red", command=self.close)
        close_btn.grid(row=1, column=3, columnspan=2, pady=10)

        parent.protocol("WM_DELETE_WINDOW", self.close)
        
        
    def open_cpu(self):
        CPUWindow(self.parent) # open cpu window
    
    def open_memory(self):
        MemoryWindow(self.parent) # open memory window
    
    def open_network(self):
        NetworkWindow(self.parent) # open net window
    
    def open_disk_usage(self):
        pass # open disk window
    
    def close(self):
        if messagebox.askokcancel("Quit Program", "Quit?"):
            sys.exit()

class CPUWindow(BaseMonitorWindow):
    def __init__(self,parent):
        super().__init__(parent, title ="CPU Usage", update_interval_ms=1000)
        
        self.label = tk.Label(self, text="CPU: ...", font=("Arial", 20))
        self.label.pack(pady=20)
        
        self.schedule_update()
        
    def update_data(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        self.label.config(text=f"CPU: {cpu_usage}%")
    
class MemoryWindow(BaseMonitorWindow):
    def __init__(self,parent):
        super().__init__(parent, title="Memory Usage", update_interval_ms=1000)
        
        self.label = tk.Label(self, text="Memory ...", font=("Arial", 20))
        self.label.pack(pady=20)
        
        self.schedule_update()
    
    def update_data(self):
        memory_usage = psutil.virtual_memory()
        self.label.config(text=f"Memory: {memory_usage.percent}%")
        
class NetworkWindow(BaseMonitorWindow):
    def __init__(self,parent):
        super().__init__(parent, title ="Network Usage", update_interval_ms=1000)
        
        self.label = tk.Label(self, text="Bytes Sent: ...", font=("Arial", 20))
        self.label.pack(pady=20)
        
        self.label2 = tk.Label(self, text="Bytes Received: ...", font=("Arial", 20))
        self.label2.pack(pady=40)
        
        self.schedule_update()
        
    def update_data(self):
        network_usage = psutil.net_io_counters()
        self.label.config(text=f"Bytes Received: {network_usage.bytes_recv} ")
        self.label2.config(text=f"Bytes Sent: {network_usage.bytes_sent}")
    


    
    
def main():
    root = root = tk.Tk() # create root widget(app's main/parent window) object
    root.title("CPU Monitor")
    root.geometry("800x900")
    MainWindow(root)
    root.mainloop()


main()