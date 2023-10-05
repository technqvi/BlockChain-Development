import scripts.helpful_scripts as xhelp
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

#https://testnets.opensea.io/assets/0x58f7B97c7d2528D3FEC9464Bdf5D9ddc574DA9eD/0
def deploy_and_create():
    x_account=xhelp.get_account()
    simple_x=SimpleCollectible.deploy({"from": x_account})
    tx=simple_x.createCollectible(sample_token_uri,{"from": x_account})
    tx.wait(1)
    print(f"youn can view  NFT at {xhelp.OPENSEA_URL.format(simple_x.address,simple_x.takenCounter()-1)}")
    return simple_x,tx

def main():
    deploy_and_create()
