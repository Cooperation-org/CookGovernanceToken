import { DeployFunction } from 'hardhat-deploy/types';

// const args = require('../arguments');

const deployFunct: DeployFunction = async function({
    deployments,
    getNamedAccounts
}) {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();

    const res = await deploy("GovToken", {
        from: deployer,
        proxy: {
            owner: deployer,
            methodName: "initialize",
            proxyContract: "OpenZeppelinTransparentProxy"
        },
        // args
    });
    console.log("Deployed to: ", res.address)
};

export default deployFunct;
deployFunct.tags = ["GovToken"];