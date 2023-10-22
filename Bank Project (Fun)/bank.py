import json
import os

class Accounts: 

    def __init__(self, account_number, account_holder_name): 
        self.account_number = account_number
        self.balance = 0
        self.account_holder_name = account_holder_name

    def deposit(self):
        while True:
            message = input("Hello, would you like to deposit money? (Y/N) ").upper()
            self.balance = self.load_balance()
            if message == 'Y':
                try:
                    bank_deposit = int(input("How much would you like to deposit? "))
                    if bank_deposit <= 0:
                        print("Please enter a valid positive amount.")
                        continue
                    self.balance += bank_deposit
                    self.save_balance()
                    print(f"We have successfully updated your balance.")
                    print(f"Your new balance is {self.balance}")
                except ValueError:
                    print("Please enter a valid amount.")
                    continue
            elif message == 'N':
                break
            else:
                print("This is not a valid response...")
        print("Thanks, this transaction is complete!")


    def save_balance(self):
        with open(f"{self.account_number}_account_balance.txt", 'w') as file:
            file.write(str(self.balance))

    def load_balance(self):
        if os.path.exists(f"{self.account_number}_account_balance.txt"):
            with open(f"{self.account_number}_account_balance.txt", 'r') as file:
                return int(file.read())
        return 0
            
    def withdraw(self):
        while True:
            withdraw_request = input("Hello, would you like to withdraw money? (Y/N) ").upper()
            self.balance = self.load_balance()
            if withdraw_request == 'Y': 
                withdraw_amount = input("How much would you like to withdraw? ")
                if int(withdraw_amount): 
                    pass
                else:
                    print("Sorry, you must enter a number...")
                    continue
                withdraw_amount = int(withdraw_amount)
                self.balance -= withdraw_amount
                self.save_balance()
                print(f"You have withdrawn {withdraw_amount}.")
                print(f"Balance = {self.balance}")
                continue_request = input("Would you like to withdraw again or exit? Press 'W' or 'E': ").upper()
                if continue_request == 'W':
                    continue
                if continue_request == 'E':
                    quit()
            if withdraw_request == 'N':
                print("We are returing you to home screen...")
                break 

class UserAuthentication:

    def load_database():
        if os.path.exists("user_database.txt"):
            with open("user_database.txt", 'r') as file:
                data = file.read()
                if not data:
                    return {}
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    print("Error reading user database. Data might be corrupted.")
                    return {}
        return {}
    
    def save_database(database):
        with open("user_database.txt", 'w') as file:
            file.write(json.dumps(database))

    def register():
        registered_users = UserAuthentication.load_database()

        username = input("Please enter a username: ")
        if username in registered_users:
            print("This username has already been taken!")
            print("Please try a different username: ")
            return None
        else: 
            password = input("Please enter a password: ")
            confirm_password = input("Please confirm your password: ")
            if password == confirm_password:
                registered_users[username] = password
                UserAuthentication.save_database(registered_users)
                print("Your account has been successully created.")
                return Accounts(username, username)
            else: 
                print("Passwords do not match!")
                return None
    
    def login():
        registered_users = UserAuthentication.load_database()
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        if username in registered_users and registered_users[username] == password:
            print("Login successful!")
            return Accounts(username, username)  # Return the user's account object
        else:
            print("Invalid credentials!")
            return None
        
if __name__ == "__main__":

    print("Hello!, welcome to our bank simulation!")
    choice = input("Would you like to register or login? (R/L): ").upper()
    if choice == 'R':
        account = UserAuthentication.register()
    elif choice == 'L':
        account = UserAuthentication.login()
    else: 
        print("This is not a valid reponse...")
        quit()

    if account: 
        while True:
            option = input("Hello, what can we do for you today? (deposit/withdraw) or 'q' to quit: ").lower()
            if option == 'deposit':
                account.deposit()
            elif option == 'withdraw':
                account.withdraw()
            elif option == 'q':
                print("Thanks, have a wonderful day! ")
                break
            else: 
                print("This is not a valid response...")
                continue


