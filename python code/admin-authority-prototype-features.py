import mysql.connector
import os
from decimal import Decimal # for Decimal datatype input in mysql
from tabulate import tabulate # for precise (& effortless lol) tables & columns formatting 


def connectDatabase():
  connection = None
  try:                     # NOTE: all users who will access the database must be connected to the same network
    host = "192.168.1.24"  # Set to this according to your internet's ip address (to check the ip address, go to the terminal and type: ipconfig)
    username = "miguel"
    password = "password"
    database = "banking_system"

    connection = mysql.connector.connect(
        host= host,
        user= username,
        password= password,
        database= database
    )
    
    print("Database Initialization Successful...")
    
  except mysql.connector.Error as error:
    print(f"Failed Database Connectivity: {error}")
    
  return connection


def tableFormatter(cursor): # using the tabulate library
  rows = cursor.fetchall()
  if rows:
    # extract column names from the cursor.description
    headers = [desc[0] for desc in cursor.description]
    # use the tabulate function to format the results as a table
    table = tabulate(rows, headers, tablefmt="pretty")
    print(table)
  else:
      print("No records found.")
  
  
def continueSession(): # dedicated for looping purposes
  continue_session = int(input("\nContinue Session (1 | 0): "))
  if continue_session == 1:
    return 1
  else:
    return 0


def checkAcc_existence(cursor, accNumber, column): # to be used in the admin_editUser and admin_deleteUser
  query = f"SELECT * FROM {column} WHERE accountnumber = %s" # searches the accNumber
  cursor.execute(query, (accNumber,))
  account_exists = cursor.fetchone() # checks the account's existence
  return account_exists
  





def adminMain():
  os.system('cls')
  connection = connectDatabase()
  
  while True:
    try:
      print("\n_______ADMIN AUTHORIZED_______\n"
      "\t[1] View Users\n"
      "\t[2] Edit Users\n"
      "\t[3] Delete Users")
      
      action = int(input("\n\tAction: "))
      
      if action == 1:
        admin_viewUser(connection)
        break

      elif action == 2:
        admin_editUser(connection)
        break

      elif action == 3:
        admin_deleteUser(connection)
        break
      
      else:
        print("Invalid Input")
        
    except ValueError as error:
      print(f"Invalid Input: {error}")



def admin_viewUser(connection):
  os.system('cls')
  cursor = connection.cursor()
  
  while True:
    os.system('cls')
    print("\n_______VIEW USERS_______\n"
      "\t[1] Main Account\n"
      "\t[2] Personal Info\n"
      "\t[3] Identity Info\n"
      "\t[4] Financial Info\n"
      "\t[5] All Records")
      
    try: 
      action = int(input("\n\tAction: "))
      
      if action == 1:
        query = "SELECT * from customermainaccount"
        cursor.execute(query)
        tableFormatter(cursor) # formats the data
        if not continueSession(): # returns to home if continue_session ==0
          adminMain()
           
      elif action == 2:
        query = "SELECT * FROM userpersonalinfo"
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()

      elif action == 3:
        query = "SELECT * FROM useridentityinfo"
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()
        
      elif action == 4:
        query = "SELECT * FROM userfinanceinfo"
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()
      
      elif action == 5:
        # retrieving customer information by joining multiple tables based on foreign key references
        # combining data from CustomerMainAccount, UserPersonalInfo, UserIdentityInfo, and UserFinanceInfo tables

        query = """
        SELECT 
            P.CustomerID, 
            C.AccountNumber, 
            C.AccountType, 
            P.UserFName, 
            P.UserLName, 
            FORMAT(C.Balance, 2) AS Balance, 
            C.Status, 
            I.IDNumber, 
            I.IDType, 
            F.Occupation, 
            FORMAT(F.AnnualGrossIncome, 2) AS AnnualGrossIncome 
        FROM 
            CustomerMainAccount AS C  
        JOIN UserPersonalInfo AS P ON C.CustomerID = P.CustomerID 
        JOIN UserIdentityInfo AS I ON C.CustomerID = I.CustomerID AND C.CustomerID = I.CustomerID 
        JOIN UserFinanceInfo AS F ON C.CustomerID = F.CustomerID AND I.IDNumber = F.IDNumber
        """
        cursor.execute(query)
        tableFormatter(cursor)
        if not continueSession(): 
          adminMain()
     
      else:
        print("Invalid Input...")
        
    except ValueError as error:
      print("\n\tValue Error: ", error)
  
  

