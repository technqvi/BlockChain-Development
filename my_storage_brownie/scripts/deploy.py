from brownie import accounts,config,SimpleStorage,network
#import os
def deploy_simple_storage():
  deploy_acc=get_account()

  print(deploy_acc.address)
  acc_from={"from":deploy_acc}  #accounts[0]
  # account=accounts.add(os.getenv("PRIVATE_KEY"))     OR  account=accounts.add(config["wallets"]["from_key"])
  x_contract=SimpleStorage.deploy(acc_from)
  print(x_contract.address)

  
def get_account():
  if network.show_active() in  ["development","ganache-local"]:
    return accounts[0]
  else:
    return accounts.add(config["wallets"]["from_key"])


def main():
    print("Hello, Implement ETH using Bronwie-Python Framework")
    deploy_simple_storage()