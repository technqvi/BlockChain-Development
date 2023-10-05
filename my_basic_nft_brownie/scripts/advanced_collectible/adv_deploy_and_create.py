import scripts.helpful_scripts as xhelp
from brownie import AdvancedCollectible,network,config
#step 1

#contract_to_mock = {: LinkToken, "vrf_coordinator": VRFCoordinatorMock}
def deploy_and_create():
    x_account=xhelp.get_account()

    # refer to constructor that you are supposed to take
    # constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee)
    advanced_x=AdvancedCollectible.deploy(
        xhelp.get_contract("vrf_coordinator"),
        xhelp.get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],  
        {"from": x_account})

    xhelp.fund_with_link(advanced_x.address)
    creating_tx=advanced_x.createCollectible({"from": x_account})
    creating_tx.wait(1)
    print("New toknen has been created")    
    return advanced_x,creating_tx




def main():
    deploy_and_create()
