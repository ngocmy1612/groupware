import re, sys, json, unittest
import time, random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
from MN_functions import driver, data, ValidateFailResultAndSystem, Logging, TestCase_LogResult

n = random.randint(1,1000)
m = random.randint(1,10000)

def kanban(admin_account):
    time.sleep(3)
    try:
        project = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["project_list"]))).click()
        Logging("- Open project")
        project = True
    except:
        Logging("- No project")
        if admin_account == True:
            create_project()
            project = True
        else:
            project = False
    
    return project

def create_project():
    driver.find_element_by_xpath(data["COMANAGE"]["create_project"]).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["project_template"])))
    project_name = driver.find_element_by_xpath(data["COMANAGE"]["project_name"])
    project_name.send_keys("Project: " + str(n))

    driver.find_element_by_xpath(data["COMANAGE"]["Kanban_Project"]).click()
    driver.find_element_by_xpath(data["COMANAGE"]["save_project"]).click()

    infor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["wait_bussiness"])))
    if infor.is_displayed():
        Logging(">> Create new project Successfully")
    else:
        Logging(">> Create new project Fail")
    #create excel file for create new project anf check condition when create project fail
    time.sleep(2)
    driver.find_element_by_xpath(data["COMANAGE"]["add_leader"]).click()
    time.sleep(5)

    search_leader = driver.find_element_by_xpath(data["COMANAGE"]["search_leader"])
    search_leader.send_keys("a")
    search_leader.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_xpath(data["COMANAGE"]["user1"]).click()
    driver.find_element_by_xpath(data["COMANAGE"]["user2"]).click()
    driver.find_element_by_xpath(data["COMANAGE"]["button_add"]).click()
    driver.find_element_by_xpath(data["COMANAGE"]["save_leader"]).click()
    time.sleep(3)
    driver.find_element_by_xpath(data["COMANAGE"]["board"]).click()

def run_project(admin_account):
    project = kanban(admin_account)
    if project == True:
        try:
            insert_work()
        except:
            Logging(">>>> Cannot continue excution")
            pass

        try:
            work_list()
        except:
            Logging(">>>> Cannot continue excution")
            pass
    else:
        pass

def insert_work():
    #Insert work
    time.sleep(5)
    try:
        driver.find_element_by_xpath(data["COMANAGE"]["search_work"])
        close_search = driver.find_element_by_xpath(data["COMANAGE"]["close_search"])
        if close_search.is_displayed():
            close_search.click()
            Logging("- Close search")
    except:
        Logging(" ")

    time.sleep(3)
    insert_work_name = data["COMANAGE"]["insert_ticket"] + str(m)
    insert_work = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["frame_work"])))
    driver.switch_to.frame(insert_work)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["insert_frame"])))
    insert = driver.find_element_by_xpath(data["COMANAGE"]["insert"])
    insert.send_keys(insert_work_name)
    Logging("- Input work name")
    insert.send_keys(Keys.RETURN)
    Logging("- Insert Work")
    driver.switch_to.default_content()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))

    #Search work
    time.sleep(3)
    search_work = driver.find_element_by_xpath(data["COMANAGE"]["search_work"])
    search_work.send_keys(insert_work_name)
    search_work.send_keys(Keys.ENTER)
    Logging("- Search work")
    time.sleep(5)
    driver.find_element_by_xpath(data["COMANAGE"]["view_ticket"]).click()
    Logging("- View ticket")
    time.sleep(3)
    detail = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["detail_work"])))
    if detail.is_displayed():
        Logging("=> View work successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work"]["pass"])
        title_work = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "work-subject")))
        if insert_work_name == title_work.text:
            Logging("=> Insert work successfully")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["insert_work"]["pass"])
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["search_work"]["pass"])
        else:
            Logging("=> Insert work fail")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["insert_work"]["fail"])
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["search_work"]["fail"])
    else:
        Logging("=> View work fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work"]["fail"])

    update_work()
    driver.find_element_by_xpath(data["COMANAGE"]["close_detail_work"]).click()
    Logging("- Close detail work")
    time.sleep(2)
    driver.find_element_by_xpath(data["COMANAGE"]["close_search"]).click()
    Logging("- Close search work")

def update_work():
    driver.find_element_by_xpath(data["COMANAGE"]["show_more"]).click()
    Logging("- Show more")
    Logging("")

    try:
        update_status()   
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        update_work_type()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        update_assigned_to()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        update_priority()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        update_date()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        write_comment() 
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass

