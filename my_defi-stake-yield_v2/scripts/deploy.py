import scripts.helpful_scripts  as xhelp

from brownie import JoMoXToken,TokenFarm, accounts,config,network
from web3 import Web3
import json
import yaml
import shutil
import os
import pytest




token1_name='weth_token'
token2_name="fau_token"

def deploy_token_farm_jomox_token():
   owner= xhelp.get_account()  # deployer
   print(f"{owner.address} - {owner.balance()}")
   
   print("1 deploy main token contract and take reward token to farm")
   
   jomox_token=JoMoXToken.deploy(xhelp.INIT_SUPPLY,{"from": owner})
   token_symbol=jomox_token.symbol()
   print(f"{token_symbol}#{jomox_token.address} - Total  Supply :{Web3.fromWei(jomox_token.totalSupply(),'ether')}")

   print( f"{token_symbol} of Deployer = {Web3.fromWei(jomox_token.balanceOf(owner.address),'ether')}")

   # constructor (address _rewardTokenAddress,uint256 _pct_reward_token_dist,uint256 _digit_percent)
   print("2 deploy DefiFarm contract and supplied token to the farm for distrubuting reward")
   token_farm=TokenFarm.deploy(jomox_token.address,xhelp.PERCERNT_REWARD, {"from": owner},
   publish_source= config["networks"][network.show_active()]["verify"])

   #no_token_to_defi_farm=jomox_token.totalSupply()-xhelp.KEPT_BALANCE
   no_token_to_defi_farm=jomox_token.totalSupply()
   print(f"Send {token_symbol} token to defil-farm : {Web3.fromWei(no_token_to_defi_farm,'ether')}")
   print("######################################################################")
   
   tx=jomox_token.transfer(token_farm.address,no_token_to_defi_farm,{"from": owner})
   tx.wait(1)
   #print(tx.info())
   print(f"TotalSupply Of {token_symbol} supplied from Owner to defi-farm : {Web3.fromWei( token_farm.getTotalSupplyOfRewardToken(),'ether') }" )
   print( f"Last {token_symbol} of Deployer = {Web3.fromWei(jomox_token.balanceOf(owner.address),'ether')}")
   
   print("######################################################################")
   
   print("3. deploy some other tokens to farm to allow staker to deposit to get reward")
   print("get contract of token to be allowed for user to farm")  

   weth_token=xhelp.get_contract(token1_name)
   print(f"{token1_name}#{weth_token.address} - Total Tokens :{Web3.fromWei(weth_token.totalSupply(),'ether')}")
   fau_token=xhelp.get_contract(token2_name)
   print(f"{token2_name}#{fau_token.address} - Total Tokens :{Web3.fromWei(fau_token.totalSupply(),'ether')}")
   print("######################################################################")

   print("4. add these tokens defi farm for staking")
   dict_of_allowed_tokens={
        jomox_token: xhelp.get_contract("dai_usd_price_feed"),
        fau_token: xhelp.get_contract("dai_usd_price_feed"),
        weth_token: xhelp.get_contract("eth_usd_price_feed"),

   }
   token_farm=add_allowed_tokens(token_farm,dict_of_allowed_tokens,owner)


   print("The number of  tokens allowed on this farm : ",token_farm.listNumberOfAllowedToken())
   print("######################################################################")

  
# #    if front_end_update:
# #      update_front_end()

   return token_farm,jomox_token,weth_token,fau_token,owner

def add_allowed_tokens(token_farm,dict_allowed_tokens,account):
    print("----------  Starting Adding token  and set address for retrieving price---------------")
    for token in dict_allowed_tokens:
        
        add_tx=token_farm.addAllowedToken(token.address,{"from":account})
        add_tx.wait(1)
        
        price_feed_aggregator=dict_allowed_tokens[token]
        set_tx=token_farm.setPriceFeedContract(token.address,price_feed_aggregator.address,{"from":account})
        #set_price_tx=token_farm.setPriceFeedContract(token.address, price_feed,{"from":account})
        set_tx.wait(1)

        x_price,x_decimal=token_farm.getTokenValue(token)
        print(f"{token} - {price_feed_aggregator} | price : {Web3.fromWei( x_price,'ether')}")
      
        

    print("------------Complete adding token&price to farm-------------------")

    return token_farm

 







