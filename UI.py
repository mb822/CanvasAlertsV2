import tkinter as tk
import sys
import os.path
from os import path
import time   
from tkinter import *
import datetime
import os
from tkinter import messagebox
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from email.message import EmailMessage
import functions as funct


HEIGHT = 467
WIDTH = 830

sroot = Tk()
sroot.resizable(False,False)
sroot.minsize(height=HEIGHT,width=WIDTH)
sroot.title("CanvasAlerts")
sroot.configure()
Frame(sroot)
BG = Label(sroot)
BG.place(x=-5,y=-5)
import sys, os

sVerifImg = tk.PhotoImage(file = os.path.join(sys.path[0],"imageAssets/sendVerification.png"))
runImg = tk.PhotoImage(file = os.path.join(sys.path[0],"imageAssets/run.png"))
submitImg = tk.PhotoImage(file = os.path.join(sys.path[0],"imageAssets/submit.png"))
infoImg = tk.PhotoImage(file = os.path.join(sys.path[0],"imageAssets/infoImg.png"))
logoutImg = tk.PhotoImage(file = os.path.join(sys.path[0],"imageAssets/logout.png"))

elems = []


PATH = os.path.join(sys.path[0], funct.getCorrectDriver())
#PATH = os.path.join(sys.path[0], "chromedriver")
options = webdriver.ChromeOptions()
options.add_argument('--lang=en_US')
options.headless = True
global driver

global njitEmail
global appPassword

email = ""
passord = ""
smsGateway = ""

verificationCode = ""





    
def destroyElems():
    global elems
    for elem in elems:
        elem.destroy()



        # driver.get("http://njit.instructure.com/login/saml")
        # username = driver.find_element_by_name("j_username")
        # Password = driver.find_element_by_name("j_password")
        # username.send_keys(EMAIL.replace("@njit.edu",""))
        # Password.send_keys(PASSWORD)
        # username.send_keys(Keys.RETURN)

def verifyUPAP(EMAIL, PASSWORD):
    global email
    global password
    global appPassword
    global elems
    global njitEmail
    njitEmail="canvasalertsnjit@gmail.com"
    appPassword="eeytczejwrwbmruh"
    driver = webdriver.Chrome(PATH, options=options)
    
    errorLabel = tk.Label(sroot, text ="hello", font=("Myriad", 12), fg='#b33030')
    elems.append(errorLabel)
    
    if "@njit.edu" not in EMAIL:
        errorLabel.config(text='Invalid Email - include \'@njit.edu\'')
        errorLabel.place(relx=0.345, rely=0.73,relwidth=0.305, relheight=0.04)
    else:
        if(not (funct.authenticate(EMAIL.replace("@njit.edu",""),PASSWORD, driver))):
            driver.close()
            errorLabel.config(text='Invalid Email or Password')
            errorLabel.place(relx=0.345, rely=0.73,relwidth=0.305, relheight=0.04)
        else:
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(njitEmail, appPassword)
                server.quit()
                driver.close()
                phoneSetUpPage()
                email = EMAIL
                password = PASSWORD
            except:
                driver.close()
                errorLabel.config(text='Invalid Email or App Password')
                errorLabel.place(relx=0.345, rely=0.8,relwidth=0.305, relheight=0.04)









def upapPage():
    global BG
    global elems
    destroyElems()

    upapBG = tk.PhotoImage(file =os.path.join(sys.path[0],"imageAssets/testCABGV2.png"))
    BG.configure(image = upapBG)
    BG.image = upapBG
    BG.place(x=-5,y=-5)

    emailEntry = tk.Entry(sroot, font=40, borderwidth = 0,highlightthickness = 0,bg = '#fafafa', fg = '#636363')
    emailEntry.place(relx=0.345, rely=0.435,relwidth=0.305, relheight=0.04)
    passwordEntry = tk.Entry(sroot, font=40, borderwidth = 0,highlightthickness = 0,bg = '#fafafa', fg = '#636363', show = "•")
    passwordEntry.place(relx=0.345, rely=0.535,relwidth=0.305, relheight=0.04)
    submitButton = tk.Button(sroot, command =lambda: verifyUPAP(emailEntry.get(), passwordEntry.get()), image = submitImg)
    submitButton.place(relx=0.345, rely=0.63,relwidth=0.305, relheight=0.04)
 
    elems = [emailEntry, passwordEntry,submitButton]


