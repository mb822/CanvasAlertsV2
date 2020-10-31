import smtplib
from email.message import EmailMessage
import os.path
from os import path
import requests
from bs4 import BeautifulSoup
from lxml import html
import requests
from selenium import webdriver
import time
from os import path
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import stdiomask
import re
from datetime import datetime
from datetime import timedelta
from assignment import assignment
import platform


def getCorrectDriver():
    os = platform.system()
    if os == "Windows":
        return "drivers/chromedriver.exe"
    elif os == "Darwin":
        return "drivers/chromedriverMAC"
    elif os == "Linux":
        return "driver/chromedriverLIN"
    else:
        print("OS not supported")


global PATH
PATH = os.path.join(sys.path[0], getCorrectDriver())
global options
options = webdriver.ChromeOptions()
options.add_argument('--lang=en_US')
options.headless = True
options.detach = True

global driver

def setDriver():
    global driver
    global option
    driver = webdriver.Chrome(PATH, options=options)

# def inputSaveCreds():

#     global email
#     global password
#     global appPassword
#     global smsGateway

#     creds = open("creds.txt", "w")
#     correctCreds = False
#     while(not correctCreds):
#         username = input("username:\n")
#         print("------------------------------")
#         password = stdiomask.getpass(prompt="password:\n")
#         correctCreds = authenticate(username, password)
#         if(correctCreds == False):
#             print("Could not authenticate username and password, retry")
#             print("------------------------------")

#     creds.write(username)
#     creds.write("\n")
#     creds.write(password)
#     creds.write("\n")

#     print("------------------------------")
#     appPass1 = stdiomask.getpass(prompt="App Password:\n")
#     creds.write(appPass1)
#     creds.write("\n")
#     print("------------------------------")
#     creds.write(input("number:\n"))
#     print("------------------------------")
#     c = (input("carrier:\n       \"v\" for Verizon\n       \"a\" for AT&T\n       \"s\" for Sprint\n       \"t\" for T-Mobile\n       \"m\" for Metro PCS\n       \"b\" for Boost Mobile\n"))
#     print("------------------------------")

#     if(c == "v"):
#         creds.write("@vtext.com")
#     elif(c == "a"):
#         creds.write("@txt.att.net")
#     elif(c == "s"):
#         creds.write("@messaging.sprintpcs.com")
#     elif(c == "t"):
#         creds.write("@tmomail.net")
#     elif(c == "m"):
#         creds.write("@mymetropcs.com")
#     elif(c == "b"):
#         creds.write("@myboostmobile.com")

#     creds.close()

#     creds = open("creds.txt", "r")

#     content = creds.readlines()

#     email = content[0].replace("\n", "")
#     password = content[1].replace("\n", "")
#     appPassword = content[2].replace("\n", "")
#     smsGateway = content[3].replace("\n", "")

#     creds.close()



    

def authenticate(user, password,driver):
    driver.get("http://njit.instructure.com/login/saml")

    username = driver.find_element_by_name("j_username")
    Password = driver.find_element_by_name("j_password")

    username.send_keys(user)
    Password.send_keys(password)

    username.send_keys(Keys.RETURN)
    if("The UCID or password you entered was incorrect." in driver.page_source):
        return False
    else:
        return True


def setCreds():
    global email
    global password
    global appPassword
    global smsGateway
    creds = open("creds.txt", "r")
    content = creds.readlines()
    creds.close()
    email = content[0].replace("\n", "")
    password = content[1].replace("\n", "")
    appPassword = content[2].replace("\n", "")
    smsGateway = content[3].replace("\n", "")


def email_alert(subject, body):
    global email
    global appPassword
    global smsGateway
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = smsGateway
        msg['from'] = "canvasalertsnjit@gmail.com"
        # user must be the gmail of the sender
        # password must be the google APP password - made avalible after 2 factor verification is set up
        #"http://myaccount.google.com/" - navigate to security - signing in to google - app passwords - select app as other - name it anything - save the password that is given
        user = email
        password = appPassword
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

      #  print(user)
      #  print(appPassword)
        server.login("canvasalertsnjit@gmail.com", "eeytczejwrwbmruh")
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False


