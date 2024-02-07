'''

This project { Bank Management Project (BMP) is created by:
Ishaan Rastogi, student of Amity University, Noida
Modified program for Harvard edX Course CS50x Final Project
I am a citizen of India and this is CS50.

'''

#importing desired modules: random, pickle, os, pathlib

import random
import pickle
import os
import pathlib

# to create class Account

class Account :
    accNo = 0
    name = ''
    deposit = 0
    type = ''

#function to create user account
    
    def createAccount(self):

        # Generating Random Account Number

        p=random.randint(0,100000000000000000000)
        print("Your account number is",p)
        print("\n\t\t\t NOTE: \n")
        print("Kindly note that no new account number will be generated if the number is lost, so we request the user to  ")
        print("please note the listed above number somewhere safe. The number will be required at different places while")
        print("carrying out the bank transactions & further operations. \n")
        self.accNo= p

        #Gathering name of user

        self.name = input("Enter the account holder name : ")

        #Information about Current & Saving Accounts to user
        
        print("\n\t\t\t NOTE: \n")
        print("Current account is just for saving money in the bank, no provisional interest will be provided, be it ")
        print("compound or simple.\n")
        self.type = input("Ente the type of account [C (Current) / S (Savings) ] : ")

        #Gathering further details about deposit amount, email and phone number
        
        self.deposit = int(input("Enter The Initial amount:"))
        self.email = (input("Enter your email:"))
        self.phno = int(input("Enter your phone number:"))
        print("\n\n\n\t\t\tAccount Created!")
        

    #function to show user account
    
    def showAccount(self):
        print("Account Number : ",self.accNo)
        print("Account Holder Name : ", self.name)
        print("Type of Account",self.type)
        print("Balance : ",self.deposit)

    #function to modify user account
    
    def modifyAccount(self):
        print("Account Number : ",self.accNo)
        self.name = input("Modify Account Holder Name :")
        self.type = input("Modify type of Account :")
        self.deposit = int(input("Modify Balance :"))
        
    #function to deposit amount

    def depositAmount(self,amount):
        self.deposit += amount

    #function to withdraw amount
    
    def withdrawAmount(self,amount):
        self.deposit -= amount

    #function to create database

    def report(self):
        print(self.accNo, " ",self.name ," ",self.type," ", self.deposit)

    #functions to get Account details

    def getAccountNo(self):
        return self.accNo
    def getAcccountHolderName(self):
        return self.name
    def getAccountType(self):
        return self.type
    def getDeposit(self):
        return self.deposit

    #function to welcome users to our bank!
    #Project Details
    #Bank Details
    #Bank Notice Board

def intro():
    print(" ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲")
    print("◀                                                                                         ")
    print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
    print("◀                                                                                         ")
    print("◀\t\t\t\t \t     WELCOME !!!                                     ")
    print("◀                                                                                         ")
    print("◀\t\t\t\t ﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌                              ")
    print("◀                                                                                         ")
    print("◀\t\t\t\t     BANK  MANAGEMENT  SYSTEM                                ")
    print("◀                                                                                         ")
    print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
    print("◀                                                                                         ")
    print("◀\t\t\t                MADE BY : Ishaan Rastogi ")
    print("◀                                                                                         ")
    print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
    print("◀                                                                                         ")
    print("◀\t\t\t  University : Amity University, Noida Campus, AUUP")
    print("◀                                                                                         ")
    print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
    print("◀                                                                                         ")
    print("◀\t\t\tWelcome to Lakshmi Saraswati Parvati National Bank (LSPN Bank ) User Database!")
    print("◀                                                                                         ")
    print("◀\t\t\t\t      ࿐. *. ⋆---------•»--•--«•---------•°. *࿐                        ")
    print("◀                                                                                         ")
    print("◀\t\t\tWelcome to Lakshmi Saraswati Parvati National Bank (LSPN Bank ) Notice Board!")
    print("◀                                                                                         ")
    print("◀\t\t\t\t WARNING NOTE!:")
    print("◀                                                                                         ")
    print("◀\t Don't share the details of your bank account to anyone to ensure proper, safe and secure transactions")
    print("◀\t and operations. Bank will not be responsible for loss of any money if the listed above mistake is")
    print("◀\t being made by the user.")
    print("◀                                                                                         ")
    print("◀\t\t\t\t SAFETY NOTE!:")
    print("◀                                                                                         ")
    print("◀\t However, an user can contact the bank on 9037590375 via phone, if there is any money theft.")
    print("◀\t A proper detailed report will be filed by RBI (Reserve Bank Of India ) and we will have to act")
    print("◀\t accordingly.")
    print("◀                                                                                         ")
    print("◀\t\t\t\t AWARENESS NOTE!:")
    print("◀                                                                                         ")
    print("◀\t\t To be aware of the guidelines of RBI, visit the official website of RBI listed as")
    print("◀\t\t\t\t\t www.rbi.org.in")
    print("◀                                                                                         ")
    print("◀\t\t\t\t SUGGESTIONS WELCOMED!:")
    print("◀                                                                                         ")
    print("◀ To suggest how we can modify our user database to make the bank operations easy & 24/7 availabe, kindly")
    print("◀ reach us on the following mail: ")
    print("◀\t\t\t\t\t lspnb@gmail.com")
    print("◀                                                                                         ")
    print(" ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼")

    input("Press Enter To Continue: ")
    
