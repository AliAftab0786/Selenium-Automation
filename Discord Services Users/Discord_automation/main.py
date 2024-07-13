from utils import *
from checkInternet import check_internet_connection
from helpers import *

global driver
driver = None
def openprofile(incogniton_profile_id, profile_name):
    print(f"Starting Automation for Profile {profile_name}")
    
    for attempt in range(3):
        try:
            # Step 1: Check the status of the Incogniton profile
            # status_url = f"http://127.0.0.1:35001/profile/status/{incogniton_profile_id}"
            # resp = requests.get(status_url)
            # status = resp.json().get('status')
            
            # # If the profile is running, stop it
            # if status == 'running':
            #     stop_url = f"http://127.0.0.1:35001/profile/stop/{incogniton_profile_id}"
            #     resp = requests.get(stop_url)
            #     print(resp.json())

            # Step 2: Launch the Incogniton profile
            incogniton_url = "http://127.0.0.1:35001/automation/launch/python/"
            data = {
                "profileID": incogniton_profile_id,
                "customArgs": "--disable-notifications",
            }
            resp = requests.post(incogniton_url, data)
            resp_json = resp.json()
            print(resp_json)
            time.sleep(15)
            # If there's an error when launching the profile, raise an exception
            if resp_json.get('status') == 'error':
                raise ValueError(resp_json.get('message'))

            # Step 3: Get the remote URL and create a WebDriver instance
            incoming_url = resp_json.get("url")  # Use .get() to handle missing "url" field
            if not incoming_url:
                raise ValueError("Missing 'url' field in the response")
            driver = webdriver.Remote(
                command_executor=incoming_url, options=webdriver.ChromeOptions()
            )
            break
        except requests.RequestException as e:
            print(f"Request failed. Exception: {e}")
            if attempt < 2:
                print(f"Retrying... Attempt {attempt + 1}")
                time.sleep(2)
            else:
                print("Failed to stop and launch after multiple attempts.")
        except Exception as e:
            print(f"Unexpected exception: {e}")

    # Close any existing windows except the last one
    existing_handles = driver.window_handles
    for handle in existing_handles[:-1]:
        driver.switch_to.window(handle)
        driver.close()

    # Switch to the last window
    driver.switch_to.window(existing_handles[-1])

    # Navigate to the desired URL
    driver.get("https://affiliate-us.tiktok.com/platform/homepage?shop_region=US")

    # Set page load and script timeouts
    driver.set_page_load_timeout(1000)
    driver.set_script_timeout(1000)

    # Maximize the window
    driver.maximize_window()

def StartWorking(browser_id, profilename):
    while True:
        try:
            openprofile(browser_id, profilename)
            time.sleep(10)

            
            
        except:
            print("Error in Profile")
            if driver:
                driver.quit()
            time.sleep(10)
            clear_terminal()
            continue

def startprofile(accounttitle, messageData, assignmessages):
    print("Opening profile...")
    res = requests.get("http://127.0.0.1:35001/profile/all")
    profiles = res.json()["profileData"]
    group = "Discord".lower().strip()

    browser_id = None
    profilename = None
    for profile in profiles:
        if (
            profile["general_profile_information"]["profile_group"].lower().strip()
            == group
        ):
            browser_id = profile["general_profile_information"]["browser_id"]
            profilename = (
                profile["general_profile_information"]["profile_name"]
                .lower()
                .strip()
            )
            # print("\nProfile Ids ", browser_id, "")
            # print("Profile Names ", profilename, "\n")
            if accounttitle.lower().strip() in profilename.lower().strip():
                print("Profile found")
                print("Profile Ids ", browser_id, "\n")
                print("Profile Names ", profilename, "\n")
                print("GOING To START PROFILE")
                StartWorking(browser_id, profilename)
                break
    



if __name__ =="__main__":
    messageData=starting()
    with open('userData.json', 'r', encoding='utf-8') as file:
        data_json = json.load(file)
        choices = data_json['choices']
    numofaccount=int(input("Enter Number of Accounts:"))
    while True:
        if check_internet_connection():
            try:
                clear_terminal()
                assignmessages=set_messages(numofaccount)
                for num in range(numofaccount):
                    choice = choices[num]
                    account_title = choice['accounttitle']
                    messageData = choice['message'] + f"{choice['invitelink']}"
                    print(messageData)
                    number_of_messages = assignmessages[num]
                    print(f"Number of Message: {number_of_messages}")
                    # input("Press Enter to continue...")
                    startprofile(account_title, messageData, number_of_messages)
                break
            except Exception as e:
                print("ERROR: ", str(e))
                time.sleep(30)
        else:
            print("Internet connection lost. Retrying...")
            time.sleep(30)