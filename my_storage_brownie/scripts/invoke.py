from re import X
from brownie import SimpleStorage,accounts,config
import scripts.deploy as xdeploy

def read_favorite_number():
   xcontact=  SimpleStorage[-1]
   print(xcontact.retrieve())

def store_favorite_number(number):
   xcontact=  SimpleStorage[-1]
   tx=  xcontact.store(number,{"from":xdeploy.get_account()})
   tx.wait(1)
   print("store value successfully")
  
def add_lucky_number_of_person(key_name:str,lucky_numer:int):
   xcontract=SimpleStorage[-1]
   tx=xcontract.addPerson(key_name,lucky_numer,{"from":xdeploy.get_account()})
   tx.wait(1)
   print(f"Added {key_name} and {lucky_numer} successfully")

def list_favoriteNumber_of_people():
   xcontract=SimpleStorage[-1]
   list_people=xcontract.listAllPeople()
   for x in list_people:
     print(x[1]," - ",x[0])
     


   
def get_favoriteNumber_by_name(key_name):
   xcontract=SimpleStorage[-1]
   my_number=xcontract.nameToFavoriteNumber(key_name)
   print(my_number)


def main():
#   store_favorite_number(100)
#   read_favorite_number()
 print("Add person info")
 add_lucky_number_of_person("John",200)
 add_lucky_number_of_person("Mochi",100)
 list_favoriteNumber_of_people()
