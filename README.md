<div align="center">
  <img src="https://i.imgur.com/tqA3f3O.png"  />
  <h1>ZkSync Soft</h1>
  <p>This software simplifies wallet management on the ZkSync network, providing access to a variety of features and a high level of randomization for enhanced security.</p>
</div>

---

🔔 <b>Subscribe to me:</b> https://t.me/sybilwave

🤑 <b>Donate me:</b> 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9

---
<h2>🚀 Installation</h2>

```
git clone https://github.com/czbag/zksync.git

cd zksync

pip install -r requirements.txt

# Before you start, configure the required modules in modules_settings.py

python main.py
```
---
<h2>🚨 Modules</h2>

1) Make deposit/withdraw with official bridge

2) Make deposit/withdraw with Orbiter bridge

3) Wrap/Unwrap ETH

4) Swap on SyncSwap (+ add liqudity)

5) Swap on Mute

6) Swap on SpaceFi (+ add liqudity)

7) Swap on PancakeSwap

8) Swap on WooFi

9) Swap on Odos (my ref code is enabled, 1% of the transaction amount goes to me, come not from you, but from the Odos contract! can be turned off in config.py)

10) Swap on ZkSwap

11) Swap on XY.Finance (my ref code is enabled, 1% of the transaction amount goes to me, come not from you, but from the XY contract! can be turned off in config.py)

12) Swap on OpenOcean (my ref code is enabled, 1% of the transaction amount goes to me, come not from you, but from the OpenOcean contract! can be turned off in config.py)

13) Swap on 1inch (my ref code is enabled, 1% of the transaction amount goes to me, come not from you, but from the 1inch contract! can be turned off in config.py)

14) Swap on Maverick

15) Swap on VeSync

16) Stargate bridge $MAV token in BSC network

17) Bungee refuel

18) Landing protocol Eralend (deposit/withdraw/enable_collateral)

19) Withdraw from Eralend landing protocol

20) Landing protocol Basilisk (deposit/withdraw/enable_collateral)

21) Withdraw from Basilisk landing protocol

22) Landing protocol ReactFusion (deposit/withdraw/enable_collateral)

23) Withdraw from ReactFusion landing protocol

24) Landing protocol ZeroLend (deposit/withdraw)

25) Withdraw from ZeroLend landing protocol

26) Create onchain NFT collection on Omnisea

27) Mint + Brdige NFT with L2Telegraph (LayerZero protocol) (only in arb nova network)

28) Send messages with L2Telegraph (LayerZero protocol) (only in arb nova network)

29) Mint free NFT on NFTS2ME

30) Mint Tavaera ID + NFT

31) Mint free NFT on MailZero

32) Mint zks.network domain

33) Mint era.name domain

34) Dmail - send mails (onchain)

35) Create Gnosis Safe

36) Swap all tokens to ETH

37) Multi-swap capability - makes the specified number of swaps in the specified dexes

38) Custom routes - actions to be performed sequentially or randomly

39) Multi-approve - make approve or undo approve to any dexes

40) Check gas before starting the module, if gas > specified, the software will wait for

41) Using a proxy (http/s only), 1 account - 1 proxy, if you have 10 accounts and 5 proxy, software run 5 accounts only

42) Logging via logger module

43) Transaction count checker

---
<h2>⚙️ Settings</h2>

1) All basic settings are made in settings.py and modules_settings.py, inside there is information about what and where to write

2) In the accounts.txt file, specify your private keys

3) In the file proxy.txt specify the list of proxies, each proxy with a new line, format http/s, example in the file is specified

4) In the rpc.json file at the path zksync/data/rpc.json we can change the rpc to ours

Info on updates and just a life blog –– https://t.me/sybilwave