def update_status():
    #Select status
    start_status = driver.find_element_by_xpath(data["COMANAGE"]["start_status"])
    #Logging(start_status.text)
    driver.find_element_by_xpath(data["COMANAGE"]["status"]).click()
    Logging("- Update status")
    status_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["status_list"])))
    
    
    list_status = []
    i=0
    for i in range(status_list):
        i += 1
        status = driver.find_element_by_xpath("//ul[@class='dropdown-menu']/li[@class='dropdown-item']" + "[" + str(i) + "]/span[@class='status-item']")
        if status.text != start_status.text:
            list_status.append(status.text)
        else:
            continue

    Logging("- Total of status: " + str(len(list_status)))
    #Logging(list_status)

    x = random.choice(list_status)
    time.sleep(1)
    status_label = driver.find_element_by_xpath("//span[contains(@class, 'status-item') and contains(., '" + str(x) + "')]")
    status_label.click()
    Logging("- Select status")

    time.sleep(3)
    start_status_update = driver.find_element_by_xpath(data["COMANAGE"]["start_status"])
    if start_status_update.text == str(x):
        Logging("=> Update status successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_status"]["pass"])
    else:
        Logging("=> Update status fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_status"]["fail"])

def update_work_type():
    #Select work type
    start_work_type = driver.find_element_by_xpath(data["COMANAGE"]["start_work_type"])
    #Logging(start_work_type.text)
    driver.find_element_by_xpath(data["COMANAGE"]["work_type"]).click()
    Logging("- Update Work type")
    work_type_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["work_type_list"])))
    
    list_work_type = []
    i=0
    for i in range(work_type_list):
        i += 1
        work_type = driver.find_element_by_xpath("//div[@class='clearfix project-new-work']/div[2]//div/ul/li" + "[" + str(i) + "]/a")
        if work_type.text != start_work_type.text:
            list_work_type.append(work_type.text)
        else:
            continue

    Logging("- Total of work type: " +  str(len(list_work_type)))
    #Logging(list_work_type)

    x = random.choice(list_work_type)
    time.sleep(1)
    work_type_label = driver.find_element_by_xpath("//div[contains(@title, 'Work type')]/following-sibling::div/div/ul/li/a[contains(., '" + str(x) + "')]")
    work_type_label.click()
    Logging("- Select work type")

    time.sleep(3)
    start_work_type_update = driver.find_element_by_xpath(data["COMANAGE"]["start_work_type"])
    if start_work_type_update.text == str(x):
        Logging("=> Update work type successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_work_type"]["pass"])
    else:
        Logging("=> Update work type fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_work_type"]["fail"])

def update_assigned_to():
    #Select assigned to
    start_assign = driver.find_element_by_xpath(data["COMANAGE"]["start_assign"])
    #Logging(start_assign.text)
    driver.find_element_by_xpath(data["COMANAGE"]["assigned_to"]).click()
    Logging("- Assigned to")
    time.sleep(3)
    assign_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["assign_list"])))

    list_assign = []
    i=0
    y=1
    for i in range(assign_list):
        i += 1
        y += 1
        assign = driver.find_element_by_xpath("//ul[@class='dropdown-menu']/li" + "[" + str(y) + "]/a[@class='member assignee']/span")
        if assign.text != start_assign.text:
            list_assign.append(assign.text)
        else:
            continue

    Logging("- Total of assign: " + str(len(list_assign)))
    #Logging(list_assign)

    x = random.choice(list_assign)
    time.sleep(1)
    assign_label = driver.find_element_by_xpath("//div[contains(@title, 'Assigned to')]/following-sibling::div//li/a/span[contains(., '" + str(x) + "')]")
    assign_label.click()
    Logging("- Select user")
    
    time.sleep(3)
    start_assign_update = driver.find_element_by_xpath(data["COMANAGE"]["start_assign"])
    if start_assign_update.text == str(x):
        Logging("=> Update assigned to successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_assigned_to"]["pass"])
    else:
        Logging("=> Update assigned to fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_assigned_to"]["fail"])

def update_priority():
    #Select priority
    start_priority = driver.find_element_by_xpath(data["COMANAGE"]["start_priority"])
    #Logging(start_priority.text)
    driver.find_element_by_xpath(data["COMANAGE"]["priority"]).click()
    Logging("- Update priority")
    time.sleep(2)
    priority_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["priority_list"])))
    
    list_priority = []
    i=0
    for i in range(priority_list):
        i += 1
        priority = driver.find_element_by_xpath("//div[@class='clearfix project-new-work']/div[4]//div/ul/li/a" + "[" + str(i) + "]")
        if priority.text != start_priority.text:
            list_priority.append(priority.text)
        else:
            continue

    Logging("- Total of priority: "+ str(len(list_priority)))
    #Logging(list_priority)

    x = random.choice(list_priority)
    time.sleep(2)
    if str(x) == "Low":
        priority_label = driver.find_element_by_xpath("//div[@id='priority_tooltip']/following-sibling::div//li/a[2]/span")
        time.sleep(2)
        priority_label.click()
        Logging("- Select priority")
    else:
        priority_label = driver.find_element_by_xpath("//div[@id='priority_tooltip']/following-sibling::div//li/a/span[contains(., '" + str(x) + "')]")
        time.sleep(2)
        priority_label.click()
        Logging("- Select priority")
    
    time.sleep(3)
    start_priority_update = driver.find_element_by_xpath(data["COMANAGE"]["start_priority"])
    if start_priority_update.text == str(x):
        Logging("=> Update priority successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_priority"]["pass"])
    else:
        Logging("=> Update priority fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_priority"]["fail"])

