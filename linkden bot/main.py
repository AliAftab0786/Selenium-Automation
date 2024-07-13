Email = "takwatech.offical@gmail.com"
passwd = "BITBASH0306"

from utils import *
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
import os



emailfieldxpath = '(//*[@class="text-color-text font-sans text-md outline-0 bg-color-transparent grow"])[1]'
passwordxpath = '(//*[@class="text-color-text font-sans text-md outline-0 bg-color-transparent grow"])[2]'
submitxpath = "//button[@type='submit']"

searchbtnxpath = '//input[@class="search-global-typeahead__input"]'
searchboxxpath = '//input[@class="search-global-typeahead__input"]'

peoplebtnxpath = "(//*[text()='People'])[1]"

container_xpath = '//*[@class="search-results-container"]'
row_xpath = ".//li[contains(@class, 'reusable-search__result-container')]"
username_xpath = "//a[contains(@class, 'app-aware-link')]//span[@dir='ltr']//span[@aria-hidden='true']"
designation_xpath = '//*[@class="entity-result__primary-subtitle t-14 t-black t-normal"]'
location_xpath = '//*[@class="entity-result__secondary-subtitle t-14 t-normal"]'
current_xpath = "//p[contains(@class, 'entity-result__summary') and contains(@class, 'entity-result__summary--2-lines')]"

def export_cookies(driver, username):
    # Retrieve cookies from the browser session
    cookies = driver.get_cookies()
    
    # Write cookies to the specified file in JSON format
    file_path = f'./cookies/cookies-{username}.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(cookies, file, ensure_ascii=False, indent=4)
    
    print(f"Cookies exported successfully to {file_path}")

def openprofile(username):
    cookies_available = False 
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)  
        driver.maximize_window()
        time.sleep(1)
        driver.get("https://pk.linkedin.com/")
        time.sleep(2)
        cookie_file = f'./cookies/cookies-{username}.json'
        if os.path.isfile(cookie_file):
            cookies_available = True
            with open(cookie_file, 'r', encoding="utf-8") as file:
                cookies = json.load(file)
        else:
            pass
            
        if cookies_available:
            print("Page loaded. Adding cookies to the browser session...")
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                if 'sameSite' not in cookie or cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                    cookie['sameSite'] = 'None'  
                cookie['domain'] = '.linkedin.com'
                driver.add_cookie(cookie)
            print("Cookies added successfully.")
            time.sleep(2)
            driver.refresh()
            print("Page refreshed after adding cookies.")
            time.sleep(random.randint(5, 7))
        print("Browser should now be fully operational.")
        return driver
    except Exception as e:
        print(f"An error occurred: {e}")
        if driver is not None:  
            driver.quit()
        raise  

def type_like_human(element, text):
    for char in text:
        element.send_keys(char)

def clear_input_like_human(element):
    action = ActionChains(driver)
    action.key_down(Keys.CONTROL)
    action.send_keys('a')
    action.key_up(Keys.CONTROL)
    action.send_keys(Keys.BACKSPACE)
    action.perform()

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
    print("Searching....")
    action=ActionChains(driver)
   
    searchbtn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, searchbtnxpath)))

    action.move_to_element(searchbtn).perform()
    searchbtn.click()
    time.sleep(uniform(1.5,2.5))
    searchbox = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,searchboxxpath)))
    action.move_to_element(searchbox).perform()
    if searchbox.get_attribute('value'):
        action.key_down(Keys.COMMAND)
        action.send_keys('a')
        action.key_up(Keys.COMMAND)
        action.send_keys(Keys.BACKSPACE)
        action.perform()
        time.sleep(1) 
        type_like_human(searchbox, name)
    else:
        type_like_human(searchbox, name)
    
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)
   

def findpeople(driver):
    peoplebtn =WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, peoplebtnxpath)))
    peoplebtn.click()

def scrapdata(driver):
    time.sleep(5)
    container = driver.find_element(By.XPATH, "//*[@class='search-results-container']")
    time.sleep(1)
    rows = container.find_elements(By.XPATH, ".//li[contains(@class, 'reusable-search__result-container')]")
    time.sleep(3)
    count=2
    datalist = []
    for row in rows:
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",row)
            username = row.find_element(By.XPATH, f'(//*[@class="app-aware-link "])[{count}]').text
            split_data = username.split('\n')
            finalusername = split_data[0] if split_data else ""

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
            count += 1
        except Exception as e:
            print(f"An error occurred while processing a row: {e}")

    return datalist

def save_info(name , data_list):
    with open(f'userfiles/{name}.txt', 'w',newline="" , encoding="utf-8") as f:
        for data in data_list:
            f.write('username=' + data['username'] + ',\n')
            f.write('designations=' + data['designation'] + ',\n')
            f.write('location=' + data['location'] + ',\n')
            f.write('current=' + data['current'] + ',\n\n')

    print("Data has been saved to txt files.")

def is_login(driver):
    try:
        chklogin = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,searchbtnxpath)))
        return True
    except:
        return False
    
def main(driver , names):
    count=0
    for name in names:
        print("loading...")
        time.sleep(5)
        autosearch(driver , name)
        time.sleep(5)
        if count == 0:
            findpeople(driver)
        else:
            pass
        datalist = scrapdata(driver)
        time.sleep(5)
        save_info(name , datalist)
        count=1      
if __name__ == "__main__":
    names = ["CEO of IT Companies" , "CTO of IT Companies"]
    username="meharaliaftab0306"
    driver = openprofile(username)
    print("Wait For Loading...")
    print("CHECK LOGIN STATUS....")
    status= is_login(driver)
    if status:
        print("You are already Logged in System...")
        print("Start Working...")
        main(driver , names)
    else:
        print("You are Not Logged in System...")
        print("Start Login...")
        autologin(driver , Email , passwd)
        print("Successfully logged in.")
        # export_cookies(driver, username)
        time.sleep(random.randint(5, 7))
        print("Start Working...")
        main(driver , names)

    print("All Working Done...")
    driver.quit()

    