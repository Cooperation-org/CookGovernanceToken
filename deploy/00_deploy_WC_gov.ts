import { upgrades, ethers } from 'hardhat';
import { DeployFunction } from 'hardhat-deploy/types';


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
            owner: process.env.GNOSIS_SAFE_ADDRESS,
            methodName: "initialize",
            proxyContract: "OpenZeppelinTransparentProxy",
        },
    });
    console.log("Deployed to: ", res.address)
};


export default deployFunct;
deployFunct.tags = ["GovToken"];