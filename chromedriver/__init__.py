from selenium import webdriver
from http.client import CannotSendRequest
from socket import error
from selenium.webdriver.remote.command import Command
import os
import random

CURDIR = os.path.dirname(os.path.abspath(__file__))

class DriverManager():
    def __init__(self):
        self.drivers =  {"main":None}
        self.id = "".join([str(random.randint(0,9)) for i in range(10)])

    def get_driver(self,name=None):
        name = name or "main"
        
        if name not in self.drivers:
            self.drivers[name] = None
        
        if self.drivers[name] is None or not is_alive(self.drivers[name]):
            self.drivers[name] = webdriver.Chrome(os.path.join(CURDIR,"chromedriver.exe"))
        
        return self.drivers[name]

    def close_driver(self,name=None):
        name = name or "main"
        
        if name not in self.drivers:
            pass
        
        elif self.drivers[name] is None:
            pass

        else:
            self.drivers[name].close()
            self.drivers[name] = None

driver_manager = DriverManager()

def get_driver(name=None):
    # print("Driver ID : {}".format(driver_manager.id))
    return driver_manager.get_driver(name)

def close_driver(name=None):
    driver_manager.close_driver(name)


def is_alive(driver):
    try:
        driver.execute(Command.STATUS)
        return True
    except (error, CannotSendRequest):
        return False