def update_date():
    #Select start date, end date
    driver.find_element_by_id("workStartDate").click()
    Logging("- Start date")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["start_date"]))).click()
    Logging("- Select start date")
    driver.find_element_by_id("workDueDate").click()
    Logging("- End date")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["end_date"]))).click()
    Logging("- Select end date")

    #Input Description
    driver.find_element_by_id("work-content").click()
    time.sleep(2)
    insert_work = driver.find_element_by_xpath(data["COMANAGE"]["frame_work_detail"])
    driver.switch_to.frame(insert_work)
    insert = driver.find_element_by_xpath(data["COMANAGE"]["insert"])
    insert.clear()
    insert.send_keys(data["COMANAGE"]["input_description"])
    Logging("- Input Description")
    driver.switch_to.default_content()
    driver.find_element_by_xpath(data["COMANAGE"]["save"]).click()
    Logging("- Save Description")

def write_comment():
    #Comment
    driver.find_element_by_xpath(data["COMANAGE"]["comment"]).click()
    time.sleep(2)
    insert_comment = driver.find_element_by_xpath(data["COMANAGE"]["frame_work_comment"])
    driver.switch_to.frame(insert_comment)
    input_comment = driver.find_element_by_xpath(data["COMANAGE"]["insert"])
    input_comment.send_keys(data["COMANAGE"]["input_comment"])
    Logging("- Input comment")
    driver.switch_to.default_content()
    driver.find_element_by_xpath(data["COMANAGE"]["save_comment"]).click()
    Logging("- Save comment")
    comment_work = driver.find_element_by_xpath(data["COMANAGE"]["check_comment"])
    if (data["COMANAGE"]["input_comment"]) == comment_work.text:
        Logging("=> Write comment Successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["write_comment"]["pass"])
    else:
        Logging("=> Write comment Fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["write_comment"]["fail"])

def work_list():
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["wait_load_board"])))

    driver.find_element_by_xpath(data["COMANAGE"]["work_list"]).click()
    Logging("- Work List")
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["wait_load_work"])))
    try:
        filters_work_type()
    except:
        pass

