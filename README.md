# Nyzocli
A simple but efficient Nyzo client for command line and automation usage, in Python.

Uses the pynyzo client package https://github.com/EggPool/pynyzo

## Prerequisites

Python3.6+

## Installation

`pip3 install -r requirements.txt`

Nyzocli needs a `private_seed` file in the user private directory.      
Just copy/rename the seed file you want to use.  
Run with `-v` flag to check the location

> TODO: add support for a specific seed from the command line

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

### Get your balance:

Get balance from the given verifier (defaults to localhost)
  
`./Nyzocli.py balance`  
`./Nyzocli.py balance address`    
`./Nyzocli.py -i ip.of.verifier.toask balance address `

```
At block: 1696064
Your Balance is: 219.449753
Blocks until fee: 157
```

or as json:

`./Nyzocli.py --json balance`

```
{
  "block": 1696070, 
  "balance": 219449753, 
  "blocks_until_fee": 151, 
  "address": "abd7fede35a84b108a36e6dc361d9b32ca84d149f6eb85b4a4e63015278d4c9f"
}
```

You can query a specific verifier (default is 127.0.0.1) - use yours only or you'll likely be blacklisted.

`./Nyzocli.py -i verifier0.nyzo.co balance abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f `


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

## Not working yet :

Send a tip to Nyzocli dev:  
`./Nyzocli.py send abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f 10`


Send 100 NYZO **only** if the balance is > 200 NYZO;  
`./Nyzocli.py send abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f 100 200`  


## Tip Jar

Show your appreciation, send a few coffees or pizzas to the devs:  
`abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f`


## Known twerks

Still some debug or trace messages left over from the pynyzo package to be cleaned up later on.

## Releases

* 0.0.4 - Vote command, local signing, use of client API to forward

* 0.0.3 - Block and balance commands

* 0.0.2 - Status ok

* 0.0.1 - Initial crude version, nothing works yet


## About

Official Nyzo repo: https://github.com/n-y-z-o/nyzoVerifier

Pynyzo python package https://github.com/EggPool/pynyzo
