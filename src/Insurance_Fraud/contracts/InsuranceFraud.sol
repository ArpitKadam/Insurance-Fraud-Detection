// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InsuranceFraud {
    struct Claim {
        uint256 claimId;
        address claimant;
        uint256 amount;
        bool isFraud;
    }

    mapping(uint256 => Claim) public claims;
    uint256 public nextClaimId;
    uint256 public totalClaims;

    function fileClaim(uint256 amount) public {
        claims[nextClaimId] = Claim(nextClaimId, msg.sender, amount, false);
        totalClaims++;
        nextClaimId++;
    }

    function validateClaim(uint256 claimId, bool isFraud) public {
        require(claimId < nextClaimId, "Invalid claim ID");
        claims[claimId].isFraud = isFraud;
    }

    function getClaim(uint256 claimId) public view returns (Claim memory) {
        return claims[claimId];
    }

    function getTotalClaims() public view returns (uint256) {
        return totalClaims;
    }
}
