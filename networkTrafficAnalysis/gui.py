import tkinter as tk
import threading, ctypes
from tkinter import ttk, filedialog, messagebox
from NTAtool import NTA


class InterruptedThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._thread_id = None

    def run(self):
        try:
            super().run()
        except InterruptedError as e:
            print(f"Thread interrupted: {e}")

    def getId(self):
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def interrupt(self):
        thread_id = self.getId()
        if thread_id:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExec(thread_id, ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExec(thread_id, 0)
                print("Exception raise failure")


class GUI:
    def __init__(self):
        self.nta = NTA(log_enabled=False)
        self.output_path = ""
        self.capturing = False
        self.capture_thread = None
        self.root = tk.Tk()
        self.root.title("Network Traffic Analysis Tool")
        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.interface_label = ttk.Label(self.mainframe, text="Interface:")
        self.interface_label.grid(row=0, column=0, sticky=tk.W)
        self.interface_entry = ttk.Entry(self.mainframe, width=20)
        self.interface_entry.grid(row=0, column=1, sticky=tk.W)

        self.duration_label = ttk.Label(self.mainframe, text="Duration (seconds):")
        self.duration_label.grid(row=1, column=0, sticky=tk.W)
        self.duration_entry = ttk.Entry(self.mainframe, width=20)
        self.duration_entry.grid(row=1, column=1, sticky=tk.W)

        self.outputpath_button = ttk.Button(self.mainframe, text="Select Output Path", command=self.on_select_output_path)
        self.outputpath_button.grid(row=2, column=0, columnspan=2)

        self.start_button = ttk.Button(self.mainframe, text="Start Capture", command=self.on_start_capture)
        self.start_button.grid(row=3, column=0)
        self.stop_button = ttk.Button(self.mainframe, text="Stop Capture", command=self.on_stop_capture)
        self.stop_button.grid(row=3, column=1)

        self.debug_button = ttk.Button(self.mainframe, text="Debug Off", command=self.toggle_debug)
        self.debug_button.grid(row=4, column=0)
        self.visualize_button = ttk.Button(self.mainframe, text="Visualize Traffic", command=self.on_visualize_traffic)
        self.visualize_button.grid(row=4, column=1)

        self.root.mainloop()

    def start_capture_thread(self, interface, duration):
        self.capturing = True
        try:
            self.nta.start_packet_capture(interface, duration)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Capture Error", f"Error during capture: {e}"))
        finally:
            self.capturing = False

    def on_start_capture(self):
        interface = self.interface_entry.get()
        duration_str = self.duration_entry.get()

        if not duration_str or not duration_str.isnumeric():
            messagebox.showerror("Input Error", "Please provide an integer value for duration.")
            return

        if not interface:
            messagebox.showerror("Input Error", "Please provide a network interface.")
            return

        if not self.output_path:
            messagebox.showerror("Input Error", "Please select an output path.")
            return

        if self.capturing:
            messagebox.showerror("Capture Error", "A capture is already in progress.")
            return

        duration = int(duration_str)
        self.capture_thread = InterruptedThread(target=self.start_capture_thread, args=(interface, duration))
        self.capture_thread.start()

        if duration == 0:
            messagebox.showinfo("Capture Started", "Packet capture started. It will run until you stop it manually.")
        else:
            # Wait for thread to complete for timed captures
            def wait_for_completion():
                self.capture_thread.join()
                if not self.capturing:
                    try:
                        self.nta.save_excel(self.output_path)
                        self.root.after(0, lambda: messagebox.showinfo("Capture Complete", f"Packet capture complete. Data saved to {self.output_path}"))
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("Save Error", f"Error saving file: {e}"))

            completion_thread = threading.Thread(target=wait_for_completion)
            completion_thread.start()

    def on_select_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.output_path = file_path
            self.outputpath_button.config(text=self.output_path)
            messagebox.showinfo("Output Path Selected", f"Output path selected: {self.output_path}")
        else:
            messagebox.showerror("Output Path Error", "Please select a valid output path.")

    def on_stop_capture(self):
        if self.capturing and self.capture_thread and self.capture_thread.is_alive():
            self.nta.stop_packet_capture()
            if self.capture_thread._target == self.start_capture_thread:
                # Endless mode - interrupt the thread
                self.capture_thread.interrupt()
            self.capture_thread.join(timeout=2)
            try:
                self.nta.save_excel(self.output_path)
                self.capturing = False
                messagebox.showinfo("Capture Stopped", "Packet capture stopped. Data saved to the specified file.")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving file: {e}")
        else:
            messagebox.showerror("Capture Error", "No capture is currently running.")

    def toggle_debug(self):
        if self.nta.log_enabled:
            self.nta.disable_logging()
            self.debug_button.config(text="Debug Off")
        else:
            self.nta.enable_logging()
            self.debug_button.config(text="Debug On")

    def on_visualize_traffic(self):
        try:
            self.nta.visualize_traffic()
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Error visualizing traffic: {e}")


if __name__ == "__main__":
    try:
        GUI()
    except KeyboardInterrupt:
        print("\nGUI closed by user.")
