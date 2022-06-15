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
from datetime import datetime
import os
import MN_function
from framework_sample import *
from MN_functions import driver, data, ValidateFailResultAndSystem, Logging, TestCase_LogResult

now = datetime.now()
date = now.strftime("%m/%d/%y %H:%M:%S")

n = random.randint(1,1000)
m = random.randint(1,10000)

#chrome_path = os.path.dirname(Path(__file__).absolute())+"\\chromedriver.exe"

def board_page(domain_name):
    Logging("================================================= BOARD =======================================================")
    driver.get(domain_name + "/board/list/comp_0/")
    Waits.Wait20s_ElementLoaded(data["BOARD"]["board_list"])
    Commands.ClickElement(data["BOARD"]["hide_company_board"])
    Logging("- Hide company Board")
    time.sleep(1)

    try:
        admin_account = driver.find_element_by_xpath(data["BOARD"]["admin_account"])
        admin_account = True
        Logging("ADMIN ACCOUNT")
    except:
        admin_account = False
        Logging("USER ACCOUNT")

    return admin_account

def board(domain_name):
    admin_account = board_page(domain_name)
    if admin_account == True:
        try:
            my_folder_execution()
        except:
            Logging(">>>> Cannot continue excution")
            pass

        try:
            board_settings()
        except:
            Logging(">>>> Cannot continue excution")
            pass
    else:
        try:
            my_folder_execution()
        except:
            Logging(">>>> Cannot continue excution")
            pass

    time.sleep(3)

def setting_my_board():
    Commands.ClickElement(data["BOARD"]["SETTING"]["setting"])
    Logging("- Select Settings")

    my_folder_name = "Folder Board: " + str(n)
    Commands.InputElement(data["BOARD"]["SETTING"]["name_folder"], my_folder_name)
    Logging("- Input name my folder board")

    my_folder_type = int(len(driver.find_elements_by_xpath(data["BOARD"]["SETTING"]["my_folder_type"])))

    my_folder_type_list = []
    i = 0
    for i in range(my_folder_type):
        i += 1
        my_type = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["my_type"] + str(i) + "]")
        my_folder_type_list.append(my_type.text)

    x = random.choice(my_folder_type_list)
    Commands.ClickElement(data["BOARD"]["SETTING"]["select_type"] + str(x) + "')]")
    Logging("- Select folder type")
    Commands.ClickElement(data["BOARD"]["SETTING"]["save"][0])
    Logging("- Save my folder board")
    
    information = Waits.Wait10s_ElementLoaded(data["BOARD"]["SETTING"]["information"][0])
    time.sleep(3)
    if information.is_displayed():
        Logging("=> Add my folder board Successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_my_folder"]["pass"])

    Commands.ClickElement(data["BOARD"]["SETTING"]["close_infor"])
    time.sleep(2)

    return my_folder_name,x

def my_folder_execution():
    try:
        my_folder_name,x = setting_my_board()
    except:
        my_folder_name,x = None

    if bool(my_folder_name) == True:
        try:
            write_execution(my_folder_name,x)
        except:
            Logging(">>>> Cannot continue execution")
            pass
        try:
            delete_my_folder(my_folder_name)
        except:
            Logging(">>>> Cannot continue execution")
            pass
    else:
        Logging("=> Add my folder board Fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_my_folder"]["fail"])

def category(my_folder_name):
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    Commands.ClickElement(data["BOARD"]["SETTING"]["my_folder"] + str(my_folder_name) + "')]")
    time.sleep(3)
    Commands.ClickElement(data["BOARD"]["SETTING"]["category"])
    time.sleep(3)
    try:
        manage_categories = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["manage_categories"])
        if manage_categories.is_displayed():
            Logging("=> Display manage categories page")
            category_board = "Category Board: " + str(n)
            manage_categories.send_keys(category_board)
            Commands.ClickElement(data["BOARD"]["SETTING"]["save"][1])
            Logging("- Save category")
            time.sleep(2)
            category_list = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["category_list"] + str(category_board) + "')]")
            if category_list.is_displayed():
                Logging("=> Add manage category successfully")
                TestCase_LogResult(**data["testcase_result"]["board"]["add_category"]["pass"])
    except:
        Logging("=> Fail: Don't display manage categories page")

    driver.refresh()
    return category_board

