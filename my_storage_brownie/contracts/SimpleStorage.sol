// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;
// kovan 0x81130F719556c98d0C3AF1695d158bE8261Faa59
// rinkeby

contract SimpleStorage {
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    People[] public people;

    uint256 favoriteNumber;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
    function listAllPeople() public view returns (People[] memory peopleList){
        return people;
    }
}