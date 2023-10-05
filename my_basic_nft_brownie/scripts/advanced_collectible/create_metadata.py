from importlib.metadata import metadata
from brownie import network, AdvancedCollectible
import scripts.helpful_scripts as xhelp
import metadata.sample_metadata as xmeta
from pathlib import Path
import os
import json
import requests
#step 3
UPLOAD_IPFS=True 

#  IBANEZ_JOHN_TH2000,GIBSON_JOHN_DM1998 , FENDER_YNGWIE_SW1980
defatult_breed_to_image_uri = {
    "IBANEZ_JOHN_TH2000": "https://ipfs.io/ipfs/QmYt7adMubuWcPodMXUTVNLTuN31oQsVJziCT9s9mKus4S?filename=fender_yngwie_sw1980.jpg",
    "GIBSON_JOHN_DM1998": "https://ipfs.io/ipfs/yyyyyyy?filename=gibson_john_dm1998.jpg",
    "FENDER_YNGWIE_SW1980": "https://ipfs.io/ipfs/zzzzzzzz?filename=fender_yngwie_sw1980.jpg",
}
# def main():
#   advanced_x=AdvancedCollectible[-1]
#   number_of_collectible=advanced_x.tokenCounter()
#   print(f"You have created {number_of_collectible} NFT")
#   i=0
#   if   number_of_collectible>0:
#     for token_id in range(number_of_collectible):

#         guitar_idx=advanced_x.tokenId_To_SelectedBreed(token_id)
#         guitar_name=xhelp.get_breed(guitar_idx)
#         print(guitar_name)


def main():
  advanced_x=AdvancedCollectible[-1]
  number_of_collectible=advanced_x.tokenCounter()
  print(f"You have created {number_of_collectible} NFT")
  i=0
  if   number_of_collectible>0:
    for token_id in range(number_of_collectible):

        breed_idx=advanced_x.tokenId_To_SelectedBreed(token_id)
        breed_name=xhelp.get_breed(breed_idx)

        meta_file_name=f'idx{i}-{breed_idx}-{breed_name}.json'

        img_path_to_upload,meta_path_rinkeby=xhelp.get_meta_img_path()

        # metadata_path_file= f"./metadata/{network.show_active()}/{token_id}-{breed_name}.json"
        metadata_path_file=os.path.join(meta_path_rinkeby,meta_file_name)

        print(f'index:{i} - {metadata_path_file}')

        collectible_metadata=xmeta.metadata_template 
        if os.path.exists(metadata_path_file):
            print(f"{metadata_path_file} already exits")
        else:
            print(f"create new metadata file {metadata_path_file}")
            collectible_metadata["name"]=breed_name
            collectible_metadata["description"]=f"Ad adorable {breed_name} pup!"
            print(collectible_metadata)
            
            image_file_name=breed_name.lower()+".jpg"
            # image_path="./img/"+image_file
            image_path=os.path.join(img_path_to_upload,image_file_name)
            print(f"This actual file for upload to ipfs : { image_path}  ")

            # 1.1-upload image object
            if  UPLOAD_IPFS==True:
             image_uri=upload_to_ipfs(image_path,image_file_name)

            #1.2 upload defaul link
            if image_uri is not None:
                print(f"New Image URL : {image_uri}")
            else:
                image_uri=defatult_breed_to_image_uri[breed_name]
                print(f"Default Image URL : {image_uri}")

            collectible_metadata["image"]=image_uri

            with open(metadata_path_file,"w") as file:
                print(f"Path file to create  as metadata: {metadata_path_file}")
                json.dump(collectible_metadata,file)
            #2-upload metadata info
            if  UPLOAD_IPFS==True:    
               upload_to_ipfs(metadata_path_file,meta_file_name)

        i=i+1       
        print("==============================================================================")
  else:
        print("There is no collectible , plese create at least one.")


#https://docs.ipfs.io/install/command-line/
#https://dist.ipfs.io/#go-ipfs

# run ipfs daemon cmd first 

def upload_to_ipfs(xfilepath,xfilename):

    #https://docs.ipfs.io/reference/http/api/#api-v0-add
    if os.path.exists(xfilepath):
       print(f"Upload_to_ipfs: {xfilepath}")
       with Path(xfilepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001" 
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]

        # "./img/0-PUG.png" -> "0-PUG.png"
        # filename = filepath.split("/")[-1:][0]
        # for development
        x_uri = f"http://localhost:8080/ipfs/{ipfs_hash}?filename={ipfs_hash}"

        # for production
        #sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
        print(f"Upload to IPFS successfully  : {x_uri}")
        return x_uri
    else:
        print(f"Not found {xfilepath}")
        return None