import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from NTAtool import start_packet_capture, visualize_traffic, workbook

def start_gui():
    output_path = ""
    
    def on_start_capture():
        global output_path
        interface = interface_entry.get()
        duration = duration_entry.get()
        if not duration or not duration.isnumeric():
            messagebox.showerror("Input Error", "Please provide integer value for duration.")
        elif interface and output_path:
            duration = int(duration)
            workbook.active.append(['timestamp', 'source_ip', 'destination_ip', 'protocol', 'info'])
            start_packet_capture(interface, duration)
            workbook.save(output_path)
            messagebox.showinfo("Capture Complete", f"Packet capture complete. Data saved to {output_path}")
        else:
            print(f"interface is {interface}")
            print(f"duration is {duration}")
            print(f"output_path is {output_path}")
            messagebox.showerror("Input Error", f"Please provide valid input for all fields.")
            
    def on_select_output_path():
        global output_path
        output_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        outputpath_button.config(text=output_path)
        
    
    def on_visualize_traffic():
        visualize_traffic()

    root = tk.Tk()
    root.title("Network Traffic Analysis Tool")

    mainframe = ttk.Frame(root, padding="10 10 10 10")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(mainframe, text="Network Interface:").grid(row=1, column=1, sticky=tk.W)
    interface_entry = ttk.Entry(mainframe, width=30)
    interface_entry.grid(row=1, column=2, sticky=(tk.W, tk.E))

    ttk.Label(mainframe, text="Capture Duration (seconds):").grid(row=2, column=1, sticky=tk.W)
    duration_entry = ttk.Entry(mainframe, width=30)
    duration_entry.grid(row=2, column=2, sticky=(tk.W, tk.E))
    
    ttk.Label(mainframe, text="Excel file to save output:").grid(row=3, column=1, sticky=tk.W)
    outputpath_button = ttk.Button(mainframe, width=30, text="select output file", command=on_select_output_path)
    outputpath_button.grid(row=3, column=2, sticky=(tk.W, tk.E))

    ttk.Button(mainframe, text="Start Capture", command=on_start_capture).grid(row=4, column=1, columnspan=2)
    ttk.Button(mainframe, text="Visualize Traffic", command=on_visualize_traffic).grid(row=5, column=1, columnspan=2)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
