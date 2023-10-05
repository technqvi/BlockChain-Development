from multiprocessing.connection import wait
from brownie import JoMoXToken,TokenFarm,MockDAI,MockWETH, accounts,config,network,web3
from  scripts.deploy import deploy_token_farm_jomox_token
import scripts.helpful_scripts  as xhelp

import pytest

fau_no_stake=web3.toWei(10000, "ether")
weth_no_stake=web3.toWei(20000, "ether")
def test_stake_weth_fau():
   defi_farm,jomox_token,weth_token,fau_token,deployer=deploy_token_farm_jomox_token()
   user_test=xhelp.get_account() # get account0 is deployer/user_test

   fau_before=fau_token.balanceOf(user_test)
   weth_before= weth_token.balanceOf(user_test)

   fau_token.approve(defi_farm.address,fau_no_stake,{'from': user_test})
   tx_stake_fau=defi_farm.stakeToken(fau_no_stake,fau_token.address,{'from': user_test})
   tx_stake_fau.wait(1)

   weth_token.approve(defi_farm.address,weth_no_stake,{'from': user_test})
   tx_stake_weth=defi_farm.stakeToken(weth_no_stake,weth_token.address,{'from': user_test})
   tx_stake_weth.wait(1)

   fau_farm_stake=defi_farm.getBalaneTokensStakedByUser(user_test,fau_token)
   weth_farm_stake=defi_farm.getBalaneTokensStakedByUser(user_test,weth_token)

   fau_after=fau_token.balanceOf(user_test)
   weth_after= weth_token.balanceOf(user_test)

   assert   fau_after==fau_before-fau_no_stake
   assert   weth_after==  weth_before-weth_no_stake
   assert   fau_farm_stake+weth_farm_stake==fau_no_stake+weth_no_stake

def test_distribute():
   defi_farm,jomox_token,weth_token,fau_token,deployer=deploy_token_farm_jomox_token()
   user_test=xhelp.get_account() 

   fau_token.approve(defi_farm.address,fau_no_stake,{'from': user_test})
   tx_stake_fau=defi_farm.stakeToken(fau_no_stake,fau_token.address,{'from': user_test})
   tx_stake_fau.wait(1)
   weth_token.approve(defi_farm.address,weth_no_stake,{'from': user_test})
   tx_stake_weth=defi_farm.stakeToken(weth_no_stake,weth_token.address,{'from': user_test})
   tx_stake_weth.wait(1)

  
   init_reward=jomox_token.balanceOf(defi_farm) 

   issue_tx =defi_farm.issueTokens({"from": user_test})
   issue_tx.wait(1)

   after_dist_reward=jomox_token.balanceOf(defi_farm)
   my_reward=jomox_token.balanceOf(user_test)

   assert  init_reward==after_dist_reward+my_reward



def test_unstake_weth_fau():
   defi_farm,jomox_token,weth_token,fau_token,deployer=deploy_token_farm_jomox_token()
   user_test=xhelp.get_account() 

   fau_before=fau_token.balanceOf(user_test)
   weth_before= weth_token.balanceOf(user_test)

   fau_token.approve(defi_farm.address,fau_no_stake,{'from': user_test})
   tx_stake_fau=defi_farm.stakeToken(fau_no_stake,fau_token.address,{'from': user_test})
   tx_stake_fau.wait(1)
   weth_token.approve(defi_farm.address,weth_no_stake,{'from': user_test})
   tx_stake_weth=defi_farm.stakeToken(weth_no_stake,weth_token.address,{'from': user_test})
   tx_stake_weth.wait(1)

   tx_unstake_all_fau=defi_farm.unstakeAllToken(fau_token.address,{'from': user_test})
   tx_unstake_all_fau.wait(1)

   tx_unstake_half_weth=defi_farm.unstakePartialToken(weth_no_stake/2,weth_token.address,{'from': user_test})
   tx_unstake_half_weth.wait(1)

   fau_farm_stake=defi_farm.getBalaneTokensStakedByUser(user_test,fau_token)
   weth_farm_stake=defi_farm.getBalaneTokensStakedByUser(user_test,weth_token)


   fau_after=fau_token.balanceOf(user_test)
   weth_after= weth_token.balanceOf(user_test)

   assert   fau_after==fau_before
   assert   weth_after==weth_before- weth_no_stake/2
   assert   fau_farm_stake==0
   assert   weth_farm_stake==weth_no_stake/2

