def admin_editUser(connection):
  os.system('cls')
  cursor = connection.cursor()
  
  while True:
    os.system('cls')
    try:
      print("\n_______EDIT USERS_______\n"  # data/values editing would be table-based
          "\t[1] Main Account\n"
          "\t[2] Personal Info\n"
          "\t[3] Identity Info\n"
          "\t[4] Financial Info\n"
          "\t[5] All Records")

      action = int(input("\n\tEdit From: "))
      
      if action == 1: # for Main Account
        print("\n---Main Account---")
        accNumber = input("\n\tAccount Number (Ex. Acc001): ")
        column = "customermainaccount"
        account_exists = checkAcc_existence(cursor, accNumber, column)
        
        
        if account_exists:  
          print("\n\t [1] Account Type\n\t [2] Account Balance\n\t [3] Account Status\n\t") # specifying the column in the selected table
          attribute = int(input("Choose Account Attribute: "))
          
          if attribute == 1:
            column = "accounttype" # both are to be passed as arguments
            value = input(f"New Account Type (Savings | Checking): ")
            
          elif attribute == 2:
            column = "balance"
            value = Decimal(input("New Account Balance: ")) # aligned to the mysql datatype
            
          elif attribute == 3:
            column = "status"
            value = input("New Account Status (Active | Inactive): ")
            
          else:
            print("Invalid attribute choice")
            return
        
          main_query = f"UPDATE customermainaccount SET {column} = %s WHERE accountnumber = %s"
          cursor.execute(main_query, (value, accNumber)) 
          connection.commit() # a must
          print(cursor.rowcount, "updated...", f"ID: {accNumber}")
          
          if not continueSession(): # looping
            adminMain()
        
        
      elif action == 2: # Personal Info
        pass # same approach, won't specify it further since this is just a sample
      
      elif action == 3: # Identity Info
        pass
      
      elif action == 4: # Financial
        pass
      
      elif action == 5: # All Records
        pass
      
    except ValueError as error:
      print(f"Invalid Input: {error}")
    
        
        
def admin_deleteUser(connection):
  os.system('cls')
  cursor = connection.cursor()
  while True:
    os.system('cls')
    try:
      print("\n_______DELETE USERS_______\n"  # 
          "\t[1] Main Account\n"
          "\t[2] Personal Info\n"
          "\t[3] Identity Info\n"
          "\t[4] Financial Info\n"
          "\t[5] All Records")
      
      action = int(input("\n\tDelete From: "))
      
      if action == 1: # Main Axxount
        accNumber = input("\n\tAccount Number (Ex. Acc001): ")
        column = "customermainaccount"
        account_exists = checkAcc_existence(cursor, accNumber, column)
        
        
        if account_exists:
          query = "DELETE FROM customermainaccount WHERE accountnumber = %s"
          try: 
            cursor.execute(query, (accNumber,))
            connection.commit()
            print(cursor.rowcount, "row/s deleted....", cursor.lastrowid)
            
          except mysql.connector.Error as error:
            print(f"Deletion Error: {error}")
          
          if not continueSession():
            adminMain()
            
        else:
         print("Account does not exist.")
          
      elif action == 2: # Personal Info
        pass # same concept/approach
      
      elif action == 3: # Identity Info
        pass

      elif action == 4: # Financial Info
        pass

      elif action == 5: # All Records
        pass

    except ValueError as error:
      print(f"Invalid Input....{error}")
  
def checkCosAcc_existence(cursor, accnum):
  query = f"SELECT * FROM customermainaccount WHERE AccountNumber = %s"
  cursor.execute(query, (accnum,))
  account_exists = cursor.fetchone()
  return account_exists


