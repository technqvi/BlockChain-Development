// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

//https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol
//github name/contracts/token/ERC721/ERC721.sol
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible  is ERC721{

   uint256 public takenCounter;

   constructor() public ERC721 ("GuitarXyz", "GUITARX") {
      takenCounter=0;
   }

   function createCollectible(string memory tokenURL) public returns (uint256){
       uint256 newTokenId=takenCounter;
       _safeMint(msg.sender,newTokenId);
       _setTokenURI(newTokenId,  tokenURL);
       takenCounter=takenCounter+1;
       
       return newTokenId ;

   }

}