def write_execution(my_folder_name,x):
    try:
        category_board = category(my_folder_name)
    except:
        category_board = None

    if bool(category_board) == True:
        try:
            write_board(my_folder_name,category_board,x)
        except:
            Logging(">>>> Cannot continue execution")
            pass
    else:
        Logging("=> Add manage category fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_category"]["fail"])

def write_board(my_folder_name,category_board,x):
    Commands.Wait10s_ClickElement(data["BOARD"]["SETTING"]["show_myfolder"])
    time.sleep(3)
    Commands.Wait10s_ClickElement(data["BOARD"]["SETTING"]["select_folder"] + str(my_folder_name) + "')]")
    Logging("- Click my folder board")
    time.sleep(2)

    Commands.ClickElement(data["BOARD"]["SETTING"]["write_board"])
    Waits.Wait20s_ElementLoaded(data["BOARD"]["SETTING"]["wait_page"])
    time.sleep(2)
    Commands.Wait10s_ClickElement(data["BOARD"]["SETTING"]["dropdown_cate"])
    Logging("- Write Board")
    Commands.ClickElement(data["BOARD"]["SETTING"]["select_category"] + str(category_board) + "')]")
    tit_board = "Title of board: " + date
    Commands.InputElement(data["BOARD"]["SETTING"]["title_board"], tit_board)

    frame_board = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tox-edit-area__iframe")))
    driver.switch_to.frame(frame_board)
    content = driver.find_element_by_xpath("//body[@id='tinymce']/p")
    content.clear()
    content.send_keys("This is content of board")
    driver.switch_to.default_content()
    Logging("- Input content successfully")
    Commands.ClickElement(data["BOARD"]["SETTING"]["save"][2])
    Logging("- Save board")
    time.sleep(3)

    board = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["board"])
    if board.text == tit_board:
        Logging("=> Write board successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["write_board"]["pass"])
        Commands.ClickElement(data["BOARD"]["SETTING"]["back_list"])
        Logging("- Back to list board")
        time.sleep(3)
        if str(x) == "Photo Gallery":
            try:
                board_photo_type = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["board_photo_type"])
                if board_photo_type.is_displayed():
                    Logging("=> Correct folder photo type")
            except:
                Logging("=> Wrong folder photo type")
        elif str(x) == "List":
            try:
                board_list_type = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["board_list_type"])
                if board_list_type.is_displayed():
                    Logging("=> Correct folder list type")
            except:
                Logging("=> Wrong folder list type")
    else:
        Logging("=> Write board fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["write_board"]["fail"])

def delete_my_folder(my_folder_name):
    time.sleep(3)
    Commands.ClickElement(data["BOARD"]["SETTING"]["setting"])
    Commands.Wait10s_ClickElement(data["BOARD"]["SETTING"]["my_folder"] + str(my_folder_name) + "')]")
    time.sleep(2)
    Commands.ClickElement(data["BOARD"]["SETTING"]["delete_folder"])
    Commands.ClickElement(data["BOARD"]["SETTING"]["button_OK"])
    try:
        infor_delete = Waits.Wait10s_ElementLoaded(data["BOARD"]["SETTING"]["information"][1])
        time.sleep(3)
        if infor_delete.is_displayed():
            Logging("=> Delete folder successfully")
            TestCase_LogResult(**data["testcase_result"]["board"]["delete_my_folder"]["pass"])
            Commands.ClickElement(data["BOARD"]["SETTING"]["close_infor"])
    except:
        Logging("=> Delete folder fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["delete_my_folder"]["fail"])

    time.sleep(2)

def board_settings():
    Commands.ClickElement(data["BOARD"]["board_admin"])
    Logging("- Select Board admin")

    try:
        parent_execution()
    except:
        Logging(">>>> Cannot continue excution")
        pass

def parent_folder():
    #Create parent folder
    parent_folder_name = "Company folder: " + str(m)
    Commands.ClickElement(data["BOARD"]["company_folder"])
    Logging("- Manage Company Folders")
    
    Waits.Wait20s_ElementLoaded(data["BOARD"]["folder_list"])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    Logging("- Scroll down page")
    Commands.InputElement(data["BOARD"]["input_folder"], parent_folder_name)
    Logging("- Input parent folder name")
    time.sleep(3)
    Commands.ClickElement(data["BOARD"]["option_type"])
    Logging("- Select Optiion type")
    Commands.ClickElement(data["BOARD"]["folder_type"])
    Logging("- Select Folder type")

    time.sleep(3)
    Commands.ClickElement(data["BOARD"]["shared_user"])
    Logging("- Shared user")
    time.sleep(3)
    Commands.InputEnterElement(data["BOARD"]["search_user"], data["name_keyword"][0])
    time.sleep(2)
    Commands.ClickElement(data["BOARD"]["select_user"])
    Logging("- Select user")
    Commands.ClickElement(data["BOARD"]["plus_button"])
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    Commands.ClickElement(data["BOARD"]["save"][1])
    Logging("- Save ORG")

    try:
        share_user = driver.find_element_by_xpath(data["BOARD"]["share_user"])
        if share_user.is_displayed:
            Logging("=> Share user successfully")
            Commands.ClickElement("//*[@id='boot-strap-valid']//div/ul//span[contains(@class,'share_sel')]//select")
            time.sleep(3)
            permission_list = int(len(driver.find_elements_by_xpath(data["BOARD"]["permission_list"])))

            list_permission = []
            i = 0

            for i in range(permission_list):
                i += 1
                option = driver.find_element_by_xpath(data["BOARD"]["option"] + str(i) + "]")
                list_permission.append(option.text)

            x = random.choice(list_permission)
            Commands.ClickElement("//*[@id='boot-strap-valid']//div/ul//span[contains(@class,'share_sel')]//select/option[contains(.,'" + str(x) + "')]")
            Logging("- Select Permission for user")
    except:
        Logging("=> Share user Fail")

    time.sleep(2)

    Commands.ClickElement(data["BOARD"]["save"][0])
    Logging("- Save parent folder")
    
    time.sleep(5)
    Waits.Wait20s_ElementLoaded(data["loading_dialog"])

    return parent_folder_name,x

def parent_execution():
    try:
        parent_folder_name,x = parent_folder()
    except:
        parent_folder_name,x = None

    if bool(parent_folder_name) == True:
        try:
            sub_folder(parent_folder_name,x)
        except:
            Logging(">>>> Cannot continue execution")
            pass
    else:
        Logging("=> Create parent folder fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_parent_folder"]["fail"])

def sub_folder(parent_folder_name,x):
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    Logging("- Scroll up page")
    time.sleep(2)
    Commands.ClickElement(data["BOARD"]["button_plus"])
    Logging("- Create sub folder")
    try:
        Commands.ClickElement(data["BOARD"]["select_parent_folder"])
        time.sleep(3)
        Commands.ClickElement("//*[@id='board-folder-tree']//li[starts-with(@id,'han-board-folder')]/span/a[contains(., '" + parent_folder_name + "')]")
        Logging("=> Create parent folder successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_parent_folder"]["pass"])
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        Logging("- Scroll down page")
        
        try:
            sub_execution()
        except:
            Logging(">>>> Cannot continue execution")
            pass

        try:
            check_per(parent_folder_name,x)
        except:
            Logging(">>>> Cannot continue execution")
            pass

        try:
            board_folder_list(parent_folder_name)
        except:
            Logging(">>>> Cannot continue execution")
            pass
    except:
        Commands.ClickElement("//*[@id='board-folder-tree']//li[starts-with(@id,'han-board-folder')]//ul/li[1]")
        Logging("- Select different parent folder")
        time.sleep(2)
        sub_execution()

