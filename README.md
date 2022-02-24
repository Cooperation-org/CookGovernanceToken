# Whats Cookin Governance token

## Requirements

Following software is required to be installed to use this repo:
* [NodeJS](https://nodejs.org/en/) >= v14.0.0

This repo also uses dependecies that are associated with `hardhat` but not built-in:
* [hardhat-deploy](https://github.com/wighawag/hardhat-deploy)
* [hardhat-typechain](https://github.com/rhlsthrm/hardhat-typechain)

## Usage

On first use of this repo, run `yarn install` to install all required dependencies.
Then run `yarn run build` to set up the repo.

Available commands:
* `build` - Compiles the entire project and generates Typechain typings
* `lint` - Runs solhint on current project
* `clean` - Clears the cache and deletes all artifacts
* `compile` - Compiles the entire project, building all artifacts
* `deploy:<network>` - Run deploy script on \<network\>
* `help` - Prints all available hardhat commands
* `test` - Runs mocha tests
* `test:coverage` - Runs solidity coverage
* `typechain` - Generate Typechain typings for compiled contracts


Contract address: 0x6487A3702C2b59610109c403F67657cd101AaEc7
Gnosis Safe address: matic:0x44021CBeE888b40de6D3358B6c8f71c08af1DBED
