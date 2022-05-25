import re, sys, json, unittest
import time, random#, testlink
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
from MN_functions import driver, data, ValidateFailResultAndSystem, Logging, TestCase_LogResult#, #TestlinkResult_Fail, #TestlinkResult_Pass

now = datetime.now()
date = now.strftime("%m/%d/%y %H:%M:%S")

n = random.randint(1,1000)
m = random.randint(1,10000)

chrome_path = os.path.dirname(Path(__file__).absolute())+"\\chromedriver.exe"
#result=open(os.path.dirname(Path(__file__).absolute())+'\\result.txt','a')

def board_page(domain_name):
    Logging("================================================= BOARD =======================================================")
    driver.get(domain_name + "/board/list/comp_0/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["board_list"])))
    driver.find_element_by_xpath(data["BOARD"]["hide_company_board"]).click()
    Logging("- Hide company Board")
    time.sleep(1)

    try:
        admin_account = driver.find_element_by_xpath("//*[starts-with(@id,'mCSB') and contains(@id,'container')]//li/a[contains(@data-ng-click,'showAdminSetting($event)')]")
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
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["setting"]).click()
    Logging("- Select Settings")

    my_folder_name = "Folder Board: " + str(n)
    name_folder = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["name_folder"])
    name_folder.send_keys(my_folder_name)
    Logging("- Input name my folder board")

    my_folder_type = int(len(driver.find_elements_by_xpath(data["BOARD"]["SETTING"]["my_folder_type"])))

    my_folder_type_list = []
    i = 0
    for i in range(my_folder_type):
        i += 1
        my_type = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["my_type"] + str(i) + "]")
        my_folder_type_list.append(my_type.text)

    x = random.choice(my_folder_type_list)
    select_type = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["select_type"] + str(x) + "')]")
    select_type.click()
    Logging("- Select folder type")
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["save"][0]).click()
    Logging("- Save my folder board")
    
    information = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["SETTING"]["information"][0])))
    time.sleep(3)
    if information.is_displayed():
        Logging("=> Add my folder board Successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_my_folder"]["pass"])
        ##TestlinkResult_Pass("WUI-110")

    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["close_infor"]).click()
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
        ##TestlinkResult_Fail("WUI-110")  