def create_sub():
    #Create sub folder
    sub_folder_name = "Sub folder: " + str(n)
    Commands.InputElement(data["BOARD"]["input_folder"], sub_folder_name)
    Logging("- Input sub folder name")
    
    time.sleep(2)
    Commands.ClickElement(data["BOARD"]["save"][0])
    Logging("- Save sub folder")
    time.sleep(3)
    
    driver.refresh()
    Waits.Wait20s_ElementLoaded(data["loading_dialog"])

    Commands.ClickElement(data["BOARD"]["hide_company_board"])

    return sub_folder_name

def check_per(parent_folder_name,x):
    if str(x) == "No Permissions":
        Logging("- Folder has No permission")
        Logging("=> Folders don't display in company folder tree")
        TestCase_LogResult(**data["testcase_result"]["board"]["shared_board"]["pass"])
    else:
        try:
            company_folder = Waits.Wait20s_ElementLoaded(data["BOARD"]["company_folder_check"]+"//span[contains(.,'" + parent_folder_name + "')]")
            if company_folder.is_displayed():
                Logging("=> Folders are displayed in company folder tree")
                TestCase_LogResult(**data["testcase_result"]["board"]["shared_board"]["pass"])
        except:
            Logging("=> Folders don't display in company folder tree")
            TestCase_LogResult(**data["testcase_result"]["board"]["shared_board"]["fail"])

    time.sleep(2)

