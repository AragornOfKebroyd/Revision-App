import tkinter as tk

def window_setup(window):
    frame = tk.Frame(window)
    button1 = tk.Button(frame, text = 'New Window', width = 25, command =lambda:new_window(window))
    button1.pack()
    frame.pack()
    #Window size
    window.geometry("690x420+350+170")
    window.minsize(690,420)
    window.maxsize(690,420)
    window.title("Moo Moo Medows")
    
def new_window(window):
    newWindow = tk.Toplevel(window)
    app = popup(newWindow)

def popup(window):
    frame = tk.Frame(window)
    quitButton = tk.Button(frame, text = 'Quit', width = 25, command = lambda:close_windows(window))
    quitButton.pack()
    frame.pack()
    #Window size
    window.geometry("400x200+500+220")
    window.minsize(400,200)
    window.maxsize(400,200)

def close_windows(window):
    window.destroy() #destroys window

def main(): 
    root = tk.Tk()
    app = window_setup(root)
    root.mainloop() #keeps it running

if __name__ == '__main__':
    main()
