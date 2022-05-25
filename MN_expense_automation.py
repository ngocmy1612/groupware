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
from datetime import datetime
from pathlib import Path
import os

from MN_functions import driver, data, ValidateFailResultAndSystem, Logging, TestCase_LogResult#, #TestlinkResult_Fail, #TestlinkResult_Pass

n = random.randint(1,1000)
m = random.randint(1,10000)

#chrome_path = os.path.dirname(Path(__file__).absolute())+"\\chromedriver.exe"
#result=open(os.path.dirname(Path(__file__).absolute())+'\\result.txt','a')

now = datetime.now()
date = now.strftime("%m/%d/%y %H:%M:%S")

purpose_name = data["EXPENSE"]["ADMIN"]["name_purpose1"] + date

def settings_expense():
    driver.find_element_by_xpath(data["EXPENSE"]["SETTINGS"]["settings_expense"]).click()
    Logging("- Setting Expense")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "writeFolder")))
    Logging("- Add folder")
    parent_name = data["EXPENSE"]["SETTINGS"]["parent_folder"] + str(n)
    driver.find_element_by_xpath(data["EXPENSE"]["SETTINGS"]["folder_name"]).send_keys(parent_name)
    Logging("- Input folder name")
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["SETTINGS"]["button_OK"][0]))).click()
    Logging("- Save Parent Folder")

    last_expense_add = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["SETTINGS"]["last_list_folder"] + parent_name + "')]")))
    time.sleep(3)
    last_expense_add.click()
    Logging("=> Add folder expense Successfully")
    TestCase_LogResult(**data["testcase_result"]["expense"]["add_folder"]["pass"])
    #TestlinkResult_Pass("WUI-144")

    return parent_name

def delete_folder(parent_name):
    driver.find_element_by_xpath(data["EXPENSE"]["SETTINGS"]["delete_button"]).click()
    Logging("- Delete folder")
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["SETTINGS"]["button_OK"][1]))).click()
    Logging("- Click button OK")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["SETTINGS"]["last_list_folder"] + parent_name + "')]")))
    time.sleep(2)

    try: 
        last_expense_del = driver.find_element_by_xpath(data["EXPENSE"]["SETTINGS"]["last_list_folder"] + parent_name + "')]")
        if last_expense_del.is_displayed():
            Logging("=> Delete folder Fail")
            TestCase_LogResult(**data["testcase_result"]["expense"]["delete_folder"]["fail"])
            #ValidateFailResultAndSystem("<div>[Expense] Delete folder Fail</div>")
            #TestlinkResult_Fail("WUI-145")
    except WebDriverException:
        Logging("=> Delete folder Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_folder"]["pass"])
        #TestlinkResult_Pass("WUI-145")

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
            pass
    else:
        Logging("=> Add folder expense Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["add_folder"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Add folder expense Fail</div>")
        #TestlinkResult_Fail("WUI-144")

def admin():
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["admin"]).click()
    Logging("- Open menu Admin")

    try:
        manager_execution()
    except:
        Logging(">>>> Cannot continue excution")
        pass

    try:
        purpose()
    except:
        Logging(">>>> Cannot continue excution")
        pass

    try:
        payment_execution()
    except:
        Logging(">>>> Cannot continue excution")
        pass

    try:
        credit_execution()
    except:
        Logging(">>>> Cannot continue excution")
        pass

    try:
        currency_execution()
    except:
        Logging(">>>> Cannot continue excution")
        pass

def set_manager():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["set_manager"]))).click()
    Logging("----------//---------- SET MANAGER ----------//----------")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)
    list_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + list_counter.text)
    list_counter_number = int(list_counter.text.split(" ")[1])
    driver.find_element_by_xpath(data["write_button"][1]).click()
    Logging("- Write button")
    time.sleep(2)

    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["select_manager"]).click()
    Logging("- Select manager from ORG")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["list_ORG"])))
    Logging(">> Organization list")
    time.sleep(2)
    search_user = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["user_keyword"])))
    search_user.send_keys(data["name_keyword"][1])
    search_user.send_keys(Keys.RETURN)
    Logging(">> Search Users")
    time.sleep(2)
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["user_1"]).click()
    Logging(">> Select user")
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["plus_button"]).click()
    Logging(">> Add button")
    driver.find_element_by_xpath(data["EXPENSE"]["button_save"][0]).click()
    Logging(">> Save user")
    driver.find_element_by_xpath(data["EXPENSE"]["button_save"][1]).click()
    Logging("=> Save Manager")
    time.sleep(2)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
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
    search = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["search"])
    search.send_keys(data["name_keyword"][1])
    search.send_keys(Keys.ENTER)
    Logging("- Search user manager")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    list_search = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list search number: " + list_search.text)
    list_search_number = int(list_search.text.split(" ")[1])

    return list_search_number
    
