import ftplib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FTPClient:
    def __init__(self, master):
        self.master = master
        self.master.title("FTP Client")

        self.ftp = None

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        server_label = ttk.Label(frame, text="Server:")
        server_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.server_entry = ttk.Entry(frame, width=30)
        self.server_entry.insert(0, '192.168.89.92')
        self.server_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        port_label = ttk.Label(frame, text="Port:")
        port_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.port_entry = ttk.Entry(frame, width=30)
        self.port_entry.insert(0, '2121')
        self.port_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        user_label = ttk.Label(frame, text="Username:")
        user_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.user_entry = ttk.Entry(frame, width=30)
        self.user_entry.insert(0, 'username')
        self.user_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        password_label = ttk.Label(frame, text="Password:")
        password_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.insert(0, 'password')
        self.password_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.connect_button = ttk.Button(frame, text="Connect", command=self.connect)
        self.connect_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.file_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50, height=15)
        self.file_listbox.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))

        self.download_button = ttk.Button(frame, text="Download", command=self.download_files)
        self.download_button.grid(row=6, column=0, pady=5, sticky=tk.E)

        self.upload_button = ttk.Button(frame, text="Upload", command=self.upload_files)
        self.upload_button.grid(row=6, column=1, pady=5, sticky=tk.W)
        self.delete_button = ttk.Button(frame, text="Delete", command=self.delete_file)
        self.delete_button.grid(row=6, column=1, pady=5, sticky=tk.S)

    def connect(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        username = self.user_entry.get()
        password = self.password_entry.get()

        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(server, port)
            self.ftp.login(username, password)
            self.update_file_list()
            messagebox.showinfo("Info", "Connected to the FTP server")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        files = self.ftp.nlst()
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def download_files(self):
        selected_files = self.file_listbox.curselection()
        if not selected_files:
            messagebox.showwarning("Warning", "Select files to download")
            return

        for file_index in selected_files:
            selected_file = self.file_listbox.get(file_index)
            save_path = filedialog.asksaveasfilename(initialfile=selected_file)
            if save_path:
                with open(save_path, 'wb') as f:
                    self.ftp.retrbinary(f"RETR {selected_file}", f.write)
                messagebox.showinfo("Info", f"File {selected_file} downloaded successfully")

    def upload_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            for file_path in file_paths:
                file_name = file_path.split('/')[-1]
                with open(file_path, 'rb') as f:
                    self.ftp.storbinary(f"STOR {file_name}", f)
            self.update_file_list()
            messagebox.showinfo("Info", "Files uploaded successfully")
    def delete_file(self):
        selected_file = self.file_listbox.get(self.file_listbox.curselection())
        if not selected_file:
          messagebox.showwarning("Warning", "Select a file to delete")
          return

        try:
          self.ftp.delete(selected_file)
          self.update_file_list()
          messagebox.showinfo("Info", f"File {selected_file} deleted successfully")
        except Exception as e:
          messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClient(root)
    root.mainloop()
