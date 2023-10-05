//Traffle  https://github.com/PatrickAlphaC/dungeons-and-dragons-nft
// An NFT Contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

//https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.6/VRFConsumerBase.sol
//https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol

contract AdvancedCollectible is ERC721,VRFConsumerBase{

    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    
    enum Breed {
        IBANEZ_JOHN_TH2000,GIBSON_JOHN_DM1998 , FENDER_YNGWIE_SW1980
    }
    mapping(uint256=>Breed) public  tokenId_To_SelectedBreed;
    event breedAssigned(uint256 indexed tokenId, Breed breed);


    mapping(bytes32=> address) public requestId_To_Sender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public 
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("GuitarXyz", "GUITARX"){

        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns(bytes32){
        bytes32 requestId=requestRandomness(keyhash,fee);

        requestId_To_Sender[requestId]=msg.sender;
        emit requestedCollectible(requestId, msg.sender);
   
    }
     function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override{
         Breed breed_x=Breed(randomNumber % 3); //random breed  type
         uint256 newTokenId=tokenCounter;


         tokenId_To_SelectedBreed[newTokenId]=breed_x;
         emit breedAssigned(newTokenId, breed_x);
         
        address owner = requestId_To_Sender[requestId];
        _safeMint(owner, newTokenId);
    
        tokenCounter = tokenCounter + 1;
     }

     function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
    
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner no approved");
        _setTokenURI(tokenId, _tokenURI);


    }

}