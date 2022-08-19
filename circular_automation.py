import re, sys, json
import time, random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from random import choice
from pathlib import Path
import os
from framework_sample import *

from MN_functions import *

n = random.randint(1,1000)
m = random.randint(1,10000)

def circular(domain_name):
    Logging("================================================= CIRCULAR =======================================================")
    driver.get(domain_name + "/circular/list/received/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "message-list")))

    circular_execution()
    time.sleep(3)

def circular_folder():
    Commands.ClickElement(data["CIRCULAR"]["setting"])
    Logging("- Setting Circular")

    Waits.Wait20s_ElementLoaded(data["CIRCULAR"]["add_folder"])
    time.sleep(2)
    Logging("- Add folder")
    parent_name = data["CIRCULAR"]["parent_folder"] + objects.date_time
    Commands.InputElement(data["CIRCULAR"]["folder_name"], parent_name)
    Logging("- Input folder name")
    time.sleep(1)

    Commands.Wait10s_ClickElement(data["CIRCULAR"]["button_save"])
    Logging("- Save Parent Folder")
    time.sleep(3)

    Commands.Wait10s_ClickElement(data["CIRCULAR"]["add_fol"] % parent_name)
    Logging("=> Add folder circular Successfully")
    TestCase_LogResult(**data["testcase_result"]["circular"]["add_folder"]["pass"])

    return parent_name

def circular_execution():
    try:
        parent_name = circular_folder()
    except:
        parent_name = None

    if bool(parent_name) == True:
        try:
            delete_folder(parent_name)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Add folder circular Fail")
        TestCase_LogResult(**data["testcase_result"]["circular"]["add_folder"]["fail"])

def delete_folder(parent_name):
    Commands.ClickElement(data["CIRCULAR"]["delete_button"])
    Logging("- Delete folder")
    Commands.Wait10s_ClickElement(data["CIRCULAR"]["button_OK"])
    Logging("- Click button OK")
    time.sleep(3)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    try:
        Waits.WaitElementLoaded(5,  data["CIRCULAR"]["folder_update"] % parent_name)
        Logging("=> Delete folder Fail")
        TestCase_LogResult(**data["testcase_result"]["circular"]["delete_folder"]["fail"])
    except:
        Logging("=> Delete folder Successfully")
        TestCase_LogResult(**data["testcase_result"]["circular"]["delete_folder"]["pass"])



