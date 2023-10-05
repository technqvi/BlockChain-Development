from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]


def get_account(index=None, id=None):
    if index:
        print("Get Account By Specifying Index")
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Get Account from  Local BC")
        return accounts[0]
    if id:
        print("Get Account By Specifying ID")
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        print("Get Account From MetaMark")
        return accounts.add(config["wallets"]["from_key"])
    return None
