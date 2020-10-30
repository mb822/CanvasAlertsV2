import smtplib
from email.message import EmailMessage
import os.path
from os import path
import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
import time
import os
import sys
#"pip3 install secure-smtplib"
# bs4 mac terminal command: "pip3 install beautifulsoup4"
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
from datetime import timezone
import json
import pytz
from datetime import timedelta


class assignment:

    def __init__(self, link, driver):

        self.url = link
        self.link = str(link[0:29] + "api/v1/" +
                        link[29:len(link)])
        self.driver = driver
        self.driver.get(self.link)
        self.pageSource = driver.find_element_by_xpath(
            "/html/body/pre").text[9:]
        self.pageJson = json.loads(str(self.pageSource))
        temp = self.pageJson['due_at']
        tempDate = datetime.strptime(temp, '%Y-%m-%dT%H:%M:%SZ')
        oldZone = pytz.timezone("Zulu")
        newZone = pytz.timezone("US/Eastern")
        localTimeS = oldZone.localize(tempDate)
        self.dueDate = localTimeS.astimezone(newZone)
        self.delta = self.dueDate - datetime.now(timezone.utc)
        self.name = self.pageJson['name']
        self.courseId = self.pageJson['course_id']
        self.points = self.pageJson['points_possible']
        self.assignmentId = self.pageJson['assignment_group_id']

    def calcDelta(self):
        self.delta = self.dueDate - datetime.now(timezone.utc)
        return self.delta

    def __str__(self):
        date = str(self.delta)
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
        if(days!=""):
            easyReadTimeRemaining = days + ", "
        if(hours > 0):
           easyReadTimeRemaining = easyReadTimeRemaining + str(hours) + " hours, "
        if(minutes > 0):
            easyReadTimeRemaining = easyReadTimeRemaining + str(minutes) + " minutes"

        
        return "DUE IN: " + easyReadTimeRemaining

    def assignmentName(self):
        return self.name
    def assignmentUrl(self):
        return self.url

    def assignmentInfo(self):
        info = str(self.assignmentId) + ", " + str(self.name) + \
            ", " + str(self.dueDate) + ", " + str(self.points) + \
            ", " + str(self.link) + ", " + str(self.courseId)
        return info


# PATH = os.path.join(sys.path[0], "chromedriver")
# options = webdriver.ChromeOptions()
# options.add_argument('--lang=en_US')
# options.headless = False
# options.detach = True
# driver = webdriver.Chrome(PATH, options=options)
# # driver.get("http://njit.instructure.com/login/saml")

# # username = driver.find_element_by_name("j_username")
# # Password = driver.find_element_by_name("j_password")

# # username.send_keys("kj323")
# # Password.send_keys("inf@#123UCID+_")

# # username.send_keys(Keys.RETURN)

# # checkbox = driver.find_element_by_id("accept")
# # checkbox.click()
# # accept = driver.find_element_by_id("submitbtn")
# # accept.click()


# # links = ["https://njit.instructure.com/courses/14901/assignments/92908",
# #          "https://njit.instructure.com/courses/13721/assignments/88626"]
# # a = assignment(
# #     "https://njit.instructure.com/courses/14901/assignments/92908", driver)
# # links = assignmentLinks()
# # lis = assignmentList(links)
# # # l = []
# # # for link in links:
# # #     a = assignment(link, driver)
# #     l.append(a)

# for assign in lis:
#     print(assign)
