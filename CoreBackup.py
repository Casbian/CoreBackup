#====================================================================
import sys,subprocess,os,shutil,tkinter as tk
from tkinter import filedialog,messagebox
try:
	import customtkinter as ctk
except ImportError:
	subprocess.check_call([sys.executable,"-m","pip","install","customtkinter"])
	import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
if sys.platform=="win32":
	try:
		import ctypes
		whnd=ctypes.windll.kernel32.GetConsoleWindow()
		if whnd!=0:
			ctypes.windll.user32.ShowWindow(whnd,0)
	except Exception:
		pass
class BackupApp(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("CoreBackup")
		try:
			self.iconbitmap("logo.ico")
		except Exception as e:
			print("Error loading logo.ico:",e)
		w,h=650,400
		sw,sh=self.winfo_screenwidth(),self.winfo_screenheight()
		x,y=int((sw-w)/2),int((sh-h)/2)
		self.geometry(f"{w}x{h}+{x}+{y}")
		self.resizable(False,False)
		self.source_paths=[]
		self.title_label=ctk.CTkLabel(self,text="CoreBackup",font=("Verdana",20),text_color="white")
		self.title_label.pack(pady=(20,10))
		self.list_frame=ctk.CTkFrame(self)
		self.list_frame.pack(pady=10,padx=20,fill="both",expand=True)
		self.scrollbar=tk.Scrollbar(self.list_frame,orient="vertical")
		self.listbox=tk.Listbox(self.list_frame,bg="#2B2B2B",fg="white",selectbackground="#444444",font=("Verdana",10),activestyle="none",yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)
		self.scrollbar.pack(side="right",fill="y")
		self.listbox.pack(side="left",fill="both",expand=True,padx=10,pady=10)
		self.stats_label=ctk.CTkLabel(self,text="Total Files: 0   Total Size: 0 B",font=("Verdana",12),text_color="white")
		self.stats_label.pack(pady=10)
		self.buttons_frame=ctk.CTkFrame(self)
		self.buttons_frame.pack(pady=10)
		self.add_file_button=ctk.CTkButton(self.buttons_frame,text="Add File(s)",command=self.add_file,fg_color="#000000",text_color="white",hover_color="#333333")
		self.add_file_button.grid(row=0,column=0,padx=10,pady=10)
		self.add_folder_button=ctk.CTkButton(self.buttons_frame,text="Add Folder",command=self.add_folder,fg_color="#000000",text_color="white",hover_color="#333333")
		self.add_folder_button.grid(row=0,column=1,padx=10,pady=10)
		self.backup_button=ctk.CTkButton(self.buttons_frame,text="Backup",command=self.backup,fg_color="#000000",text_color="white",hover_color="#333333")
		self.backup_button.grid(row=0,column=2,padx=10,pady=10)
		self.clear_button=ctk.CTkButton(self.buttons_frame,text="Clear List",command=self.clear_list,fg_color="#000000",text_color="white",hover_color="#333333")
		self.clear_button.grid(row=0,column=3,padx=10,pady=10)
	def add_file(self):
		files=filedialog.askopenfilenames(title="Select File(s) to Backup")
		for file in files:
			if file not in self.source_paths:
				self.source_paths.append(file)
				self.listbox.insert(tk.END,file)
		self.update_stats()
	def add_folder(self):
		folder=filedialog.askdirectory(title="Select Folder to Backup")
		if folder and folder not in self.source_paths:
			self.source_paths.append(folder)
			self.listbox.insert(tk.END,folder)
		self.update_stats()
	def clear_list(self):
		self.source_paths.clear()
		self.listbox.delete(0,tk.END)
		self.update_stats()
	def backup(self):
		if not self.source_paths:
			messagebox.showwarning("No Sources","No files or folders selected for backup!")
			return
		dest=filedialog.askdirectory(title="Select Backup Destination")
		if not dest:return
		for path in self.source_paths:
			try:
				base_name=os.path.basename(path.rstrip(os.sep))
				target_path=os.path.join(dest,base_name)
				if os.path.isdir(path):
					shutil.copytree(path,target_path,dirs_exist_ok=True)
				else:
					shutil.copy2(path,target_path)
			except Exception as e:
				messagebox.showerror("Error",f"Error backing up {path}:\n{str(e)}")
				return
		messagebox.showinfo("Success","Backup completed successfully!")
	def update_stats(self):
		total_files=0
		total_size=0
		for path in self.source_paths:
			if os.path.isfile(path):
				total_files+=1
				try:
					total_size+=os.path.getsize(path)
				except Exception:
					pass
			elif os.path.isdir(path):
				for root,_,files in os.walk(path):
					total_files+=len(files)
					for f in files:
						try:
							total_size+=os.path.getsize(os.path.join(root,f))
						except Exception:
							pass
		readable_size=self.human_readable_size(total_size)
		self.stats_label.configure(text=f"Total Files: {total_files}   Total Size: {readable_size}")
	def human_readable_size(self,size,decimal_places=2):
		for unit in ['B','KB','MB','GB','TB']:
			if size<1024:
				return f"{size:.{decimal_places}f} {unit}"
			size/=1024
		return f"{size:.{decimal_places}f} PB"
if __name__=="__main__":
	try:
		app=BackupApp()
		app.mainloop()
	except Exception as e:
		messagebox.showerror("Fatal Error",f"An unexpected error occurred:\n{str(e)}")
		sys.exit(1)
#====================================================================