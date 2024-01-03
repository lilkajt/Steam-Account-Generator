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
import discord
import pathlib

ChromeOptions = Options()
ChromeOptions.add_argument("--log-level=3")
Version = "2.2"
Url = "https://store.steampowered.com/join"
SteamIcon = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/240px-Steam_icon_logo.svg.png"
BotUrl="https://github.com/lilkajt/Steam-Account-Generator"
DomainInput = ""
ClearConsole = os.system("cls||clear")
BotPath = pathlib.Path().resolve()

# FILE FUNCTIONS
def ExportCSV(email, username, password):
    data = {"Email": email, "Username": username, "Password": password}
    df = pd.DataFrame(data, index=[0])
    filePath = f"{BotPath}\\CreatedAccounts.csv"

    if not os.path.exists(filePath):
        df.to_csv(filePath, index=False)
    else:
        df.to_csv(filePath, mode="a", index=False, header=False)

def AccountsFromCSV():
    fileName = input("\tWhat is the file name(without extension): ")
    file = pd.read_csv(f"{BotPath}\\{fileName}.csv")
    emails = file["Email"].tolist()
    usernames = file["Username"].tolist()
    passwords = file["Password"].tolist()
    return emails, usernames, passwords

def ExampleFile(fileName):
    data = {"Email":"Testemail@domain.com", "Username":"test1", "Password":"testpassword"}
    df = pd.DataFrame(data, index=[0])
    filePath = f"{BotPath}\\{fileName}.csv"

    if not os.path.exists(filePath):
        df.to_csv(filePath, index=False)

def WebhookURL():
    f = open(f"{pathlib.Path().resolve()}\\webhook.txt", "r")
    return f.readline()

# NOTIFICATIONS
def Notification(notiType):
    if notiType == "email":
        key = "m"
    elif notiType == "captcha":
        key = "c"
    else:
        key = "n"
    print(f"\n\tCheck {notiType} to confirm!\n\tPress \"{key}\" to continue!")
    while True:
        if BasicBoard.is_pressed(key):
            break

