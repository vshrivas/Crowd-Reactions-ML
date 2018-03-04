import tkinter as tk
from application import Application

# Constants used in application setup
# Dimensions of application window
WIDTH = 1600
HEIGHT = 900
NAME = "Crowd Reactions"

# Start the application
root = tk.Tk();
root.title(NAME);
root.geometry('{}x{}'.format(WIDTH, HEIGHT))
app = Application(root, WIDTH, HEIGHT);
print("[INFO] Application " + NAME + " has been started.")
root.mainloop();