def carrierInfo():
    messagebox.showinfo("Carrier Options", "The following are supported carriers:\n     Verizon\n     T-Mobile\n     Sprint\n     AT&T\n     Metro PCS\n     Boost\n\n If you use a differnt carrier, enter the SMS Gateway extension here")



def createSMSGateway(number, carrier):
    print(number)
    print(carrier)
    
    global smsGateway
    smsGateway = ""
    smsGateway+=number
    if(carrier == "Verizon"):
        smsGateway += "@vtext.com"
    elif(carrier == "AT&T"):
        smsGateway += "@txt.att.net"
    elif(carrier == "Sprint"):
        smsGateway += "@messaging.sprintpcs.com"
    elif(carrier == "T-Mobile"):
        smsGateway += "@tmomail.net"
    elif(carrier == "Metro PCS"):
        smsGateway += "@mymetropcs.com"
    elif(carrier == "Boost"):
        smsGateway += "@myboostmobile.com"
    else:
        smsGateway += carrier
    return smsGateway



def sendVerificationCode(number, carrier):
    global smsGateway
    global email
    global appPassword
    global verificationCode
    global elems
    
    verificationCode = str(int(random.random() * 10)) + str(int(random.random() * 10)) + str(int(random.random() * 10)) + str(int(random.random() * 10))

    cleanNumber = number.replace(" ", "").replace("-","").replace("(","").replace(")","")
    
    msg = EmailMessage()
    msg.set_content(verificationCode)
    msg['subject'] = "CanvasAlerts Verification Code"
    msg['to'] = createSMSGateway(cleanNumber, carrier)
    msg['from'] = njitEmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(njitEmail, appPassword)
    server.send_message(msg)
    server.quit()

    sentLabel = tk.Label(sroot, text ="Verification Code was sent to " + cleanNumber, font=("Myriad", 12), fg='#3e95ef')
    sentLabel.place(relx=0.345, rely=0.9,relwidth=0.305, relheight=0.04)
    elems.append(sentLabel)

def verifyVerificationCode(code):
    global elems
    if(code == verificationCode):
        creds = open("creds.txt", "w")
        creds.write(email + "\n")
        creds.write(password + "\n")
        creds.write(appPassword + "\n")
        creds.write(smsGateway)
        creds.close()
        runPage()
    else:
        errorLabel = tk.Label(sroot, text ="Incorrect Verification Code", font=("Myriad", 12), fg='#b33030')
        errorLabel.place(relx=0.345, rely=0.9,relwidth=0.305, relheight=0.04)
        elems.append(errorLabel)

def phoneSetUpPage():
    global elems
    global BG
    destroyElems()

    phoneBG = tk.PhotoImage(file =os.path.join(sys.path[0],"imageAssets/phoneBG.png"))
    BG.configure(image = phoneBG)
    BG.image = phoneBG
    BG.place(x=-5,y=-5)

    numberEntry = tk.Entry(sroot, font=40, borderwidth = 0,highlightthickness = 0,bg = '#fafafa', fg = '#636363')
    numberEntry.place(relx=0.345, rely=0.435,relwidth=0.305, relheight=0.04)
    verificationCodeEntry = tk.Entry(sroot, font=40, borderwidth = 0,highlightthickness = 0,bg = '#fafafa', fg = '#636363')
    verificationCodeEntry.place(relx=0.345, rely=0.734,relwidth=0.305, relheight=0.04)
    # carrier dropdown
