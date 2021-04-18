# use file to store database of bank account users
# save files in data directory
# name files according to account number, so account_number.txt
# add user details to file (eg name, email, password, balance)

import os #needed to delete files

# global variables
user_db_path = "data/accounts/"
user_auth_path = "data/authSession/"

# create file named account_number.txt
# add user details to file
def create_account(account_number, user_details):
    account_created = False
    try:
        f = open(user_db_path + str(account_number) + ".txt", "x")
        user_details = ",".join(user_details)
        f.write(user_details)
        account_created = True
    except:
        print("Unable to create account")
        delete_account(account_number)
    finally:
        f.close()
    return account_created

# check account number and password combination
def authenticate_user(account_number, password):
    if(account_exists(account_number)):
        details_str = get_account_details(account_number)
        if(details_str != "Error"):
            details_arr = str.split(details_str,",")
            return details_arr[3] == password
        else:
            print("Unable to authenticate user")
    else:
        print("Incorrect account number")
    return False

# delete file accountNumber.txt
def delete_account(account_number):
    if(account_exists):
        os.remove(user_db_path + str(account_number) + ".txt")

# get firstname, lastname, email, balance, password information for account number passed in
def get_account_details(account_number):
    ret_val = ""
    if(account_exists(account_number)):
        try:
            f = open(user_db_path + str(account_number) + ".txt")
            ret_val = f.readline()
        except:
            print("Unable to get account details")
            ret_val="Error"
        finally:
            f.close()

    return ret_val

# check if account number is in the database (e.g. file exists with name account_number.txt)
def account_exists(account_number):
    all_accounts = os.listdir(user_db_path)
    account = str(account_number) + ".txt"

    if(account in all_accounts):
        return True
    
    return False

# used when updating balance information
# overwrite file with user details
def update_account_balance(account_number, user_details):
    account_updated = False
    if(account_exists(account_number)):
        try:
            f = open(user_db_path + str(account_number) + ".txt", "w")
            f.write(",".join(user_details))
            account_updated = True
        except:
            print("Unable to update account balance")
        finally:
            f.close()

    return account_updated

# remove user from auth session
def delete_auth_session(account_number):
    try:
        os.remove(user_auth_path + str(account_number) + ".auth")
    except:
        print("Unable to remove user from auth session")

# create user auth session
def create_auth_session(account_number):
    try:
        open(user_auth_path + str(account_number) + ".auth", "x")
    except:
        print("Unable to create user auth session")
    
        
