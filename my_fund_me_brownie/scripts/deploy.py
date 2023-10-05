from brownie import accounts,FundMe,MockV3Aggregator,network,config
from web3 import Web3
import scripts.helpful_scripts as x_help
#import os
def deploy_fund_me():
    account=x_help.get_account()

    if network.show_active() not in x_help.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address=config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        x_help.deploy_mocks()
        price_feed_address=MockV3Aggregator[-1].address  # recent contract

    x_contract=FundMe.deploy(price_feed_address,
    {"from":account},
    publish_source=config["networks"][network.show_active()].get("verify")
    )

    print("Deploy Fund me to address ",x_contract. address )
    return x_contract


def main():
    # print("Hello, Implement ETH using Bronwie-Python Framework")
    x=deploy_fund_me()    

    