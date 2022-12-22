import re, sys, json, time, random, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from random import choice
from datetime import datetime
from pathlib import Path
from framework_sample import *
from MN_functions import *

n = random.randint(1,1000)
m = random.randint(1,10000)

purpose_name = data["EXPENSE"]["ADMIN"]["name_purpose1"] + objects.date_time

def settings_expense():
    Commands.ClickElement(data["EXPENSE"]["SETTINGS"]["settings_expense"])
    Logging("- Setting Expense")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='writeFolder']")))
    Logging("- Add folder")
    parent_name = data["EXPENSE"]["SETTINGS"]["parent_folder"] + str(n)
    Commands.InputElement(data["EXPENSE"]["SETTINGS"]["folder_name"], parent_name)
    Logging("- Input folder name")
    time.sleep(1)
    Commands.Wait10s_ClickElement(data["EXPENSE"]["SETTINGS"]["button_OK"][0])
    Logging("- Save Parent Folder")

    Commands.Wait10s_ClickElement(data["EXPENSE"]["SETTINGS"]["last_list_folder"] % parent_name)
    Logging("=> Add folder expense Successfully")
    TestCase_LogResult(**data["testcase_result"]["expense"]["add_folder"]["pass"])

    return parent_name

def delete_folder(parent_name):
    Commands.ClickElement(data["EXPENSE"]["SETTINGS"]["delete_button"])
    Logging("- Delete folder")
    time.sleep(2)
    Commands.Wait10s_ClickElement(data["EXPENSE"]["SETTINGS"]["button_OK"][1])
    Logging("- Click button OK")
    Waits.Wait10s_ElementLoaded(data["EXPENSE"]["SETTINGS"]["last_list_folder"] % parent_name)
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    try: 
        driver.find_element_by_xpath(data["EXPENSE"]["SETTINGS"]["last_list_folder"] % parent_name)
        Logging("=> Delete folder Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_folder"]["fail"])
    except WebDriverException:
        Logging("=> Delete folder Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_folder"]["pass"])

def setting_execution():
    try:
        parent_name = settings_expense()
    except:
        parent_name = None

    if bool(parent_name) == True:
        try:
            delete_folder(parent_name)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Add folder expense Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["add_folder"]["fail"])

def admin():
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["admin"])
    Logging("- Open menu Admin")

    try:
        manager_execution()
    except:
        Logging(">>>> Cannot continue excution")

    try:
        purpose()
    except:
        Logging(">>>> Cannot continue excution")

    try:
        payment_execution()
    except:
        Logging(">>>> Cannot continue excution")

    try:
        credit_execution()
    except:
        Logging(">>>> Cannot continue excution")

    try:
        currency_execution()
    except:
        Logging(">>>> Cannot continue excution")

def set_manager():
    Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["set_manager"])
    Logging("----------//---------- SET MANAGER ----------//----------")

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    list_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + list_counter.text)
    list_counter_number = int(list_counter.text.split(" ")[1])
    Commands.ClickElement(data["write_button"][1])
    Logging("- Write button")
    time.sleep(2)

    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["select_manager"])
    Logging("- Select manager from ORG")
    Waits.Wait20s_ElementLoaded(data["EXPENSE"]["ADMIN"]["list_ORG"])
    Logging(">> Organization list")
    time.sleep(2)

    search_user = driver.find_element_by_xpath("//*[@id='getManagerList']//div[@class='nav-search']//input")
    search_user.send_keys(data["name_keyword"][1])
    search_user.send_keys(Keys.ENTER)
    time.sleep(2)

    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["user_1"])
    Logging(">> Select user")
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["plus_button"])
    Logging(">> Add button")
    Commands.ClickElement(data["EXPENSE"]["button_save"][0])
    Logging(">> Save user")
    time.sleep(2)
    Functions.pop_up(data["EXPENSE"]["ADMIN"]["org_popup"], data["EXPENSE"]["ADMIN"]["close_org_popup"])
    Commands.ClickElement(data["EXPENSE"]["button_save"][1])
    Logging("=> Save Manager")
    time.sleep(2)

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    list_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    list_counter_update_number = int(list_counter_update.text.split(" ")[1])

    return list_counter_number,list_counter_update_number

