import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from tkinter import *
from tkinter.ttk import *
from functools import partial

import json

import csv

import concurrent.futures

from time import sleep

class ISISWebdriver():
    def __init__(self, url, user_agend):
        self.url = url
        self.ua = user_agend
        self.userName = None
        self.pw = None
        self.isLoggedIn = False
        self.data = {}
        self.driver = self.getDriver()

    def getDriver(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'----user-agent={self.ua}')
        #chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(executable_path="C:\SeleniumDrivers\chromedriver.exe", options=chrome_options)
        return driver

    def setLogin(self):
        self.userName = self.entry_name.get()
        self.pw = self.entry_pw.get()
        self.master.destroy()

    def setLoginData(self):
        self.master = Tk()
        self.master.geometry("900x400")
        label_front = Label(self.master, text="Geben Sie bitte ihre Isis login Daten ein")
        label_front.config(font=("Courier", 25))
        label_front.pack(pady=30)

        label_name = Label(self.master, text="Username")
        label_name.pack()

        self.entry_name = Entry(self.master)
        self.entry_name.pack()

        label_pw = Label(self.master, text="Password")
        label_pw.pack()

        self.entry_pw = Entry(self.master)
        self.entry_pw.pack()

        button_save = Button(self.master, text="submit", command = self.setLogin)
        button_save.pack()
        mainloop()

    def login(self):
        self.setLoginData()

        try:

            self.driver.get(self.url)
            time.sleep(2)
            tu_login_btn = self.driver.find_element_by_id("shibbolethbutton")
            tu_login_btn.submit()
            time.sleep(2)

            username = self.driver.find_element_by_name("j_username")
            username.send_keys(self.userName)
            time.sleep(2)
            pwd = self.driver.find_element_by_name("j_password")
            pwd.send_keys(self.pw)
            time.sleep(2)

            submit_login = self.driver.find_element_by_id("login-button")
            submit_login.click()

            time.sleep(3)
            if self.driver.current_url == "https://isis.tu-berlin.de/my/":
                self.userName = None
                self.pw = None
                self.isLoggedIn = True

        except:
            self.setLoginData()


    def search_course(self, course):
        search_box = self.driver.find_element_by_id("navsearchbox")
        search_box.send_keys(course)
        search_box.submit()
        time.sleep(4)

        search_result = self.driver.find_element_by_class_name("aalink")
        search_result.click()

        self.course = {course:{"name":course,"link":self.driver.current_url}}
        self.courseName = course
        time.sleep(3)




    def getData(self):
        time.sleep(2)
        title = self.driver.find_element_by_class_name("discussionname")
        title = title.text
        content = self.driver.find_elements_by_class_name("post-content-container")
        links = self.driver.find_elements_by_class_name("btn.btn-link")
        #print(links[0].get_property('attributes')[0])
        messages = []
        counter = 0

        for message in content:
            messages.append({"text":message.text,"answers_in_thread":len(content),"tutor_answer_in_thread":"","link": links[counter].get_attribute('baseURI')})
            counter += 1
        data = {'title': title, 'posts': messages}
        self.driver.back()
        return data


    def clickLink(self):
        time.sleep(3)
        forum = self.course[self.courseName]["forum"]
        counter = 0
        for f in forum:
            #link = self.driver.find_element_by_link_text(f["name"])
            link = self.driver.get(f["link"])
            #link.click()
            time.sleep(3)

            liste = self.driver.find_elements_by_class_name("w-100.h-100.d-block")

            self.course[self.courseName]["forum"][counter]["entry"] = []
            for i in range(len(liste)):
                time.sleep(3)
                liste = crowler.driver.find_elements_by_class_name("w-100.h-100.d-block")
                liste[i].click()
                self.course[self.courseName]["forum"][counter]["entry"].append(self.getData())
                time.sleep(2)

            self.driver.back()
            counter += 1

    def getForenFromCourse(self,key):
        allActivities = self.driver.find_elements_by_class_name("aalink")

        self.course[key]["forum"] = []

        for activities in allActivities:
            ac_link = activities.get_attribute('href')

            if "forum" in ac_link:
                ac_name = activities.find_element_by_class_name("instancename").text
                self.course[key]["forum"].append({"name":ac_name,"link":ac_link})



if __name__ == "__main__":
    url = "https://www.isis.tu-berlin.de"
    user_agend = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    #course = "IntroProg"
    #foren = ["Nachrichtenforum","C-Kurs","Offenes Forum","IntroProg"]

    course = ["WS 19/20 ODS Einführung in die Programmierung"]

    #foren = ["C-Kurs", "Offenes Forum", "Häufig gestellte Fragen und technische Fragen zu Hausaufgaben und Vorlesungen im Semester","Nachrichtenforum"]
    crowl_data = {}
    crowler = ISISWebdriver(url, user_agend)

    while crowler.isLoggedIn == False:
        crowler.login()

    for course in course:
        crowl_data[course] = {}
        crowler.search_course(course)
        crowler.getForenFromCourse(course)
        crowler.clickLink()
        crowl_data[course] = crowler.course

    with open('dataISIS.json', 'w') as outfile:
        json.dump(crowl_data, outfile)

    print("JSON Created ................")



