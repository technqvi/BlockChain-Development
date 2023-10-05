from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account,get_meta_img_path
import os
import json
# Actually you have to load metadata directly from D:\BlockChain-World\BC-Dev_Project\ETH_DEV_Python\my_py_nft\nft_py_demo\metadata\rinkeby
dog_metadata_dic = {
    "IBANEZ_JOHN_TH2000": "https://ipfs.io/ipfs/xxxxxx?filename=ibanez_john_th2000.jpg",
    "GIBSON_JOHN_DM1998": "https://ipfs.io/ipfs/yyyyyyy?filename=gibson_john_dm1998.jpg",
    "FENDER_YNGWIE_SW1980": "https://ipfs.io/ipfs/zzzzzzzz?filename=fender_yngwie_sw1980.jpg",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    i=0;


    img_path_to_upload,meta_path_rinkeby=get_meta_img_path()
    for token_id in range(number_of_collectibles):

        breed_idx=advanced_collectible.tokenId_To_SelectedBreed(token_id)
        breed_name=get_breed(breed_idx)
        # https://docs.openzeppelin.com/contracts/4.x/api/token/erc721#ERC721-tokenURI-uint256-
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            
            meta_file_name=f'idx{i}-{breed_idx}-{breed_name}.json'
            meta_file_path=os.path.join(meta_path_rinkeby,meta_file_name)
            if os.path.exists(meta_file_path):
             print(f"Setting tokenURI of {token_id} from file {meta_file_name}")
             with open(meta_file_path) as f:
                data = json.load(f)
                data_name=data['name']
                data_image_uri=data['image']
                print(f"{data_name} - {data_image_uri}")
                set_tokenURI(token_id, advanced_collectible, data_image_uri)

        i=i+1    


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
