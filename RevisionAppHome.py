#Imports
import tkinter as tk
from tkinter import ttk
import os
from os import listdir
import stat
import random

class RevisionApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) #creates the base Tk window that everything is placed in
        
        #Create the window
        self.Window = tk.Frame(self,bg="green")
        #Make sure it fits the whole window
        self.Window.pack(fill="both",side="top",expand=True)

        #makes sure there is only 1 row and 1 coplumn
        self.Window.grid_rowconfigure(0, weight = 1)
        self.Window.grid_columnconfigure(0, weight = 1)

        self.frames = {} #initialise a list for the different pages

        #Interates through the page classes
        for fr in (TitlePage,QuizPage,VideoPage,ChecklistPage,FlashcardPage):
            #Creating objects for each page
            #fr is each object in the above list, making self.Window the controller of all of them
            self.frame = fr(self.Window, self)
            self.frame["bg"] = "#8ee6de"
            self.frames[fr] = self.frame
            
            
        #Call the function to show the main title page
        self.showPage(TitlePage)

    def showPage(self, frame):
        try: #If it has allready started
            self.previousPage = self.page #where it will go to the except 
            self.page = self.frames[frame]
            self.page.grid(row=0,column=0,sticky="nsew")
            self.page.tkraise()#Brings the frame to the front
            self.previousPage.grid_forget()
            
        except: #There is no previous page, e.g its starting up
            self.page = self.frames[frame]
            self.page.grid(row=0,column=0,sticky="nsew")
            self.page.tkraise()#Brings the frame to the front