# function to write Account

def writeAccount():
    account = Account()
    account.createAccount()
    writeAccountsFile(account)

# function to display Accounts created

def displayAll():
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        mylist = pickle.load(infile)
        for item in mylist :
            print(item.accNo," ", item.name, " ",item.type, " ",item.deposit )
        infile.close()
    else :
        print("No records to display")
        
# function to calculate balance of a bank account

def displaySp(num): 
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        mylist = pickle.load(infile)
        infile.close()
        found = False
        for item in mylist :
            if item.accNo == num :
                print("Your account Balance is : ",item.deposit)
                found = True
    else :
        print("No records to Search")
    if not found :
        print("No existing record with this number")

# function to deposit or withdraw a certain amount from the bank account

def depositAndWithdraw(num1,num2): 
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        mylist = pickle.load(infile)
        infile.close()
        os.remove('accounts.dat')
        for item in mylist :
            if item.accNo == num1 :
                if num2 == 1 :
                    amount = int(input("Enter the amount to deposit : "))
                    item.deposit += amount
                    print("Your account is updated!")
                elif num2 == 2 :
                    amount = int(input("Enter the amount to withdraw : "))
                    if amount <= item.deposit :
                        item.deposit -=amount
                        print("Amount withdrawn succefully!")
                    else :
                        print("You cannot withdraw larger amount")
                
    else :
        print("No records to Search")
    outfile = open('newaccounts.dat','wb')
    pickle.dump(mylist, outfile)
    outfile.close()
    os.rename('newaccounts.dat', 'accounts.dat')

# function to delete the bank account
    
def deleteAccount(num):
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        oldlist = pickle.load(infile)
        infile.close()
        newlist = []
        for item in oldlist :
            if item.accNo != num :
                newlist.append(item)
        os.remove('accounts.dat')
        outfile = open('newaccounts.dat','wb')
        pickle.dump(newlist, outfile)
        outfile.close()
        os.rename('newaccounts.dat', 'accounts.dat')

# function to find Simple Interest on the principal amount

def simple_interest(nm):
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        mylist = pickle.load(infile)
        for item in mylist:
            if int(item.accNo) == nm:
                if item.type != 'C':
                    P = item.deposit
                    N = float(input("Enter the number of years : "))
                    R = 4
                    #calculate simple interest by using this formula
                    myint =P*N*R/100
                #print
                print("Simple interest : {}".format(myint))
        infile.close()
    else :
        print("No records to display")
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        mylist = pickle.load(infile)
        infile.close()
        found = False
        for item in mylist :
            if item.accNo == num :
                print("Amount after applying simple interest: ",item.deposit+myint)
                found = True
    else :
        print("No records to Search")
    if not found :
        print("No existing record with this number")

#function to carry out operations on bank loans

