#Imports
from ast import excepthandler
from calendar import c
from copyreg import constructor
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from os import listdir
import stat
import shutil
import random

## THIS ALLOWS YOU TO GET ATTRIBUTES FROM DIFFERENT CLASSES ##
#        self.controller.frames[{class}].{attribute}         #
## THIS ALLOWS YOU TO GET ATTRIBUTES FROM DIFFERENT CLASSES ##

clearOnStartUp = False

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
        for fr in (TitlePage,QuizPage,VideoPage,ChecklistPage,FlashcardPage,WriteFlashcardPage):
            #Creating objects for each page
            #fr is each object in the above list, making self.Window the controller of all of them
            self.frame = fr(self.Window, self)
            self.frame["bg"] = "#8ee6de"
            self.frames[fr] = self.frame
            
            
        #Call the function to show the main title page
        self.showPage(TitlePage)

    def showPage(self, *args):
        self.frame = args[0]        
        try: #If it has allready started
            self.previousPage = self.page #where it will go to the except 
            self.page = self.frames[self.frame]
            self.page.grid(row=0,column=0,sticky="nsew")
            self.page.tkraise()#Brings the frame to the front
            self.previousPage.grid_forget()
            
        except: #There is no previous page, e.g its starting up
            self.page = self.frames[self.frame]
            self.page.grid(row=0,column=0,sticky="nsew")
            self.page.tkraise()#Brings the frame to the front


#Each Class is a different UI in the app, this is the one it opens on  
class TitlePage(tk.Frame):
    #init runs when a new object is assigned to this class
    def __init__(self, parent, controller): #self is the class Object TitlePage
        tk.Frame.__init__(self, parent)
        self.parent = parent #parent is the parent window
        self.controller = controller
        #Window Setup
        self.controller.title("Revision App")
        self.controller.geometry("942x669")
        self.controller.minsize(942,669)
        ######controller.resizable(width=False, height=False) #cant full screen
        
        #Widgits In Main Frame
        self.button = tk.Button(self, text="Leave",command = lambda:self.controller.destroy()) # Leave button
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
        self.QuizButton = tk.Button(self.buttonFrame, text="Quizes",command = lambda:self.controller.showPage(QuizPage))
        self.VideoButton = tk.Button(self.buttonFrame, text="Videos",command = lambda:self.controller.showPage(VideoPage))
        self.FlashcardButton = tk.Button(self.buttonFrame, text="Flashcards",command = lambda:self.controller.showPage(FlashcardPage))
        self.ChecklistButton = tk.Button(self.buttonFrame, text="Checklists",command = lambda:self.controller.showPage(ChecklistPage))

        #Packing widgits in Button Frame
        self.QuizButton.grid(row = 0, column = 0, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "se")
        self.VideoButton.grid(row = 1, column = 0, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "ne")
        self.FlashcardButton.grid(row = 0, column = 1, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "sw")
        self.ChecklistButton.grid(row = 1, column = 1, ipadx = 90, ipady = 50, padx = 50, pady=30, sticky = "nw")
        
    #MainFrame functions
    
        
class QuizPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class
        self.button = tk.Button(self,text="back",command=lambda:self.controller.showPage(TitlePage))
        self.button.pack()

    
class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class
        self.button = tk.Button(self,text="back",command=lambda:self.controller.showPage(TitlePage))
        self.button.pack()


class ChecklistPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class
        self.button = tk.Button(self,text="back",command=lambda:self.controller.showPage(TitlePage))
        self.button.pack()


class FlashcardPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent) # initialises the first parameter of the class
        
        #First Time Setup Of OS, makes the file directory if it doesnt allready exist
        self.parent_dir = os.getcwd()
        self.directory = "Flashcards"
        self.path = os.path.join(self.parent_dir, self.directory)
        self.filePathText = tk.StringVar()
        self.filePathText.set("Flashcards\\")
        self.currentDir = self.path #Keeps track of what to display
        self.construction = False #makes sure no new folders can be gone into whilst one is being set up
        try:
            os.mkdir(self.path)
        except OSError:
            #It allready exists
            pass
        
        #Widgits In Main Frame
        self.button = tk.Button(self,text="back",command=lambda:self.controller.showPage(TitlePage))
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
        self.FilePathTextBox = tk.Label(self.flashFrame, textvariable=self.filePathText,anchor=tk.W,relief=tk.GROOVE,width=20)
        self.FileList = tk.Listbox(self.flashFrame, selectmode = "single",activestyle = "none")
        self.ScrollBar = tk.Scrollbar(self.flashFrame)
        self.openButton = tk.Button(self.flashFrame, text="Open", state = "disabled",command = lambda:self.SelectOrEditPathway())
        self.backButton = tk.Button(self.flashFrame, text="Back", state = "disabled",command = lambda:self.BackButton())
        self.renameButton = tk.Button(self.flashFrame, text="Rename", state = "disabled",command = lambda:self.RenameItem())
        self.deleteButton = tk.Button(self.flashFrame, text="Delete", state = "disabled",command = lambda:self.DeleteItem())
        self.addFlashcardButton = tk.Button(self.flashFrame, text="Add New Flashcard", width = 15, height = 8,command = lambda:self.CreatePopup("File"))
        self.addFolderButton = tk.Button(self.flashFrame, text="Add New Folder", width = 15, height = 8, command = lambda:self.CreatePopup("Folder"))
        self.editFlashcardButton = tk.Button(self.flashFrame, text="Edit Flashcard", width = 15, height = 8, state = "disabled",command = lambda:self.SelectOrEditPathway())

            
        #Griding widgits in flashcard frame
        self.Title.grid(row=0,column=0,columnspan=2,sticky="n")
        self.Revise.grid(row=1,column=0,sticky="n")
        self.FilePathTextBox.grid(row=1,column=0,columnspan=2,sticky="new")
        self.FileList.grid(row=1,column=0,columnspan=2,sticky="nsew",pady=(20,0))
        self.ScrollBar.grid(row=1,column=0,columnspan=2,sticky="nes")
        self.openButton.grid(row=2,column=0,sticky="w",padx=10)
        self.backButton.grid(row=2,column=0,sticky="w",padx=55)
        self.renameButton.grid(row=2,column=0,sticky="w",padx=96)
        self.deleteButton.grid(row=2,column=1,sticky="e",padx=10)
        self.addFlashcardButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(25,0))
        self.addFolderButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(200,0))
        self.editFlashcardButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(375,0))
        
        #Config
        self.listBoxWithNothing()
        self.FileList.config(yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.config(command=self.FileList.yview)
        self.FileList.bind("<<ListboxSelect>>", lambda x:self.ListBoxClicked())
        self.FileList.bind('<Double-Button-1>', lambda x:self.SelectOrEditPathway()) 
        self.FileList.bind('<Return>',lambda x: self.SelectOrEditPathway())
        self.FileList.bind('<Escape>', lambda x: self.BackButton())

        #Clears the root directory if the setting is enabled (mainly for when i dont want to have to clear it every time manually)
        if clearOnStartUp == True:
            for thing in os.listdir(self.path):
                thingPath = os.path.join(self.path,thing)
                try:
                    os.remove(thingPath)
                except OSError: #will except if it is a directory
                    try:
                        #empty directory deletion
                        os.rmdir(thingPath)
                    except:
                        #delete a directory and everything in it
                        shutil.rmtree(thingPath) 
        else:
            self.ListBoxUpdate()

    def listBoxWithNothing(self):
        self.FileList.insert(tk.END,"create folders or flashcards")
        self.FileList.config(state=tk.DISABLED)
        self.selectedType = "None"

    def CreatePopup(self,createType):
        if createType == "Folder":
            self.MessageBox = Popup("Add Folder",self,createType)
        elif createType == "File":
            self.MessageBox = Popup("Add File",self,createType)

    def AddFolderOrFile(self,text,createType):
        #Validation
        #Check if something with that name allready exists
        if self.checkIfItemExistsYet(text,createType) == True:
            messagebox.showinfo(title="(︶︿︶)", message="That file or folder allready exists!")
            return

        #check there is any text
        if text == "" or text.replace(" ","") == "":
            messagebox.showinfo(title="XD", message="You need a name silly!")
            return
        
        if ".ben" in text:
            messagebox.showinfo(title=">.<", message="Can you not please, .ben is a very important file type, dont mess with it!")
            return

        for x in ["#","%","&","{","}","\\","<",">","*","?","/","$","!","\'","\"",":","@","+","`","|","="]:
            if x in text:
                messagebox.showinfo(title="(︶︿︶)", message="You can not include "+x+" in a file or folder name!")
                return

        if self.FileList.cget("state") == tk.DISABLED:
            #if there is nothing yet in the list, change it to active and delete the message to add new stuff
            self.FileList.config(state=tk.NORMAL)
            self.FileList.delete(0)
        
        #just in case yknow
        self.FileList.config(state = tk.NORMAL) 

        if createType == "Folder":
            self.FileList.insert(tk.END,"📁"+text) #This is really buggy with the folder icon, apparently not in vscode

            #create a new folder
            self.newPath = os.path.join(self.currentDir,text)
            os.mkdir(self.newPath)

        elif createType == "File":
            self.FileList.insert(tk.END,text)

            #Create a new text file with directory of the root, need to change in future
            self.filename = text+".ben"
            self.filepath = os.path.join(self.currentDir,self.filename)
            with open(self.filepath,"w") as newTextFile:
                newTextFile.write("work please")
        
    def EditFolderOrFile(self,oldName,newName):
        #check if it is legal to change it
        if self.checkIfItemExistsYet(newName,self.selectedType) == True:
            messagebox.showinfo(title="(︶︿︶)", message="That file or folder allready exists!")
            return

        #File or folder
        if self.selectedType == "File":
            self.FileList.delete(self.selectedIndex)
            self.FileList.insert(self.selectedIndex,newName)
            os.rename(os.path.join(self.currentDir,oldName+".ben"),os.path.join(self.currentDir,newName+".ben")) 

        else:
            self.FileList.delete(self.selectedIndex)
            self.FileList.insert(self.selectedIndex,"📁"+newName) #This is really buggy with the folder icon, apparently not in vscode
            os.rename(os.path.join(self.currentDir,oldName),os.path.join(self.currentDir,newName))


    #For getting a random hex value
    def randomColour(self):
        r = lambda: random.randint(0,255)
        hexval = ('#%02X%02X%02X' % (r(),r(),r()))
        return str(hexval)

    def ListBoxClicked(self):
        try:
            self.selectedIndex = self.FileList.curselection()
            self.selectedValue = self.FileList.get(self.FileList.curselection())
        except:
            self.selectedIndex = None
            self.selectedValue = None
            return
        
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

    
    def ListBoxUpdate(self):
        #lists will hold the names to be sorted and displayed in the right order
        self.flashcardList = []
        self.folderList = []

        #Removes the current gui
        self.FileList.config(state=tk.NORMAL)
        self.FileList.delete(0,tk.END)
        self.selectedValue = None

        #Adds all the stuff in the folder
        try:
            ListOfThings = os.listdir(self.currentDir)
        except Exception as e:
            self.currentDir = os.path.dirname(self.currentDir)
            ListOfThings = os.listdir(self.currentDir)

        #Get all the contents fo the current directory into 2 lists for folders and files
        for entry in ListOfThings:
            self.fullDirItt = os.path.join(self.currentDir,entry)
            if os.path.isdir(self.fullDirItt) == True:
                self.folderList.append("📁"+entry)
            else:
                self.flashcardList.append(entry.replace(".ben",""))
        
        #sort the lists
        self.folderList.sort()
        self.flashcardList.sort()

        for folder in self.folderList:
            self.FileList.insert(tk.END,folder)
        
        for falshcard in self.flashcardList:
            self.FileList.insert(tk.END,falshcard)

        #if folder is empty
        if self.FileList.get(0) == "":
            self.listBoxWithNothing()
        
        
    def SelectOrEditPathway(self):
        if self.selectedType == "File" and self.selectedValue != None:
            self.OpenFile(self.selectedValue)

        elif self.selectedType == "Folder" and self.selectedValue != None: 
            #[1:] gets rid of folder icon
            self.OpenFolder(self.selectedValue[1:])

    def checkIfItemExistsYet(self,item,createType):
        self.CheckItemtext = item
        self.CheckItemtype = createType
        self.folderList = []
        self.flashcardList = []
        
        try:
            ListOfThings = os.listdir(self.currentDir)
        except Exception:
            self.currentDir = os.path.dirname(self.currentDir)
            ListOfThings = os.listdir(self.currentDir)

        for entry in ListOfThings:
            self.fullDirItt = os.path.join(self.currentDir,entry)
            if os.path.isdir(self.fullDirItt) == True:
                self.folderList.append(entry)
            else:
                self.flashcardList.append(entry.replace(".ben","")) 
        

        if self.CheckItemtype == "Folder":
            if self.CheckItemtext in self.folderList:
                return True
            else:
                return False
        elif self.CheckItemtype == "File":
            if self.CheckItemtext in self.flashcardList:
                return True
            else:
                return False
    
    #Button Functions
    def OpenFile(self,fileName):
        self.controller.frames[WriteFlashcardPage].startup(fileName)
        #Shows the page
        self.controller.showPage(WriteFlashcardPage)
        
    def OpenFolder(self,folderName):
        self.currentDir = os.path.join(self.currentDir,folderName)

        #Make sure it doesnt strech the page and add the folder to the string filepath label
        self.filepathTextFullTemp = "Flashcards\\"+self.currentDir[len(self.path)+1:]+"\\"
        if len(self.filepathTextFullTemp) > 60:
            self.filePathText.set("<<"+self.filepathTextFullTemp[len(self.filepathTextFullTemp)-60:])
        else:
            self.filePathText.set(self.filepathTextFullTemp)
        self.ListBoxUpdate()

    def BackButton(self):
        #If you are not at the root, else you cant go back any further so error
        if self.currentDir != self.path:
            self.currentDir = os.path.dirname(self.currentDir)
            #Gets rid of the latest folder on the string that is in the label for file path
            self.filepathTextFullTemp = "Flashcards"+self.currentDir[len(self.path):]+"\\"
            #Make sure that it doesnt stretch the page
            if len(self.filepathTextFullTemp) > 60:
                self.filePathText.set("<<"+self.filepathTextFullTemp[len(self.filepathTextFullTemp)-60:])
            else:
                self.filePathText.set(self.filepathTextFullTemp)
        else:
            messagebox.showinfo(title=":D",message="You cannot go back any further")
        #make the Listbox refresh
        self.ListBoxUpdate()


    def RenameItem(self):
        if self.selectedType == "Folder":
            self.EditNamePopup = Popup("Edit Name",self,"Edit",self.selectedValue[1:])
        else:
            self.EditNamePopup = Popup("Edit Name",self,"Edit",self.selectedValue)

    def DeleteItem(self):
        self.areYouSure = messagebox.askokcancel(title="^o^",message="Are You Sure")
        if self.areYouSure == True:
            if self.selectedType == "Folder":
                self.deleteDir = os.path.join(self.currentDir,self.selectedValue[1:])
            else:
                self.deleteDir = os.path.join(self.currentDir,self.selectedValue)+".ben"
            try:
                os.remove(self.deleteDir)
            except OSError: #will except if it is a directory
                try:
                    #empty directory deletion
                    os.rmdir(self.deleteDir)
                except:
                    #delete a directory and everything in it
                    self.areYouReallySure = messagebox.askokcancel(title="^O^",message="Are You Really Sure, this folder has items in it?")
                    if self.areYouReallySure:
                        shutil.rmtree(self.deleteDir)
                    else:
                        return
            self.FileList.delete(self.selectedIndex)
            #If there is nothing left put up the text to add more files and folders
            if self.FileList.get(0) == "":
                self.listBoxWithNothing()
        else:
            pass

   
class WriteFlashcardPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        #OS stuff
        self.parent_dir = os.getcwd()
        self.directory = "Flashcards"
        self.path = os.path.join(self.parent_dir, self.directory)
        print()
        #self.currentDir = 

        #Widgits In Main Frame
        self.button = tk.Button(self,text="back",command=lambda:self.controller.showPage(FlashcardPage))                
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
        self.addImageButton = tk.Button(self.flashFrame, text="Add Image")
        self.changeFontButton = tk.Button(self.flashFrame, text="Font")
        self.changeTextSizeButton = tk.Button(self.flashFrame, text="Size")
        self.saveButton = tk.Button(self.flashFrame, text="Save")
        self.saveAndExitButton = tk.Button(self.flashFrame, text="Save & Exit")
        self.flipFlashcardButton = tk.Button(self.flashFrame, text="Flip")
        self.hideOtherSidePreviewButton = tk.Button(self.flashFrame, text="Hide preview")
        self.flashCardFrame = tk.Frame(self.flashFrame,bg = "#34c9eb")


        #Griding widgits in flashcard frame
        self.Title.grid(row=0,column=0,columnspan=2,sticky="n")
        self.addImageButton.grid(row=2,column=0,sticky="w",padx=10)
        self.changeFontButton.grid(row=2,column=0,sticky="w",padx=105)
        self.changeTextSizeButton.grid(row=2,column=0,sticky="w",padx=296)
        self.saveButton.grid(row=2,column=1,sticky="e",padx=10)
        self.saveAndExitButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(25,0))
        self.flipFlashcardButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(200,0))
        self.hideOtherSidePreviewButton.grid(row=1,rowspan=2,column=2,sticky="n",pady=(375,0))
        self.flashCardFrame.grid(row=1,column=0,columnspan=2,sticky="nsew")

    def startup(self,fileName):
        self.fileNameOpened = fileName
        self.currentDir = os.path.join(self.controller.frames[FlashcardPage].currentDir,self.fileNameOpened+".ben")
        print(self.currentDir)
    
        
#For all popups
class Popup(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self)
        #get a var from args
        self.message = args[0]
        self.controller = args[1]
        self.createType = args[2]
        try: #If it is the edit one, so jank, ik
            self.editName = args[3]
        except:
            pass
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
        self.inputBox = tk.Entry(self.popup)

        if self.createType in ["Folder","File"]: #Change what enter button does depending what the popup is for
            self.enterButton = tk.Button(self.popup, text="Enter", command = lambda:self.CreationEnter())
            
        elif self.createType == "Edit":
            self.enterButton = tk.Button(self.popup, text="Enter", command = lambda:self.EditingName())

        #Griding
        self.inputBox.grid(row=0,column=1)
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
        self.controller.EditFolderOrFile(self.editName,self.newName)

    
#Check it is run not imported
if __name__ == "__main__":
    app = RevisionApp()
    print("start")
    app.mainloop()
    print("end")