def customerWith(connection, accnum):
  os.system('cls')
  cursor = connection.cursor()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]

  while True:
    while True:
      os.system('cls')
      try:
        print("\n\t___________________________\n"
            f"\n\tYour cerrent balance is {Balance:.2f}\n")
        action = int(input("\tEnter the amount you want to withdraw: "))
        break
      except ValueError:
        print("\n\t___________________________\n"
              "\n\tError, please enter a valid integer")
      
    if action <= Balance:
      os.system('cls')
      print(f"\n\tThe amount you want to withdraw is {action}...\n")
      newbal = Balance - action
      query = "UPDATE customermainaccount SET Balance = %s where AccountNumber = %s"
      cursor.execute(query, (newbal, accnum))
      connection.commit()

      query = "SELECT Balance from customermainaccount where AccountNumber = %s"
      cursor.execute(query,(accnum,))
      result = cursor.fetchone()
      Balance = result[0]
    
      print("\n\t___________________________\n"
            f"\n\tTransaction completed successfully, your new balance is {newbal:.2f}.")
      input("\tPress Enter to Return to Customer Home Page...")
      break

    elif action > Balance:
      os.system('cls')
      print(f"\n\t___________________________\n"
            "\n\tThe amount you want to withdraw exceeds your current balnce")
      if not continueSession():
          break


def customerDpst(connection, accnum):
  os.system('cls')
  cursor = connection.cursor()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]

  while True:
    try:
      os.system('cls')
      print("\n\t___________________________\n"
          f"\n\tYour cerrent balance is {Balance:.2f}\n")
      action = int(input("\tEnter the amount you want to deposit: "))
      break
    except ValueError:
      print("\n\t___________________________\n"
            "\n\tError, please enter a valid integer")
    
  os.system('cls')
  print(f"\n\tThe amount you want to deposit is {action}...\n")
  newbal = Balance + action
  query = "UPDATE customermainaccount SET Balance = %s where AccountNumber = %s"
  cursor.execute(query, (newbal, accnum))
  connection.commit()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]

  print("\n\t___________________________\n"
        f"\n\tTransaction completed successfully, your new balance is {newbal:.2f}.")
  input("\tPress Enter to Return to Customer Home Page...")


def customerBal(connection, accnum):
  os.system('cls')
  cursor = connection.cursor()

  query = "SELECT Balance from customermainaccount where AccountNumber = %s"
  cursor.execute(query,(accnum,))
  result = cursor.fetchone()
  Balance = result[0]
  print("\n\t___________________________\n")
  print(f"\tYour Current Balance is {Balance:.2f}.")
  input("\tPress Enter to Return to Customer Home Page...")

def customerMain():
  os.system('cls')
  connection = connectDatabase()
  cursor = connection.cursor()

  while True:
    accnum = input(str("\n\tEnter you dedicated account number: "))
    account_exist = checkCosAcc_existence(cursor, accnum)
    if account_exist:
      while True:
        try:
          os.system('cls')
          print("\n_______Customer Page_______\n"
          "\t[1] Withdraw Money\n"
          "\t[2] Deposit Amount\n"
          "\t[3] Transfer Money\n"
          "\t[4] Check Balance\n"
          "\t[5] Logout")
          
          action = int(input("\n\tAction: "))
          
          if action == 1:
            customerWith(connection, accnum)

          elif action == 2:
            customerDpst(connection, accnum)

          elif action == 3:
            break

          elif action == 4:
            customerBal(connection, accnum)
          
          elif action == 5:
            os.system('cls')
            break
          
          else:
            print("Invalid Input...")
            
        except ValueError as error:
          print(f"Invalid Input...")
    else:
      os.system('cls')
      print(f"Invalid Account Number...")

  
# program entrance
adminMain()
#customerMain() # for customer page














# def fetchValues(cursor): # user-defined function to avoid reps in implementing the fetch_all function
#   results = cursor.fetchall()
#   for rows in results:
#     print(rows)