def delete_manager(list_search_number):
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["delete"]).click()
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["button_OK"]).click()
    Logging("- Delete user")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    list_delete_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    list_delete_update_number = int(list_delete_update.text.split(" ")[1])
    
    if list_search_number > list_delete_update_number:
        Logging("=> Total list delete number update: " + list_delete_update.text)
        Logging("=> Delete manager Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_manager"]["pass"])
        #TestlinkResult_Pass("WUI-188")
    else:
        Logging("=> Total list delete number update: " + list_delete_update.text)
        Logging("=> Delete manager Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_manager"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Delete manager Fail</div>")
        #TestlinkResult_Fail("WUI-188")

def purpose():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["purpose"]))).click()
    Logging("----------//---------- PURPOSE ----------//----------")
    try:
        Logging("** Add Purpose 1 **")
        add_purpose()
        Logging("")
    except:
        pass

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["purpose_2"]))).click()
        Logging("** Add Purpose 2 **")
        add_purpose()
        Logging("")
    except:
        pass

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["purpose_3"]))).click()
        Logging("** Add Purpose 3 **")
        add_purpose()
        Logging("")
    except:
        pass

def add_purpose():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)
    driver.find_element_by_xpath(data["write_button"][1]).click()
    Logging("- Write button")  
    time.sleep(2)
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["input_name"]).send_keys(purpose_name)
    Logging("- Input purpose")
    driver.find_element_by_xpath(data["EXPENSE"]["button_save"][1]).click()
    Logging("=> Save Purpose")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["pop_up"])))
        time.sleep(2)
        Logging("=> " + success.text)
        TestCase_LogResult(**data["testcase_result"]["expense"]["add_purpose"]["pass"])
        #TestlinkResult_Pass("WUI-167")
        driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["close"]).click()
        Logging("- Close pop up")
        time.sleep(2)

        delete_purpose()
    except WebDriverException:
        Logging("=> Save Purpose Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["add_purpose"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Save Purpose Fail</div>")
        #TestlinkResult_Fail("WUI-167")

