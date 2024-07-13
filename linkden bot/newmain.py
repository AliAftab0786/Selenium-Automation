Email = "70110669@student.uol.edu.pk"
passwd = "BITBASH2024"

import csv
import time
from random import uniform
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException,WebDriverException,NoSuchElementException
import os

emailfieldxpath = '(//*[@class="text-color-text font-sans text-md outline-0 bg-color-transparent grow"])[1]'
passwordxpath = '(//*[@class="text-color-text font-sans text-md outline-0 bg-color-transparent grow"])[2]'
submitxpath = "//button[@type='submit']"

searchbtnxpath = '//button[@class="search-global-typeahead__collapsed-search-button"]'
searchboxxpath = '//input[@class="search-global-typeahead__input"]'

peoplebtnxpath = "(//*[text()='People'])[1]"

container_xpath = '//*[@class="search-results-container"]'
row_xpath = ".//li[contains(@class, 'reusable-search__result-container')]"
username_xpath = "//a[contains(@class, 'app-aware-link')]//span[@dir='ltr']//span[@aria-hidden='true']"
designation_xpath = '//*[@class="entity-result__primary-subtitle t-14 t-black t-normal"]'
location_xpath = '//*[@class="entity-result__secondary-subtitle t-14 t-normal"]'
current_xpath = "//p[contains(@class, 'entity-result__summary') and contains(@class, 'entity-result__summary--2-lines')]"

def type_like_human(element, text):
    for char in text:
        element.send_keys(char)

def clear_input_like_human(element):
    input_text = element.get_attribute('value')
    for _ in range(len(input_text)):
        # time.sleep(random.uniform(0.1, 0.2))
        element.send_keys(Keys.BACKSPACE)

def is_login(driver):
    try:
        chklogin = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,searchbtnxpath)))
        return True
    except:
        return False

def save_user_in_csv(file_path, username):
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([username])
        print(f"User {username} save in Csv...")

def username_exists(username, alreadysendmsg_filepath):
    # Check if the username exists in alreadysendmsg.csv
    with open(alreadysendmsg_filepath, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if username == row[0]:
                return True
    return False
    

def openprofile(profileid):
    incogniton_profile_id = profileid

    incogniton_url = 'http://127.0.0.1:25000/automation/launch/python/'
    data = {
        "profileID": incogniton_profile_id,
        "customArgs": "--disable-notifications"
    }
    try:
        resp = requests.post(incogniton_url, json=data)
        resp.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        print(f"Browser opened successfully with profile ID: {incogniton_profile_id}")
        incoming_json = resp.json()
        incoming_url = incoming_json.get('url')

        # Creating a remote WebDriver instance
        options = webdriver.ChromeOptions()
        # Add any additional options you may need
        driver = webdriver.Remote(command_executor=incoming_url, options=options)
        driver.maximize_window()
        time.sleep(5)
        
        # Perform actions with the WebDriver
        driver.get('https://pk.linkedin.com/')
        time.sleep(3)
        print(f"{driver.title} is open !!!!")
        return driver
    except requests.exceptions.RequestException as e:
        print(f"Failed to open the browser: {e}")

def autologin(driver , Email , passwd):
    emailfield = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH , emailfieldxpath)))
    if emailfield.get_attribute("value"):
        clear_input_like_human(emailfield)  
        type_like_human(emailfield, Email)
    else:
        emailfield.click()
        type_like_human(emailfield, Email)
    
    time.sleep(uniform(1.5 , 2.5))

    passwordfield = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH , passwordxpath)))
    if passwordfield.get_attribute("value"):
        clear_input_like_human(passwordfield)  
        type_like_human(passwordfield, passwd)
    else:
        emailfield.click()
        type_like_human(passwordfield, passwd)
    
    time.sleep(uniform(1.5 , 2.5))   
    
    action = ActionChains(driver)
    action.send_keys(Keys.ENTER).perform()

