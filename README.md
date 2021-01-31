# Nyzocli
A simple but efficient Nyzo client for command line and automation usage, in Python.

Uses the pynyzo client package https://github.com/EggPool/pynyzo

## Prerequisites

Python3.6+, pip
On default Ubuntu you can install pip by `apt install python3-pip`  

## Installation

`pip3 install -r requirements.txt`

If you have errors when installing the requirements, you may need other libs that can be missing on your setup.  
You can try to  
`sudo apt install python3-setuptools`  
`sudo apt install build-essential`  
and redo the requirements install.

Nyzocli needs a `private_seed` file in the user private directory.      
Just copy/rename the seed file you want to use.  
Run with `-v` flag to check the location

If no file is found, it will create a new one.

## Help

`./Nyzocli.py --help`

(under windows, use `python3 Nyzocli.py [...]` invocation)

To get detailed help for a specific command, use --help with the command, for instance:

`./Nyzocli status --help`

## Example commands

### Get client info:

(does not connect anywhere)

`./Nyzocli.py info`

```
Your private dir is /home/my_redacted_username/nyzo-private
Your public address is abd7fede-35a84b10-8a36e6dc-361d9b32-ca84d149-f6eb85b4-a4e63015-278d4c9f
Default host is 127.0.0.1 on port 9444
```

### Get your balance (from verifier):

Get balance from the given verifier (defaults to localhost)
  
`./Nyzocli.py vbalance`  
`./Nyzocli.py vbalance address`    
`./Nyzocli.py -i ip.of.verifier.toask vbalance address `

```
At block: 1696064
Your Balance is: 219.449753
Blocks until fee: 157
```

or as json:

`./Nyzocli.py --json vbalance`

```
{
  "block": 1696070, 
  "balance": 219449753, 
  "blocks_until_fee": 151, 
  "address": "abd7fede35a84b108a36e6dc361d9b32ca84d149f6eb85b4a4e63015278d4c9f"
}
```

You can query a specific verifier (default is 127.0.0.1) - use yours only or you'll likely be blacklisted.

`./Nyzocli.py -i verifier0.nyzo.co vbalance abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f `


### Get your balance (from client):

Get balance from a nyzo client (defaults to client.nyzo.co)
  
`./Nyzocli.py balance`  
`./Nyzocli.py balance address`    

```
At block: 1696064
Your Balance is: 219.449753
```

or as json:

`./Nyzocli.py --json balance`

```
{
  "block": 1696070, 
  "balance": 219449753, 
  "address": "abd7fede35a84b108a36e6dc361d9b32ca84d149f6eb85b4a4e63015278d4c9f",
  "id_address": "id__8aMo_KWTH4JgzAsDV3puDRbayd59.LL5KajDc1kEAkQw84KHcKwc"
}
```

You can query a specific client (default is client.nyzo.co) 

`./Nyzocli.py -c client.nyzo.co balance abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f `


### Get a node status

`./Nyzocli.py status`  
`./Nyzocli.py -i verifier0.nyzo.co status`

```
{
  "message_type": "StatusResponse18", 
  "value": [
    "nickname: Nyzo 0", 
    "version: 487", 
    "ID: b5fd...173b", 
    "mesh: 1398 total, 527 in cycle", 
    "cycle length: 530", 
    "transactions: 0", 
    "retention edge: 1694074", 
    "trailing edge: 1694098", 
    "frozen edge: 1696216 (Grimnoshtadrano)", 
    "open edge: 1696217", 
    "blocks transmitted/created: 206/104847", 
    "votes requested: 458237", 
    "- h: +1, n: 2, v: 79(79)", 
    "requester identifier: abd7...4c9f"
  ]
}
```

### Get a specific block info

> Block has to be recent enough, checking status before hand could help.

`./Nyzocli.py -i verifier0.nyzo.co block 1696093` 

```
{
"message_type": "BlockResponse12", 
"value": {
  "balance": false, 
  "blocks": [
    {"message_type": "Block", 
     "value": {
       "height": 1696093, 
       "previous_block_hash": "148c51632c67dbc141a70ffef4ae136b1fb3436742efbafdeba14fa6def8a18e", 
       "start_timestamp": 1548669451000, 
       "verification_timestamp": 1548669460552, 
       "transactions": [
         {"message_type": "Transaction", 
          "value": {
            "type": 1, "timestamp": 1548669452000, 
            "amount": 562278171, 
            "receiver_identifier": "12d454a69523f739eb5eb71c7deb87011804df336ae0e2c19e0b24a636683e31", 
            "previous_hash_height": 0, 
            "previous_block_hash": "", 
            "sender_identifier": "12d454a69523f739eb5eb71c7deb87011804df336ae0e2c19e0b24a636683e31", 
            "sender_data": "", 
            "signature": "32914e455244234cbe0bbd4c5fa711dbdf8e25d540d8d73c577b55b3afe0e7ebde9f7848e4656444f8ec2d7f8373cd5c175a5050ed3d83b300ad5062d9e23006"
            }}], 
       "balance_list_hash": "ad6aa5df2d9b40fa1d67400ed4598e9057666453ee70822245df2ac57d91b091", 
       "verifier_identifier": "3b558f9de4b66a7d91aece0780f2858b32e6e333e4c977d481ed54806f1ba4fc", 
       "verifier_signature": "9d692637da21310bd27d86de0ba01b4532f64a65bc25310c41bd23fb847c54e4b2fc8ddd7dfc139ca2f04a36acfd5849a897f89c06b6db5441e72db20ad34406"
  }}], 
  "initial_balance_list": null
  }
}
```


