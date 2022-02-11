#Tkinter Interface Code
import tkinter as tk
from tkinter import ttk
import random

class RevisionApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) # initialises the first parameter of the class

        #Create the window
        Window = tk.Frame(self,bg="green")
        #Make sure it fits the whole window
        Window.pack(fill="both",side="top",expand=True)

        #makes sure there is only 1 row and 1 coplumn
        Window.grid_rowconfigure(0, weight = 1)
        Window.grid_columnconfigure(0, weight = 1)

        
        #initialise a list for the different pages
        self.frames = {}

        #Interates through the page classes
        for fr in (TitlePage,QuizPage,VideoPage,ChecklistPage,FlashcardPage):
            #Creating objects for each page
            frame = fr(Window, self)
            frame["bg"] = "#8ee6de"
            self.frames[fr] = frame
            #Fills the whole screen
            frame.grid(row=0,column=0,sticky="nsew")
            
        #Call the function to show the main title page
        self.showPage(TitlePage)

    
    def showPage(self, frame):
        #Select the page to bring to front
        page = self.frames[frame]
        page.tkraise() #Brings the frame to the front


#Each Class is a different UI in the app, this is the one it opens on  
class TitlePage(tk.Frame):
    #init runs when a new object is assigned to this class
    def __init__(self, parent, controller): #self is the class Object TitlePage
        tk.Frame.__init__(self, parent)
        self.parent = parent #parent is the parent window
        
        #Window Setup
        controller.title("test")
        controller.minsize(942,669)
        
        #Widgits In Main Frame
        self.button = tk.Button(self, text="Leave",command = lambda:controller.destroy()) # Leave button
        self.textLabel = tk.Label(self, text="Title") # Title
        self.buttonFrame = tk.Frame(self, bg ="#d633a8") #For the 4 buttons; blue just for now 

        #Button Frame Config
        self.buttonFrame.grid_rowconfigure(0, weight = 1)
        self.buttonFrame.grid_columnconfigure(0, weight = 1)
        self.buttonFrame.grid_rowconfigure(1, weight = 1)
        self.buttonFrame.grid_columnconfigure(1, weight = 1)
        
        #Packing widgits in the Main Frame
        self.textLabel.pack(side="top")
        self.buttonFrame.pack(padx=50,pady=50,fill="both",expand=True)
        self.button.pack(side="bottom")

        #Widgits in Button Frame
        self.QuizButton = tk.Button(self.buttonFrame, text="Quizes",command = lambda:controller.showPage(QuizPage))
        self.VideoButton = tk.Button(self.buttonFrame, text="Videos",command = lambda:controller.showPage(VideoPage))
        self.FlashcardButton = tk.Button(self.buttonFrame, text="Flashcards",command = lambda:controller.showPage(FlashcardPage))
        self.ChecklistButton = tk.Button(self.buttonFrame, text="Checklists",command = lambda:controller.showPage(ChecklistPage))

        #Packing widgits in Button Frame
        self.QuizButton.grid(row = 0, column = 0, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "se")
        self.VideoButton.grid(row = 1, column = 0, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "ne")
        self.FlashcardButton.grid(row = 0, column = 1, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "sw")
        self.ChecklistButton.grid(row = 1, column = 1, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "nw")
        
    #MainFrame functions
    

        
class QuizPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class
        self.button = tk.Button(self,text="back",command=lambda:controller.showPage(TitlePage))
        self.button.pack()

    

class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class
        self.button = tk.Button(self,text="back",command=lambda:controller.showPage(TitlePage))
        self.button.pack()


class ChecklistPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class
        self.button = tk.Button(self,text="back",command=lambda:controller.showPage(TitlePage))
        self.button.pack()



class FlashcardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class

        #Widgits In Main Frame
        self.button = tk.Button(self,text="back",command=lambda:controller.showPage(TitlePage))
        self.flashFrame = tk.Frame(self, bg ="#a643f8")

        #Flash Frame Config
        self.flashFrame.grid_rowconfigure(0,weight=1)
        self.flashFrame.grid_rowconfigure(1,weight=5)
        self.flashFrame.grid_rowconfigure(2,weight=2)
        self.flashFrame.grid_columnconfigure(0,weight=3)
        self.flashFrame.grid_columnconfigure(1,weight=2)
        self.flashFrame.grid_columnconfigure(2,weight=1)
        
        #Packing Widgits In Main Frame
        self.button.pack()
        self.flashFrame.pack(padx=15,pady=15,fill="both",expand=True)

        #Widgits in Flashcard Frame
        self.Title = tk.Label(self.flashFrame, text="Flashcards")
        self.Revise = tk.Label(self.flashFrame, text="Revise Flashcards")
        self.FileList = tk.Listbox(self.flashFrame)
        self.ScrollBar = tk.Scrollbar(self.flashFrame)
        self.selectButton = tk.Button(self.flashFrame, text="Select", state = "disabled")
        self.backButton = tk.Button(self.flashFrame, text="Back", state = "disabled")
        self.renameButton = tk.Button(self.flashFrame, text="Rename", state = "disabled")
        self.deleteButton = tk.Button(self.flashFrame, text="Delete", state = "disabled")
        self.addFlashcardButton = tk.Button(self.flashFrame, width = 15, height = 8, text="Add New Flashcard")
        self.editFlashcardButton = tk.Button(self.flashFrame, width = 15, height = 8, text="Edit Flashcard", state = "disabled")

        
        #Griding widgits in flashcard frame
        self.Title.grid(row=0,column=0,columnspan=2,sticky="n")
        self.Revise.grid(row=1,column=0,sticky="n")
        self.FileList.grid(row=1,column=0,columnspan=2,sticky="nsew")
        self.ScrollBar.grid(row=1,column=0,columnspan=2,sticky="nes")
        self.selectButton.grid(row=2,column=0,sticky="w",padx=10)
        self.backButton.grid(row=2,column=0,sticky="w",padx=60)
        self.renameButton.grid(row=2,column=0,sticky="w",padx=100)
        self.deleteButton.grid(row=2,column=1,sticky="e",padx=10)
        self.addFlashcardButton.grid(row=1,rowspan=3,column=2,sticky="n",pady=50)
        self.editFlashcardButton.grid(row=1,rowspan=3,column=2,sticky="n",pady=250)


        
        #Config
        self.listBoxSetup(self.FileList)
        self.FileList.config(yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.config(command=self.FileList.yview)
        

    def listBoxSetup(self,listbox):
            for value in range(101):
                self.listbox = listbox
                self.listbox.insert(tk.END,"📁"+str(value)) #This is really buggy with the folder icon,

    def randomColour(self):
        r = lambda: random.randint(0,255)
        hexval = ('#%02X%02X%02X' % (r(),r(),r()))
        return str(hexval)
    
#Check it is run not imported
if __name__ == "__main__":
    #Driver code
    #root = tk.Tk()
    #App = RevisionApp(root)
    #root.mainloop()

    app = RevisionApp()
    app.mainloop()