# RANDOM STRINGS
def RndString(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def RndPassword(length):
    return RndString(length)

def RndDomainEmail(domain):
    username = RndString(8)
    return f"{username}@{domain}"

# DATA INPUTS
def GenerateOption(option):
    if option == "domain":
        email, username, password = Domain()
        GenAccount(email, username, password)
    elif option == "newAccount":
        email, username, password = OneAccount()
        GenAccount(email, username, password)
    else:
        emails, usernames, passwords = AccountsFromCSV()
        for i in range(len(emails)):
            print(f"\tGenerating account nr {i+1}")
            GenAccount(emails[i], usernames[i], passwords[i])

def OneAccount():
        email = input("\tEnter your email: ")
        username = email.split("@")[0]
        password = RndPassword(14)
        return email, username, password

def Domain():
    global DomainInput
    if DomainInput == "":
        DomainInput = input("\tEnter your domain: ")
        email = RndDomainEmail(DomainInput)
    else:
        email = RndDomainEmail(DomainInput)
    username = email.split("@")[0]
    password = RndPassword(14)
    return email, username, password

# WEBHOOK
def WebhookSend(email, username, password, profLink):
    webhookUrl = WebhookURL()
    if webhookUrl == "INSTEAD OF THIS LINE PUT YOUR DISCORD WEBHOOK TO GET NOTIFICATIONS!" or webhookUrl == "":
        print("\tInvalid webhook, change in webhook.txt.\n\tContinue...")
    else:
        webhook = discord.SyncWebhook.from_url(webhookUrl)
        webhook.send(embed=DiscordEmbed(email, username, password, profLink))

def DiscordEmbed(email, username, password, profLink):
    embed = discord.Embed(
        title="New Steam Account",
        color=0x669900
    )
    embed.set_author(name="SAG - Steam Account Generator", url=BotUrl)
    embed.add_field(name="Username", value=f"{username}")
    embed.add_field(name="Password", value=f"||{password}||")
    embed.add_field(name="Email", value=f"{email}",inline=False)
    embed.add_field(name="Profile link", value=f"{profLink}",inline=False)
    embed.set_footer(text="Account generated using SAG bot by Lilkajt", icon_url=SteamIcon)
    return embed

# MESSAGE
def MenuMessage():
    print("")
    print("--------------------------------------------------")
    print(f"| WELCOME TO STEAM-ACCOUNT-GENERATOR Version {Version} |")
    print("--------------------------------------------------")
    print("")
    messageList = [[1, "create accounts from file"], [2, "create new account each time"], [3, "create accounts using your domain"], [4, "Create example file"], [5, "HELP"], [6, "Contact info"]]
    column = ["Options", "Description"]
    df = pd.DataFrame(messageList, columns=column)
    print(df.to_string(index=False))

def Help():
    print("\n\tHELP")
    print("\tOption domain supports custom user domains")

def Contact():
    print("\n\tContact information")
    print("\tdiscord: lilkajt#6121")

# GENERATOR
def GenAccount(email, username, password):
    time.sleep(np.random.uniform(0, 0.1))
    driver = webdriver.Chrome(options=ChromeOptions)
    driver.get(Url)
    time.sleep(6)
    driver.find_element(By.XPATH, '//*[@id="email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(x), time.sleep(np.random.uniform(0, 0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="reenter_email"]').send_keys(x), time.sleep(np.random.uniform(0, 0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="i_agree_check"]').click()
    Notification("captcha")
    print("\n\tCaptcha confirmed!")
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    Notification("email")
    print("\n\tEmail confirmed!")
    # SameEmail(driver)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="accountname"]').click()
    for x in username: driver.find_element(By.XPATH, '//*[@id="accountname"]').send_keys(x), time.sleep(np.random.uniform(0, 0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(x), time.sleep(np.random.uniform(0, 0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="reenter_password"]').send_keys(x), time.sleep(np.random.uniform(0, 0.1))
    # username = NameCheck(driver, username)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    time.sleep(6)
    profLink = ExtractLink(driver)
    print("\tAccount successfully created")
    ExportCSV(email, username, password)
    WebhookSend(email, username, password, profLink)
    driver.close()

# Not working
def SameEmail(driver,option=True):
    element = f"return document.querySelectorAll(\"button\")[2].textContent"
    element = driver.execute_script(element)
    if element == "Continue" and option == True:
        driver.execute_script("EmailConfirmedVerified( 0 );")
    else:
        print("\tWaiting for input...")
        input()

# Not working
def NameCheck(driver, username):
    element = "return document.querySelectorAll(\".password_tag.warning\")[0].textContent"
    element = driver.execute_script(element)
    # print(f"name check script run element {element}")
    if element == "Not Available":
        time.sleep(1)
        newUsername = driver.execute_script("return document.querySelector(\"#suggested_name_1\").text")
        # newUsername = driver.find_element(By.XPATH, '//*[@id="suggested_name_1"]').text
        driver.find_element(By.ID, "suggested_name_1").click()
        print(f"\tName taken. Changing name.\n\tNew name {newUsername}")
        Notification("account name")
        return newUsername
    return username

def ExtractLink(driver):
    profLink = f"return document.querySelector(\"a\").getAttribute(\"href\")"
    profLink = driver.execute_script(profLink)
    return profLink

def ProgramMenu():
    ClearConsole
    MenuMessage()
    match (input("Input number you choose: ")):
        case "1":
            ClearConsole
            print("\tYou choose creating accounts from CSV file")
            GenerateOption("file_accounts")
        case "2":
            ClearConsole
            print("\tYou choose creating new accounts each time")
            for i in range(int(input("\tHow many accounts would you like to generate? "))):
                print(f"\tGenerating account nr {i+1}")
                GenerateOption("newAccount")
        case "3":
            ClearConsole
            print("\tYou choose creating accounts using your domain\t")
            for i in range(int(input("\tHow many accounts would you like to generate? "))):
                print(f"\tGenerating account nr {i+1}")
                GenerateOption("domain")
        case "4":
            ClearConsole
            print("\tCreating example file")
            ExampleFile(input("\tWhat file name do you want: "))
            print("\tDone! Check current folder")
            time.sleep(3)
            ProgramMenu()
        case "5":
            ClearConsole
            Help()
            time.sleep(5)
            ProgramMenu()
        case "6":
            ClearConsole
            Contact()
            time.sleep(5)
            ProgramMenu()
        case other:
            print(f"Incorrect input! {other}")
            print("Restarting!")
            time.sleep(5)
            ClearConsole
            ProgramMenu()

try:
    ProgramMenu()
    time.sleep(1)
except Exception as err:
    print(err)
    print("Press any key to close the program...")
    input()