def manager_execution():
    try:
        list_counter_number,list_counter_update_number = set_manager()
    except:
        list_counter_number,list_counter_update_number = None

    if bool(list_counter_number) == True:
        if list_counter_number < list_counter_update_number:
            Logging("=> Set manager Successfully")
            TestCase_LogResult(**data["testcase_result"]["expense"]["set_manager"]["pass"])
            list_search_number = search_manager()
            delete_manager(list_search_number)
        else:
            list_search_number = search_manager()
            if list_search_number == 1:
                Logging("=> Manager was set already")
                delete_manager(list_search_number)
            elif list_search_number == 0:
                Logging("=> Set manager Fail")
                TestCase_LogResult(**data["testcase_result"]["expense"]["set_manager"]["fail"])
            else:
                Logging("=> Search Manager Fail")
    else:
        Logging("=> Set manager Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["set_manager"]["fail"])

def search_manager():
    Commands.InputEnterElement(data["EXPENSE"]["ADMIN"]["search"], data["name_keyword"][1])
    Logging("- Search user manager")
    
    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    list_search = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list search number: " + list_search.text)
    list_search_number = int(list_search.text.split(" ")[1])

    return list_search_number
    
def delete_manager(list_search_number):
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["delete"])
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["button_OK"])
    Logging("- Delete user")

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    list_delete_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    list_delete_update_number = int(list_delete_update.text.split(" ")[1])
    
    if list_search_number > list_delete_update_number:
        Logging("=> Total list delete number update: " + list_delete_update.text)
        Logging("=> Delete manager Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_manager"]["pass"])
    else:
        Logging("=> Total list delete number update: " + list_delete_update.text)
        Logging("=> Delete manager Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_manager"]["fail"])

def purpose():
    Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["purpose"])
    Logging("----------//---------- PURPOSE ----------//----------")
    try:
        Logging("** Add Purpose 1 **")
        add_purpose()
        Logging("")
    except:
        pass

    try:
        Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["purpose_2"])
        Logging("** Add Purpose 2 **")
        add_purpose()
        Logging("")
    except:
        pass

    try:
        Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["purpose_3"])
        Logging("** Add Purpose 3 **")
        add_purpose()
        Logging("")
    except:
        pass

def add_purpose():
    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    Commands.ClickElement(data["write_button"][1])
    Logging("- Write button")  
    time.sleep(2)
    Commands.InputElement(data["EXPENSE"]["ADMIN"]["input_name"], purpose_name)
    Logging("- Input purpose")
    Commands.ClickElement(data["EXPENSE"]["button_save"][1])
    Logging("=> Save Purpose")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["pop_up"])))
        time.sleep(2)
        Logging("=> " + success.text)
        TestCase_LogResult(**data["testcase_result"]["expense"]["add_purpose"]["pass"])
        Commands.ClickElement(data["EXPENSE"]["ADMIN"]["close"])
        Logging("- Close pop up")
        time.sleep(2)
        Functions.pop_up(data["title_popup"], data["close_popup"])

        delete_purpose()
    except WebDriverException:
        Logging("=> Save Purpose Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["add_purpose"]["fail"])

def delete_purpose():
    Commands.InputEnterElement(data["EXPENSE"]["ADMIN"]["search_general"], purpose_name)
    Logging("- Search Purpose")

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["select_purpose"])
    Logging("- Select Purpose")

    purpose_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + purpose_counter.text)
    purpose_counter_number = int(purpose_counter.text.split(" ")[1])

    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["delete_purpose"])
    Logging("- Delete purpose")
    time.sleep(2)
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["button_OK"])
    Logging("- Click OK")
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    purpose_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    purpose_counter_update_number = int(purpose_counter_update.text.split(" ")[1])
    
    if purpose_counter_number > purpose_counter_update_number:
        Logging("=> Total list number update: " + purpose_counter_update.text)
        Logging("=> Delete Purpose Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_purpose"]["pass"])
    else:
        Logging("=> Total list number update: " + purpose_counter_update.text)
        Logging("=> Delete Purpose Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_purpose"]["fail"])

def payment_method():
    Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["payment_method"])
    Logging("----------//---------- PAYMENT METHOD ----------//----------")

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    payment_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + payment_counter.text)
    payment_counter_number = int(payment_counter.text.split(" ")[1])
    Commands.ClickElement(data["write_button"][1])
    Logging("- Write button")
    time.sleep(3)

    payment_method_name = data["EXPENSE"]["ADMIN"]["payment_name"] + objects.date_time
    Commands.InputElement(data["EXPENSE"]["ADMIN"]["input_name"], payment_method_name)
    Logging("- Input Payment Method")
    Commands.ClickElement(data["EXPENSE"]["button_save"][1])
    Logging("=> Save Payment Method")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["pop_up"])))
        time.sleep(2)
        Logging("=> " + success.text)
        TestCase_LogResult(**data["testcase_result"]["expense"]["payment_method"]["pass"])
        Commands.ClickElement(data["EXPENSE"]["ADMIN"]["close"])
        Logging("- Close pop up")
        time.sleep(2)
        Functions.pop_up(data["title_popup"], data["close_popup"])
    except WebDriverException:
        Commands.ClickElement("//*[@id='ngw.expense.paymentMethod']//button[contains(@data-ng-click, 'goList($event)')]")
        Logging("- Click back to list")

    return payment_method_name,payment_counter_number