#    carrier = StringVar(sroot)
#    carrier.set("Select Carrier")  # default value
#    carrierDropdown = OptionMenu(sroot, carrier, "Verizon","T-Mobile", "AT&T", "Sprint", "Metro PCS", "Boost")
#    carrierDropdown.place(relx=0.333, rely=0.5, relwidth=0.328, relheight=0.1)
    carrierEntry = tk.Entry(sroot, font=40, borderwidth = 0,highlightthickness = 0,bg = '#fafafa', fg = '#636363')
    carrierEntry.place(relx=0.345, rely=0.535,relwidth=0.305, relheight=0.04)
    sVerifButton = tk.Button(sroot, command =lambda: sendVerificationCode(numberEntry.get(), carrierEntry.get()), image = sVerifImg)
    sVerifButton.place(relx=0.345, rely=0.615,relwidth=0.305, relheight=0.04)
    submitButton = tk.Button(sroot, command =lambda: verifyVerificationCode(verificationCodeEntry.get()), image = submitImg)
    submitButton.place(relx=0.345, rely=0.82,relwidth=0.305, relheight=0.04)
    infoButton = tk.Button(sroot, command =lambda: carrierInfo(), image = infoImg)
    infoButton.place(relx=0.661, rely=0.51,relwidth=0.04, relheight=0.065)
    elems = [numberEntry,verificationCodeEntry,carrierEntry,sVerifButton,submitButton, infoButton]

#doesnt load correctly
#def showRunLabelAndRun():
#    global sroot
#    runningLabel = tk.Label(sroot, text ="Canvas Alerts is running.\nPlease allow up to 2 minutes.", font=("Myriad", 12), fg='#3e95ef')
#    runningLabel.place(relx=0.345, rely=0.61,relwidth=0.305, relheight=0.06)
#    sroot.update_idletasks()
 #   elems.append(runningLabel)
 #   runScript()


def runScript(delta):
    global elems


    file = open("delta.txt", 'w')
    file.write(str(delta))
    file.close()


    funct.setDelta(delta)
    
    print("SCRIPT IS RUNNING")
    funct.setDriver()
    funct.setCreds()
    listA = funct.assignmentList(funct.assignmentLinks())
    funct.sendAlertIfDue(listA)
    #destroyElems()
    doneLabel = tk.Label(sroot, text ="Canvas Alerts has finished running.", font=("Myriad", 12), fg='#3e95ef')
    doneLabel.place(relx=0.345, rely=0.6,relwidth=0.305, relheight=0.04)
    elems.append(doneLabel)

def confirmLogout():
    if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?") == True:
        os.remove("creds.txt")
        upapPage()
    

def runPage():
    global BG
    global elems
    delta = 7

    if(path.exists("delta.txt")):
        file = open("delta.txt", 'r')
        delta = file.read()
        file.close()
    
    
    destroyElems()
        
    runBG = tk.PhotoImage(file =os.path.join(sys.path[0],"imageAssets/runBG.png"))
    BG.configure(image = runBG)
    BG.image = runBG
    BG.place(x=-5,y=-5)

    daysBefore = tk.Entry(sroot, font='Helvetica 14 bold', borderwidth = 0,highlightthickness = 0,bg = '#ffffff', fg = '#a94848') #636363
    daysBefore.insert(0, str(delta))
    daysBefore.place(relx=0.44, rely=0.735,relwidth=0.025, relheight=0.06)
    
    runButton = tk.Button(sroot, command =lambda: runScript(daysBefore.get()), image = runImg)
    runButton.place(relx=0.345, rely=0.535,relwidth=0.305, relheight=0.04)

    logoutButton = tk.Button(sroot, command =lambda: confirmLogout(), image = logoutImg)
    logoutButton.place(relx=0.01, rely=0.01,relwidth=0.04, relheight=0.07)

    elems.append(runButton)
    elems.append(logoutButton)
    elems.append(daysBefore)

    



if(path.exists("creds.txt")):
    runPage()
else:
    upapPage()
    

mainloop()




 
