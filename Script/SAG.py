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
Version = '1.5'
url = "https://store.steampowered.com/join"
Domain_Input = ''

# FILE FUNCTIONS
def Data_to_excel_file(email, username, password):
    data = {"Email": email, "Username": username, "Password": password}
    df = pd.DataFrame(data, index=[0])
    file_path = f"{pathlib.Path().resolve()}\\Created_accounts.xlsx"

    if not os.path.exists(file_path):
        df.to_excel(file_path,sheet_name="Accounts",index=False)
    else:
        with pd.ExcelWriter(file_path,mode='a',engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer,sheet_name="Accounts",startrow=writer.sheets["Accounts"].max_row,index=False, header=False)

def read_accounts_from_excel_file():
    print('\tReading emails from excel file')
    file_name = input('\tWhat is the file name(without extension[must be xlsx]): ')
    emails = pd.read_excel(f"{pathlib.Path().resolve()}\\{file_name}.xlsx")
    return emails['Email'].tolist()

def Create_new_example_file(File_name):
    data = {"Email": 'Testemail@domain.com'}
    df = pd.DataFrame(data, index=[0])
    file_path = f"{pathlib.Path().resolve()}\\{File_name}.xlsx"

    if not os.path.exists(file_path):
        df.to_excel(file_path,sheet_name="Accounts",index=False)

def Read_webhook():
    f = open(f"{pathlib.Path().resolve()}\\webhook.txt", "r")
    return f.readline()

# WINDOWS NOTIFICATIONS
def Notification(Type):
    if Type == "email":
        key = "m"
    elif Type == "captcha":
        key = "c"
    else:
        key = "n"
    print(f'\n\tCheck {Type} to confirm!\n\tPress \"{key}\" to continue!')
    while True:
        # toast.show_toast(
        #     f"Check {Type} Steam",
        #     f"Press \"{key}\" to continue!",
        #     duration = 10,
        #     icon_path='icon.ico',
        #     threaded = True
        # )
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

def create_account_launch_option(option):
    if (option == 'domain' or option == 'new_account'):
        email,username,password = data_return(option)
        Create_steam_account(email,username,password)
    else:
        email_list = data_return(option)
        for i in range(len(email_list)):
            print(f"\tGenerating account nr {i+1}")
            Create_steam_account(email_list[i],email_list[i].split("@")[0],random_password(12))

def data_return(x):
    if x == "domain":
        email,username, password = user_domain()
        return email,username, password
    elif x == 'new_account':
        email = input('\tEnter your email: ')
        username = email.split("@")[0]
        password = random_password(12)
        return email,username, password
    else:
        emails_list = read_accounts_from_excel_file()
        return emails_list

def user_domain():
    global Domain_Input
    if Domain_Input == '':
        Domain_Input = input("\tInput domain: ")
        email = random_domain_email(Domain_Input)
    else:
        email = random_domain_email(Domain_Input)
    username = email.split("@")[0]
    password = random_password(12)
    return email,username,password

# WEBHOOK

def send_to_webhook(email,username,password):
    if Read_webhook()!='':
        webhook = SyncWebhook.from_url(Read_webhook())
        webhook.send(f"Steam account created\nEmail: {email}\nUsername: {username}\nPassword: {password}")

# MESSAGE

def welcome_message():
    print('')
    print('---------------------------------------------------')
    print('| WELCOME TO STEAM-ACCOUNT-GENERATOR BETA VERSION |')
    print('---------------------------------------------------')
    print(' ' * int((len('| WELCOME TO STEAM-ACCOUNT-GENERATOR BETA VERSION |')- len(f'version {Version}'))/2) + f'version {Version}')
    print('')
    programe_options = [[1,"create accounts from file"],[2,"create new account each time"],[3,"create accounts using your domain"],[4,"Create example file"],[5,"HELP"],[6,"Contact info"]]
    column = ["Options","Description"]
    df = pd.DataFrame(programe_options,columns=column)
    print(df.to_string(index=False))

def help_func():
    # advanced descriptions of functions
    print('Help not working currently!')

# WEBDRIVER MAIN PROG

def Create_steam_account(email, username, password):
    # input()
    time.sleep(np.random.uniform(0,0.1))
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(6)
    driver.find_element(By.XPATH, '//*[@id="email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(x),time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="reenter_email"]').send_keys(x),time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="i_agree_check"]').click()
    Notification("captcha")
    print("\n\tCaptcha confirmed!")
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    Notification("email")
    print("\n\tEmail confirmed!")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="accountname"]').click()
    for x in username: driver.find_element(By.XPATH, '//*[@id="accountname"]').send_keys(x),time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(x),time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="reenter_password"]').send_keys(x),time.sleep(np.random.uniform(0,0.1))
    username = Name_check(driver,username)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    time.sleep(7)
    print("\tAccount successfuly created")
    Data_to_excel_file(email,username,password)
    send_to_webhook(email,username,password)
    driver.close()

def Name_check(driver, og_username):
    if driver.find_element(By.ID, 'accountname_availability').text == "Not Available":
        time.sleep(1)
        driver.find_element(By.ID,"suggested_name_1").click()
        username = driver.find_element(By.XPATH, '//*[@id="suggested_name_1"]').text
        print(f"\tName taken. Changing name.\n\tNew name {username}")
        Notification("account name")
        return username
    return og_username


def Main():
    os.system('cls||clear')
    welcome_message()
    match (input("Input number you choose: ")):
        case "1":
            os.system('cls||clear')
            print('\tYou choose creating accounts from file')
            create_account_launch_option("file_accounts")
        case "2":
            os.system('cls||clear')
            print('\tYou choose creating new accounts each time')
            for i in range(int(input('\tHow many accounts would you like to generate? '))):
                print(f"\tGenerating account nr {i+1}")
                create_account_launch_option("new_account")
        case "3":
            os.system('cls||clear\n')
            print('\tYou choose creating accounts using your domain\t')
            for i in range(int(input('\tHow many accounts would you like to generate? '))):
                print(f"\tGenerating account nr {i+1}")
                create_account_launch_option("domain")
        case "4":
            os.system('cls||clear')
            print('\tCreating example file')
            Create_new_example_file(input("\tWhat file name do you want: "))
            print('\tDone! Check current folder')
            time.sleep(3)
            Main()
        case "5":
            os.system('cls||clear')
            print('\n\tHELP')
            help_func()
            time.sleep(5)
            Main()
        case "6":
            os.system('cls||clear')
            print('\n\tContact information')
            print('\tdiscord: lilkajt#6121')
            print('\temail: contact@wavebead.net')
            time.sleep(5)
            Main()
        case other:
            print(f"Incorrect input! {other}")
            print('Restarting!')
            time.sleep(2)
            os.system('cls||clear')
            Main()

try:
    Main()
    time.sleep(1)
except Exception as err:
    print(err)