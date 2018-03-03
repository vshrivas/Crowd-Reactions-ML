import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

class Application: 

  # quits the application 
  def quit(self): 
    self.master.destroy()
    print("Successfully exited application")

  # starts the live camera feed
  def start_cam(self): 
    print("Starting camera feed. You will need a webcam.")

  # open a video file 
  def open_video(self):
    print("Opening file.")
    filename = askopenfilename()
    print("Filename being opened: " + filename)

  # create the control panel widgets  
  def buildControlPanel(self, master):
    # configure the rows and columns of this panel to have weight
    for x in range(5):
      master.columnconfigure(x, weight = 1)
 
    # the close button
    self.close_button = ttk.Button(master, text = "Close")
    self.close_button.configure(command = lambda: self.quit())
    self.close_button.grid(row = 0, column = 5)
    # the camera source button
    self.camera_button = ttk.Button(master, text = "Activate Camera")
    self.camera_button.configure(command = lambda: self.start_cam())
    self.camera_button.grid(row = 0, column = 2) 
    # button to select a file
    self.file_path_button = ttk.Button(master, text = "Select a Video")
    self.file_path_button.configure(command = lambda: self.open_video())
    self.file_path_button.grid(row = 0, column = 0)

  def __init__(self,master): 
    self.master = master;
    
    # create all of the main containers

    # the control panel
    self.control_panel = tk.Frame(master, bg = 'white', width = 1200, height = 100)
    self.control_panel.grid(row = 0, columnspan = 6)
    self.control_panel.grid_propagate(0)
    # the video display
    self.video_display = tk.Frame(master, bg = 'blue', width = 600, height = 600)
    self.video_display.grid(row = 1, columnspan = 3)
    # the graph display 
    self.graph = tk.Frame(master, bg = 'red', width = 600, height = 600)
    self.graph.grid(row = 1, column = 3, columnspan = 3)

    # build up each component of the ui
    self.buildControlPanel(self.control_panel)
       
  
root = tk.Tk();
root.title("Crowd Emotional Response");
root.geometry('{}x{}'.format(1200,700))
app = Application(root);
root.mainloop();
