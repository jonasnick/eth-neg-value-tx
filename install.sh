#!/bin/bash
echo "Ensure that you have the develop branch (643eda5) of go-ethereum installed"
echo "Install malicious miner"
go get github.com/jonasnick/go-ethereum
go build -o ethereum-malicious-miner github.com/jonasnick/go-ethereum/cmd/ethereum