def delete_purpose():
    search_purpose = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["search_general"])
    Logging("- Search Purpose")
    search_purpose.send_keys(purpose_name)
    search_purpose.send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["select_purpose"]))).click()
    Logging("- Select Purpose")

    purpose_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + purpose_counter.text)
    purpose_counter_number = int(purpose_counter.text.split(" ")[1])

    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["delete_purpose"]).click()
    Logging("- Delete purpose")
    time.sleep(2)
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["button_OK"]).click()
    Logging("- Click OK")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    purpose_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    purpose_counter_update_number = int(purpose_counter_update.text.split(" ")[1])
    
    if purpose_counter_number > purpose_counter_update_number:
        Logging("=> Total list number update: " + purpose_counter_update.text)
        Logging("=> Delete Purpose Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_purpose"]["pass"])
        #TestlinkResult_Pass("WUI-208")
    else:
        Logging("=> Total list number update: " + purpose_counter_update.text)
        Logging("=> Delete Purpose Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_purpose"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Delete Purpose Fail</div>")
        #TestlinkResult_Fail("WUI-208")

def payment_method():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["payment_method"]))).click()
    Logging("----------//---------- PAYMENT METHOD ----------//----------")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)
    payment_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + payment_counter.text)
    payment_counter_number = int(payment_counter.text.split(" ")[1])
    driver.find_element_by_xpath(data["write_button"][1]).click()
    Logging("- Write button")
    time.sleep(3)

    payment_method_name = data["EXPENSE"]["ADMIN"]["payment_name"] + str(m)
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["input_name"]).send_keys(payment_method_name)
    Logging("- Input Payment Method")
    driver.find_element_by_xpath(data["EXPENSE"]["button_save"][1]).click()
    Logging("=> Save Payment Method")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["pop_up"])))
        time.sleep(2)
        Logging("=> " + success.text)
        TestCase_LogResult(**data["testcase_result"]["expense"]["payment_method"]["pass"])
        driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["close"]).click()
        Logging("- Close pop up")
    except WebDriverException:
        driver.find_element_by_xpath("//*[@id='ngw.expense.paymentMethod']//button[contains(@data-ng-click, 'goList($event)')]").click()
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
            pass
    else:
        Logging("=> Save Payment Method Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["payment_method"]["fail"])

def delete_payment_method(payment_method_name,payment_counter_number):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//td[contains(., '" + payment_method_name + "')]")))
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["delete"]).click()
    Logging("- Delete Payment method")
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["button_OK"]).click()
    Logging("- Click OK")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    payment_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    payment_counter_update_number = int(payment_counter_update.text.split(" ")[1])
    
    if payment_counter_number == payment_counter_update_number:
        Logging("=> Total list number update: " + payment_counter_update.text)
        Logging("=> Delete Payment method Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_payment_method"]["pass"])
        #TestlinkResult_Pass("WUI-169")
    else:
        Logging("=> Total list number update: " + payment_counter_update.text)
        Logging("=> Delete Payment method Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_payment_method"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Delete Payment method Fail</div>")
        #TestlinkResult_Fail("WUI-169")

def credit_card():
    my_list_bank = ["BIDV", "Agribank", "Shinhanbank", "Techcombank", "Sacombank"]
    Logging("LIST BANK: " + str(my_list_bank))
    num = random.randint(1,1000000000)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["credit_card"]))).click()
    Logging("----------//---------- CREDIT CARD ----------//----------")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)
    credit_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + credit_counter.text)
    credit_counter_number = int(credit_counter.text.split(" ")[1])
    driver.find_element_by_xpath(data["write_button"][1]).click()
    Logging("- Write button")
    time.sleep(2)

    bank_name = random.choice(my_list_bank)
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["input_name"]).send_keys(bank_name)
    Logging("- Input Bank name")
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["credit_card_number"]).send_keys(num)
    Logging("- Input Credit Card Number")
    owner = "Auto " + str(n)
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["credit_card_owner"]).send_keys(owner)
    Logging("- Input Credit Card Owner")
    driver.find_element_by_xpath(data["EXPENSE"]["button_save"][1]).click()
    Logging("=> Save Credit Card")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["pop_up"])))
        time.sleep(2)
        Logging("=> " + success.text)
        TestCase_LogResult(**data["testcase_result"]["expense"]["credit_card"]["pass"])
        driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["close"]).click()
        Logging("- Close pop up")
    except WebDriverException:
        driver.find_element_by_xpath("//*[@id='ngw.expense.paymentMethod']//button[contains(@data-ng-click, 'goList($event)')]").click()
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
            pass
    else:
        Logging("=> Save credit Card Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["credit_card"]["fail"])

def delete_credit_card(owner,credit_counter_number):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//td[contains(., '" + owner + "')]")))
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["delete"]).click()
    Logging("- Delete Credit card")
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["button_OK"]).click()
    Logging("- Click OK")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    credit_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    credit_counter_update_number = int(credit_counter_update.text.split(" ")[1])
    
    if credit_counter_number == credit_counter_update_number:
        Logging("=> Total list number update: " + credit_counter_update.text)
        Logging("=> Delete Credit card Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_credit_card"]["pass"])
        #TestlinkResult_Pass("WUI-171")
    else:
        Logging("=> Total list number update: " + credit_counter_update.text)
        Logging("=> Delete Credit card Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_credit_card"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Delete Credit card Fail</div>")
        #TestlinkResult_Fail("WUI-171")

def currency():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["currency"]))).click()
    Logging("----------//---------- CURRENCY ----------//----------")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)
    currency_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + currency_counter.text)
    currency_counter_number = int(currency_counter.text.split(" ")[1])
    driver.find_element_by_xpath(data["write_button"][1]).click()
    Logging("- Write button")
    time.sleep(3)

    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["currency_name"]).click()
    Logging("- Currency Name")
    time.sleep(2)

    currency_dropdown = int(len(driver.find_elements_by_xpath(data["EXPENSE"]["ADMIN"]["currency_dropdown"])))
    select = driver.find_element_by_xpath("//form/div/div/select[@name='currency_id']/option[contains(@selected,'selected')]")
    selected = select.text
    print(selected)

    currency_list = []
    i=0
    for i in range(currency_dropdown):
        i+=1
        currency = driver.find_element_by_xpath("//form/div/div/select[@name='currency_id']/option[" + str(i) + "]")
        if currency.text != selected:
            currency_list.append(currency.text)
        else:
            continue

    #Logging("- Total of currency: " + str(len(currency_list)))
    #Logging(currency_list)

    x = random.choice(currency_list)
    time.sleep(1)
    currency_label = driver.find_element_by_xpath("//form/div/div/select[@name='currency_id']/option[contains(.,'" + str(x) + "')]")
    currency_label.click()
    Logging("- Select Currency")
    currency_label_name = currency_label.text                                                                             
    driver.find_element_by_xpath(data["EXPENSE"]["button_save"][1]).click()
    Logging("=> Save Currency")

    try:
        driver.find_element_by_xpath("//h4[contains(., 'Success')]")
        success = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["pop_up"])
        time.sleep(2)
        Logging("=> " + success.text)
        #TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["pass"])
        #TestlinkResult_Pass("WUI-196")
        driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["close"]).click()
        Logging("- Close pop up")
    except WebDriverException:
        driver.find_element_by_xpath("//h4[contains(., 'Error')]")
        error = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["pop_up"])
        time.sleep(2)
        Logging("=> " + error.text)
        #TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["fail"])
        #TestlinkResult_Fail("WUI-196")
        driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["close"]).click()
        Logging("- Close pop up error")
        driver.close()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    currency_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    currency_counter_update_number = int(currency_counter_update.text.split(" ")[1])
    
    if currency_counter_number < currency_counter_update_number:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Add Currency Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["pass"])
        #TestlinkResult_Pass("WUI-196")
    else:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Add Currency Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Add Currency Fail</div>")
        #TestlinkResult_Fail("WUI-196")

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
            pass
    else:
        Logging("=> Add Currency Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["currency"]["fail"])

def delete_currency(currency_label_name):
    search_currency = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["search_general"])
    Logging("- Search Currency")
    search_currency.send_keys(currency_label_name)
    search_currency.send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["EXPENSE"]["ADMIN"]["select_currency"]))).click()
    Logging("- Select Currency")

    currency_counter = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    Logging("=> Total list number: " + currency_counter.text)
    currency_counter_number = int(currency_counter.text.split(" ")[1])

    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["delete"]).click()
    Logging("- Delete currency")
    driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["button_OK"]).click()
    Logging("- Click OK")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["loading_dialog"])))
    time.sleep(2)

    currency_counter_update = driver.find_element_by_xpath(data["EXPENSE"]["ADMIN"]["total_list"])
    currency_counter_update_number = int(currency_counter_update.text.split(" ")[1])
    
    if currency_counter_number > currency_counter_update_number:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Delete currency Successfully")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_currency"]["pass"])
        #TestlinkResult_Pass("WUI-216")
    else:
        Logging("=> Total list number update: " + currency_counter_update.text)
        Logging("=> Delete currency Fail")
        TestCase_LogResult(**data["testcase_result"]["expense"]["delete_currency"]["fail"])
        #ValidateFailResultAndSystem("<div>[Expense] Delete currency Fail</div>")
        #TestlinkResult_Fail("WUI-216")
    
def expense_page(domain_name):
    Logging("================================================= EXPENSE =======================================================")
    driver.get(domain_name + "/expense/list/share/share/")
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "expense-list")))

    try:
        admin_account = driver.find_element_by_xpath("//*[starts-with(@id,'mCSB') and contains(@id,'container')]//li/a[contains(@data-ng-click,'showAdminSetting()')]")
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
            pass

        try:
            admin()
        except:
            Logging(">>>> Cannot continue excution")
            pass
    else:
        try:
            setting_execution()
        except:
            Logging(">>>> Cannot continue excution")
            pass

    time.sleep(3)

