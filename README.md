# Nyzocli
A simple but efficient Nyzo client for command line and automation usage, in Python.

## Prerequisites

Python3.6+

## Installation

`pip3 install -r requirements.txt`

Nyzocli needs a `private_seed` file in the same directory.    
Just copy/rename the seed file you want to use in Nyzocli's dir.  

> TODO: add support for a specific seed from the command line

If no file is found, it will create a new one.

## Help

`./Nyzocli.py --help`

(under windows, use `python3 Nyzocli.py [...]` invocation)

To get detailed help for a specific command, use --help with the command, for instance:

`./Nyzocli status --help`

## Example commands

Show your balance:  
`./Nyzocli.py balance`


Send a tip to Nyzocli dev:  
`./Nyzocli.py send abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f 10`


Send 100 NYZO **only** if the balance is > 200 NYZO;  
`./Nyzocli.py send abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f 100 200`  


## Tip Jar

Show your appreciation, send a few coffees or pizzas to the devs:  
`abd7fede35a84b10-8a36e6dc361d9b32-ca84d149f6eb85b4-a4e63015278d4c9f`


## Releases

* 0.0.1 - Initial crude version, nothing works yet


## About

Official Nyzo repo: https://github.com/n-y-z-o/nyzoVerifier