def loans():
    print(" NOTICE : Please visit your nearest NNB bank for more detailed information about loans personally ! ↴")
    print("  ")
    print("\tTypes of loans our bank offers:")
    print("  ")
    print("\t1. HOME LOANS-")
    print("\n\t\tHome loans are a secured mode of finance that give you the funds to buy or build the home of")
    print("\t\tyour choice")
    print("\n\t\t\tTypes of Home Loans:\n")
    print("\t\t\t\t ① Land Purchase Loan")
    print("\t\t\t\t ② Home Construction")
    print("\t\t\t\t ③ Loan-Top Up Loan")
    print("\n\t2. GOLD LOAN-")
    print("\n\t\tGold loans requires you to pledge gold jewellery or coins as collateral.")
    print("\n\t3. LOANS AGAINST MUTUAL FUNDS AND SHARES-")
    print("\n\t\tMutual funds can also be pledged as collateral for a loan. ")
    print("\t\tYou can pledge equity or hybrid funds to the financial institution for availing of a loan.")
    print("\n\t4. PERSONAL LOAN")
    print("\n\t\tThe interest rates are higher than secured loans here as it is an unsecured loan. A good credit")
    print("\t\tscore and high stable income ensures that you can avail this loan at a competitive interet rate.")
    print("\n\t5. SHORT TERM BUSINESS LOAN-")
    print("\n\t\tIt can be used to meet various entities and organisation's expansion, and daily expenses.")
    print("\n\t6. EDUCATION LOAN-")
    print("\n\t\tIt is availed specifically to finance educational requirements towards a school or a college.")
    print("\n\t7. VEHICLE LOAN-")
    print("\n\t\tA vehicle loan is extended in the form of a two or four wheeler loan that helps you buy your")
    print("\t\tdream vehicle.")
    print("\n\t8. AGRICULTURE LOAN-")
    print("\n\t\tThese loans are provided to farmers to meet the expenses of their day-to-day or general")
    print("\t\tagricultural requirements.")
    print("\n\t9. LOAN AGAINST CREDIT CARD-")
    print("\n\t\tThis loan is like a personal loan that is taken against your credit card.")
    print("\t\tThese are usually pre-approved loans that do not require any additional documentation.")
    print("\n\t10. CONSUMER DURABLE LOAN-")
    print("\n\t\tThese loans are availed to finance the purchase of consumer durables such as a electronic")
    print("\t\tgadgets and household appliances.")

# function to find Compound Interest on the principal amount

def Compd(nm):
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        mylist = pickle.load(infile)
        for item in mylist:
            if int(item.accNo) == nm:
                if item.type != 'C':
                    P = item.deposit
                    N = float(input("Enter the number of years : "))
                    R = 4
                    #calculate compound interest by using this formula
                    myint = P*(1+R/100)**N
                #print
                print("Compound interest : {}".format(myint))
        infile.close()
    else :
        print("No records to display")
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        mylist = pickle.load(infile)
        infile.close()
        found = False
        for item in mylist :
            if item.accNo == num :
                print("Amount after applying compound interest: ",item.deposit+myint)
                found = True
    else :
        print("No records to Search")
    if not found :
        print("No existing record with this number")

    
# function to modify the details of the bank account
     
def modifyAccount(num):
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        oldlist = pickle.load(infile)
        infile.close()
        os.remove('accounts.dat')
        for item in oldlist :
            if item.accNo == num :
                item.name = input("Enter the account holder name : ")
                item.type = input("Enter the account Type : ")
                item.deposit = int(input("Enter the Amount : "))
                print("\n\nAccount Modified")   

        outfile = open('newaccounts.dat','wb')
        pickle.dump(oldlist, outfile)
        outfile.close()
        os.rename('newaccounts.dat', 'accounts.dat')

# function to write down the whole data in file
        
def writeAccountsFile(account): 
    
    file = pathlib.Path("accounts.dat")
    if file.exists ():
        infile = open('accounts.dat','rb')
        oldlist = pickle.load(infile)
        oldlist.append(account)
        infile.close()
        os.remove('accounts.dat')
    else :
        oldlist = [account]
    outfile = open('newaccounts.dat','wb')
    pickle.dump(oldlist, outfile)
    outfile.close()
    os.rename('newaccounts.dat', 'accounts.dat')
    
        
                                    # Start of the program

ch=''
num=0
intro()

ch='y'                                    # MAIN MENU
while ch =='y':
    print("\n\tMAIN MENU ↴")
    print("\t1. NEW ACCOUNT")
    print("\t2. DEPOSIT AMOUNT")
    print("\t3. WITHDRAW AMOUNT")
    print("\t4. BALANCE ENQUIRY")
    print("\t5. SIMPLE INTEREST")
    print("\t6. COMPOUND INTEREST")
    print("\t7. ALL ACCOUNT HOLDER LIST")
    print("\t8. CLOSE AN ACCOUNT")
    print("\t9. MODIFY AN ACCOUNT")
    print('\t10. TYPES OF LOANS OFFERED')
    print("\t11. EXIT")
    print("\tSelect Your Option (1-11) ")
    ch = input('\nEnter the choice:')

