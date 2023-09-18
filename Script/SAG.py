import os
import string
import random
import time
import numpy as np
import keyboard as BasicBoard
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from discord import SyncWebhook
import pathlib

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
version = '2.1'
url = "https://store.steampowered.com/join"
Domain_Input = ''
clear_line = "cls||clear"
path = pathlib.Path().resolve()

# FILE FUNCTIONS
def data_to_csv(email, username, password):
    data = {"Email": email, "Username": username, "Password": password}
    df = pd.DataFrame(data, index=[0])
    file_path = f"{path}\\Created_accounts.csv"

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', index=False, header=False)

def read_accounts_from_csv_file():
    print('\tReading emails from csv file')
    file_name = input('\tWhat is the file name(without extension): ')
    emails = pd.read_csv(f"{path}\\{file_name}.csv")
    return emails['Email'].tolist()

def create_new_example_file(file_name):
    data = {'Email':'Testemail@domain.com'}
    df = pd.DataFrame(data, index=[0])
    file_path = f"{path}\\{file_name}.csv"

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)

def read_webhook():
    f = open(f"{pathlib.Path().resolve()}\\webhook.txt", "r")
    return f.readline()

# TIME FUNC
def sleep(n):
    time.sleep(n)

# NOTIFICATIONS
def notification(type_notifi):
    if type_notifi == "email":
        key = "m"
    elif type_notifi == "captcha":
        key = "c"
    else:
        key = "n"
    print(f'\n\tCheck {type_notifi} to confirm!\n\tPress \"{key}\" to continue!')
    while True:
        if BasicBoard.is_pressed(key):
            break

# RANDOM STRINGS
def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_password(length):
    return random_string(length)

def random_domain_email(domain):
    username = random_string(8)
    return f"{username}@{domain}"

# DATA INPUTS
def launch_option(option):
    if option == 'domain' or option == 'new_account':
        email, username, password = data_return(option)
        create_steam_account(email.lower(), username.lower(), password)
    else:
        email_list = data_return(option)
        for i in range(len(email_list)):
            print(f"\tGenerating account nr {i+1}")
            create_steam_account(email_list[i].lower(), email_list[i].split("@")[0].lower(), random_password(14))

def data_return(x):
    if x == "domain":
        email, username, password = user_domain()
        return email, username, password
    elif x == 'new_account':
        email = input('\tEnter your email: ')
        username = email.split("@")[0]
        password = random_password(14)
        return email, username, password
    else:
        emails_list = read_accounts_from_csv_file()
        return emails_list

def user_domain():
    global Domain_Input
    if Domain_Input == '':
        Domain_Input = input("\tInput domain: ")
        email = random_domain_email(Domain_Input)
    else:
        email = random_domain_email(Domain_Input)
    username = email.split("@")[0]
    password = random_password(14)
    return email, username, password

# WEBHOOK
def send_to_webhook(email, username, password):
    webhook_url = read_webhook()
    if webhook_url == 'INSTEAD OF THIS LINE PUT YOUR DISCORD WEBHOOK TO GET NOTIFICATIONS!' or webhook_url == "":
        print(f"\tInvalid webhook, change in webhook.txt if you would like to.\n\tContinue...")
    else:
        webhook = SyncWebhook.from_url(webhook_url)
        webhook.send(f"Steam account created\nEmail: {email}\nUsername: {username}\nPassword: {password}")

# MESSAGE
def welcome_message():
    print('')
    print('--------------------------------------------------')
    print(f'| WELCOME TO STEAM-ACCOUNT-GENERATOR VERSION {version} |')
    print('--------------------------------------------------')
    print('')
    list_message = [[1, "create accounts from file"], [2, "create new account each time"], [3, "create accounts using your domain"], [4, "Create example file"], [5, "HELP"], [6, "Contact info"]]
    column = ["Options", "Description"]
    df = pd.DataFrame(list_message, columns=column)
    print(df.to_string(index=False))

def Help():
    # advanced descriptions of functions NEEDS TO BE DONE
    print('\n\tHELP')
    print('\tOption domain supports custom user domains')

def Contact():
    print('\n\tContact information')
    print('\tdiscord: lilkajt#6121')

# GENERATOR
def create_steam_account(email, username, password):
    sleep(np.random.uniform(0, 0.1))
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    sleep(6)
    driver.find_element(By.XPATH, '//*[@id="email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(x), sleep(np.random.uniform(0, 0.1))
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="reenter_email"]').send_keys(x), sleep(np.random.uniform(0, 0.1))
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="i_agree_check"]').click()
    notification("captcha")
    print("\n\tCaptcha confirmed!")
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    notification("email")
    print("\n\tEmail confirmed!")
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="accountname"]').click()
    for x in username: driver.find_element(By.XPATH, '//*[@id="accountname"]').send_keys(x), sleep(np.random.uniform(0, 0.1))
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(x), sleep(np.random.uniform(0, 0.1))
    sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="reenter_password"]').send_keys(x), sleep(np.random.uniform(0, 0.1))
    username = name_check(driver, username)
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    sleep(7)
    print("\tAccount successfully created")
    data_to_csv(email, username, password)
    send_to_webhook(email, username, password)
    driver.close()

def name_check(driver, og_username):
    if driver.find_element(By.ID, 'accountname_availability').text == "Not Available":
        sleep(1)
        driver.find_element(By.ID, "suggested_name_1").click()
        username = driver.find_element(By.XPATH, '//*[@id="suggested_name_1"]').text
        print(f"\tName taken. Changing name.\n\tNew name {username}")
        notification("account name")
        return username
    return og_username

# start
def program_start():
    os.system(clear_line)
    welcome_message()
    match (input("Input number you choose: ")):
        case "1":
            os.system(clear_line)
            print('\tYou choose creating accounts from file')
            launch_option("file_accounts")
        case "2":
            os.system(clear_line)
            print('\tYou choose creating new accounts each time')
            for i in range(int(input('\tHow many accounts would you like to generate? '))):
                print(f"\tGenerating account nr {i+1}")
                launch_option("new_account")
        case "3":
            os.system(clear_line)
            print('\tYou choose creating accounts using your domain\t')
            for i in range(int(input('\tHow many accounts would you like to generate? '))):
                print(f"\tGenerating account nr {i+1}")
                launch_option("domain")
        case "4":
            os.system(clear_line)
            print('\tCreating example file')
            create_new_example_file(input("\tWhat file name do you want: "))
            print('\tDone! Check current folder')
            sleep(3)
            program_start()
        case "5":
            os.system(clear_line)
            Help()
            sleep(5)
            program_start()
        case "6":
            os.system(clear_line)
            Contact()
            sleep(5)
            program_start()
        case other:
            print(f"Incorrect input! {other}")
            print('Restarting!')
            sleep(5)
            os.system(clear_line)
            program_start()

try:
    program_start()
    sleep(1)
except Exception as err:
    print(err)
    print("Press any key to close the program...")
    input()