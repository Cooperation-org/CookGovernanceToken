import { DeployFunction } from 'hardhat-deploy/types';


const deployFunct: DeployFunction = async function({
    deployments,
    getNamedAccounts
}) {
    const { deploy } = deployments;
    const { deployer } = await getNamedAccounts();
    console.log('deployer: ', deployer);

    const res = await deploy("GovToken", {
        from: deployer,
        skipIfAlreadyDeployed: false,
    });
    console.log("Deployed to: ", res.address)
};


export default deployFunct;
deployFunct.tags = ["GovToken"];