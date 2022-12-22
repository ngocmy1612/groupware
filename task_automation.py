import re, sys, json, time, random, os
from turtle import st
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
from framework_sample import *
from MN_functions import *

n = random.randint(1,1000)
m = random.randint(1,10000)

def work_diary():
    #Chờ xuất hiện danh sách work
    Logging("+++ WORK DIARY +++")
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["setting_workdiary"])
    Logging("- Setting folder")
    
    Waits.Wait20s_ElementLoaded(data["TASK"]["Work_Diary"]["diary_setting_form"])
    Logging("- Wait add folder")
    input_name = data["TASK"]["Work_Diary"]["folder_name"] + str(n)
    Commands.InputElement(data["TASK"]["Work_Diary"]["input_folder_name"], input_name)
    Logging("- Input Folder name")
    time.sleep(3)
    
    try:
        share_folder()
    except:
        try:
            Commands.Wait10s_ClickElement("//*[@id='getJournalShare']//button[@class='close']")
            Logging("- Close ORG")
        except:
            pass
    
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["button_save"][1])
    Logging("- Save folder")
    time.sleep(3)
    Functions.pop_up(data["TASK"]["Work_Diary"]["org_popup"], data["TASK"]["Work_Diary"]["close_org_popup"])

    time.sleep(2)
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["fol_name"] % str(input_name))
    Logging("=> Add folder successfully")
    TestCase_LogResult(**data["testcase_result"]["work_diary"]["add_folder"]["pass"])

    return input_name

def workdiary_execution():
    try:
        input_name = work_diary()
    except: 
        input_name = None

    if bool(input_name) == True:
        try:
            delete_folder_workdiary(input_name)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Add folder fail")
        TestCase_LogResult(**data["testcase_result"]["work_diary"]["add_folder"]["fail"])

def share_folder():
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["share"])
    Logging("- Click button Share")
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["permit_write"])
    Logging("- Select permit write") 

    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["invite_user"])
    Logging("- Invite user")
    Waits.Wait20s_ElementLoaded(data["TASK"]["Work_Diary"]["list_ORG"])
    Logging("- Organization list")
    time.sleep(2)

    search_user = driver.find_element_by_xpath("//*[@id='getJournalShare']//div[@class='nav-search']//input")
    search_user.send_keys(data["user_name"])
    search_user.send_keys(Keys.ENTER)
    time.sleep(2)

    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["user_1"])
    Logging("- Select user 1")
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["plus_button"])
    Logging("- Add button")
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["button_save"][0])
    Logging("- Save user")

def delete_folder_workdiary(input_name):
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["delete_button"])
    Logging("- Delete button")
    time.sleep(2)
    Commands.Wait10s_ClickElement("//button[contains(.,'OK')]")
    Logging("- Click OK")
    time.sleep(3)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    try:
        Waits.WaitElementLoaded(5, data["TASK"]["Work_Diary"]["fol_name"] % str(input_name))
        Logging("=> Delete folder Fail")
        TestCase_LogResult(**data["testcase_result"]["work_diary"]["delete_folder"]["fail"])
    except:
        Logging("=> Delete folder successfully")
        TestCase_LogResult(**data["testcase_result"]["work_diary"]["delete_folder"]["pass"])

def manage_folders():
    manage_folders = Waits.WaitElementLoaded(5, "//span[contains(.,'Manage Folders ')]")
    manage_folders.location_once_scrolled_into_view
    manage_folders.click()
    Logging("- Manage Folders")

    Waits.Wait10s_ElementLoaded(data["TASK"]["Task_Report"]["task_tab_content"])
    Logging("- Wait add folder")
    task_name = data["TASK"]["Task_Report"]["folder_task"] + str(n)
    Commands.InputElement(data["TASK"]["Task_Report"]["folder_task_name"][0], task_name)
    Logging("- Input Folder name")
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["button_save"][2])
    Logging("- Save folder")
    time.sleep(3)

    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["fol_name"] % str(task_name))
    Logging("=> Create folder successfully")
    TestCase_LogResult(**data["testcase_result"]["task_report"]["add_folder"]["pass"])

    return task_name

