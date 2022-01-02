import { upgrades, ethers } from 'hardhat';
import { DeployFunction } from 'hardhat-deploy/types';

const args = ['0x04181A9FeeC83a9692f2126333660e7A0CF13A73'];

const deployFunct: DeployFunction = async function({
    deployments,
    getNamedAccounts
}) {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();

    const res = await deploy("GovToken", {
        from: deployer,
        skipIfAlreadyDeployed: false,
        proxy: {
            owner: deployer,
            methodName: "initialize",
            proxyContract: "OpenZeppelinTransparentProxy",
        },
        args
    });
    console.log("Deployed to: ", res.address)
};


export default deployFunct;
deployFunct.tags = ["GovToken"];