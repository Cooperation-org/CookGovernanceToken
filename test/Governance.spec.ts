import { ethers, deployments, getNamedAccounts } from "hardhat";
import { BigNumber, Signer } from "ethers";
import { Deployment } from "hardhat-deploy/types";
import { expect, use } from "chai";
import chaiAsPromised from "chai-as-promised";

import { GovToken } from "../typechain/GovToken";

use(chaiAsPromised);

describe("Whats Cookin Governance Token", () => {
    let deployer: string;
    let signers: Signer[];
    let GovToken: GovToken;
    let GovTokenDeployment: Deployment;
    let accountsAddresses: string[];

    before(async () => {
        const namedAccounts = await getNamedAccounts();
        deployer = namedAccounts.deployer;
        signers = await ethers.getSigners();

        accountsAddresses = await Promise.all(
            signers.map((signer: Signer) => {
                return signer.getAddress();
            })
        );
    });

    beforeEach(async () => {
        ({GovToken: GovTokenDeployment} = await deployments.fixture());

        GovToken = (await ethers.getContractAt(
            GovTokenDeployment.abi,
            GovTokenDeployment.address,
            signers[0]
        )) as GovToken;
    });

    describe("Initialize()", async () => {
        it("Should sucessfully deploy contract", async () => {
            expect(GovToken.address).to.not.be.null;
        });
    });

    describe("mint()", () => {
        it("should mint tokens to user, executed by owner", async () => {
            const newHolder = accountsAddresses[3];
            const balance = 100000000;

            const initialBalance = await GovToken.balanceOf(newHolder);
            expect(initialBalance).to.be.deep.equal(BigNumber.from(0));

            const mintTx = await GovToken.mint(newHolder, balance);
            await mintTx.wait();

            const newBalance = await GovToken.balanceOf(newHolder);
            expect(newBalance).to.be.deep.equal(BigNumber.from(newBalance));
        });

        it("Should revert transaction if called by anyone other than the owner", async () => {
            const notOwner = signers[2];
            const GovernanceToken = await ethers.getContractAt(
                GovTokenDeployment.abi,
                GovTokenDeployment.address,
                notOwner
            );
            await expect(
                GovernanceToken.mint(await notOwner.getAddress(), 10000)
            ).to.be.rejectedWith(
                "VM Exception while processing transaction: reverted with reason string 'Ownable: caller is not the owner"
            );
        });
    });

    describe("mintMultiple()", () => {
        it("should mint tokens to multiple users, executed by owner", async () => {
            const newHolder = accountsAddresses[3];
            const anotherHolder = accountsAddresses[4];
            const balance = 100000000;
            const initialNewHolderBalance = await GovToken.balanceOf(newHolder);
            const initialAnotherHolderBalance = await GovToken.balanceOf(anotherHolder);
            expect(initialNewHolderBalance).to.be.deep.equal(BigNumber.from(0));
            expect(initialAnotherHolderBalance).to.be.deep.equal(BigNumber.from(0));

            const mintTx = await GovToken.mintMultiple(
                [newHolder, anotherHolder],
                [balance, balance]
            );
            await mintTx.wait();

            const newBalanceOfNewHolder = await GovToken.balanceOf(newHolder);
            const newBalanceOfAnotherHolder = await GovToken.balanceOf(anotherHolder);
            expect(newBalanceOfNewHolder).to.be.deep.equal(BigNumber.from(balance));
            expect(newBalanceOfAnotherHolder).to.be.deep.equal(BigNumber.from(balance));
        });

        it("should revert if not called by owner", async () => {
            const newHolder = accountsAddresses[3];
            const anotherHolder = accountsAddresses[4];
            const balance = 100000000;
            await expect(
                GovToken.mintMultiple([newHolder, anotherHolder], [balance])
            ).to.be.rejectedWith(
                "VM Exception while processing transaction: reverted with reason string 'There is a mismatch between the addresses and amounts"
            );
        });
    });

    describe("burnFrom()", () => {
        it("should burn tokens of user, executed by owner", async () => {
            const newHolder = accountsAddresses[3];
            const balance = 100000000;

            const mintTx = await GovToken.mint(newHolder, balance);
            await mintTx.wait();

            const newBalance = await GovToken.balanceOf(newHolder);
            expect(newBalance).to.be.deep.equal(BigNumber.from(balance));

            const burnTx = await GovToken.burnFrom(newHolder, balance);
            await burnTx.wait();

            const balanceAfterBurn = await GovToken.balanceOf(newHolder);
            expect(balanceAfterBurn).to.be.deep.equal(BigNumber.from(0));
        });

        it("should revert if not called by owner", async () => {
            const GovernanceToken = await ethers.getContractAt(
                GovTokenDeployment.abi,
                GovTokenDeployment.address,
                signers[5]
            );

            const newHolder = accountsAddresses[3];
            const balance = 100000000;

            const mintTx = await GovToken.mint(newHolder, balance);
            await mintTx.wait();

            const newBalance = await GovToken.balanceOf(newHolder);
            expect(newBalance).to.be.deep.equal(BigNumber.from(balance));

            await expect(
                GovernanceToken.burnFrom(newHolder, balance)
            ).to.be.rejectedWith(
                "VM Exception while processing transaction: reverted with reason string 'Ownable: caller is not the owner"
            );
        });
    });

    describe("transfer()", async () => {
        it("should fail to transfer the token for a non whitelisted address", async () => {
            const GovernanceToken = await ethers.getContractAt(
                GovTokenDeployment.abi,
                GovTokenDeployment.address,
                signers[5]
            );
            const newHolder = accountsAddresses[3];
            const balance = 100000000;
            await expect(
                GovernanceToken.transfer(newHolder, balance)
            ).to.be.rejectedWith(
                "VM Exception while processing transaction: reverted with reason string 'Caller is not a whitelisted address"
            );
        });

        it("should allow whitelisted addresses to transfer the token", async () => {
            const GovernmentToken1 = await ethers.getContractAt(
                GovTokenDeployment.abi,
                GovTokenDeployment.address,
                signers[0]
            );

            const GovernmentToken2 = await ethers.getContractAt(
                GovTokenDeployment.abi,
                GovTokenDeployment.address,
                signers[2]
            );
            const balance = 100000000;

            const transferer = accountsAddresses[2];
            const transfere = accountsAddresses[4];
            await GovToken.mint(transferer, balance);
            await GovernmentToken1.whitelistAdd(transferer);

            await GovernmentToken2.transfer(transfere, 1);
        });
    });
});