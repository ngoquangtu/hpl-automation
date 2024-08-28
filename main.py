import json
import requests
from selenium import webdriver

def create_profile():
    url = "http://localhost:35000/api/v2/profile"
    body = {
        "name": "TEST",
        "browser": "mimic",
        "os": "win"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    
    response = requests.post(url, data=json.dumps(body), headers=headers)
    if response.status_code == 200:
        uuid = response.json().get("uuid")
        
        return uuid
    else:
        print(f"Failed to create profile. Status code: {response.status_code}, Message: {response.text}")
        return None
def start_profile(mla_profile_id):
    mla_url=f'http://127.0.0.1:35000/api/v1/profile/start?automation=true&profileId={mla_profile_id}'
    response=requests.get(mla_url)
    if response.status_code == 200:
        profile_info = response.json()
        print(profile_info)
        driver = webdriver.Remote(command_executor=profile_info['value'])
        return driver
    else:
        print(f"Failed to start profile. Status code: {response.status_code}, Message: {response.text}")
        return None
def run_profile():
    mla_profile_id = create_profile()
    if not mla_profile_id:
        print(1)
        return None
    
    mla_url = f'http://127.0.0.1:35000/api/v1/profile/start?automation=true&profileId={mla_profile_id}'
    response = requests.get(mla_url)
    if response.status_code == 200:
        profile_info = response.json()
        print(profile_info)
        driver = webdriver.Remote(command_executor=profile_info['value'])
        return driver
    else:
        print(f"Failed to start profile. Status code: {response.status_code}, Message: {response.text}")
        return None

def automation():
    driver=run_profile()
    if driver:
        driver.get("https://www.multilogin.com/")
        print(driver.title) 
        driver.quit()
        # Add your automation steps here
    else:
        print("Automation could not proceed due to errors in starting the profile.")

automation()
