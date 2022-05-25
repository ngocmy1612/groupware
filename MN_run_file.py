import re, sys, json
import time, random#, testlink
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from random import choice
from pathlib import Path
import os

import MN_functions,MN_function,MN_comanage_automation, MN_board_automation, MN_task_automation, MN_circular_automation, MN_expense_automation
from MN_functions import execution_log, fail_log, error_log, Logging, testcase_log, driver

def MyExecution(domain_name):
    error_menu = []
    error_screenshot = []
    
    try:
        MN_functions.access_qa(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_functions.access_qa")
    
    try:
        MN_functions.close_pop_up()
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_functions.close_pop_up")
    
    try:
        MN_task_automation.task(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_task_automation.task")

    try:
        MN_expense_automation.expense(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_expense_automation.expense")

    try:
        MN_comanage_automation.comanage(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_comanage_automation.comanage")

    try:
        MN_newcomanage_automation.comanage(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_comanage_automation.comanage")

    try:
        MN_board_automation.board(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_board_automation.board")

    try:
        MN_circular_automation.circular(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("MN_circular_automation.circular")
    
    ngoc_log = {
        "execution_log": execution_log,
        "fail_log": fail_log,
        "error_log": error_log,
        "error_menu": error_menu
    }

    return ngoc_log

def My_Execution(domain_name):
    MN_functions.access_qa(domain_name)
    MN_functions.close_pop_up()
    try:
        MN_task_automation.task(domain_name)
    except:
        Logging(">>>> Cannot continue execution")
        pass

    try:
        MN_expense_automation.expense(domain_name)
    except:
        Logging(">>>> Cannot continue execution")
        pass

    try:
        MN_comanage_automation.comanage(domain_name)
    except:
        Logging(">>>> Cannot continue execution")
        pass

    try:
        MN_board_automation.board(domain_name)
    except:
        Logging(">>>> Cannot continue execution")
        pass

    try:
        MN_circular_automation.circular(domain_name)
    except:
        Logging(">>>> Cannot continue execution")
        pass

#My_Execution("http://myngoc.hanbiro.net/ngw/app/#")
#My_Execution("https://global3.hanbiro.com/ngw/app/#")

My_Execution("http://qavn.hanbiro.net/ngw/app/#")




def clockout_function():
    out = clockout.text
    status = statusclockout.text

    clock_out = {
        "time" : out,
        "stat" : status
    }

    return clock_out
