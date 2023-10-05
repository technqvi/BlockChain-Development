from brownie import (
    network,
    accounts,
    config,
    interface,
    LinkToken,
    MockV3Aggregator,
    MockWETH,
    MockDAI,
    Contract,
)

from web3 import Web3
#JoMoX Token mint : 1000000000000000000000000  
INITIAL_PRICE_FEED_VALUE = 5000000000000000000  # 1 ETH =5 Price
# Mock_PRICE_WETH=2000000000000000000000
# Mock_PRICE_JOMOX=5000000000000000000
# Mock_PRICE_STABLECOIN =1000000000000000000
DECIMALS = 18


# 1=e18 
#https://eth-converter.com/
#KEPT_BALANCE=Web3.toWei(1000,"ether")
INIT_SUPPLY=Web3.toWei(1000000,"ether")
KEPT_BALANCE=Web3.toWei(10000,"ether")

# get reward  2 percent of your total value
PERCERNT_REWARD=1  # 1 % of your current value
#PERCERNT_REWARD=0.1 # invalid in float type


NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development","ganache-local"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]

# Dict to stor contract object by key
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "fau_token": MockDAI,
    "weth_token": MockWETH,
}


def get_account(index=None, id=None):
    print(f"Your account are on {network.show_active()}")
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS: #focus on development network
        return accounts[0]  # account 0 is owner (deployer)
    if id:
        return accounts.load(id)

    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """If you want to use this function, go to the brownie config and add a new entry for
    the contract that you want to be able to 'get'. Then add an entry in the in the variable 'contract_to_mock'.
    You'll see examples like the 'link_token'.
        This script will then either:
            - Get a address from the config
            - Or deploy a mock to use for a network that doesn't have it

        Args:
            contract_name (string): This is the name that is refered to in the
            brownie config and 'contract_to_mock' variable.

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            Contract of the type specificed by the dictonary. This could be either
            a mock or the 'real' contract on a live network.
    """
    contract_type = contract_to_mock[contract_name]
    print(f"===================Start Getting {contract_name}=====================")
    if network.show_active() in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(f"NON_FORKED_LOCAL_BLOCKCHAIN : {network.show_active()}")
        if len(contract_type) <= 0:
            print("Deploy Mock to create contract-Abi")
            deploy_mocks()

        print("Get Latest contract")    
        contract = contract_type[-1]
        
    else:
        print(f"Live_OR_Fork_BLOCKCHAIN : {network.show_active()}")
        try:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )
            print(
                f"brownie run scripts/deploy_mocks.py --network {network.show_active()}"
            )
    print(f"===================Completed To Get {contract_name}=====================")        
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=1000000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = interface.LinkTokenInterface(link_token).transfer(
        contract_address, amount, {"from": account}
    )
    print("Funded {}".format(contract_address))
    return tx


def get_verify_status():
    verify = (
        config["networks"][network.show_active()]["verify"]
        if config["networks"][network.show_active()].get("verify")
        else False
    )
    return verify


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_PRICE_FEED_VALUE):
    """
    Use this script if you want to deploy mocks to a testnet
    """

    print("Deploying Mocks...")
    account = get_account()

    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Deployed to {link_token.address}")

    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print(f"Deployed to {mock_price_feed.address}")

    print("Deploying Mock DAI...")
    dai_token = MockDAI.deploy(INIT_SUPPLY,{"from": account})
    print(f"Deployed to {dai_token.address}")

    print("Deploying Mock WETH")
    weth_token = MockWETH.deploy(INIT_SUPPLY,{"from": account})
    print(f"Deployed to {weth_token.address}")
    
# We didn't have this in the video, but it's a helpful script to have you issue the tokens!
def issue_tokens():
    """You can call this function once you have deployed your TokenFarm contract to a live network
    and have users that have staked tokens.

    Note that it relies on get_contract, so be mindful to correctly configure your Token Farm contract
    into brownie-config.yaml as well as the contract_to_mock dict as described in the get_contract docstring

    Run this function with this command: `brownie run scripts/issue_tokens.py --network kovan`

        This function will:
            - Print your account address and deployed TokenFarm contract address to confirm that you're using the right ones
            - Call issueTokens on your deployed TokenFarm contract to issue the DAPP token reward to your users
    """
    account = get_account()
    print(f"Issue Tokens called by: {account}")
    token_farm = get_contract("TokenFarm")
    print(f"TokenFarm contract called to issue tokens: {token_farm}")
    tx = token_farm.issueTokens({"from": account})
    tx.wait(1)
