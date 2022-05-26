import random
from selenium import webdriver
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from MN_functions import driver

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Yellow(msg):
    '''• Usage: Color msg in yellow'''
    
    string_output = bcolors.WARNING + str(msg) + bcolors.ENDC

    return string_output

def Green(msg):
    '''• Usage: Color msg in green'''
    
    string_output = bcolors.OKGREEN + str(msg) + bcolors.ENDC

    return string_output

def Red(msg):
    '''• Usage: Color msg in red'''
    
    string_output = bcolors.FAIL + str(msg) + bcolors.ENDC

    return string_output

def WaitElementLoaded(time, xpath):
    '''• Usage: Wait until element VISIBLE in a selected time period'''
    
    WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))

def Wait10s_ElementLoaded(xpath):
    '''• Usage: Wait 10s until element VISIBLE'''
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

def WaitElementInvisibility(time, xpath):
    '''• Usage: Wait until element INVISIBLE in a selected time period'''
    
    WebDriverWait(driver, time).until(EC.invisibility_of_element_located((By.XPATH, xpath)))

def Wait10s_ElementInvisibility(xpath):
    '''• Usage: Wait 10s until elementIN VISIBLE'''
    
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, xpath)))

def GetListLength(xpath):
    '''• Usage: Count how many elements are visible
            return a number int()'''

    list_length = int(len(driver.find_elements_by_xpath(xpath)))

    return list_length

def ClickElement(xpath):
    '''• Usage: Do the click on element
            return WebElement'''

    element = driver.find_element_by_xpath(xpath)
    element.click()

    return element

def Wait20s_ClickElement(xpath):
    '''• Usage: Wait until the element visible and do the click
            return WebElement'''

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
    element = driver.find_element_by_xpath(xpath)
    element.click()

    return element

def InputElement(xpath, value):
    '''• Usage: Send key value in input box
            return WebElement'''

    element = driver.find_element_by_xpath(xpath)
    element.send_keys(value)

    return element

def Wait10s_InputElement(xpath, value):
    '''• Usage: Wait until the input box visible and send key value
            return WebElement'''

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    element = driver.find_element_by_xpath(xpath)
    element.send_keys(value)

    return element

def getRandomNumber_fromSpecificRange(assigned_range):
    '''• Usage: Get a list of random numbers
            return a number int()'''

    random_number = random(randint(range(assigned_range)))

    return random_number

def getRandomList_fromSpecificRange(picked_numbers, assigned_range):
    '''• Usage: Get a list of random numbers and remove duplicated number
            return a list()'''

    random_number = random(randint(range(assigned_range)))

    random_list = []
    i=1
    for i in range(assigned_range):
        random_number = random(randint(range(assigned_range)))
        random_list.append(random_number)
        
        random_list = list(dict.fromkeys(random_list))
        if len(random_list) == picked_numbers:
            break
        
        i+=1 

    return random_list

def RemoveDuplicate_fromList(selected_list):
    '''• Usage: Remove duplicated items in the assigned list
            return the assigned list without duplicated item'''
    
    selected_list = list(dict.fromkeys(selected_list))

    return selected_list

def checkIf_ElementVisible(xpath):
    '''• Usage: check element is visible
                return True if element is visible'''
    
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except WebDriverException:
        return False

def waitIf_ElementVisible(xpath):
    '''• Usage: Wait 10s until element is visible
                return True if element is visible'''
    
    try:
        Wait10s_ElementLoaded(xpath)
        return True
    except WebDriverException:
        return False
