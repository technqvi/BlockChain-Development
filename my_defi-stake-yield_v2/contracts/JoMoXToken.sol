pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
//https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol
//https://docs.openzeppelin.com/contracts/4.x/erc20
contract JoMoXToken is ERC20{

    constructor(uint256 initialSupply) ERC20("JoMo Token V22", "JOMO") {
    // constructor() ERC20("JoMoMini", "JOMOMINI") {    
        //_mint(msg.sender, 1000000000000000000000000);
        //https://eth-converter.com/
        _mint(msg.sender, initialSupply);  //assert(1 ether == 1e18);
    }

}