def payment_execution():
    try:
        payment_method_name,payment_counter_number = payment_method()
    except:
        payment_method_name,payment_counter_number = None

    if bool(payment_method_name) == True:
        try:
            delete_payment_method(payment_method_name,payment_counter_number)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Save Payment Method Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["payment_method"]["fail"])

def delete_payment_method(payment_method_name,payment_counter_number):
    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    Waits.Wait10s_ElementLoaded("//td[contains(., '%s')]" % payment_method_name)
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["delete"])
    Logging("- Delete Payment method")
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["button_OK"])
    Logging("- Click OK")
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    payment_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    payment_counter_update_number = int(payment_counter_update.text.split(" ")[1])
    
    if payment_counter_number == payment_counter_update_number:
        Logging("=> Total list number update: " + payment_counter_update.text)
        Logging("=> Delete Payment method Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_payment_method"]["pass"])
    else:
        Logging("=> Total list number update: " + payment_counter_update.text)
        Logging("=> Delete Payment method Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_payment_method"]["fail"])

def credit_card():
    my_list_bank = ["BIDV", "Agribank", "Shinhanbank", "Techcombank", "Sacombank"]
    Logging("LIST BANK: " + str(my_list_bank))
    num = random.randint(1,1000000000)

    Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["credit_card"])
    Logging("----------//---------- CREDIT CARD ----------//----------")

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    credit_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + credit_counter.text)
    credit_counter_number = int(credit_counter.text.split(" ")[1])
    Commands.ClickElement(data["write_button"][1])
    Logging("- Write button")
    time.sleep(2)

    bank_name = random.choice(my_list_bank)
    Commands.InputElement(data["EXPENSE"]["ADMIN"]["input_name"], bank_name)
    Logging("- Input Bank name")
    Commands.InputElement(data["EXPENSE"]["ADMIN"]["credit_card_number"], num)
    Logging("- Input Credit Card Number")
    owner = "Auto " + str(n)
    Commands.InputElement(data["EXPENSE"]["ADMIN"]["credit_card_owner"], owner)
    Logging("- Input Credit Card Owner")
    driver.find_element_by_xpath(data["EXPENSE"]["button_save"][1]).click()
    Logging("=> Save Credit Card")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["pop_up"])))
        time.sleep(2)
        Logging("=> " + success.text)
        TestCase_LogResult(**data["testcase_result"]["expense"]["credit_card"]["pass"])
        Commands.ClickElement(data["EXPENSE"]["ADMIN"]["close"])
        Logging("- Close pop up")
        time.sleep(2)
        Functions.pop_up(data["title_popup"], data["close_popup"])
    except WebDriverException:
        Commands.ClickElement("//*[@id='ngw.expense.paymentMethod']//button[contains(@data-ng-click, 'goList($event)')]")
        Logging("- Click back to list")
    
    return owner,credit_counter_number

def credit_execution():
    try:
        owner,credit_counter_number = credit_card()
    except:
        owner,credit_counter_number = None

    if bool(owner) == True:
        try:
            delete_credit_card(owner,credit_counter_number)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Save credit Card Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["credit_card"]["fail"])

def delete_credit_card(owner,credit_counter_number):
    Waits.Wait10s_ElementLoaded("//td[contains(., '%s')]" % owner)
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["delete"])
    Logging("- Delete Credit card")
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["button_OK"])
    Logging("- Click OK")
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    credit_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    credit_counter_update_number = int(credit_counter_update.text.split(" ")[1])

    if credit_counter_number == credit_counter_update_number:
        Logging("=> Total list number update: " + credit_counter_update.text)
        Logging("=> Delete Credit card Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_credit_card"]["pass"])
    else:
        Logging("=> Total list number update: " + credit_counter_update.text)
        Logging("=> Delete Credit card Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_credit_card"]["fail"])

