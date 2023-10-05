// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
//https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
//https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
//https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

// stakeTokens
// unstakeTokens
// IssueTokens
// addAllowedTokens
// getTokenValue

// 100 ETH 1:1 for every 1 ETH, we give 1 X-Token
// 50 ETH and 50 DAI staked, and we want to give a reward of 1 DAPP / 1 DAI

contract TokenFarm is Ownable{
   // mapping token address  of staker who belong to  amount 
   mapping(address=>mapping(address=>uint256) ) public stakingBalance;
   /*{'tokenA_addd':{ 'add_user1': 20,'add_user2':10 ,'add_user3': 30}
    'tokenB_addd':{ 'add_user2': 20,'add_user5':10 ,'add_user6': 30}
   }*/
   // mapping how many token name the staker stake 
   mapping(address=>uint256) public uniqueTokensStaked;
   // mapping token to where to get price from chainlink orable
   mapping(address=>address) public tokenPriceFeedMapping;

   mapping(address=>uint256) private totalValueOfStaker; 
   // list staker address
   address[] public stakers;
   // list token allowed to stake  such as dia,jomos
   address[] public allowedTokens;

   // Reward Token
   IERC20 public rewardToken;
   //way#1 distribute reward base on  fixed amount of token in each time   
   //int256 private reward_token_dist_to_holder;
 
   // way#2  disttrubute   1 % of total against value of staker   1/100  
   uint256 private  percent_reward_token_dist_to_holder;  //0.01= 1% =1e16


   event DistributeReward(
        address indexed reward_token,
        uint256 bal_rewardToken_before,
        uint256 all_totalValue,
        uint256 percent_reward_token_distributed,
        uint256 all_reward_token_distributed,
        uint256 bal_rewardToken_after,
        uint256 timestamp
    );


   //constructor (address _rewardTokenAddress,_reward_token_dist) public  
   constructor (address _rewardTokenAddress,uint256 _percent_reward_token_dist) public  
   { // Token reward  
     
     rewardToken=IERC20(_rewardTokenAddress);
 
     // Way1
     //require(_reward_token_dist<=rewardToken.totalSupply(),"The number of reward token to distribute in each time must be less than or equal total suppply");
     
     percent_reward_token_dist_to_holder=_percent_reward_token_dist;

   }
   function setPercentRewardTokenToStaker(uint256 _percent_reward_token_dist)  public onlyOwner{
       percent_reward_token_dist_to_holder=_percent_reward_token_dist;

   }
   //https://docs.chain.link/docs/ethereum-addresses/
   function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner{
      tokenPriceFeedMapping[_token]=_priceFeed;
   }


   function issueTokens() public onlyOwner{
      
      uint256 rewardToken_bal= rewardToken.balanceOf(address(this));

      // Way#1  
      //require(rewardToken_bal>=reward_token_dist_to_holder,"The number of reward token to distribute in each time must be less than or equal total suppply");
    

       uint256 allTotalValue=0 ;
       for (uint256 index = 0; index < stakers.length; index++) {

         address recipient=stakers[index];
         
         uint256 userTotalValue=getUserTotalValue(recipient);
         allTotalValue=allTotalValue+userTotalValue;

         totalValueOfStaker[recipient]=userTotalValue;
         
       }
        // Way#2 
        //uint256 allRewardTokenToBeDistributed=allTotalValue/(percent_reward_token_dist_to_holder);
        uint256 allRewardTokenToBeDistributed=allTotalValue/100*percent_reward_token_dist_to_holder;
        require(rewardToken_bal>=allRewardTokenToBeDistributed,"The value of reward token to distribute in each time must be less than or equal total suppply");
        
        for (uint256 index = 0; index < stakers.length; index++) {
             
             address recipient=stakers[index];
             uint256 userTotalValue=totalValueOfStaker[recipient];
             rewardToken.transfer(recipient,userTotalValue/100*percent_reward_token_dist_to_holder);

            //  uint256 rewardValue = userTotalValue  *(percent_reward_token_dist_to_holder);
            //  rewardToken.transfer(recipient,rewardValue);
        }

        uint256 rewardToken_bal_after= rewardToken.balanceOf(address(this));

        emit DistributeReward(
        address(rewardToken),
        rewardToken_bal,
        allTotalValue,
        percent_reward_token_dist_to_holder,
        allRewardTokenToBeDistributed,
        rewardToken_bal_after,
        block.timestamp
    );

         
   }
   function getUserTotalValue(address _user) public view returns(uint256) {
       uint256 totalValue=0;
       
       if (uniqueTokensStaked[_user] > 0){
       for (uint256 allowTokensIndex = 0; allowTokensIndex < allowedTokens.length; allowTokensIndex++) {
           totalValue=totalValue + getUserSingleTokenValue(_user,  allowedTokens[allowTokensIndex]);
       }}

      return totalValue;
   }
   // function getUserTokenStakingBalanceEthValue(address user, address token)
   function getUserSingleTokenValue(address _user,address _token) public view returns(uint256){

        if (uniqueTokensStaked[_user]<=0){
            return 0;
        }

       (uint256 price,uint256 decimals) = getTokenValue(_token);
        // price of the token * stakingBalance[_token][user] (price of the token*amount of token)   
        // 10 18decimals(000000000000000000) ETH  ==>(10**decimanls)
        // ETH/USD -> 10000000000  ==>price
        // 10 * 100 = 1,000
        // X worth of  token
       return  (stakingBalance[_token][_user] * price) / (10**decimals) ;
   }
    //function getTokenEthPrice(address token) public view returns (uint256, uint8)
    function getTokenValue(address _token) public view returns (uint256, uint256) {
        // priceFeedAddress (Proxy column in table datafeed)  
        //https://docs.chain.link/docs/ethereum-addresses/  
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        // create conttract instance for getting current price of the token
        //https://github.com/smartcontractkit/chainlink-brownie-contracts/blob/main/contracts/abi/v0.8/AggregatorV3Interface.json
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
 
        // Do 2 steps 1. get price 2. get the number of decimal
        (,int256 price,,,)= priceFeed.latestRoundData();

        uint256 x_price= uint256(price);
        uint256 x_decimals = uint256(priceFeed.decimals());
        return (x_price, x_decimals);
    }


   function stakeToken(uint256 _amount, address _token) public{
      
       // What token do you want to stake
       // How much  you can stake
       require(_amount>0,"Amount must be more than 0");
       require(tokenIsAllowed(_token),"This token is not allowed");
        
       //https://docs.openzeppelin.com/contracts/4.x/api/token/erc20#IERC20-transferFrom-address-address-uint256-
       //transferFrom(address from, address to, uint256 amount)
       IERC20(_token).transferFrom(msg.sender,address(this),_amount);

       updateUniqueTokensStaked(msg.sender,_token);

       stakingBalance[_token][msg.sender]=stakingBalance[_token][msg.sender]+_amount;
       if (uniqueTokensStaked[msg.sender]==1)
        {
          stakers.push(msg.sender);
        }

   }
   function unstakeAllToken(address _token) public{

       uint256 balance=stakingBalance[_token][msg.sender];
       require(balance>0,"Staking balance cannot be 0");
       IERC20(_token).transfer(msg.sender,balance);

       // Unstake all amount  by clearing balance of user who staked in that token
       stakingBalance[_token][msg.sender]=0;

       // remove the token after unstaking
       uniqueTokensStaked[msg.sender]=uniqueTokensStaked[msg.sender]-1;
         
         // For multiple stake and unstake such stake#1=4 +stake2=2 and unstake#1=3 and last-unstake=3
         // 4+2=3+3 
         // The code below fixes a problem not addressed in the video, where stakers could appear twice
        // in the stakers array, receiving twice the reward.
        // if (uniqueTokensStaked[msg.sender] == 0) {
        //     for ( uint256 stakersIndex = 0; stakersIndex < stakers.length; stakersIndex++) {
        //         if (stakers[stakersIndex] == msg.sender) {
        //             stakers[stakersIndex] = stakers[stakers.length - 1];
        //             stakers.pop();
        //         }
        //     }
        // }

   }

  function unstakePartialToken(uint256 _amount, address _token) public{

       uint256 balance=stakingBalance[_token][msg.sender];
       require(balance>=_amount,"Current balance cannot be less than required unstake.");

       IERC20(_token).transfer(msg.sender,_amount);

       // Unstake some amount 
       stakingBalance[_token][msg.sender]=balance-_amount;

    }
   

   // how many tokens does the staker have in this dApp
   function updateUniqueTokensStaked(address _user,address _token) internal{
       if (stakingBalance[_token][_user]<=0){
           uniqueTokensStaked[_user]=uniqueTokensStaked[_user]+1;
           }
   }

  
   function addAllowedToken(address _token) public onlyOwner{

       allowedTokens.push(_token);
   }


   function tokenIsAllowed(address _token) public returns(bool){
       for (uint256 token_index = 0; token_index < allowedTokens.length; token_index++) {
           if ( allowedTokens[token_index]==_token){
                   return true;
           }
       }
       return false;

   }
   function listNumberOfAllowedToken() public view returns(uint256){

       return   allowedTokens.length;
   }
   function getTotalSupplyOfRewardToken() public view returns(uint256){

       return rewardToken.balanceOf(address(this));
   }
function getBalaneTokensStakedByUser(address _user,address _token) public view returns(uint256){
       return stakingBalance[_token][_user];
   }
function listAllStaker() public view returns(address[] memory){
       return stakers;
   }

 function listAllAllowedTokenForStaking() public view returns(address[] memory ){
       return allowedTokens;
   }  
   function getPercentRewardTokenToStaker()  public view returns(uint256){
      return percent_reward_token_dist_to_holder;

   }
} 
