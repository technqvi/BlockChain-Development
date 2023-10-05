from brownie import SimpleStorage,accounts

def test_deploy():
    account=accounts[0]

    x_contract=SimpleStorage.deploy({'from': account})
    initial_value=x_contract.retrieve()
    expected=0
    #Assert
    assert initial_value==expected

def test_updating_storage():
    account=accounts[0]

    x_contract=SimpleStorage.deploy({'from': account})
    
    expected=50
    x_contract.store(expected,{'from': account})
    assert expected==x_contract.retrieve()
    #assert 10==x_contract.retrieve()