def manager_folder_execution():
    try:
        task_name = manage_folders()
    except:
        task_name = None

    if bool(task_name) == True:
        try:
            delete_manage_folder(task_name)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Create folder fail")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["add_folder"]["fail"])

def delete_manage_folder(task_name):
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["delete_button"])
    Logging("- Delete button")
    Commands.Wait10s_ClickElement("//button[contains(.,'OK')]")
    Logging("- Click OK")
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    try:
        Waits.WaitElementLoaded(5,data["TASK"]["Task_Report"]["fol_name"] % str(task_name))
        Logging("=> Delete folder Fail")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["delete_folder"]["fail"])
    except:
        Logging("=> Delete folder successfully")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["delete_folder"]["pass"])

def set_recipients():
    Logging("===========================================================")
    Logging("+++ SET RECIPIENTS +++")

    time.sleep(1)
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["set_recipients"])
    Logging("- Set recipients")
    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["add_button"][0])
    Logging("- Click Add button")
    time.sleep(2)
    input_group = data["TASK"]["Task_Report"]["name_group"] + objects.date_time
    Commands.InputElement(data["TASK"]["Task_Report"]["recipients_group"], input_group)
    Logging("- Input name group")

    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["recipients_ORG"])
    Logging("- View ORG")
    Waits.Wait20s_ElementLoaded(data["TASK"]["Task_Report"]["list_ORG"])
    Logging(">> Organization list")
    time.sleep(2)
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["user_1"])
    Logging(">> Select user 1")
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["plus_button"])
    Logging(">> Add button")
    time.sleep(2)
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["button_save"][0])
    Logging(">> Save user")
    Logging("=> Add recipients successfully")
    time.sleep(3)
    Functions.pop_up(data["TASK"]["Task_Report"]["org_popup"], data["TASK"]["Task_Report"]["close_org_popup"])

    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["button_save"][1])
    Logging("- Save recipients group")
    time.sleep(2)

    find_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//td[contains(., '%s')]" % input_group)))
    if find_list.is_displayed():
        Logging("=> Set recipients successfully")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["set_recipients"]["pass"])
    
    return input_group

def recipient_execution():
    try:
        input_group = set_recipients()
    except:
        input_group = None

    try:
        write_task_report(input_group)
    except:
        Logging(">>>> Cannot continue execution")
        pass

    if bool(input_group) == True:
        try:
            delete_recipients(input_group)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Set recipients fail")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["set_recipients"]["fail"])

def write_task_report(input_group):
    Logging("===========================================================")
    Logging("+++ MY TASK REPORT +++")
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["my_task_report"])
    Logging("- My Task Report")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='report-list']")))
    Commands.Wait10s_ClickElement(data["write_button"][0])
    Logging("- Click button write")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["TASK"]["Task_Report"]["wait_editor"])))

    title = data["TASK"]["Task_Report"]["task_title"] + objects.date_time
    Commands.InputElement(data["TASK"]["Task_Report"]["input_title"], title)
    Logging("- Input title")

    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["recipients"])
    Logging("- Select Recipients")
    try:
        Commands.Wait10s_ClickElement("//option[contains(., '%s')]" % input_group)
        Logging("- Select default recipients")
    except:
        Logging("==> Don't have default recipients")
        Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["organization"])
        Logging("- Select recipients from org")
        Waits.Wait20s_ElementLoaded(data["TASK"]["Task_Report"]["list_ORG"])
        Logging(">> Organization list")
        time.sleep(2)
        Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["user_1"])
        Logging(">> Select user")
        Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["plus_button"])
        Logging(">> Add button")
        Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["button_save"][0])
        Logging(">> Save user")
        time.sleep(2)
        Functions.pop_up(data["TASK"]["Task_Report"]["org_popup"], data["TASK"]["Task_Report"]["close_org_popup"])
        
    frame_task = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='tox-edit-area__iframe']")))
    driver.switch_to.frame(frame_task)
    content = driver.find_element_by_xpath("//body[@id='tinymce']/p")
    content.clear()
    content.send_keys(data["TASK"]["Task_Report"]["task_content"] + objects.date_time)
    driver.switch_to.default_content()
    Logging("- Input content successfully")
    
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["button_save"][2])
    Logging("- Save Task Report")
    Commands.Wait10s_ClickElement("//button[contains(.,'OK')]")
    Logging("- Click button OK")
    time.sleep(3)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='report-view']")))
        time.sleep(3)
        Logging("=> Task Report save successfully")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["write_task"]["pass"])
    except:
        Logging("=> Task Report save fail")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["write_task"]["fail"])

