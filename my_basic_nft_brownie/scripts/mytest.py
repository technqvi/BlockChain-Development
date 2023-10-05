from pathlib import Path
import os


def testpath():
    file='idx0-1-SHIBA_INU.json'
    path = Path(f"./metadata/rinkeby/{file}").parent.absolute()

    file_path=os.path.join(path,file)
    if os.path.exists(file_path):
     print(f'Full path : {file_path}')
    else:
     print('Not found file')

project_path=os.path.abspath(r'D:\BlockChain-World\BC-Dev_Project\ETH_DEV_Python\my_py_nft\nft_py_demo')
def get_meta_img_path():
    img_path=os.path.join(project_path,'img')
    meta_path_rinkeby=os.path.join(project_path,'metadata','rinkeby')

    return img_path,meta_path_rinkeby

def main():
    img_path,meta_path_rinkeby= get_meta_img_path()
    print(img_path)
    print(meta_path_rinkeby)
    meta_file_name=f'xxxx.json'
    print(os.path.join(meta_path_rinkeby,meta_file_name))
