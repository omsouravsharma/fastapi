
import pytest
from app.calculation import BankAccount, add, mul, div

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected",[
    (3,2,5),(1,7,8),(12,4,16)
])

def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1,num2) == expected

def test_mul():
    print("Testing mul function")
    assert mul(2,4) == 8

def test_div():
    print("Testing div function")
    assert div(4,2) == 2

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance ==50
    

def test_bank_default_account(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance ==0

def test_withdraw(bank_account):
    #bank_account = BankAccount(50)
    bank_account.withdrawl(20)
    assert bank_account.balance == 30

def test_deposite(bank_account):
    #bank_account = BankAccount(50)
    bank_account.deposite(20)
    assert bank_account.balance == 70

def test_collect_interest(bank_account):
    #bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,2) == 55

@pytest.mark.parametrize("deposited,withdrew,expected",[
    (300,100,200),(1000,700,300),(1200,400,800)
])

def test_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposite(deposited)
    zero_bank_account.withdrawl(withdrew)
    assert zero_bank_account.balance ==expected

def test_insufficient_fund(bank_account):
    with pytest.raises(Exception):
        bank_account.wihdrawl(200)