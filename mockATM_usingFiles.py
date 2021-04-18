#Nicole Peacock
#email: nap06c@gmail.com

from datetime import datetime  # needed to get current date/time
from getpass import getpass  # used to not display password when typing it
import random   # needed to generate random number
import database  # local module created


#keep count of number of incorrect logins
incorrect_login_count = 0


def init():
    print("\n\n######### Welcome to Bank XYZ #########\n")

    have_account = input("Do you already have an account with us? Enter yes or no \n")
    have_account = have_account.lower()

    if(have_account == "yes" or have_account == "y"):
        login()
    elif(have_account == "no" or have_account == "n"):
        register()
    else:
        print("You have entered an invalid response")
        init()

def login():
    print("\n\n######### Login #########\n")

    try:
        account_number = int(input("Please enter your account number\n"))
    except:
        print("Invalid account number")      
    else:
        password = getpass("Please enter your password\n")
        
        # check if account_number/password combination exists in database
        if(database.authenticate_user(account_number, password)):
            # convert user account information to array
            user_account = str.split(database.get_account_details(account_number), ",")
            database.create_auth_session(account_number)
            dt = datetime.now()
            dt_time = dt.strftime("%H:%M:%S")
            dt_date = dt.strftime("%m/%d/%Y")
            print("\nWelcome %s %s. Logged in at %s on %s" % (user_account[0], user_account[1], dt_time, dt_date))
            bank_menu(account_number, user_account)

    print("You have entered an incorrect account number or password")
     # if user enters 3 or more incorrect passwords, take back to main menu
    global incorrect_login_count
    incorrect_login_count += 1
    if(incorrect_login_count >= 3):
        incorrect_login_count = 0
        print("User name and password have been entered incorrectly too many times. Returning to main screen")
        init()
   
    login()


def register():
    print("\n\n######### Registration #########\n")

    firstname = input("Enter your first name\n")
    lastname = input("Enter your last name\n")
    email = input("Enter your email address\n")
    balance=input("Enter your starting account balance\n")
    
    # check if balance is a number (e.g. can be converted to float)
    if(is_valid_amount(balance)):
        password = getpass("Please enter your password\n")

        account_number = generateaccount_number()
        user_details = [firstname, lastname, email, password, balance]

        if(database.create_account(account_number, user_details)):
            print("\nCongratulation %s %s, your account has been created." % (firstname, lastname))  
            print("Your account number is %d" % (account_number))
            login()
   
    register()

def generateaccount_number():
    ranNum = random.randrange(1111111111,9999999999)

    # check if account number already exists
    if(database.account_exists(ranNum)):
        generateaccount_number()
    
    return ranNum

def bank_menu(account_number, user_accountDetails):
    print("\n\n######### Bank Main Menu #########\n")

    print("These are the available options:")
    print("(1) Withdrawal")
    print("(2) Cash Deposit")
    print("(3) Balance Inquiry")
    print("(4) Complaint")
    print("(5) Logout")
    print("(6) Exit")

    try:
        selected_option = int(input("Please select an option: "))
    except:
        print("You have entered an invalid option")
    else:
        if(selected_option == 1):
            withdrawal(account_number, user_accountDetails)
        elif(selected_option == 2):
            deposit(account_number, user_accountDetails) 
        elif(selected_option == 3):
            print("Your current balance is $%.2f" % float(user_accountDetails[4]))
        elif(selected_option == 4):
            input("What issue would you like to report?\n")
            print("Thank you for contacting us")
        elif(selected_option == 5):
           logout(account_number)
        elif(selected_option == 6):
           bank_exit(account_number)
        else:
            print("You have selected an invalid option")

    bank_menu(account_number, user_accountDetails)

            
def withdrawal(acct_num, user_account):
    withdraw_amount = input("How much would you like to withdraw\n")
    balance = float(user_account[4])
    if(is_valid_amount(withdraw_amount)):
        withdraw_amount = float(withdraw_amount)
        if(withdraw_amount > balance):
            print("Sorry, you do not have the required funds in your account to withdraw")
        else:
            user_account[4] = str(balance - withdraw_amount)
            if(database.update_account_balance(acct_num, user_account)):
                print("Take your cash!")
            else:
                user_account[4] = balance
        

def deposit(acct_num, user_account):
    deposit_amt = input("How much would you like to deposit?\n")
    balance = float(user_account[4])
    if(is_valid_amount(deposit_amt)):
        deposit_amt = float(deposit_amt)
        user_account[4] = str(balance + deposit_amt)
        if(database.update_account_balance(acct_num, user_account)):
            print("Your current balance is $%.2f" % float(user_account[4]))
        else:
            user_account[4] = balance

def logout(acct_num):
    print("\nLogging out........")
    database.delete_auth_session(acct_num)
    login()

def bank_exit(acct_num):
    database.delete_auth_session(acct_num)
    print("\nGoodbye")
    exit()

# verify balance is a proper float
def is_valid_amount(balance):
    try:
        float(balance)
        return True
    except:
        print("Invalid amount entered")
        return False


init()


