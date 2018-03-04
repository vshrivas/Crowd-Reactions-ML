import tkinter as tk
from application import Application
import constants

# Start the application
root = tk.Tk();
root.title(constants.NAME);
root.geometry('{}x{}'.format(constants.WIDTH, constants.HEIGHT))
app = Application(root, constants.WIDTH, constants.HEIGHT);
print("[INFO] Application " + constants.NAME + " has been started.")
root.mainloop();

