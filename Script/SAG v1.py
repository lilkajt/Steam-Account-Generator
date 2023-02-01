import time
from discord import SyncWebhook
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import string
import random
import keyboard as BasicBoard
import pandas as pd
import os

# 01.02.2023
token = 'discordwebhook' # Put here your discord webhook to receive successfuly created accounts details.
webhook = SyncWebhook.from_url(token)
url = "https://store.steampowered.com/join"
region = "ARS" # region where you create accounts
Limit = 10 #How many accounts you want to generate

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_email():
    username = random_string(8)
    domain = "yourdomain"
    return f"{username}@{domain}"

def random_password(length):
    return random_string(length)

def SteamAccount():
    email = random_email()
    username = email.split("@")[0]
    password = random_password(16)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="reenter_email"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="i_agree_check"]').click()
    while True:
        print("Press \"c\" to continue! CAPTCHA!")
        if (BasicBoard.is_pressed('c')):
            break
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    print("Creating Account - confirm mail")
    while True:
        print("Press \"m\" to continue! Mail!")
        if (BasicBoard.is_pressed('m')):
            break
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="accountname"]').click()
    for x in username: driver.find_element(By.XPATH, '//*[@id="accountname"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="reenter_password"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    time.sleep(2)
    print("Account succesfuly created")
    ExcelFile(email,username,password)
    webhook.send("Steam account created\nEmail: "+email+"\nUsername: "+username+"\nPassword: "+password)
    driver.close()

def ExcelFile(email, username,password):
    data = {"Email": email, "Username": username, "Password": password}
    df = pd.DataFrame(data, index=[0])

    file_path = f"yourfilepath{region}_accounts.xlsx" #input your file path
    if not os.path.exists(file_path):
        df.to_excel(file_path,sheet_name="Accounts",index=False)
    else:
        with pd.ExcelWriter(file_path,mode='a',engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer,sheet_name="Accounts",startrow=writer.sheets["Accounts"].max_row,index=False, header=False)


try:
    Count = 0
    while (Count < Limit):
        SteamAccount()
        time.sleep(1)
        Count +=1
        print("Accounts generated: "+str(Count))
except Exception as err:
    print(err)