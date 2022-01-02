import { HardhatUserConfig } from 'hardhat/types';
import dotenv from 'dotenv';

import "@openzeppelin/hardhat-upgrades";
import "@nomiclabs/hardhat-ethers";
import "@nomiclabs/hardhat-etherscan";

import "solidity-coverage";
import "hardhat-gas-reporter";
import "hardhat-deploy";
import "hardhat-typechain";

dotenv.config();

const config: HardhatUserConfig = {
    defaultNetwork: 'hardhat',
    solidity: {
        compilers: [
            {
                version: "0.8.3"
            }
        ]
    },
    paths: {
        sources: './contracts',
        artifacts: './artifacts'
    },
    networks: {
        maticMainnet: {
            url: `https://rpc-mainnet.matic.network`,
            accounts: [`${process.env.POLYGON_PRIVATE_KEY}`]
        },
        mumbai: {
            url: 'https://rpc-mumbai.maticvigil.com',
            accounts: [`${process.env.POLYGON_PRIVATE_KEY}`]
        },
        rinkeby: {
            url: `https://mainnet.infura.io/v3/${process.env.INFURA_PROJECT_ID}`,
            accounts: [`${process.env.RINKEBY_PRIVATE_KEY}`]
        },
        mainnet: {
            url: '',
            accounts: [`0x${process.env.MAINNET_PRIVATE_KEY}`]
        }
    },
    etherscan: {
        apiKey: process.env.ETHERSCAN_API_KEY
    },
    typechain: {
        outDir: 'typechain',
        target: 'ethers-v5'
    },
    namedAccounts: {
        deployer: 0
    }
};

export default config;