### Vote for a cycle tx:

Vote for the given cycle tx sig with the optionally provided key_... nyzostring.    
If no seed is given, use the wallet one.

`./Nyzocli.py vote sig_gc6VHCY_yfjRc_DyosRLdi084AbY5wP9yVdTTRhajp4JUk7nbRw9c-aufwEwGY~.x0m55u.v.tGzjnA7VYP4V0m-eXyG`  

`./Nyzocli.py vote sig_gc6VHCY_yfjRc_DyosRLdi084AbY5wP9yVdTTRhajp4JUk7nbRw9c-aufwEwGY~.x0m55u.v.tGzjnA7VYP4V0m-eXyG 1`  

`./Nyzocli.py vote sig_gc6VHCY_yfjRc_DyosRLdi084AbY5wP9yVdTTRhajp4JUk7nbRw9c-aufwEwGY~.x0m55u.v.tGzjnA7VYP4V0m-eXyG 0 key_...  `  

Sample answer:
```
[
  {'block height': '7572863', 
   'sender ID (raw)': 'f7e40b5eeb7471d2-2b50d63e945e8e05-9658c62f5e2ada2f-82da1b6267330a34', 
   'sender ID (Nyzo string)': 'id__8fwB2TZIu77iaT3nfGhvAxnnncpMozIrbWbr6U9EcNFSAvPFJ~pC', 
   'receiver ID (raw)': 'null', 
   'receiver ID (Nyzo string)': 'null', 
   'amount': '∩0.000000', 
   'previous verifier ID (raw)': '0b19818e841b764c-30a176a3e32b9a98-7f1cbf03204bb093-58c45147288ed7f9', 
   'previous verifier ID (Nyzo string)': 'id__80JqxpY46Vqcca5UF~cIDGy_7b-384LNBTA4kktFAKwXLEfqcvaR', 
   'expected verifier ID (raw)': '1c86e2b23e1b6e4e-ec70c48c53fc2ad9-6e366c82889d4f6d-3784e570d769874f', 
   'expected verifier ID (Nyzo string)': 'id__81Q6WI8~6UXeZ734A5f-aKCLdDQ2z9Tfsjv4Xo3orpufoNietWIg', 
   'next verifier ID (raw)': 'aed5ae8e69d5c823-ecf5474d60533a62-6079ac05667a1bdb-1c7bc88c4bb65fd9', 
   'next verifier ID (Nyzo string)': 'id__8aZmIFXGTtxAZfm7jn1jeD9xvrN5qEFsUPPZQ8PbKC_qzSwCQ0g5', 
   'forwarded': 'true'}
]

```

## Utils

see utils dir

### massvote.py

A Mass voter helper

Say you have several in-cycle verifiers, and wand to vote for several cycle tx.  
You can vote from your sentinel but that would expose your verifiers (close timing, same order every time)

This script uses NyzoCli individual vote feature to vote with every verifier for every cycle tx once.  
It's to be run on a local secure box.

- create a "keys.txt" text file with one key_ a line, from in-cycle verifiers
- create a "sigs.txt" text file with one sig_ vote a line  
each line has a sig, one space, the vote (1 for yes or 0 for no)  
if no vote is provided, default 1 is assumed.  
For ncfp3, you can get and rename the ncfp3-sigs.txt from open nyzo github to vote yes for all.
- edit massvote.py settings if needed (min and max wait time)   
- run massvote.py  
- you'll get a "vote.sh" script you can then chmod +x and run. This will run the Nyzocli with all needed votes, randomized and with random wait in between.  
(of course, you can check that vote.sh in a text editor and make sure it does what it claims)

**New:** Now does query nyzo.today API for existing votes.  
Does not give any info about your verifiers, just asks the list of votes for a given sig_ and process locally.  
That way, you can re-run the script after a first pass to check and re-submit missing votes.  
You can deactivate that feature.


## New in 0.0.6:

### Send regular tx, with optional data and any key

Ex: Send a tip to Nyzocli dev, using local account:    
`./Nyzocli.py send abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f 10`

or with recipient id_ :  
`./Nyzocli.py send id__8aMo_KWTH4JgzAsDV3puDRbayd59.LL5KajDc1kEAkQw84KHcKwc 10`


Send 10 NYZO **only** if the balance is > 200 NYZO:  
`./Nyzocli.py send abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f 10 200`  

