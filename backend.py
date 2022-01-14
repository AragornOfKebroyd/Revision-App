#imports
import sqlite3
#constants
questionTypes = ["MultiChoice","SingleChoice"]

def CreateQuestion(questionInput,answerInput,questionType):
    #Validation
    if not isinstance(questionInput, (str)):
        return "Error 69"
    if not isinstance(answerInput, (str)):
        return "Error 70"
    if not questionType in questionTypes:
        return "Error 71"


    #open database
    with sqlite3.connect("Questions.db") as db: cursor=db.cursor()
    


    
def main():
    print(CreateQuestion("what?","","SingleChoice"))



if __name__ == "__main__":
    main()
