import re, sys, json
import time, random#, testlink
from selenium import webdriver
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

from MN_functions import driver, data, ValidateFailResultAndSystem, Logging, TestCase_LogResult#, #TestlinkResult_Fail, #TestlinkResult_Pass

n = random.randint(1,1000)
m = random.randint(1,10000)

#chrome_path = os.path.dirname(Path(__file__).absolute())+"\\chromedriver.exe"
#result=open(os.path.dirname(Path(__file__).absolute())+'\\result.txt','a')

def circular(domain_name):
    Logging("================================================= CIRCULAR =======================================================")
    driver.get(domain_name + "/circular/list/received/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "message-list")))

    circular_execution()
    time.sleep(3)

def circular_folder():
    driver.find_element_by_xpath("//span[contains(., ' Settings')]").click()
    Logging("- Setting Circular")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["CIRCULAR"]["add_folder"])))
    time.sleep(2)
    Logging("- Add folder")
    parent_name = data["CIRCULAR"]["parent_folder"] + str(n)
    driver.find_element_by_xpath(data["CIRCULAR"]["folder_name"]).send_keys(parent_name)
    Logging("- Input folder name")
    time.sleep(1)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["CIRCULAR"]["button_save"]))).click()
    Logging("- Save Parent Folder")
    time.sleep(3)

    folder_circular = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//circular-tree-folder//ul[@class='dynatree-container']//li//a[contains(., '" + parent_name + "')]")))
    folder_circular.click()
    Logging("=> Add folder circular Successfully")
    TestCase_LogResult(**data["testcase_result"]["circular"]["add_folder"]["pass"])
    #TestlinkResult_Pass("WUI-142")

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
            pass
    else:
        Logging("=> Add folder circular Fail")
        TestCase_LogResult(**data["testcase_result"]["circular"]["add_folder"]["fail"])
        #TestlinkResult_Fail("WUI-142")

def delete_folder(parent_name):
    driver.find_element_by_xpath(data["CIRCULAR"]["delete_button"]).click()
    Logging("- Delete folder")
    driver.find_element_by_xpath(data["CIRCULAR"]["button_OK"]).click()
    Logging("- Click button OK")
    time.sleep(3)

    try:
        folder_update = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//circular-tree-folder//ul[@class='dynatree-container']//li//a[contains(., '" + parent_name + "')]")))
        Logging("=> Delete folder Fail")
        TestCase_LogResult(**data["testcase_result"]["circular"]["delete_folder"]["fail"])
        #ValidateFailResultAndSystem("<div>[Circular] Delete folder Fail</div>")
        #TestlinkResult_Fail("WUI-143")
    except:
        Logging("=> Delete folder Successfully")
        TestCase_LogResult(**data["testcase_result"]["circular"]["delete_folder"]["pass"])
        #TestlinkResult_Pass("WUI-143")



