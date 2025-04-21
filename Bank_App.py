from abc import ABC, abstractmethod
class Customer:
    def __init__(self, customer_id, name,email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        
    def display_info(self):
        print(f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}")   
    
    
    class Account(ABC):
        def __init__(self, account_number, balance, customer):
            self.account_number = account_number
            self.balance = balance
            self.customer = customer
        
        @abstractmethod
        def deposit(self, amount):
            pass
        
        @abstractmethod
        def withdraw(self, amount):
            pass
        
        @abstractmethod
        def get_balance(self):
            pass
        @abstractmethod
        def display_account_info(self):
            pass
        
    class SavingsAccount(Account):
        def __init__(self, account_number, customer, interest_rate):
            super().__init__(account_number, customer)
            self.interest_rate = interest_rate 
    
        def deposit(self, amount):
            if amount > 0:
                self.balance += amount
                print(f"Deposited ${amount:.2f}")
            else:
                print("Deposit amount must be positive.")
    
        def withdraw(self, amount):
            if amount <= 0:
                print("You do not have enough balance!.")
            elif amount > self.balance:
                print("Insufficient balance.")
            else:
                self.balance -= amount
                print(f"Withdrew ${amount:.2f}")
    
        def get_balance(self):
            return self.balance
    
        def display_account_info(self):
            print("\n--- Savings Account Info ---")
            self.customer.display_info()
            print(f"Account Number: {self.account_number}")
            print(f"Balance: ${self.balance:.2f}")
            print(f"Interest Rate: {self.interest_rate * 100}%")
    
        def apply_interest(self):
            interest = self.balance * self.interest_rate
            self.balance += interest
            print(f"Applied interest: ${interest:.2f}")

    class CurrentAccount(Account):
        def __init__(self, account_number, customer, overdraft_limit):
            super().__init__(account_number, customer)
            self.overdraft_limit = overdraft_limit  

        def deposit(self, amount):
            if amount > 0:
                self.balance += amount
                print(f"Deposited ${amount:.2f}")
            else:
                print("Deposit amount must be positive.")

        def withdraw(self, amount):
            if amount <= 0:
                print("Withdrawal amount must be positive.")
            elif self.balance - amount < -self.overdraft_limit:
                print("Withdrawal exceeds overdraft limit.")
            else:
                self.balance -= amount
                print(f"Withdrew ${amount:.2f}")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        print("\n--- Current Account Info ---")
        self.customer.display_info()
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ${self.balance:.2f}")
        print(f"Overdraft Limit: ${self.overdraft_limit:.2f}")

# classes are already defined: Customer, BankAccount, SavingsAccount, CurrentAccount

# Dictionary to store accounts by account number
accounts = {}

def create_customer():
    customer_id = input("Enter customer ID: ")
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    return Customer(customer_id, name, email)

def open_account():
    customer = create_customer()
    account_type = input("Enter account type (savings/current): ").lower()
    account_number = input("Enter new account number: ")

    if account_type == "savings":
        interest_rate = float(input("Enter interest rate (e.g. 0.05 for 5%): "))
        account = Customer.SavingsAccount(account_number, customer, interest_rate)
    elif account_type == "current":
        overdraft_limit = float(input("Enter overdraft limit: "))
        account = Customer.CurrentAccount(account_number, customer, overdraft_limit)
    else:
        print("Invalid account type.")
        return

    accounts[account_number] = account
    print("Account created successfully!")

def deposit_money():
    account_number = input("Enter account number: ")
    if account_number in accounts:
        amount = float(input("Enter amount to deposit: "))
        accounts[account_number].deposit(amount)
    else:
        print("Account not found.")

def withdraw_money():
    account_number = input("Enter account number: ")
    if account_number in accounts:
        amount = float(input("Enter amount to withdraw: "))
        accounts[account_number].withdraw(amount)
    else:
        print("Account not found.")

def show_account_info():
    account_number = input("Enter account number: ")
    if account_number in accounts:
        accounts[account_number].display_account_info()
    else:
        print("Account not found.")

# Main Menu
def main():
    while True:
        print("\n--- Welcome to MY Bank ---")
        print("1. Open New Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Show Account Info")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            open_account()
        elif choice == "2":
            deposit_money()
        elif choice == "3":
            withdraw_money()
        elif choice == "4":
            show_account_info()
        elif choice == "5":
            print("Thank you for using MY Bank. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
