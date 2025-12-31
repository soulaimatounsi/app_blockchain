const { ethers } = require("hardhat");

async function main() {
    // Récupérer le factory du contrat
    const Traceability = await ethers.getContractFactory("Traceability");

    // Déployer le contrat
    const traceability = await Traceability.deploy();

    // Récupérer l'adresse du contrat (await nécessaire)
    const address = await traceability.getAddress();

    console.log("Traceability contract deployed to:", address);
}

// Exécuter le script
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
