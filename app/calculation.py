def add (num1:int, num2:int):
    return num1 + num2 


def mul (num1:int, num2:int):
    return num1 * num2 

def div (num1:int, num2:int):
    return num1 / num2 

class BankAccount():
    def __init__(self, starting_balance =0):
        self.balance = starting_balance
    
    def deposite(self, amount):
        self.balance +=amount
    
    def withdrawl(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient amount")
        self.balance -=amount
    
    def collect_interest(self):
        self.balance *=1.1