def category(my_folder_name):
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["my_folder"] + str(my_folder_name) + "')]").click()
    time.sleep(3)
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["category"]).click()
    time.sleep(3)
    try:
        manage_categories = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["manage_categories"])
        if manage_categories.is_displayed():
            Logging("=> Display manage categories page")
            category_board = "Category Board: " + str(n)
            manage_categories.send_keys(category_board)
            driver.find_element_by_xpath(data["BOARD"]["SETTING"]["save"][1]).click()
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
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["SETTING"]["show_myfolder"]))).click()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["SETTING"]["select_folder"] + str(my_folder_name) + "')]"))).click()
    Logging("- Click my folder board")
    time.sleep(2)

    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["write_board"]).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["SETTING"]["wait_page"])))
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["SETTING"]["dropdown_cate"]))).click()
    Logging("- Write Board")
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["select_category"] + str(category_board) + "')]").click()
    title_board = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["title_board"])
    tit_board = "Title of board: " + date
    title_board.send_keys(tit_board)

    frame_board = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tox-edit-area__iframe")))
    driver.switch_to.frame(frame_board)
    content = driver.find_element_by_xpath("//body[@id='tinymce']/p")
    content.clear()
    content.send_keys("This is content of board")
    driver.switch_to.default_content()
    Logging("- Input content successfully")
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["save"][2]).click()
    Logging("- Save board")
    time.sleep(3)

    board = driver.find_element_by_xpath(data["BOARD"]["SETTING"]["board"])
    if board.text == tit_board:
        Logging("=> Write board successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["write_board"]["pass"])
        driver.find_element_by_xpath(data["BOARD"]["SETTING"]["back_list"]).click()
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
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["setting"]).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["SETTING"]["my_folder"] + str(my_folder_name) + "')]"))).click()
    time.sleep(2)
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["delete_folder"]).click()
    driver.find_element_by_xpath(data["BOARD"]["SETTING"]["button_OK"]).click()
    try:
        infor_delete = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["SETTING"]["information"][1])))
        time.sleep(3)
        if infor_delete.is_displayed():
            Logging("=> Delete folder successfully")
            TestCase_LogResult(**data["testcase_result"]["board"]["delete_my_folder"]["pass"])
            ##TestlinkResult_Pass("WUI-265")
            driver.find_element_by_xpath(data["BOARD"]["SETTING"]["close_infor"]).click()
    except:
        Logging("=> Delete folder fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["delete_my_folder"]["fail"])
        ##TestlinkResult_Fail("WUI-265")

    time.sleep(2)

def board_settings():
    driver.find_element_by_xpath(data["BOARD"]["board_admin"]).click()
    Logging("- Select Board admin")

    try:
        parent_execution()
    except:
        Logging(">>>> Cannot continue excution")
        pass

def parent_folder():
    #Create parent folder
    parent_folder_name = "Company folder: " + str(m)
    driver.find_element_by_xpath(data["BOARD"]["company_folder"]).click()
    Logging("- Manage Company Folders")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["folder_list"])))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    Logging("- Scroll down page")
    driver.find_element_by_xpath(data["BOARD"]["input_folder"]).send_keys(parent_folder_name)
    Logging("- Input parent folder name")
    time.sleep(3)
    option_type = driver.find_element_by_xpath(data["BOARD"]["option_type"]).click()
    Logging("- Select Optiion type")
    folder_type = driver.find_element_by_xpath(data["BOARD"]["folder_type"]).click()
    Logging("- Select Folder type")

    time.sleep(3)
    driver.find_element_by_xpath(data["BOARD"]["shared_user"]).click()
    Logging("- Shared user")
    time.sleep(3)
    search_user = driver.find_element_by_xpath(data["BOARD"]["search_user"])
    search_user.send_keys(data["name_keyword"][0])
    search_user.send_keys(Keys.ENTER)
    time.sleep(2)
    select_user = driver.find_element_by_xpath(data["BOARD"]["select_user"])
    select_user.click()
    Logging("- Select user")
    driver.find_element_by_xpath(data["BOARD"]["plus_button"]).click()
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_xpath(data["BOARD"]["save"][1]).click()
    Logging("- Save ORG")

    try:
        share_user = driver.find_element_by_xpath("//*[@id='boot-strap-valid']//div/ul//span[contains(@class,'share_user')]")
        if share_user.is_displayed:
            Logging("=> Share user successfully")
            driver.find_element_by_xpath("//*[@id='boot-strap-valid']//div/ul//span[contains(@class,'share_sel')]//select").click()
            time.sleep(3)
            permission_list = int(len(driver.find_elements_by_xpath("//*[@id='boot-strap-valid']//div/ul//span[contains(@class,'share_sel')]//select/option")))

            list_permission = []
            i = 0

            for i in range(permission_list):
                i += 1
                option = driver.find_element_by_xpath("//*[@id='boot-strap-valid']//div/ul//span[contains(@class,'share_sel')]//select/option[" + str(i) + "]")
                list_permission.append(option.text)

            #Logging(list_permission)

            x = random.choice(list_permission)
            select_option = driver.find_element_by_xpath("//*[@id='boot-strap-valid']//div/ul//span[contains(@class,'share_sel')]//select/option[contains(.,'" + str(x) + "')]")
            select_option.click()
            Logging("- Select Permission for user")
    except:
        Logging("=> Share user Fail")

    time.sleep(2)

    driver.find_element_by_xpath(data["BOARD"]["save"][0]).click()
    Logging("- Save parent folder")
    
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))

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
        #ValidateFailResultAndSystem("<div>[Board] Create parent folder fail</div>")
        ##TestlinkResult_Fail("WUI-251")

def sub_folder(parent_folder_name,x):
    #driver.find_element_by_id("btn-scroll-up").click()
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    Logging("- Scroll up page")
    time.sleep(2)
    driver.find_element_by_xpath(data["BOARD"]["button_plus"]).click()
    Logging("- Create sub folder")
    try:
        driver.find_element_by_xpath(data["BOARD"]["select_parent_folder"]).click()
        time.sleep(3)
        parent_folder = driver.find_element_by_xpath("//*[@id='board-folder-tree']//li[starts-with(@id,'han-board-folder')]/span/a[contains(., '" + parent_folder_name + "')]")
        parent_folder.click()
        Logging("=> Create parent folder successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["add_parent_folder"]["pass"])
        ##TestlinkResult_Pass("WUI-251")
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
        parent_folder_dif = driver.find_element_by_xpath("//*[@id='board-folder-tree']//li[starts-with(@id,'han-board-folder')]//ul/li[1]")
        parent_folder_dif.click()
        Logging("- Select different parent folder")
        time.sleep(2)
        sub_execution()

def create_sub():
    #Create sub folder
    sub_folder_name = "Sub folder: " + str(n)
    driver.find_element_by_xpath(data["BOARD"]["input_folder"]).send_keys(sub_folder_name)
    Logging("- Input sub folder name")
    
    time.sleep(2)
    driver.find_element_by_xpath(data["BOARD"]["save"][0]).click()
    Logging("- Save sub folder")
    time.sleep(3)
    
    driver.refresh()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))

    driver.find_element_by_xpath(data["BOARD"]["hide_company_board"]).click()

    return sub_folder_name

