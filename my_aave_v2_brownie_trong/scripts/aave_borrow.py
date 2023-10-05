from brownie import accounts, network, config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth,return_weth
from web3 import Web3

# 0.1
AMOUNT = Web3.toWei(0.1, "ether")

#https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool
#https://docs.aave.com/developers/v/2.0/the-core-protocol/weth-gateway
#https://docs.aave.com/developers/v/2.0/the-core-protocol/price-oracle
#https://docs.aave.com/developers/v/2.0/the-core-protocol/protocol-overview
#https://docs.aave.com/developers/v/2.0/deployed-contracts/deployed-contracts
#https://aave-api-v2.aave.com/
#https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool/ilendingpool


def main():



    account = get_account()
    print(account)


    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
        print("Get WETH Already")

    lending_pool = get_lending_pool()
    print(f"Lending Pool V2 :{lending_pool.address}")

    approve_tx = approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)
    print(f"Approve using  ETH for AAVE Lending Pool   :{lending_pool.address}")
    
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")


    # ...how much do you want borrow?
    # borrowable_eth ==> 0.1 worth of ETH deposited.
    # total_debt_eth ==> 0 worth of ETH borrowed.
    # total_collateral_et ==> can borrow 0.0825 worth of ETH of your collateral.
    
    print("AVVE Account before borrowing")
    # float(available_borrow_eth), float(total_debt_eth),float(total_collateral_eth))
    borrowable_eth, total_debt,total_collateral_eth = get_borrowable_data(lending_pool, account)


    print("Let's borrow!")
    # DAI in terms of ETH
    #https://docs.chain.link/docs/ethereum-addresses/
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    print(dai_eth_price)
    
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    # borrowable_eth -> borrowable_dai * 95%
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")


    # # # Now we will borrow!
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI!")

    print("AVVE Account  before repaying")
    get_borrowable_data(lending_pool, account)

    # I made an oopsie in the video with this!!
    repay_x(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)
    # repay_x(Web3.toWei(243.50159, "ether"), lending_pool, account)
    # repay_x(Web3.toWei(0.000008158836209, "ether"), lending_pool, account)
    


    print("AVVE Account after repaying abosolutely")
    borrowable_eth, total_debt,total_collateral_eth =get_borrowable_data(lending_pool, account)
    print(
        "You just deposited, borrowed, and repayed with Aave, Brownie, and Chainlink!"
    )

    print("Withdrawing...")
    amount_to_withdraw=total_collateral_eth
    print(amount_to_withdraw)
    tx = lending_pool.withdraw(
        erc20_address, Web3.toWei(0.1, "ether"), account.address,  {"from": account})
    tx.wait(1)

    return_weth(0.5) 



def repay_x(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)

    print("Repaid!")




def get_asset_price(price_feed_address):
    #https://docs.chain.link/docs/get-the-latest-price/
    #function getLatestPrice() public view returns (int) 
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)

    # only the index 1 
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)


def get_borrowable_data(lending_pool, account):
    #https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#getuseracountdata
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print("=====================YourAccountData=============================")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    print(f"Your liquidation threshold is {current_liquidation_threshold}")
    print(f"Your loan to value (LVT) is {ltv}")
    print(f"Your health_factor is {health_factor}")

    print("================================================================")
    
    return (float(available_borrow_eth), float(total_debt_eth),float(total_collateral_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