def assignmentLinks():
    global email
    global password
    global driver
    driver.get("http://njit.instructure.com/login/saml")

    username = driver.find_element_by_name("j_username")
    Password = driver.find_element_by_name("j_password")

    username.send_keys(email.replace("@njit.edu", ""))
    Password.send_keys(password)

    username.send_keys(Keys.RETURN)

    checkbox = driver.find_element_by_id("accept")
    checkbox.click()
    accept = driver.find_element_by_id("submitbtn")
    accept.click()
    
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    courseCards = soup.find_all('div', class_='ic-DashboardCard__header')
    coursesList = []

    for card in courseCards:
        coursesList.append(card.a['href'])




    print("COURSELIST")
    print(coursesList)


    

    assignmentLinks = []

    for course in coursesList:

        driver.get("http://njit.instructure.com" + course)
        try:
            #time.sleep(5)
            assignmentTab = driver.find_element_by_class_name("assignments")
            assignmentTab.click()
            print(course + "goes through")

        except(NoSuchElementException, StaleElementReferenceException) as e:
            continue
        try:
            element = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "assignment_group_upcoming_assignments")))
            print("why is this working now: " + course)
        except(TimeoutException)as e:
            continue

        
        time.sleep(5)
        
        assignmentPageSoup = BeautifulSoup(driver.page_source, 'html.parser')
        upA = BeautifulSoup(str(assignmentPageSoup.find("div", {"id": "assignment_group_upcoming_assignments"})), 'html.parser')

        print("\n")
        print(course)
        print(upA)
        print("\n")
        
        upAList = upA.find_all("div", {"id": re.compile('^assignment_\d+')})#assignment_97613 #assignment_[0-9]{3,5}




        
        for assignment in upAList:
            assignmentLinks.append(assignment.a['href'])
            print(assignment.a['href'])

            
        overDueA=BeautifulSoup(str(assignmentPageSoup.find("div", {"id": "assignment_group_overdue"})), 'html.parser')
        overDueAList=overDueA.find_all("div", {"id": re.compile('assignment_[0-9]{3,5}')})
        for assignment in overDueAList:
            assignmentLinks.append(assignment.a['href'])
            print(assignment.a['href'])
    return assignmentLinks

    # assignments = []

    # for link in assignmentLinks:
    #     a = assignment(link, driver)
    #     assignments.append(a)
    #     print(a)

    # print("if you just got an index out of bounds error that means that assignmentLinks was not populated - i think it may have to do with headless mode - i didnt get this issue when headless was False")


# def cleanAssignments(assignments):

#     file = open("cleanAssignments.txt", "w")

#     for a in assignments:
#         print(str(a))
#         file.write(str(a.assignmentInfo()))

#     file.close()


def getEasyReadTime(date):
    temp = date.split(",")
    days = ""
    hours = ""
    minutes = ""
    notDays = ""

    if(len(temp) == 1):
        notDays = temp[0]
        hours = notDays[0:notDays.index(":")]
        minutes = notDays[notDays.index(":") + 1:notDays.index(":") + 3]
    else:
        notDays = temp[1]
        days = temp[0]
        hours = notDays[0:notDays.index(":")]
        minutes = notDays[notDays.index(":") + 1:notDays.index(":") + 3]

    hours = int(hours)
    minutes = int(minutes)

    easyReadTimeRemaining = ""
    if(days != ""):
        easyReadTimeRemaining = days + ", "
    if(hours > 0):
        easyReadTimeRemaining = easyReadTimeRemaining + str(hours) + " hours, "
    if(minutes > 0):
        easyReadTimeRemaining = easyReadTimeRemaining + \
            str(minutes) + " minutes"
    return easyReadTimeRemaining


def assignmentList(links):
    assignments = []
    for link in links:
        a = assignment(link, driver)
        assignments.append(a)
   # print(assignments)
    return assignments


def sendAlertIfDue(assignmentList):
    # daily divider - keep track of recent notifications more easily
    d = datetime.now()
    email_alert("", "________________" + d.strftime("%d") + "/" + d.strftime("%m") + "________________")
    time.sleep(5)

    # # file = open("cleanAssignments.txt", "r")
    # assignments = file.readlines()
    # file.close()

    assignmentProperties = []

    for assignment in assignmentList:
        print(assignment)

    for assignment in assignmentList:
        if((assignment.delta) <= timedelta(days=7)):
            time.sleep(1)


            print(len(str(assignment)) + len(assignment.assignmentUrl()) +len(assignment.assignmentName()))
            
            if(len(str(assignment)) + len(assignment.assignmentUrl()) +len(assignment.assignmentName()) > 150):
                body = str(assignment)
                email_alert(assignment.assignmentName(), body)
                time.sleep(1)
                email_alert("",assignment.assignmentUrl())
                print("done")
            else:  
                body = str(assignment) +" " + assignment.assignmentUrl()
                email_alert(assignment.assignmentName(), body)
                print("done")