#Each Class is a different UI in the app, this is the one it opens on  
class TitlePage(tk.Frame):
    #init runs when a new object is assigned to this class
    def __init__(self, parent, controller): #self is the class Object TitlePage
        tk.Frame.__init__(self, parent)
        self.parent = parent #parent is the parent window
        
        #Window Setup
        controller.title("Revision App")
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
        self.FileList = tk.Listbox(self.flashFrame, selectmode = "single")
        self.ScrollBar = tk.Scrollbar(self.flashFrame)
        self.openButton = tk.Button(self.flashFrame, text="Open", state = "disabled",command = lambda:self.SelectOrEditPathway())
        self.backButton = tk.Button(self.flashFrame, text="Back", state = "disabled")
        self.renameButton = tk.Button(self.flashFrame, text="Rename", state = "disabled",command = lambda:self.RenameItem())
        self.deleteButton = tk.Button(self.flashFrame, text="Delete", state = "disabled",command = lambda:self.DeleteItem())
        self.addFlashcardButton = tk.Button(self.flashFrame, text="Add New Flashcard", width = 15, height = 8,command = lambda:self.CreatePopup("File"))
        self.addFolderButton = tk.Button(self.flashFrame, text="Add New Folder", width = 15, height = 8, command = lambda:self.CreatePopup("Folder"))
        self.editFlashcardButton = tk.Button(self.flashFrame, text="Edit Flashcard", width = 15, height = 8, state = "disabled",command = lambda:self.SelectOrEditPathway())

            
        #Griding widgits in flashcard frame
        self.Title.grid(row=0,column=0,columnspan=2,sticky="n")
        self.Revise.grid(row=1,column=0,sticky="n")
        self.FileList.grid(row=1,column=0,columnspan=2,sticky="nsew")
        self.ScrollBar.grid(row=1,column=0,columnspan=2,sticky="nes")
        self.openButton.grid(row=2,column=0,sticky="w",padx=10)
        self.backButton.grid(row=2,column=0,sticky="w",padx=55)
        self.renameButton.grid(row=2,column=0,sticky="w",padx=96)
        self.deleteButton.grid(row=2,column=1,sticky="e",padx=10)
        self.addFlashcardButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(25,0))
        self.addFolderButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(200,0))
        self.editFlashcardButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(375,0))
        
        #Config
        self.listBoxSetup()
        self.FileList.config(yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.config(command=self.FileList.yview)
        self.FileList.bind("<<ListboxSelect>>", lambda x:self.ListBoxUpdate())
        self.FileList.bind('<Double-Button-1>', lambda x:self.SelectOrEditPathway())
        self.FileList.bind('<Return>',lambda x: self.SelectOrEditPathway())

    def listBoxSetup(self):
        self.FileList.insert(tk.END,"create folders or flashcards")
        self.FileList.config(state=tk.DISABLED)
        self.selectedType = "None"

    def CreatePopup(self,createType):
        if createType == "Folder":
            self.MessageBox = Popup("Add Folder",self,createType)
        elif createType == "File":
            self.MessageBox = Popup("Add File",self,createType)

    def AddFolderOrFile(self,text,createType):
        if self.FileList.cget("state") == tk.DISABLED:
            #print(self.FileList.cget("state"))
            self.FileList.config(state=tk.NORMAL)
            self.FileList.delete(0)
        self.FileList.config(state = tk.NORMAL) 
        if createType == "Folder":
            self.FileList.insert(tk.END,"📁"+str(text)) #This is really buggy with the folder icon,
        elif createType == "File":
            self.FileList.insert(tk.END,text)

    def EditFolderOrFile(self,text):
        if self.selectedType == "File":
            self.FileList.delete(self.selectedIndex)
            self.FileList.insert(self.selectedIndex,text)
        else:
            self.FileList.delete(self.selectedIndex)
            self.FileList.insert(self.selectedIndex,"📁"+str(text))#This is really buggy with the folder icon,

    
    #For getting a random hex value
    def randomColour(self):
        r = lambda: random.randint(0,255)
        hexval = ('#%02X%02X%02X' % (r(),r(),r()))
        return str(hexval)

    def ListBoxUpdate(self):
        self.selectedIndex = self.FileList.curselection()
        self.selectedValue = self.FileList.get(self.FileList.curselection())
        if self.selectedValue[0] == "📁":
            self.selectedType = "Folder"
            #Change buttons to use depending on what is selected
            self.openButton.configure(state = "active")
            self.backButton.configure(state = "active")
            self.renameButton.configure(state = "active")
            self.deleteButton.configure(state = "active")
            self.editFlashcardButton.configure(state = "disabled")
        else:
            self.selectedType = "File"
            #Change buttons to use depending on what is selected
            self.openButton.configure(state = "disabled")
            self.backButton.configure(state = "active")
            self.renameButton.configure(state = "active")
            self.deleteButton.configure(state = "active")
            self.editFlashcardButton.configure(state = "active")

        print(self.selectedValue[1:],self.selectedIndex)
        
    def SelectOrEditPathway(self):
        if self.selectedType == "File":
            self.OpenFile()
        elif self.selectedType == "Folder":
            self.OpenFolder()
        
    #Button Functions
    def OpenFile(self):
        print("opening file...")

    def OpenFolder(self):
        print("opening floder...")

    def RenameItem(self):
        self.EditNamePopup = Popup("Edit Name",self,"Edit")

    def DeleteItem(self):
        self.AreYouSure = Popup("Are You Sure",self,"Confirmation")
    
#For all popups
class Popup(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self)
        #get a var from args
        self.message = args[0]
        self.controller = args[1]
        self.createType = args[2]
        #run popup code
        self.popupmsg()
        
    def popupmsg(self):
        #Winodw Creation
        self.popup = tk.Toplevel()
        self.popup.attributes('-topmost', True)
        self.popup.update()
        self.popup.title("^_^")
        self.popup.geometry("200x70+300+200")
        self.popup.minsize(200,70)
        self.popup.maxsize(200,70)
        
        #Make this the only interactable window
        self.popup.grab_set()
        self.popup.takefocus = True
        self.popup.focus_set()

        #Grid Config
        self.popup.grid_rowconfigure(0,weight=1)
        self.popup.grid_rowconfigure(1,weight=1)
        self.popup.grid_columnconfigure(0,weight=1)
        self.popup.grid_columnconfigure(1,weight=1)
        
        #Widgits
        self.message = tk.Label(self.popup, text=self.message)
        self.destroyButton = tk.Button(self.popup, text="Cancel", command = lambda:self.QuitPopup())

        if self.createType in ["Folder","File"]: #Change what enter button does depending what the popup is for
            self.inputBox = tk.Entry(self.popup)
            self.enterButton = tk.Button(self.popup, text="Enter", command = lambda:self.CreationEnter())
            #grid
            self.inputBox.grid(row=0,column=1)
            
        elif self.createType == "Edit":
            self.inputBox = tk.Entry(self.popup)
            self.enterButton = tk.Button(self.popup, text="Enter", command = lambda:self.EditingName())
            #grid
            self.inputBox.grid(row=0,column=1)
            
        elif self.createType == "Confirmation":
            self.enterButton = tk.Button(self.popup, text="Yes", command = lambda:self.ConfirmButton())
            
        #Griding
        self.message.grid(row=0,column=0)
        self.destroyButton.grid(row=1,column=0)
        self.enterButton.grid(row=1,column=1)
        
    def QuitPopup(self):
        self.popup.destroy()
        self.grab_release()

    def CreationEnter(self):
        self.message = self.inputBox.get()
        self.QuitPopup()
        self.controller.AddFolderOrFile(self.message,self.createType)
        
    def EditingName(self):
        self.newName = self.inputBox.get()
        self.QuitPopup()
        self.controller.EditFolderOrFile(self.newName)

    def ConfirmButton(self):
        self.QuitPopup()
        self.controller.FileList.delete(self.controller.selectedIndex)
        if self.controller.FileList.get(0) == "":
            self.controller.listBoxSetup()
    
#Check it is run not imported
if __name__ == "__main__":
    app = RevisionApp()
    print("start")
    app.mainloop()
    print("end")
