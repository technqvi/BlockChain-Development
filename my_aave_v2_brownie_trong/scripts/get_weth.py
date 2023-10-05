from scripts.helpful_scripts import get_account
from brownie import interface, config, network, accounts
import sys


def main():
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})
    tx.wait(1)
    print("Received 0.1 WETH")

def return_weth(weth_val):
    """
    Mints WETH by withdraw ETH.
    """
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.withdraw( weth_val * 10 ** 18, {"from": account})
    tx.wait(1)
    print(f"Withdraw {weth_val} WETH")    
