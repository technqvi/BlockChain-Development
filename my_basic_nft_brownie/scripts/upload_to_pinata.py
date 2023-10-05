import os
from pathlib import Path
import requests
#https://docs.pinata.cloud/api-pinning/pin-file
PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"

# Change this filepath
filepath = "./img/shiba-inu.png"
filename = filepath.split("/")[-1:][0]

# headers = {
#     "pinata_api_key": os.getenv("PINATA_API_KEY"),
#     "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
# }
headers = {
    "pinata_api_key": "59f688fc176607d1efd9",
    "pinata_secret_api_key":"2bba563bfd22c5914c2c86f377c22c67e40ca42e9405829d4cdb1a2c8492bcca",
}

def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())


if __name__ == "__main__":
    main()

