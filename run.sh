#!/bin/bash
log_file="/tmp/eth.log"

echo "start private network between malicious miner and regular node"
echo "run malicious miner"

./ethereum-malicious-miner -mine=true -rpcport=8080 -rpc=true -loglevel=5 -dial=false -datadir="$HOME/.ethereum/eth_test1/" -conf="$HOME/.ethereum/eth_test1/conf.ini" > $log_file &

read -p "Enter malicious miner's enode URL from $log_file: " miner

ethereum -port="30304" -bootnodes="$miner" -datadir="$HOME/.ethereum/eth_test2" -conf="$HOME/.ethereum/eth_test2/conf.ini" -dial=true -rpcport=8081 -rpc=true -loglevel=5