def autosearch(driver , name):
    searchbtn =WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="global-nav-search"]')))
    searchbtn.click()
    time.sleep(uniform(1.5,2.5))
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,searchboxxpath)))
    if searchbox.get_attribute("value"):
        clear_input_like_human(searchbox)  
        type_like_human(searchbox, name)
    else:
        type_like_human(searchbox, name)
    
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)

def findpeople(driver):
    peoplebtn =WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, peoplebtnxpath)))
    peoplebtn.click()

def save_info(name , data_list):
    with open(f'userfiles/{name}.txt', mode='a', newline="" , encoding="utf-8") as f:
        for data in data_list:
            f.write('username=' + data['username'] + ',\n')
            f.write('designations=' + data['designation'] + ',\n')
            f.write('location=' + data['location'] + ',\n')
            f.write('current=' + data['current'] + ',\n\n')

    print("Data has been saved to txt files.")

def find_next(driver):
    action = ActionChains(driver)
    nextbtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",nextbtn)
    action.move_to_element(nextbtn)
    time.sleep(1)
    nextbtn.click()

def scrapdata(driver):
    datalist = []
    count = 2
    container = driver.find_element(By.XPATH, "//*[@class='search-results-container']")
    time.sleep(1)
    rows = container.find_elements(By.XPATH, ".//li[contains(@class, 'reusable-search__result-container')]")
    for row in rows:
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", row)
            try:
                follow_button = WebDriverWait(row, 5).until(EC.element_to_be_clickable((By.XPATH, "(.//button[normalize-space(.)='Follow'])[1]")))
                state=1
            except:
                connect_button = WebDriverWait(row, 5).until(EC.element_to_be_clickable((By.XPATH, "(.//button[normalize-space(.)='Connect'])[1]")))
                state=2
            try: 
                if state == 1 or state == 2:
                    print(f"Count: {count}")
                    username_element = WebDriverWait(row, 5).until(EC.visibility_of_element_located((By.XPATH, f'(//*[@class="app-aware-link "])[{count}]')))
                    username = username_element.text
                    split_data = username.split('\n')
                    finalusername = split_data[0] if split_data else ""
                    print(f"User: {finalusername}")
                    designation = row.find_element(By.XPATH, ".//*[@class='entity-result__primary-subtitle t-14 t-black t-normal']").text
                    location = row.find_element(By.XPATH, ".//*[@class='entity-result__secondary-subtitle t-14 t-normal']").text
                    summary = row.find_element(By.XPATH, ".//p[contains(@class, 'entity-result__summary') and contains(@class, 'entity-result__summary--2-lines')]").text
                    split_data = summary.split(':')
                    current = split_data[-1] if split_data else ""
                    datalist.append({
                        "username": finalusername,
                        "designation": designation,
                        "location": location,
                        "current": current
                    })
                    count+=1
                else:
                    continue
            except:
                count+=1
                continue
                
        except Exception as e:
            count+=1
            print(f"Something Happened: {count}")
            continue
    return datalist
def send_message(driver, message):
    try:
        action = ActionChains(driver)
        try:
            connectbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//span[text()='Connect']/ancestor::button)[2]")))
            action.move_to_element(connectbtn)
            time.sleep(1)
            connectbtn.click()
            print("Connect Button Clicked.")
        except:
            pass
        try:
            morebtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//button[@aria-label='More actions'])[2]")))
            action.move_to_element(morebtn)
            time.sleep(1)
            morebtn.click()
            print("More Button Clicked.")
            connectbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//span[contains(text(), 'Connect')])[2]")))
            action.move_to_element(connectbtn)
            time.sleep(1)
            connectbtn.click()
            print("Connect Button Clicked.")
        except:
            pass
        try:
            connectpopup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Send without a note']/ancestor::button")))
            action.move_to_element(connectpopup)
            time.sleep(1)
            connectpopup.click()
            print("Pop up Clicked...")
        except:
            pass

        time.sleep(5)

        msgbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//button[contains(., 'Message')])[2]")))
        action.move_to_element(msgbtn)
        time.sleep(1)
        msgbtn.click()
        print("Message Btn Clicked")
        time.sleep(5)
        msgarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'msg-form__msg-content-container') and contains(@class, 'msg-form__message-texteditor')]//div[contains(@class, 'msg-form__msg-content-container--scrollable')]//div[contains(@class, 'msg-form__contenteditable')]")))
        action.move_to_element(msgarea)
        time.sleep(1)
        msgarea.click()
        print("Message Area Clicked")
        print("Type Message...")
        type_like_human(msgarea, message)
        sendbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Send']")))
        action.move_to_element(sendbtn)
        time.sleep(3)
        # sendbtn.click()
        
        closebtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']")))
        action.move_to_element(closebtn)
        time.sleep(1)
        closebtn.click()
        time.sleep(2)

        discardbtn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH ,"//button[normalize-space(.)='Discard']")))
        action.move_to_element(discardbtn)
        time.sleep(1)
        discardbtn.click()
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred while sending message:")
        try:
            closebtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']")))
            action.move_to_element(closebtn)
            time.sleep(1)
            closebtn.click()
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred while closing the message window:")

