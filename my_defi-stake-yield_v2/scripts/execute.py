from brownie import JoMoXToken,TokenFarm,MockDAI,MockWETH, accounts,config,network,Contract,web3

#from web3 import Web3
from  scripts.deploy import deploy_token_farm_jomox_token
import scripts.helpful_scripts  as xhelp
#from web3 import Web3
import pytest



def main():
#    brownie run scripts\execute.py --network ganache-local
#    brownie run scripts\execute.py --network development
#    brownie run scripts\execute.py --network rinkeby  kovan
 #https://eth-brownie.readthedocs.io/en/stable/core-contracts.html
 defi_farm,jomox_token,weth_token,fau_token,deployer=deploy_token_farm_jomox_token()
#  defi_farm=Contract.from_abi("TokenFarm","0xedD819CF2Ff375E7a3188d7cb6550Ccd425D6adA",TokenFarm.abi)
#Contract.from_explorer("0x6b175474e89094c44da98b954eedeac495271d0f")
#  print(defi_farm.listAllAllowedTokenForStaking())
 #defi_farm=TokenFarm[-1]
 #print(defi_farm.address)
 #print(type(TokenFarm.abi))
 #print("defi-stake deploy")