def currency():
    Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["currency"])
    Logging("----------//---------- CURRENCY ----------//----------")

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)
    currency_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + currency_counter.text)
    currency_counter_number = int(currency_counter.text.split(" ")[1])
    Commands.ClickElement(data["write_button"][1])
    Logging("- Write button")
    time.sleep(3)

    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["currency_name"])
    Logging("- Currency Name")
    time.sleep(2)

    currency_dropdown = int(len(driver.find_elements_by_xpath(data["EXPENSE"]["ADMIN"]["currency_dropdown"])))
    select = driver.find_element_by_xpath("//form/div/div/select[@name='currency_id']/option[contains(@selected,'selected')]")
    selected = select.text

    currency_list = []
    i=0
    for i in range(currency_dropdown):
        i+=1
        currency = driver.find_element_by_xpath("//form/div/div/select[@name='currency_id']/option[" + str(i) + "]")
        if currency.text != selected:
            currency_list.append(currency.text)
        else:
            continue

    x = random.choice(currency_list)
    time.sleep(1)
    currency_label = driver.find_element_by_xpath("//form/div/div/select[@name='currency_id']/option[contains(.,'%s')]" % str(x))
    currency_label.click()
    Logging("- Select Currency")
    currency_label_name = currency_label.text     
    Commands.ClickElement(data["EXPENSE"]["button_save"][1])
    Logging("=> Save Currency")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["pop_up"])
        time.sleep(2)
        Logging("=> " + success.text)
        Commands.ClickElement(data["EXPENSE"]["ADMIN"]["close"])
        Logging("- Close pop up")
        time.sleep(2)
        Functions.pop_up(data["title_popup"], data["close_popup"])
    except WebDriverException:
        driver.find_element_by_xpath("//h4[contains(., 'Error')]")
        error = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["pop_up"])
        time.sleep(2)
        Logging("=> " + error.text)
        Commands.ClickElement(data["EXPENSE"]["ADMIN"]["close"])
        Logging("- Close pop up error")
        time.sleep(2)
        Functions.pop_up(data["title_popup"], data["close_popup"])
        driver.close()

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    currency_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    currency_counter_update_number = int(currency_counter_update.text.split(" ")[1])
    
    if currency_counter_number < currency_counter_update_number:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Add Currency Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["pass"])
    else:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Add Currency Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["fail"])

    return currency_label_name

def currency_execution():
    try:
        currency_label_name = currency()
    except:
        currency_label_name = None

    if bool(currency_label_name) == True:
        try:
            delete_currency(currency_label_name)
        except:
            Logging(">>>> Cannot continue execution")
    else:
        Logging("=> Add Currency Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["fail"])

def delete_currency(currency_label_name):
    Commands.InputEnterElement(data["EXPENSE"]["ADMIN"]["search_general"], currency_label_name)
    Logging("- Search Currency")

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(1)
    Commands.Wait10s_ClickElement(data["EXPENSE"]["ADMIN"]["select_currency"])
    Logging("- Select Currency")

    currency_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + currency_counter.text)
    currency_counter_number = int(currency_counter.text.split(" ")[1])

    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["delete"])
    Logging("- Delete currency")
    Commands.ClickElement(data["EXPENSE"]["ADMIN"]["button_OK"])
    Logging("- Click OK")
    time.sleep(2)
    Functions.pop_up(data["title_popup"], data["close_popup"])

    Waits.Wait20s_ElementLoaded(data["loading_dialog"])
    time.sleep(2)

    currency_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    currency_counter_update_number = int(currency_counter_update.text.split(" ")[1])
    
    if currency_counter_number > currency_counter_update_number:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Delete currency Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_currency"]["pass"])
    else:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Delete currency Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_currency"]["fail"])
    
def expense_page(domain_name):
    Logging("================================================= EXPENSE =======================================================")
    driver.get(domain_name + "/expense/list/share/share/")
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[@id='expense-list']")))

    try:
        admin_account = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["admin_account"])
        admin_account = True
        Logging("ADMIN ACCOUNT")
    except:
        admin_account = False
        Logging("USER ACCOUNT")

    return admin_account

def expense(domain_name):
    admin_account = expense_page(domain_name)
    if admin_account == True:
        try:
            setting_execution()
        except:
            Logging(">>>> Cannot continue excution")

        try:
            admin()
        except:
            Logging(">>>> Cannot continue excution")
    else:
        try:
            setting_execution()
        except:
            Logging(">>>> Cannot continue excution")

    time.sleep(3)

