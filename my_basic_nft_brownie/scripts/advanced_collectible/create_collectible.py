from brownie import AdvancedCollectible,accounts
import scripts.helpful_scripts as xhelp
from web3 import Web3
#step 2

def main():
 x_account=xhelp.get_account()
 advanced_x=AdvancedCollectible[-1]
 xhelp.fund_with_link(advanced_x.address,amount=Web3.toWei(0.1,"ether"))
 creation_tx=advanced_x.createCollectible({"from":x_account})
 creation_tx.wait(1)
 print("Collectible created")

