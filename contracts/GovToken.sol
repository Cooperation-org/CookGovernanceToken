//SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20BurnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

/**
@title GovToken
@author Too-Far
@notice Contract to implement a basic governance token. Will allow minting, 
@notice Group minting and burning from a given address
@notice Contract is upgradable
 */

contract GovToken is
    Initializable,
    ERC20BurnableUpgradeable,
    OwnableUpgradeable
    {
        ///@dev Create a mapping that will show all whitelisted addresses
        mapping(address => bool) public whitelist;

        ///@dev Ensure that only whitelisted addresses can call a method
        modifier onlyWhiteListed() {
            require(
                whitelist[_msg.sender()] == true,
                "Caller is not a whitelisted address"
            );
            _;
        }

        /**
        @dev: this function is the constructor. takes an array of addresses, and an array of amounts along with a string representing the token name. 
        Creates the token and calls the mint multiple
        @notice: This constructor is set up to initialize with an initial list of addresses to have tokens minted to
         */
        function initialize(address[] memory tokenHolders, uint256[] memory amounts) public initializer {
            OwnableUpgradeable._Ownable_init();
            ERC20BurnableUpgradeable._ERC20Burnable_init();
            ERC20Upgradeable._ERC20_init("COOKTEAM", "COOKTEAM");
        }

        ///@dev Allows the owner of the contract to mint tokens to a given address
        function mint(address to, uint256 amount) public onlyOwner {
            super._mint(to, amount);
        }

        ///@dev This function mints tokens to multiple addresses. Called from constructor,
        ///@dev will allow for a csv setup passed in as arrays
        function mintMultiple(
            address[] memory tokenHolders,
            uint256[] memory amounts
        ) public onlyOwner {
            require(
                tokenHolders.length == amounts.length,
                "There is a mismatch between the addresses and amounts"
            );

            for (uint256 i=0; i< tokenHolders.length; i++) {
                mint(tokenHolders[i], amounts[i]);
            }
        }
        /**
        @dev Allows contract owner to burn tokens that are in a given address
        @notice A use case for this would be if a user is kicked from the DAO
        The contract owner can reclaim and burn their tokens
         */
        function burnFrom(address account, uint256 amount)
            public
            override
            onlyOwner
        {
            super._burn(account, amount)
        }

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

        function whitelistAdd(address _add) external onlyOwner {
            whitelist[_add] = true;
        }

        function whitelistRemove(address _remove) external onlyOwner {
            whitelist[_remove] = false;
        }
    }