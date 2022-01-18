//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
@title Whats Cookin Governance Token
@author Ryan Turner
@notice Contract to implement a basic governance token. Will allow minting
@notice Group minting and burning from a given address
@notice Contract is upgradable
 */

contract GovToken is
    ERC20,
    ERC20Burnable,
    Ownable
    {
        ///@notice mapping to track users that are whitelisted
        mapping(address => bool) public whitelist;

        ///@dev only allows whitelisted users to call a given function
        modifier onlyWhiteListed() {
            require(
                whitelist[_msgSender()] == true,
                "Caller is not a whitelisted address"
            );
            _;
        }
        ///@notice Create token and transfer ownership
        ///@dev acts as constructor
        constructor() ERC20("Cook Team", "COOKTEAM")  {}

        function mint(address recipient, uint256 amount) public onlyOwner {
            _mint(recipient, amount);
        }


        ///@notice Mint tokens to an array of addresses
        ///@dev requires array of addresses and an additional array of amounts (must match)
        function mintMultiple(
            address[] memory tokenHolders,
            uint256[] memory amounts
        ) public onlyOwner {
            require(
                tokenHolders.length == amounts.length,
                "There is a mismatch between the addresses and amounts"
            );

            for (uint256 i = 0; i < tokenHolders.length; i++) {
                _mint(tokenHolders[i], amounts[i]);
            }
        }
 
        ///@notice Add user address to whitelist
        ///@dev Only callable by contract owner
        function whitelistAdd(address _add) external onlyOwner {
            whitelist[_add] = true;
        }

        ///@notice Remove user address from whitelist
        ///@dev Only callable by contract owner
        function whitelistRemove(address _remove) external onlyOwner {
            whitelist[_remove] = false;
        }
    }