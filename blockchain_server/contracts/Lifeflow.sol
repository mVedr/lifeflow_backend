// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12 <0.9.0;

contract Lifeflow {
    address public owner;

    struct Transaction {
        uint256 id;
        uint32 did;
        uint32 rid;
        uint32 eid;
        uint32 volReceived;
    }

    mapping(address => Transaction[]) public transactions;
    mapping(uint32 => Transaction[]) public transactionsByID;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner is allowed to perform this action");
        _;
    }

    function addTransaction(
        uint32 did,
        uint32 rid,
        uint32 eid,
        uint32 volReceived
    ) public {
        Transaction memory tr = Transaction({
            id: transactions[msg.sender].length, 
            did: did,
            rid: rid,
            volReceived: volReceived,
            eid: eid
        });
       transactions[msg.sender].push(tr);
       transactionsByID[tr.did].push(tr);
       transactionsByID[tr.rid].push(tr);
       //return tr;
    }

    function getTransactions() public view returns (Transaction[] memory) {
        return transactions[msg.sender];
    }

    function getTransactionsByUserID(uint32 id) public view returns (Transaction[] memory) {
        return transactionsByID[id];
    }
}