def check_per(parent_folder_name,x):
    if str(x) == "No Permissions":
        Logging("- Folder has No permission")
        Logging("=> Folders don't display in company folder tree")
        TestCase_LogResult(**data["testcase_result"]["board"]["shared_board"]["pass"])
        ##TestlinkResuxlt_Pass("WUI-257")
    else:
        try:
            company_folder = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["company_folder_check"]+"//span[contains(.,'" + parent_folder_name + "')]")))
            if company_folder.is_displayed():
                Logging("=> Folders are displayed in company folder tree")
                TestCase_LogResult(**data["testcase_result"]["board"]["shared_board"]["pass"])
                ##TestlinkResult_Pass("WUI-257")
        except:
            Logging("=> Folders don't display in company folder tree")
            TestCase_LogResult(**data["testcase_result"]["board"]["shared_board"]["fail"])
            ##TestlinkResult_Fail("WUI-257")

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
    search_folder = driver.find_element_by_xpath(data["BOARD"]["search_folder"])
    search_folder.send_keys(sub_folder_name)
    search_folder.send_keys(Keys.ENTER)
    Logging("- Search folder")
    time.sleep(2)
    driver.find_element_by_xpath("//*[starts-with(@id,'han-board-folder')]//span//a[contains(.,'" + sub_folder_name + "')]").click()
    Logging("=> Add sub folder Successfully")
    TestCase_LogResult(**data["testcase_result"]["board"]["add_sub_folder"]["pass"])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element_by_xpath(data["BOARD"]["delete_folder"][0]).click()
    Logging("- Delete sub folder")
    driver.find_element_by_xpath(data["BOARD"]["button_OK"]).click()
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["close"]))).click()
    Logging("- Delete sub-folder successfully")
    Logging(" ")
    time.sleep(2)

def board_folder_list(parent_folder_name):
    driver.find_element_by_xpath(data["BOARD"]["hide_company_board"]).click()
    time.sleep(1)
    driver.find_element_by_xpath(data["BOARD"]["board_admin"]).click()
    driver.find_element_by_xpath(data["BOARD"]["board_folder_list"]).click()
    Logging("- Board folder list")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["BOARD"]["list_folder"])))

    search_parent_folder = driver.find_element_by_xpath(data["BOARD"]["search_parent_folder"])
    search_parent_folder.send_keys(parent_folder_name)
    search_parent_folder.send_keys(Keys.ENTER)
    Logging("- Search parent folder")
    time.sleep(3)

    list_counter = driver.find_element_by_xpath(data["BOARD"]["total_list"])
    Logging("=> Total list number: " + list_counter.text)
    list_counter_number = int(list_counter.text.split(" ")[1])

    select_folder = driver.find_element_by_xpath("//*[@id='ngw.board.admin_folder']//board-folder-react-list//td[contains(.,'" + parent_folder_name + "')]")
    if select_folder.is_displayed():
        select_folder.click()
        Logging("=> Search folder Successfully")
        TestCase_LogResult(**data["testcase_result"]["board"]["search_folder"]["pass"])
        ##TestlinkResult_Pass("WUI-256")
        Logging("- Select parent folder")
        driver.find_element_by_xpath(data["BOARD"]["delete_folder"][1]).click()
        Logging("- Delete parent folder")
        driver.find_element_by_xpath(data["BOARD"]["button_OK"]).click()
        time.sleep(4)

        list_counter_update = driver.find_element_by_xpath(data["BOARD"]["total_list"])
        Logging("=> Total list number update: " + list_counter_update.text)
        list_counter_number_update = int(list_counter_update.text.split(" ")[1])

        if list_counter_number > list_counter_number_update:
            Logging("- Delete parent folder successfully")
            TestCase_LogResult(**data["testcase_result"]["board"]["delete_folder"]["pass"])
            ##TestlinkResult_Pass("WUI-253")
        else:
            Logging("- Delete parent folder fail")
            TestCase_LogResult(**data["testcase_result"]["board"]["delete_folder"]["fail"])
            ##TestlinkResult_Fail("WUI-253")
    else:
        Logging("=> Search parent folder fail")
        TestCase_LogResult(**data["testcase_result"]["board"]["search_folder"]["fail"])
        ##TestlinkResult_Fail("WUI-256")




    


