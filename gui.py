
import tkinter as tk

# create main application window
root = tk.Tk()
root.title("Simple Widget Example")
root.geometry("300x200")

# label
label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
label.pack(pady=10)

# entry box
entry = tk.Entry(root, width=25)
entry.pack()

# button with action
def greet():
	name = entry.get()
	output.config(text=f"Hello, {name}!")

button = tk.Button(root, text="Greet", command=greet)
button.pack(pady=5)

# output label
output = tk.Label(root, text="")
output.pack()

# start the GUI loop
root.mainloop()
