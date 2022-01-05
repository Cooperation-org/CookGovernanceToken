//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20BurnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

/**
@title Whats Cookin Governance Token
@author Ryan Turner
@notice Contract to implement a basic governance token. Will allow minting
@notice Group minting and burning from a given address
@notice Contract is upgradable
 */

contract GovToken is
    Initializable,
    ERC20BurnableUpgradeable,
    OwnableUpgradeable
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
        function initialize() public initializer {
            OwnableUpgradeable.__Ownable_init();
            ERC20BurnableUpgradeable.__ERC20Burnable_init();
            ERC20Upgradeable.__ERC20_init("COOKTEAM", "COOKTEAM");
        }

        ///@notice changes the owner of the contract
        ///@dev Only callable by current contract owner
        function changeOwner(address _newOwner) public onlyOwner {
            OwnableUpgradeable.transferOwnership(_newOwner);
        }

        ///@notice mint tokens to a single address
        ///@dev Only contract owner can call this function
        function mint(address to, uint256 amount) public onlyOwner {
            super._mint(to, amount);
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
                mint(tokenHolders[i], amounts[i]);
            }
        }
        ///@notice Allow burning of tokens that have already been issued (removes token from given address)
        ///@dev Callable by contract owner
        function burnFrom(address account, uint256 amount)
            public
            override
            onlyOwner
        {
            super._burn(account, amount);
        }
        ///@notice Allows for transfer of tokens between addresses
        ///@dev returns bool (true) for successful transfer
        function transfer(address recipient, uint256 amount)
            public
            virtual
            override
            onlyWhiteListed
            returns (bool)
        {
            _transfer(_msgSender(), recipient, amount);
            return true;
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