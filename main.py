import tkinter as tk
from tkinter import ttk
import threading
import os
import subprocess
import requests
from tkinter import messagebox

def download_file(url, filename, progress_bar, callback=None):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_length = int(r.headers.get('content-length'))
            bytes_downloaded = 0
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                        percent = (bytes_downloaded / total_length) * 100
                        progress_bar["value"] = percent
                        progress_bar.update()
        messagebox.showinfo("Download", f"{filename} 下载成功！")
        if callback:
            callback()
    except Exception as e:
        messagebox.showerror("Error", f"下载 {filename} 时发生错误: {str(e)}")

def open_url_1(progress_bar):
    url = "https://update.intloc.cn/ZuluOpenJDK21.msi"
    filename = "ZuluOpenJDK21.msi"  # Update filename here
    threading.Thread(target=download_file, args=(url, filename, progress_bar, run_jdk)).start()

def open_url_2(progress_bar):
    url = "https://update.intloc.cn/HSTG%200.2.0.mrpack"
    filename = "HSTG 0.2.0.mrpack"
    threading.Thread(target=download_file, args=(url, filename, progress_bar)).start()

def open_url_3(progress_bar):
    url = "https://update.intloc.cn/HMCL-3.5.8.exe"
    filename = "HMCL-3.5.8.exe"
    threading.Thread(target=download_file, args=(url, filename, progress_bar)).start()

def run_hmcl():
    current_dir = os.getcwd()
    hmcl_path = os.path.join(current_dir, "HMCL-3.5.8.exe")
    if os.path.exists(hmcl_path):
        subprocess.Popen(hmcl_path)
        messagebox.showinfo("Drag and Drop", "请将HSTG.mrpack文件拖拽至HMCL软件内")
    else:
        messagebox.showerror("Error", "HMCL-3.5.8.exe 未找到!")

def run_jdk():
    current_dir = os.getcwd()
    msi_path = os.path.join(current_dir, "ZuluOpenJDK21.msi")
    if os.path.exists(msi_path):
        subprocess.Popen(["msiexec", "/i", msi_path])
        messagebox.showinfo("Installation", "Java Development Kit 安装中...")
    else:
        messagebox.showerror("Error", "ZuluOpenJDK21.msi 未找到!")

def execute_cmd():
    cmd = "java -jar .minecraft\\versions\\HSTG\\DynamicLoader-1.1.jar"
    subprocess.Popen(cmd, shell=True)

root = tk.Tk()
root.title("INTLOC HS Hub vHSTG0.2.1")
root.geometry("700x200")

# Add style
style = ttk.Style(root)
style.theme_use("clam")  # Change to your preferred theme

# Create frames
progress_frame = tk.Frame(root)
progress_frame.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Progress bar
progress_label = tk.Label(progress_frame, text="下载进度:")
progress_label.pack(side="left")

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate", length=200)
progress_bar.pack(side="left")

# Buttons
button2 = tk.Button(button_frame, text="Download ZuluOpenJDK21", command=lambda: open_url_1(progress_bar), bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
button2.pack(pady=5, padx=10, side="left")

button1 = tk.Button(button_frame, text="Download HSTG", command=lambda: open_url_2(progress_bar), bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
button1.pack(pady=5, padx=10, side="left")

button3 = tk.Button(button_frame, text="Download MC启动器", command=lambda: open_url_3(progress_bar), bg="#FF5722", fg="white", font=("Arial", 10, "bold"))
button3.pack(pady=5, padx=10, side="left")

button5 = tk.Button(button_frame, text="Run GAME", command=run_hmcl, bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
button5.pack(pady=5, side="left")

# New Button
button4 = tk.Button(root, text="点我更新", command=execute_cmd, bg="#FF4081", fg="white", font=("Arial", 12, "bold"))
button4.pack(pady=5)

root.mainloop()