#basic imports
import json
import time
from datetime import datetime

#webserver imports
import asyncio
import websockets

#selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
'''

'''
def json_handler(action, new_data='{}', filename='data.json'):

    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        
        if action == 'count': return len(file_data["girls"])

        file_data["girls"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

            
options = Options()
options.headless = False
options.add_argument(
    "user-data-dir='Users/marcus/Library/Application Support/Google/Chrome/Default/'")
options.add_argument("--window-size=1000,1000")

# browser:
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

# browser:
browser_path = Service('/usr/local/bin/chromedriver')
browser = webdriver.Chrome(
    options=options, service=browser_path, desired_capabilities=desired_capabilities)

url = 'https://www.tinder.com'

browser.get(url)

time.sleep(9)


def tinder_controls(action):
    user_id = browser.find_elements(By.TAG_NAME,'div')[0].get_attribute('id')
    ids = browser.find_elements(By.CLASS_NAME, 'Hidden')
    like = [l for l in ids if l.get_attribute('innerHTML') == 'Like'][0]
    nope = [l for l in ids if l.get_attribute('innerHTML') == 'Nope'][0]
    if "like" in [action]: 
#        browser.find_element(By.XPATH, like_Xpath).click()
        like.find_element(By.XPATH, './../../..').click()
        print("nice one, lets continue...")
    elif "nope" in [action]:
        nope.find_element(By.XPATH, './../../..').click()
        print("too bad, next...")



def log_filter(log_):
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
    )

def get_data():
# extract requests from logs
    time.sleep(10)
    logs_raw = browser.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        print(f"Caught {resp_url}")
        if resp_url == "https://api.gotinder.com/v2/recs/core?locale=en-GB":
            time.sleep(1)
            res = browser.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": request_id}) #body:#
            time.sleep(1)
            res = json.loads(res['body'])
            for i in range(len(res["data"]["results"])):
                bio=res["data"]["results"][i]["user"]["bio"]
                name = res["data"]["results"][i]["user"]["name"]
                photos = [x["url"] for x in res["data"]["results"][i]["user"]["photos"]]
                try:
                    distance = ''
                except:
                    distance = 'no_data'
                birthday = res["data"]["results"][i]["user"]["birth_date"].split('T')[0] 
                #date = datetime.strftime(birthday, '%y-%m-%d')
                # "2003-11-21"
                #age = date-datetime.today()
                starsign = 'Cancer'
                school = 'no_data'
                lives_in = 'no data'
                #identifier = json_handler(action='count')
                identifier= '234'
                age = 0
                user = {
                    identifier:{
                        "name": name,
                        "age": age,
                        "bio": bio,
                        "distance": distance,
                        "starsign":starsign,
                        "school":school,
                        "lives_in": lives_in,
                        "photos": photos
                    }
                }

                #
                # json_handler(action='write', new_data=user)
                print(user)
                tinder_controls(input("like? || nope?"))
                #return user

get_data()

if input('Quit? (y/n)') == 'y':
    browser.quit()
    print('Quitting...')



#altcode:
# browser.execute_script("window.open('');")
# Switch to the new window and open new URL
# browser.switch_to.window(browser.window_handles[i+1])

# for pix in photos:
#    browser.get(pix)
#    print(pix)
#    time.sleep(3)