def userselection(driver , message): 
    action = ActionChains(driver)
    rows = driver.find_elements(By.XPATH, ".//li[contains(@class, 'reusable-search__result-container')]")
    time.sleep(5)
    count=1
    for row in rows:
        
        row = driver.find_element(By.XPATH, f"(.//li[contains(@class, 'reusable-search__result-container')])[{count}]")
        print(f"{row.text}")
        action.move_to_element(row)
        time.sleep(1)
        row.click()
        try:
            dismiss = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Got it']/ancestor::button")))
            if dismiss:
                print("Dismiss found!")
            action.move_to_element(dismiss)
            dismiss.click()
            time.sleep(5)
            count+=1
            continue
        except:
            pass
        time.sleep(5)
        print("Start Messaging....")
        send_message(driver, message)
        print("Now Back to Page...")
        time.sleep(5)
        driver.back()
        time.sleep(5)
        count+=1

def main(driver, names ):
    try:
        count = 0
        for name in names:
            print(f"1: {name}")
            autosearch(driver, name)
            time.sleep(5)
            if count == 0:
                findpeople(driver)
            time.sleep(5)
            datalist = scrapdata(driver)
            save_info(name, datalist)
            for _ in range(2):
                find_next(driver)
                print("Wait for Loading...")
                time.sleep(10)
                datalist = scrapdata(driver)
                time.sleep(5)
                save_info(name, datalist)
            count = 1
            time.sleep(5)
    except Exception as e:
        print(f"Unhandled Exception occurred: {e}")

def main2(driver, message, names): 
    for name in names:
        try:
            autosearch(driver , name)
            time.sleep(5)
            userselection(driver , message)
            for _ in range(2):
                find_next(driver)
                print("Wait for Loading...")
                time.sleep(10)
                userselection(driver , message)
                time.sleep(5)
        except:
            print("Main 2 Error")
            pass 

if __name__ == "__main__":
    names = ["CEO of IT Companies" , "CTO of IT Companies"]
    profileid='bbd273f6-08db-4cf3-95c9-88cfa4ee9060'
    message = "Hey! This is test message."
    max_attempts=3
    for attempt in range(max_attempts):
        try:
            driver = openprofile(profileid)
            if driver:
                break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")

    print("Wait For Loading...")
    time.sleep(10)
    try:
        print("CHECK LOGIN STATUS....")
        status= is_login(driver)
        # if status:
        #     print("You are already Logged in System...")
        #     print("Start Working...")
        #     main(driver , names )
        # else:
        #     print("You are Not Logged in System...")
        #     print("Start Login...")
        #     autologin(driver , Email , passwd)
        #     print("Wait For Loading...")
        #     time.sleep(20)
        #     print("Start Working...")
        #     main(driver , names )
        #     print("Scrapping Done...")
        #     time.sleep(5)
    except Exception as e:
        print("Scrraping issue....")
        pass

    try:
        print("Start Message and Invitation...")
        main2(driver, message, names)
    except:
        print("Message and Invitation Issue....")
        pass

    print("All Working Done...")
    driver.quit()
    