or with a specific key (sender):    
`./Nyzocli.py send id__8aMo_KWTH4JgzAsDV3puDRbayd59.LL5KajDc1kEAkQw84KHcKwc 10 0 '' key_....`  
Note: in that precise case you HAVE to specify the "above" condition as 0, data as empty '' then only the key_... 

Full command `[]` denote an optional field, that has to be filled if there is another field following

`./Nyzocli.py send recipient amount [above_condition] [data] [key_...]`    
So to use the "data" field you have to specify a "above" param (0 to send without condition)

## New since 0.0.7:
You can send the full balance by using "-1" as amount.  
Ex: Send whole balance:   
`./Nyzocli.py send -- abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f -1`

**Note:** In order to differentiate options (like -v) from arguments (like -1 amount), you need to use `--` (two dashes) to consider all further elements as arguments and not options.   
Any required option then goes *before* the `--`.

**Note:** This will empty the account and remove it from the nyzo balances list. The address will be unusable until it gets at leat a n10 deposit.


### Get current frozen edge from a client
(default is client.nyzo.co)

`./Nyzocli.py frozen`
```
height: 10228622
hash: 018f197a54452589fff7783e8a3f745272cb6716b7f01431a898061486a6d4d2
timestamp: 1608397162591
distance: 1
```

or as json: 
`./Nyzocli.py --json frozen`  

```
{"height": 10228594, 
 "hash": "513f156b8ba4cac0a5feb14715aa689571cc1eb9d16711cb2919800496343c5d", 
 "timestamp": 1608397162091, 
 "distance": "1"
}`
``` 

## New in 0.0.11, safe_send command

Same as send, with no "above" parameter.
Signs and sends a tx. Wait until the block is frozen.  
If the transaction is not in that block, resend it until it passes (5 tries).  
ex:  
`./Nyzocli.py safe_send abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f 10 key_...`

Can be used without "key_" to use the default wallet.


## New in 0.0.10, Nytro Tokens commands

### Token send

Example command: `./NyzoCli token send id_xxxx 10 TEST`    
sends 10 "TEST" tokens to id_xxxx

### Token balance

Get balances - all tokens - for an address (raw or id__)  
`./Nyzocli.py token balance a49138f27485cae4096c3eb72f9425943fe4b6f346d0fc76ef40084ec767365d`

or just get balance for a specific token  
`./Nyzocli.py token balance a49138f27485cae4096c3eb72f9425943fe4b6f346d0fc76ef40084ec767365d TEST2`

### Token issue

Issue a token: token name, number of decimals, supply   
`./Nyzocli.py --verbose token issue -- TEST3 3 -1`

If you use "-1" as supply (meaning mintable token) you need to use the `--` after the " token issue" command.

### Token mint

Only for mintable tokens, if you are the current owner.  
Ex: mint 100 tokens "TEST3"  
`./Nyzocli.py --verbose token mint TEST3 100`

### Token burn

Only for mintable tokens, up to the amount you have on your balance.    
Ex: burn 3.123 tokens "TEST3"    
`./Nyzocli.py --verbose token burn TEST3 3.123`

### Token ownership

Only for mintable tokens, if you are the current owner.    
Ex: transfer the ownership of "TEST3" to the recipient:     
`./Nyzocli.py --verbose token ownership TEST3 3f19e603b9577b6f91d4c84531e1e94e946aa172063ea3a88efb26e3fe75bb84`



## Tip Jar

Show your appreciation, send a few coffees or pizzas to the devs:  
`abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f`  
or
`id__8aMo_KWTH4JgzAsDV3puDRbayd59.LL5KajDc1kEAkQw84KHcKwc`


## Known twerks

Still some debug or trace messages left over from the pynyzo package to be cleaned up later on.

## Short term roadmap

- (done) Move from using a verifier to using a nyzo client by default (balance)
- Fine tune commands and options
- Done (partially?) Generalize autodetection of address format between raw bytes and nyzostrings.
- Add conversion utils from/to Nyzo strings
- (Done) allow to send full balance (empty wallet)

## Mid term roadmap

- (Done) Add support for Nyzo tokens
- Easier installation, Windows pre-compiled releases


## Releases

* 0.0.11 - safe_send command (retries if necessary until the tx is frozen or fails)

* 0.0.10 - Tokens support

* 0.0.8 - Bugfix and proper doc for send full balance.

* 0.0.7 - Allow use of id__ or raw wallet id with auto detection.  
Get balance from client(balance) or verifier (vbalance), Send whole balance.  
*Note:* sending whole balance removes the address from the system, the address will then need 10n min to be used again.

* 0.0.6 - Get frozen edge, Send regular TX.

* 0.0.5 - Randomized Massvote and omitting of existing votes with help from nyzo.today API.

* 0.0.4 - Vote command, local signing, use of client API to forward

* 0.0.3 - Block and balance commands

* 0.0.2 - Status ok

* 0.0.1 - Initial crude version, nothing works yet


## About

Official Nyzo repo: https://github.com/n-y-z-o/nyzoVerifier

Pynyzo python package https://github.com/EggPool/pynyzo
