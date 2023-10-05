from brownie import FundMe
from web3 import Web3

import scripts.helpful_scripts as x_help
def fund():
    fund_me = FundMe[-1]
    account = x_help.get_account()
    print(account)
    print(fund_me.address)
    entrance_fee = fund_me.getEntranceFee()
    print(f"The current entry fee is {entrance_fee}")
    print("=============Funding===========")
    fund_me.fund({"from":account,"value":entrance_fee })

def withdraw():
     fund_me=FundMe[-1] 
     account=x_help.get_account()
     fund_me.withdraw({"from":account})

def fund_serveral_accouns(x):
    amount_accs=[2,4,1,3,5]
    for i in range(0,len(amount_accs)):
        acc=x_help.get_account(index=i)
        amount=Web3.toWei(amount_accs[i],'ether')
        print(f"{acc.address} has {Web3.fromWei(acc.balance(),'ether')} and spend {amount_accs[i]} to FundME")
        tx=x.fund({'from':acc,'value': amount})

        tx.wait(1)
        print(f"{acc.address} has {Web3.fromWei(acc.balance(),'ether')} left")

    print("===============================================")
    listFunders=x.listAllFunders()
    for funder in listFunders:
        my_fund=x.addressToAmountFunded(funder)
        print(my_fund)
    
    
def main():
    fund()
    withdraw()