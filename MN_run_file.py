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

import MN_functions,comanage_automation, board_automation, task_automation, circular_automation, expense_automation
from MN_functions import *

def My_Execution(domain_name):
    MN_functions.access_qa(domain_name)
    MN_functions.close_pop_up()
    
    try:
        task_automation.task(domain_name)
    except:
        Logging(">>>> Cannot continue execution")

    # try:
    #     expense_automation.expense(domain_name)
    # except:
    #     Logging(">>>> Cannot continue execution")

    # try:
    #     comanage_automation.comanage(domain_name)
    # except:
    #     Logging(">>>> Cannot continue execution")

    # try:
    #     board_automation.board(domain_name)
    # except:
    #     Logging(">>>> Cannot continue execution")

    # try:
    #     circular_automation.circular(domain_name)
    # except:
    #     Logging(">>>> Cannot continue execution")

My_Execution("http://tg01.hanbiro.net/ngw/app/#")



# def clockout_function():
#     out = clockout.text
#     status = statusclockout.text

#     clock_out = {
#         "time" : out,
#         "stat" : status
#     }

#     return clock_out