def delete_recipients(input_group):
    time.sleep(3)
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["set_recipients"])

    Waits.Wait10s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    Commands.Wait10s_ClickElement("//td[contains(., '%s')]/following-sibling::td//a[contains(@data-ng-click, 'del(item.id)')]" % input_group)
    time.sleep(2)
    Logging("- Delete Recipients")
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["button_OK"])
    Logging("- Click OK")
    time.sleep(3)
    Functions.pop_up(data["title_popup"], data["close_popup"])

def create_folder():
    Logging("- Create folder to add auto-sort")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='task-tab-content']")))
    Logging("- Wait add folder")
    task_name = data["TASK"]["Task_Report"]["folder_task"] + str(n)
    Commands.InputElement(data["TASK"]["Task_Report"]["folder_task_name"][1], task_name)
    Logging("- Input Folder name")
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["button_save"][2])
    Logging("- Save folder")
    time.sleep(2)

def auto_sort():
    Logging("===========================================================")
    Logging("+++ Auto-Sort +++")
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["auto_sort"])
    Logging("- Auto Sort")
    time.sleep(3)
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["add_button"][1])
    Logging("- Click add button")

    try:
        error = driver.find_element_by_xpath("//div//button[contains(@ng-click, 'cancel(false)')]")
        Logging("- There is no folder to add auto-sort")
        if error.is_displayed():
            error.click()
            create_folder()
            time.sleep(2)
            auto_sort()
            time.sleep(2)
        else:
            Logging(">>>> Cannot continue execution")
    except WebDriverException:
        create_auto_sort()

def create_auto_sort():
    name_sort = data["TASK"]["Task_Report"]["word_sort"] + str(m)
    Commands.Wait10s_InputElement(data["TASK"]["Task_Report"]["input_word"], name_sort)
    Logging("- Input word sort")
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["button_save"][2])
    Logging("- Save auto sort")

    auto_sort_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//td[contains(., '%s')]" % name_sort)))
    if auto_sort_name.is_displayed():
        Logging("=> Create Auto_sort Successfully")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["add_auto_sort"]["pass"])
    else:
        Logging("=> Create Auto_sort Fail")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["add_auto_sort"]["fail"])
    
    time.sleep(3)
    auto_sort_name.click()
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["delete_auto"])
    Logging("- Delete auto_sort")
    Commands.Wait10s_ClickElement("//button[contains(.,'OK')]")
    Logging("- Click button OK")
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//td[contains(., '%s')]" % name_sort)))
        Logging("=> Delete Auto_sort Fail")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["delete_auto_sort"]["fail"])
    except WebDriverException:
        Logging("=> Delete Auto_sort Successfully")
        TestCase_LogResult(**data["testcase_result"]["task_report"]["delete_auto_sort"]["pass"])

def task_report():
    Logging("===========================================================")
    Logging("+++ TASK REPORT +++")
    Commands.Wait10s_ClickElement(data["TASK"]["Work_Diary"]["hidden_workdiary"])
    Logging("- Hidden Work Diary")
    time.sleep(2)
    Commands.Wait10s_ClickElement(data["TASK"]["Task_Report"]["open_taskreport"])
    Logging("- Open Task Report")
    
    try:
        manager_folder_execution()
    except:
        Logging(">>>> Cannot continue execution")

    try:
        recipient_execution()
    except:
        Logging(">>>> Cannot continue execution")

    try:
        auto_sort()
    except:
        Logging(">>>> Cannot continue execution")
    
def task(domain_name):
    driver.get(domain_name + "/task/diary/list/pdefault/")
    time.sleep(3)
    Logging("================================================= TASK =======================================================")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='diary-list']")))

    try:
        workdiary_execution()
    except:
        Logging(">>>> Cannot continue excution")

    try:
        task_report()
    except:
        Logging(">>>> Cannot continue excution")
    
