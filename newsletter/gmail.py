from parsel import Selector
from time import sleep
from selenium.webdriver.common.keys import Keys
import os


from driver_manager import get_driver
from newsletter.commands import press_ctrl_enter, press_tab

def to_gmail():
    driver = get_driver()
    driver.get("https://mail.google.com/")
    login()

def login():
    driver = get_driver()
    # LOGIN
    username = driver.find_element_by_name("identifier")
    email = input("Email: ")
    username.send_keys(email)
    sleep(1.5)

    next_button = driver.find_element_by_id("identifierNext")
    next_button.click()
    sleep(5)

    username = driver.find_element_by_name("password")
    passw = input("Password: ")
    username.send_keys(passw)
    sleep(1.5)

    next_button = driver.find_element_by_id("passwordNext")
    next_button.click()
    sleep(15)

def new_mail():
    driver = get_driver()
    # NEW MAIL
    new_mail = driver.find_elements_by_class_name("T-I.J-J5-Ji.T-I-KE.L3")[0]
    new_mail.click()
    sleep(5)

def select_to_mail():
    driver = get_driver()
    to_button = driver.find_elements_by_xpath("//td[contains(concat(' ', @class, ' '), ' eV ')]/div[contains(concat(' ', @class, ' '), ' oj ')]/div[contains(concat(' ', @class, ' '), ' wO nr l1 ')]")[0]
    to_button.click()
    sleep(0.1)

def set_to_mail(to_mail):
    select_to_mail()

    driver = get_driver()
    success = False
    for i,t in enumerate(driver.find_elements_by_tag_name("textarea")):
        try:
            t.send_keys(to_mail)
            sleep(1)
            success = True
        except Exception as err:
            pass
    assert success, "Failed to input to"


def select_subject():
    driver = get_driver()
    # SUBJECT FIELD
    subject_button = driver.find_elements_by_xpath("//td[contains(concat(' ', @class, ' '), ' eV ')]/div[contains(concat(' ', @class, ' '), ' oj ')]/div[contains(concat(' ', @class, ' '), ' wO nr l1 ')]")[0]
    subject_button.click()
    sleep(0.1)

def set_subject(subject):
    select_subject()

    driver = get_driver()
    subject_boxes = driver.find_elements_by_name("subjectbox")
    success = False
    for i,t in enumerate(subject_boxes):
        try:
            t.send_keys(subject)
            sleep(1)
            success = True
        except Exception as err:
            pass
    assert success, "Failed to input subject"

def select_body():
    driver = get_driver()
    # BODY FIELD
    body_button = driver.find_element_by_class_name("Am.Al.editable.LW-avf.tS-tW")
    body_button.click()
    sleep(0.1)

def set_body(body):
    driver = get_driver()
    body_button = driver.find_element_by_class_name("Am.Al.editable.LW-avf.tS-tW")
    body_button.click()
    sleep(0.1)
    body_button.send_keys(body)
    sleep(1)

def send_mail_action():
    driver = get_driver()
    # SENDING
    # send_button = driver.find_element_by_class_name("T-I.J-J5-Ji.aoO.v7.T-I-atl.L3")
    # send_button.click()
    press_ctrl_enter()
    sleep(2)

def send_mail(to_mail,subject,body):
    new_mail()
    set_to_mail(to_mail)    
    set_subject(subject)    
    set_body(body)
    send_mail_action()