def sub_execution():
    try:
        sub_folder_name = create_sub()
    except:
        sub_folder_name = None

    if bool(sub_folder_name) == True:
        try:
            delete_sub(sub_folder_name)
        except:
            Logging(">>>> Cannot continue execution")
            pass
    else:
        Logging("=> Add sub folder Fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_sub_folder"]["fail"])
        
def delete_sub(sub_folder_name):
    time.sleep(3)
    Commands.InputEnterElement(data["BOARD"]["search_folder"], sub_folder_name)
    Logging("- Search folder")
    time.sleep(2)
    Commands.ClickElement("//*[starts-with(@id,'han-board-folder')]//span//a[contains(.,'" + sub_folder_name + "')]")
    Logging("=> Add sub folder Successfully")
    TestCase_LogResult(**data["testcase_result"]["board"]["add_sub_folder"]["pass"])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    Commands.ClickElement(data["BOARD"]["delete_folder"][0])
    Logging("- Delete sub folder")
    Commands.ClickElement(data["BOARD"]["button_OK"])
    Commands.Wait10s_ClickElement(data["BOARD"]["close"])
    Logging("- Delete sub-folder successfully")
    Logging(" ")
    time.sleep(2)

def board_folder_list(parent_folder_name):
    Commands.ClickElement(data["BOARD"]["hide_company_board"])
    time.sleep(1)
    Commands.ClickElement(data["BOARD"]["board_admin"])
    Commands.ClickElement(data["BOARD"]["board_folder_list"])
    Logging("- Board folder list")
    Waits.Wait20s_ElementLoaded(data["BOARD"]["list_folder"])

    Commands.InputEnterElement(data["BOARD"]["search_parent_folder"], parent_folder_name)
    Logging("- Search parent folder")
    time.sleep(3)

    list_counter = driver.find_element_by_xpath(data["BOARD"]["total_list"])
    Logging("=> Total list number: " + list_counter.text)
    list_counter_number = int(list_counter.text.split(" ")[1])

    select_folder = driver.find_element_by_xpath(data["BOARD"]["select_folder"] + parent_folder_name + "')]")
    if select_folder.is_displayed():
        select_folder.click()
        Logging("=> Search folder Successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["search_folder"]["pass"])
        Logging("- Select parent folder")
        Commands.ClickElement(data["BOARD"]["delete_folder"][1])
        Logging("- Delete parent folder")
        Commands.ClickElement(data["BOARD"]["button_OK"])
        time.sleep(4)

        list_counter_update = driver.find_element_by_xpath(data["BOARD"]["total_list"])
        Logging("=> Total list number update: " + list_counter_update.text)
        list_counter_number_update = int(list_counter_update.text.split(" ")[1])

        if list_counter_number > list_counter_number_update:
            Logging("- Delete parent folder successfully")
            TestCase_LogResult(**data["testcase_result"]["board"]["delete_folder"]["pass"])
        else:
            Logging("- Delete parent folder fail")
            TestCase_LogResult(**data["testcase_result"]["board"]["delete_folder"]["fail"])
    else:
        Logging("=> Search parent folder fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["search_folder"]["fail"])
