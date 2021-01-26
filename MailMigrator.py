# This script is limited to downloading from one server and uploading to another all the emails from the email accounts provided in the "migrationData.csv" file.
import csv
import imaplib
import os
import re
from printFormatter import colors
from datetime import datetime

now = datetime.now()
dateTime = now.strftime("%d-%m-%Y_%H:%M:%S")
os.system(f"mkdir ./{dateTime}/")
rootFolder = f"./{dateTime}/"

def openConnection(Server, serverPort, Account, Passwd): # It generates a connection with a mail server and authenticates with it using a given email and password.
    Connection = imaplib.IMAP4(host=Server, port=serverPort)
    try:
        Connection.login(user=Account, password=Passwd)
    except Exception as Error:
        print(f"{colors.bold}{colors.fg.red}[!] ERROR:{colors.reset} {colors.fg.red}{Error}{colors.reset}.")
        exit()
    return Connection

def listMailboxes(Server, serverPort, Account, Passwd, Row): # List all the mailboxes in an email account.s
    
    def parseMailboxes(Mailbox): # Extract the mailbox names from the raw output of the mailbox listing.
        listResponsePattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
        Match = listResponsePattern.match(Mailbox.decode("utf-8"))
        _Flags, _Delimiter, mailboxName = Match.groups()
        mailboxName = mailboxName.strip('"')
        return (mailboxName)

    Connection = openConnection(Server, serverPort, Account, Passwd)
    Name, _Domain = Account.split("@")
    userRootFolder = f"{rootFolder}{Name}/"
    os.system(f"mkdir -p {userRootFolder}")
    _serverResponse, rawMailboxes = Connection.list()
    Mailboxes = list()
    for Mailbox in rawMailboxes:
        Mailboxes.append(parseMailboxes(Mailbox))

    downloadMails(Connection, Mailboxes, Row, userRootFolder, Name)

def downloadMails(Connection, Mailboxes, Row, userRootFolder, Name): # Goes through all the mailboxes previously listed one by one and download all the emails within them in an orderly manner.
    for Mailbox in Mailboxes:
        serverResponse, Data = Connection.select(Mailbox)
        if serverResponse == "OK":
            print(f"{colors.bold}{colors.fg.blue}[⬇] Downloading from {Mailbox}.{colors.reset}")
            os.system(f"mkdir {userRootFolder}{Mailbox}")
            serverResponse, Data = Connection.search(None, "ALL")
            if serverResponse != "OK":
                print(f"{colors.bold}{colors.fg.red}[!] No messages found.{colors.reset}")
                return
            for Number in Data[0].split():
                serverResponse, Data = Connection.fetch(Number, '(RFC822)')
                if serverResponse != "OK":
                    print(f"{colors.bold}{colors.fg.red}[!] Error fetching message {int(Number)}{colors.reset}")
                    return
                
                fileName = os.path.join(f"{userRootFolder}{Mailbox}", f"{int(Number)}.eml")
                print(f"{colors.fg.green}[+] Saving message {fileName}{colors.reset}")
                with open(fileName, "wb") as File:
                    File.write(Data[0][1])
            Connection.close()
        else:
            print(f"{colors.bold}{colors.fg.red}!] Error opening mailbox {Mailbox}")
            Connection.close()

    Connection.logout()
    Connection = openConnection(Row[4], Row[5], Row[6], Row[7])
    uploadMails(Connection, Mailboxes, userRootFolder)

def uploadMails(Connection, Mailboxes, userRootFolder): # Create the old mailboxes on the new server and upload all previously downloaded emails in order.
    availableFolders = list(map(lambda x: x.split()[-1].decode(), Connection.list()[1]))
    for Mailbox in Mailboxes:
        if not Mailbox in availableFolders:
            Connection.create(Mailbox)
        print(f"{colors.bold}{colors.fg.blue}[⬆] Uploading to {Mailbox}.{colors.reset}")

        emlFileNames = [File for File in os.listdir(f"{userRootFolder}{Mailbox}") if File.endswith(".eml")]
        failedUploads = list()

        for i, emlFileName in enumerate(emlFileNames):
            with open(os.path.join(f"{userRootFolder}{Mailbox}", emlFileName), "rb") as eml:
                print(f"{colors.fg.green}[+] Uploading email {emlFileName} | {i+1}/{len(emlFileNames)}{colors.reset}")
                try:
                    serverResponse, Message = Connection.append(Mailbox, None, None, eml.read())
                except Exception as Error:
                    serverResponse = "ERR"
                    Message = Error
                
                if serverResponse != "OK":
                    failedUploads.append(emlFileName)
                    print(f"{colors.bold}{colors.fg.red}[!] Error uploading message.{colors.reset}")
                    print(f"{colors.bold}{colors.fg.red}{Message}{colors.reset}")
        
    print(f"{colors.bold}{colors.fg.green}[✔] Upload completed!{colors.reset}")
    print(f"{colors.bold}{colors.fg.red}[✘] {len(failedUploads)} failed uploads {failedUploads}.{colors.reset}")
    Connection.logout()


if __name__ == "__main__":
    os.system("clear")
    with open("migratioNData.csv") as migrationData:
        csvReader = csv.reader(migrationData, delimiter=",")
        lineCount = 0

        for Row in csvReader:
            if lineCount == 0:
                lineCount += 1
            else:
                print(f"{colors.bold}{colors.fg.blue}\t[✍] Migrating {Row[2]} on {Row[0]}:{Row[1]} to {Row[6]} on {Row[4]}:{Row[5]}...{colors.reset}")
                listMailboxes(Row[0], Row[1], Row[2], Row[3], Row)

                lineCount += 1

        print(f"{colors.bold}{colors.fg.green}[✔] Migrated {(lineCount - 1)} email accounts.{colors.reset}")