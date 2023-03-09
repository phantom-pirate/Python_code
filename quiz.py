#!/usr/bin/python3

# Importing required modules
import datetime
import time
import threading
import csv
from click.termui import clear

# Collecting personal data
class person():
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name= last_name
        
def personal(details):
    fn=input(details.first_name) # first name
    ln=input(details.last_name) # last name
    if fn.isalpha() and ln.isalpha(): # Checking for numerical charactes
        pass
    else:
        print("Name must contain alphabets only!")
        personal(details)
    return fn,ln

# User input Personal Details
details = person("Enter first name: ", "Enter last name: ")
info=personal(details)

# Rules of the quiz
print("The test is for 3 minutes and will last for the entirity of the time. Once the time has lapsed the results will be publishe\nThe test is divided into three parts:\n 1) True or False\n 2) Multiple Choice Questions\n 3) Fill in the blanks\nThe final score would be a sum of the three sections and will be converted to percent")
input("\n\nPress enter to contine")
clear()        
    
# Quiz questions 
class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer
# Answering and analysing the quiz
def run_quiz(questions,section,response_data):
    score = 0
    for question in questions:
        global time_left
        if time_left<0:
            break
        answer = input(question.prompt)
        if section == "bool":
            if  answer.lower() =="true" or answer.lower() =="false":  
                print("Valid response.")              
                pass        
            else:
                print("Invalid response. No score")
        elif section == "mcq":
            if  answer.lower() =="a" or answer.lower() == "b" or answer.lower() =="c" or answer.lower() =="d":
                print("Valid response.")
                pass
            else:
                print("Invalid response. No score")
        elif section=="blank":
            pass
       
        if answer.lower() == question.answer.lower():
            score += 1
        response_data.append([question.prompt[:-2],answer,question.answer]) # appending data into tuple so as to obtain a csv file
    return score,response_data

#start time calculation

now = datetime.datetime.now()
start_time = now.strftime("%H:%M:%S")
st=time.time() #start time in seconds to calculate the elapsed time
print(f"The start time is {start_time}")
# Start timer
def timer():
    global time_left
    while time_left > 0:
        global stop_threads
        time.sleep(1)
        time_left -= 1
        if stop_threads:
            break
    print("Time's up!")

time_left = 10 # time limit in seconds
timer_thread = threading.Thread(target=timer)
timer_thread.start()
stop_threads=False
response_data=[]
clear()
# The quiz
print("\nComment if the statements are True (T) or False (F)\n")
# Section 1: True or false Question("\n ", "True"),
boolean_questions = [
    Question("01. Chemical reactions always occur spontaneously in the direction that releases energy.\n", "False"),
    Question("02. The ideal gas law assumes that gases have no volume or intermolecular attractions.\n", "True"),
    Question("03. The Reynolds number is a dimensionless parameter that describes the ratio of inertial forces to viscous forces in a fluid.\n", "True"),
    Question("04. The entropy of a closed system always increases over time.\n", "True"),
    Question("05. The heat of fusion is the amount of heat required to raise the temperature of a substance from a solid to a liquid.\n", "False"),
    Question("06. The critical temperature of a substance is the highest temperature at which it can exist as a liquid.\n", "False")
]

# Section 2: Multiple Choice questions
mcq_questions=[
    Question("07. What is the most common method for separating components in a liquid mixture?\nA) Distillation\nB) Filtration\nC) Extraction\nD) Crystallization\n", "A"),
    Question("08. Which unit operation is used for separating solids of different sizes?\nA) Distillation\nB) Filtration\nC) Centrifugation\nD) Sedimentation\n", "B"),
    Question("09. What is the term for the measure of how easily a fluid flows?\nA) Viscosity\nB) Surface tension\nC) Density\nD) Specific heat capacity\n", "A"),
    Question("10. What is the primary function of a chemical reactor?\nA) Heat transfer\nB) Mass transfer\nC) Chemical reaction\nD) Fluid mixing\n", "C")
    ] 

# Section 3: Fill in the  blanks questions
blank_questions=[
    Question("11. In chemical engineering, a substance that speeds up a chemical reaction without being consumed in the process is called a ____________.\n", "Catalyst"),
    Question("12.The __________ law of thermodynamics states that energy cannot be created or destroyed, only transferred or converted.\n", "First"),
    Question("13. The process of removing impurities from a metal by heating it to a high temperature and allowing the impurities to oxidize and separate is called ____________.\n", "smelting"),
    Question("14. The chemical reaction that occurs when an acid and a base are combined to form a salt and water is called a ____________ reaction.\n", "Neutralization"),
    Question("15. A substance's __________ capacity is defined as the amount of heat required to raise the temperature of one gram of the substance by one degree Celsius.\n", "specific heat")
    ]

# Run the quiz
[boolean_score,boolean_response]=run_quiz(boolean_questions,"bool",response_data)
[mcq_score,mcq_response]=run_quiz(mcq_questions,"mcq",response_data)
[blank_score,blank_response]=run_quiz(blank_questions,"blank",response_data)
    
# End time calculaion
now = datetime.datetime.now()
end_time = now.strftime("%H:%M:%S")
print(f"The end time is {end_time}")
et=time.time() #end time in seconds to calculate elapsed time

# Calculation of score
score=boolean_score+blank_score+mcq_score
questions=len(boolean_questions)+len(mcq_questions)+len(blank_questions)
stop_threads=True
# Wait for the timer thread to finish
timer_thread.join()

# Output the final score
percentage=score/15.0*100 # pecentage
print("You got %2.2f percent correct, " % percentage + info[0]+" "+info[1])
# elapsed time
duration=(et-st)
print(f"\nTime started: {start_time}        Time ended: {end_time}        Duration: %d seconds" % duration)

# Writing the file 
response_data=boolean_response,mcq_response,blank_response
with open("responses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(response_data)