def filters_work_type():
    work_list_counter = driver.find_element_by_xpath(data["COMANAGE"]["total_work_list"])
    Logging("=> Total work list: " + work_list_counter.text)
    work_list_counter_number = int(work_list_counter.text.split(" ")[1])
    #Logging(work_list_counter_number)

    driver.find_element_by_xpath(data["COMANAGE"]["filters"]).click()
    Logging("- Search Filters")
    filter_work_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["filter_work_list"])))

    list_filter_work = []
    i=0

    for i in range(filter_work_list):
        i += 1
        filter_work = driver.find_element_by_xpath(data["COMANAGE"]["filter_work_list"] + "[" + str(i) + "]") 
        list_filter_work.append(filter_work.text)
    
    Logging("- Total filter Work type: "+ str(len(list_filter_work)))
    #Logging(list_filter_work)

    x = random.choice(list_filter_work)
    filter_work_select = driver.find_element_by_xpath("//div[@class='wrap-iframe']//button[contains(@class, 'member') and contains(., '" + str(x) + "')]")
    filter_work_select.click()
    Logging("- Filter Work type")

    #Check filters
    driver.find_element_by_xpath(data["COMANAGE"]["apply_filter"]).click()
    Logging("- Apply filter")

    time.sleep(3)
    work_list_counter_update = driver.find_element_by_xpath(data["COMANAGE"]["total_work_list"])
    work_list_counter_number_update = int(work_list_counter_update.text.split(" ")[1])

    if work_list_counter_number > work_list_counter_number_update:
        Logging("=> Total work list update: " + work_list_counter_update.text)
        Logging("=> Search filter Work type Successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["filters_work_type"]["pass"])
        if work_list_counter_number_update > 0:
            driver.find_element_by_xpath(data["COMANAGE"]["close_filter"]).click()
            Logging("- Close filter")
            driver.find_element_by_xpath(data["COMANAGE"]["view_work"]).click()
            Logging("- View work")
            time.sleep(2)

            detail_work = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["work_content"])))
            if detail_work.is_displayed():
                Logging("=> View work list successfully")
                TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work_list"]["pass"])
                time.sleep(2)
                type_text = driver.find_element_by_xpath(data["COMANAGE"]["type_result"])
                if type_text.text == str(x) == "Sub Task":
                    Logging("=> Correct Work type")
                elif type_text.text == str(x):
                    Logging("=> Correct Work type")
                    driver.find_element_by_xpath(data["COMANAGE"]["sub_work"]).click()
                    Logging("- Create Sub work")
                    sub_name = "Auto Test: Sub work " + str(m)
                    driver.find_element_by_xpath(data["COMANAGE"]["input_sub_work"]).send_keys(sub_name)
                    Logging("- Input Sub work name")
                    driver.find_element_by_xpath(data["COMANAGE"]["save_sub_work"]).click()
                    Logging("- Save Sub work")
                    time.sleep(3)
                    sub_work_title = driver.find_element_by_xpath("//*[@id='collapseSubWorks']//div//p[contains(.,'" + sub_name + "')]")
                    if sub_work_title.is_displayed:
                        Logging("=> Create sub-work successfully")
                        TestCase_LogResult(**data["testcase_result"]["co_manage"]["sub-work"]["pass"])
                    else:
                        Logging("=> Create sub-work fail")
                        TestCase_LogResult(**data["testcase_result"]["co_manage"]["sub-work"]["fail"])
                else:
                    Logging("=> Wrong Work type")

                driver.find_element_by_xpath(data["COMANAGE"]["filters"]).click()
                driver.find_element_by_xpath(data["COMANAGE"]["reset_filter"]).click()
                driver.find_element_by_xpath(data["COMANAGE"]["close_filter"]).click()
            else:
                Logging("=> View work list fail")
                TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work_list"]["fail"])
        else:
            Logging("=> Total filter = 0")
            driver.find_element_by_xpath(data["COMANAGE"]["reset_filter"]).click()
            driver.find_element_by_xpath(data["COMANAGE"]["close_filter"]).click()
    else:
        Logging("=> Total work list update: " + work_list_counter_update.text)
        Logging("=> Search filter Work type Fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["filters_work_type"]["fail"])
    
def drag_drop():
    '''time.sleep(3)
    search_work = driver.find_element_by_xpath(data["COMANAGE"]["search_work"])
    search_work.send_keys("Automation Test: Insert work 737")
    search_work.send_keys(Keys.ENTER)
    Logging("- Search work")'''
    time.sleep(5)
    source = driver.find_element_by_xpath("//*[@id='boardStatus']/div/div/div/div[1]/div[3]/span/div/div[1]/div/div")
    target= driver.find_element_by_xpath("//*[@id='boardStatus']/div/div/div/div[3]/div[2]")
    #action = ActionChains(driver)
    #drag and drop operation and the perform
    webdriver.ActionChains(driver).drag_and_drop(source,target).perform()
    #action.drag_and_drop(source, target).perform()

def write_work():
    try:
        driver.find_element_by_xpath(data["write_button"][2]).click()
        Logging("- Write Work")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tox-editor-header")))
        Logging("check")

        time.sleep(5)
        insert_work_name = data["COMANAGE"]["insert_ticket"] + str(m)
        insert_work = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["frame_work"])))
        driver.switch_to.frame(insert_work)
        test = driver.find_element_by_xpath("//*[@id='tinymce']/p")
        test.send_keys(insert_work_name)
        Logging("- Input work name")
        test.send_keys(Keys.RETURN)
        Logging("- Insert Work")
        driver.switch_to.default_content()



        '''driver.find_element_by_xpath("//form/div[4]/input").send_keys("test")
        Logging("success")'''
    except WebDriverException:
        Logging("- Cannot write work")

def co_manage(domain_name):
    Logging("================================================= CO-MANAGE =======================================================")
    driver.get(domain_name + "/projectnew/project-folder/normal/0_0")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'mCSB') and contains(@id,'container')]//li[contains(@data-category,'projectnew')]//input")))

    try:
        admin_account = driver.find_element_by_xpath("//*[starts-with(@id,'mCSB') and contains (@id,'container')]//li/a[contains(@ng-click,'showAdminSetting($event)')]")
        admin_account = True
        Logging("ADMIN ACCOUNT")
    except:
        admin_account = False
        Logging("USER ACCOUNT")

    return admin_account

def comanage(domain_name):
    admin_account = co_manage(domain_name)
    if admin_account == True:
        run_project(admin_account)
    else:
        run_project(admin_account)

    time.sleep(3)

