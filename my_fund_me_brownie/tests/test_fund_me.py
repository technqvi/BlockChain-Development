
from multiprocessing.connection import wait

import pytest
from scripts.helpful_scripts import get_account,LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import accounts, network,exceptions

def test_can_fund_and_withdraw():
    account=get_account()
    x_contract=deploy_fund_me()

    entrance_fee=x_contract.getEntranceFee()+100
    tx1=x_contract.fund({"fund": account,"value":entrance_fee })
    tx1.wait(1)
    assert  x_contract.addressToAmountFunded(account.address)==entrance_fee
   
    tx2=  x_contract.withdraw({"from":account})
    tx2.wait(1)
    assert  x_contract.addressToAmountFunded(account.address)==0


def test_only_owner_can_withdraw():
   if network.show_active() not in     LOCAL_BLOCKCHAIN_ENVIRONMENTS:
       pytest.skip("only for local testing")

   fund_me=deploy_fund_me()
   bad_actor=accounts.add()
   print(bad_actor)
   
   with pytest.raises(exceptions.VirtualMachineError):
     print("Error")  
     fund_me.withdraw({"from":bad_actor})
