from gui import *
import os
import sys

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


button_start=tk.Button(canvas, text='Restart', width=25, height=10, command=restart_program)
button_start.place(x=950, y=500)
root.mainloop()