# CALLING OF FUNCTIONS TO MAKE THE PROJECT WORK!
    
    if ch == '1':
        writeAccount()
    elif ch =='2':
        num = int(input("\tEnter The account No. : "))
        depositAndWithdraw(num, 1)
    elif ch == '3':
        num = int(input("\tEnter The account No. : "))
        depositAndWithdraw(num, 2)
    elif ch == '4':
        num = int(input("\tEnter The account No. : "))
        displaySp(num)
    elif ch=='5':
        num = int(input("\tEnter The account No. : "))
        simple_interest(num)
    elif ch=='6':
        num = int(input("\tEnter The account No. : "))
        Compd(num)
    elif ch == '7':
        print("The following is the list of all accounts' details:\n\n")
        displayAll()
    elif ch == '8':
        num =int(input("\tEnter The account No. : "))
        deleteAccount(num)
        print("The bank account has been deleted successfully from our bank database!")
    elif ch == '9':
        num = int(input("\tEnter The account No. : "))
        modifyAccount(num)
    elif ch=='10':
        loans()

    #function to exit from our bank!
    #Project Details
    #Bank Details
    #Bank Notice Board
                                        
    elif ch == '11':

        print(" ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲")
        print("◀                                                                                         ")
        print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
        print("◀                                                                                         ")
        print("◀\t\t\t             Thanks for using BANK  MANAGEMENT  SYSTEM !!!                                     ")
        print("◀                                                                                         ")
        print("◀\t\t\t\t ﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌                              ")
        print("◀                                                                                         ")
        print("◀\t\t\t\t     COME BACK SOON!                                ")
        print("◀                                                                                         ")
        print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
        print("◀                                                                                         ")
        print("◀\t\t\t                MADE BY : Ishaan Rastogi ")
        print("◀                                                                                         ")
        print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
        print("◀                                                                                         ")
        print("◀\t\t\t  University : Amity University, Noida Campus, AUUP")
        print("◀                                                                                         ")
        print("◀\t\t\t\t   •——————•°•✧•°•——————•                                 ")
        print("◀                                                                                         ")
        print("◀You are biding a farewell to Lakshmi Saraswati Parvati National Bank (LSPN Bank ) User Database but don't forget us!")
        print("◀But before you go, let's hear sbout the future scope of this project. Wwe will like to extend our work")
        print("◀to run out foreign exchange services for our bank. So to ease the Indians going to foreign countries for")
        print("◀various purposes like Travel, Job, Education, etc. Our first aim will be to have American Dollar (USD) ($)")
        print("◀and Euro (€) transactions as they hold the strongest economic currency value currently and many of the ")
        print("◀students and people looking for employment go to America or other European countires like Germany UK, etc.. mostly ")
        print("◀                                                                                         ")
        print("◀\t\t\t\t      ࿐. *. ⋆---------•»--•--«•---------•°. *࿐                        ")
        print("◀                                                                                         ")
        print("◀\t\t\tWelcome to Lakshmi Saraswati Parvati National Bank (LSPN Bank ) Notice Board!")
        print("◀                                                                                         ")
        print("◀\t\t\t\t WARNING NOTE!:")
        print("◀                                                                                         ")
        print("◀\t Don't share the details of your bank account to anyone to ensure proper, safe and secure transactions")
        print("◀\t and operations. Bank will not be responsible for loss of any money if the listed above mistake is")
        print("◀\t being made by the user.")
        print("◀                                                                                         ")
        print("◀\t\t\t\t SAFETY NOTE!:")
        print("◀                                                                                         ")
        print("◀\t However, an user can contact the bank on 9037590375 via phone, if there is any money theft.")
        print("◀\t A proper detailed report will be filed by RBI (Reserve Bank Of India ) and we will have to act")
        print("◀\t accordingly.")
        print("◀                                                                                         ")
        print("◀\t\t\t\t AWARENESS NOTE!:")
        print("◀                                                                                         ")
        print("◀\t\t To be aware of the guidelines of RBI, visit the official website of RBI listed as")
        print("◀\t\t\t\t\t www.rbi.org.in")
        print("◀                                                                                         ")
        print("◀\t\t\t\t SUGGESTIONS WELCOMED!:")
        print("◀                                                                                         ")
        print("◀ To suggest how we can modify our user database to make the bank operations easy & 24/7 availabe, kindly")
        print("◀ reach us on the following mail: ")
        print("◀\t\t\t\t\t lspnb@gmail.com")
        print("◀                                                                                         ")
        print(" ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼")
    
        break
    else :
        print("Invalid choice! Please re-enter your choice again!")
    
    ch = input('Do you want to enter more? [y/n]:')
