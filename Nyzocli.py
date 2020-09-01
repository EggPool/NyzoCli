#!/usr/bin/env python3
"""
Console mode Nyzo client - Connects to a peer and API client, console mode.

EggdraSyl

"""

import json
import logging
# import pprint
import sys
from os import path
from time import time

import click
from nyzostrings.nyzostringencoder import NyzoStringEncoder
# from nyzostrings.nyzostringsignature import NyzoStringSignature
# from nyzostrings.nyzostringprivateseed import NyzoStringPrivateSeed
from nyzostrings.nyzostringtransaction import NyzoStringTransaction
from requests import get

import pynyzo.config as config
from modules.helpers import get_private_dir, extract_status_lines, fake_table_to_json
from pynyzo.byteutil import ByteUtil
from pynyzo.connection import Connection
from pynyzo.keyutil import KeyUtil
from pynyzo.message import Message
from pynyzo.messageobject import EmptyMessageObject
from pynyzo.messages.blockrequest import BlockRequest
from pynyzo.messagetype import MessageType
from pynyzo.transaction import Transaction

__version__ = '0.0.5'


VERBOSE = False
app_log = False


def connect(ctx, verifier_ip):
    """Tries to connect to the peer, depending on the context."""
    if verifier_ip == '':
        verifier_ip = ctx.obj['verifier_ip']
    if ctx.obj.get('verifier_connection', None):
        return
    try:
        connection = Connection(verifier_ip, 9444, verbose=ctx.obj['verbose'])
        ctx.obj['verifier_connection'] = connection
    except Exception as e:
        app_log.error(f"Error {e} connecting to {verifier_ip}:9444.")
        sys.exit()
    return


def reconnect(ctx):
    """Should not be needed?"""
    ctx.obj['verifier_connection'].close()
    ctx.obj['verifier_connection'].sdef = None  # Temp hack for pynyzo version
    ctx.obj['verifier_connection'].check_connection()


@click.group()
@click.option('--verifier_ip', '-i', default="127.0.0.1", help='Set a specific verifier ip (default=localhost)')
@click.option('--client', '-c', default="https://client.nyzo.co", help='Set a specific client (default=https://client.nyzo.co)')
@click.option('--port', '-p', default=80, help='Client port (default 80)')
@click.option('--unlock', '-U', default="", help='Wallet Unlock code')
@click.option('--json', '-j', is_flag=True, default=False, help='Try to always answer with json (default false)')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Be verbose! (default false)')
@click.pass_context
def cli(ctx, verifier_ip, client, port, unlock, verbose, json):
    global VERBOSE
    # ctx.obj['host'] = host
    # ctx.obj['port'] = port
    ctx.obj['verifier_ip'] = verifier_ip
    ctx.obj['client'] = client
    ctx.obj['port'] = port
    ctx.obj['unlock'] = unlock
    ctx.obj['json'] = json
    ctx.obj['verbose'] = verbose
    VERBOSE = verbose
    ctx.obj['verifier_connection'] = None
    ctx.obj['client_connection'] = None
    if VERBOSE:
        app_log.info(f"Key Loaded, public id {ByteUtil.bytes_as_string_with_dashes(config.PUBLIC_KEY.to_bytes())}")


@cli.command()
@click.pass_context
def version(ctx):
    """Print version"""
    if ctx.obj['json']:
        print(json.dumps({"version": __version__, "private_dir": get_private_dir}))
    else:
        print(f"Nyzocli version {__version__} - Your private dir is {get_private_dir()}")


@cli.command()
@click.pass_context
def info(ctx):
    """Print version"""
    if ctx.obj['json']:
        print(json.dumps({"version": __version__,
                          "private_dir": get_private_dir(),
                          "public_address": ByteUtil.bytes_as_string_with_dashes(config.PUBLIC_KEY.to_bytes()),
                          "client": ctx.obj['client'],
                          "port": ctx.obj['port'],
                          }))
    else:
        print(f"Nyzocli version {__version__}")
        print(f"Your private dir is {get_private_dir()}")
        print(f"Your public address is {ByteUtil.bytes_as_string_with_dashes(config.PUBLIC_KEY.to_bytes())}")
        print(f"Default verifier is {ctx.obj['verifier_ip']}")
        print(f"Client is {ctx.obj['client']} on port {ctx.obj['port']}")


@cli.command()
@click.pass_context
@click.argument('block_number', type=int)
def block(ctx, block_number):
    """Get a block detail"""
    connect(ctx, ctx.obj['verifier_ip'])
    if VERBOSE:
        app_log.info(f"Connected to {ctx.obj['verifier_ip']}:9444")
        app_log.info(f"block {block_number}")
    req = BlockRequest(start_height=block_number, end_height=block_number, include_balance_list=False, app_log=app_log)
    message = Message(MessageType.BlockRequest11, req, app_log=app_log)
    res = ctx.obj['verifier_connection'].fetch(message)
    print(res.to_json())


@cli.command()
@click.pass_context
@click.argument('address', default='', type=str)
def balance(ctx, address):
    """Get balance of an ADDRESS (Uses the one from localhost by default)
    Question: ask from verifier or from Client? Two commands?
    Client by default would make more sense (available with no need for a verifier)
    """
    connect(ctx, ctx.obj['verifier_ip'])
    if address == '':
        address = config.PUBLIC_KEY.to_bytes().hex()
    else:
        address = address.replace('-', '')
    if VERBOSE:
        app_log.info(f"Get balance for address {address}")
    assert(len(address) == 64)  # TODO: better user warning

    if VERBOSE:
        app_log.info(f"Connected to {ctx.obj['verifier_ip']}")
        app_log.info(f"address {address}")
    empty = EmptyMessageObject()
    message = Message(MessageType.StatusRequest17, empty, app_log=app_log)
    res = ctx.obj['verifier_connection'].fetch(message)
    status = res.get_lines()
    frozen = int(extract_status_lines(status, "frozen edge")[0])
    if VERBOSE:
        app_log.info(f"Frozen Edge: {frozen}")

    reconnect(ctx)

    req = BlockRequest(start_height=frozen, end_height=frozen, include_balance_list=True, app_log=app_log)
    message2 = Message(MessageType.BlockRequest11, req, app_log=app_log)
    res = ctx.obj['verifier_connection'].fetch(message2)
    # Wow, this is quite heavy. move some logic the pynyzo
    # Also list is *supposed* to be sorted, can help find faster
    bin_address = bytes.fromhex(address)
    for item in res.get_initial_balance_list().get_items():
        if item.get_identifier() == bin_address:
            if ctx.obj['json']:
                print(json.dumps({"block": frozen, "balance":item.get_balance(), "blocks_until_fee": item.get_blocks_until_fee(),
                                  "address": address}))
            else:
                print(f"At block: {frozen}")
                print(f"Your Balance is: {item.get_balance()/1000000}")
                print(f"Blocks until fee: {item.get_blocks_until_fee()}")
            return (item.get_balance(), item.get_blocks_until_fee())

    # Address Not found
    if ctx.obj['json']:
        print(json.dumps({"block": frozen, "balance": 0, "blocks_until_fee": None, "address": address}))
    else:
        print(f"At block: {frozen}")
        print(f"Your Balance is: N/A")
        print(f"Blocks until fee: N/A")
    return 0, 0


@cli.command()
@click.pass_context
def status(ctx):
    """Get Status of distant server"""
    # ex : python3 Nyzocli.py  -j status 159.69.216.65
    connect(ctx, ctx.obj['verifier_ip'])
    if VERBOSE:
        app_log.info(f"Connected to {ctx.obj['verifier_ip']}")
    empty = EmptyMessageObject(app_log=app_log)
    message = Message(MessageType.StatusRequest17, empty, app_log=app_log)
    res = ctx.obj['verifier_connection'].fetch(message)
    print(res.to_json())
    # print(json.dumps(status))


@cli.command()
@click.pass_context
@click.argument('recipient', type=str)
@click.argument('amount', default=0, type=float)
@click.argument('above', default=0, type=float)
def send(ctx, recipient, amount: float=0, above: float=0):
    """
    Send Nyzo to a RECIPIENT.
    OPERATION is optional and should be empty for regular transactions.
    ABOVE is optional, if > 0 then the tx will only be sent when balance > ABOVE
    """

    # check_address(recipient)
    # load_keys(ctx)
    # connect(ctx)
    # con = ctx.obj['connection']
    """
    if above > 0:
        my_balance = float(con.command('balanceget', [ctx.obj['address']])[0])
        if my_balance <= above:
            if VERBOSE:
                app_log.warning("Balance too low, {} instead of required {}, dropping.".format(my_balance, above))
            print(json.dumps({"result": "Error", "reason": "Balance too low, {} instead of required {}"
                             .format(my_balance, above)}))
            return
    """
    return "WIP - Soon!"


@cli.command()
@click.pass_context
@click.argument('cycle_tx_sig', type=str)  # Cycle tx to vote for
@click.argument('vote', default=1, type=int)  # Vote
@click.argument('key_', default="", type=str)    # key_ to vote with
def vote(ctx, cycle_tx_sig: str, vote: int=1, key_: str=""):
    """
    Vote for the given cycle tx sig with the provided seed.
    If no seed is given, use the wallet one.
    - ex: python3 Nyzocli.py vote sig_gc6VHCY_yfjRc_DyosRLdi084AbY5wP9yVdTTRhajp4JUk7nbRw9c-aufwEwGY~.x0m55u.v.tGzjnA7VYP4V0m-eXyG
    - ex: python3 Nyzocli.py vote sig_gc6VHCY_yfjRc_DyosRLdi084AbY5wP9yVdTTRhajp4JUk7nbRw9c-aufwEwGY~.x0m55u.v.tGzjnA7VYP4V0m-eXyG 1
    - ex: python3 Nyzocli.py vote sig_gc6VHCY_yfjRc_DyosRLdi084AbY5wP9yVdTTRhajp4JUk7nbRw9c-aufwEwGY~.x0m55u.v.tGzjnA7VYP4V0m-eXyG 0 key_...
    """
    if key_ == "":
        seed = config.PRIVATE_KEY.to_bytes()
    else:
        seed = NyzoStringEncoder.decode(key_).get_bytes()
    # reconvert key to address
    address = KeyUtil.private_to_public(seed.hex())
    if VERBOSE:
        app_log.info(f"Voting {vote} for {cycle_tx_sig} with id {address}")
    cycle_tx_sig_bytes = NyzoStringEncoder.decode(cycle_tx_sig).get_bytes()
    # Create a tx
    timestamp = int(time()*10)*100 + 10000  # Fixed 10 sec delay for inclusion
    # print(timestamp, hex(timestamp))
    cycle_transaction_signature_hex = cycle_tx_sig_bytes.hex()
    transaction = Transaction.from_vote_data(timestamp, bytes.fromhex(address), vote, cycle_tx_sig_bytes)
    print(transaction.to_json())
    key, _ = KeyUtil.get_from_private_seed(seed.hex())
    sign = KeyUtil.sign_bytes(transaction.get_bytes(for_signing=True)[:106], key)
    tx = NyzoStringTransaction.from_hex_vote(hex(timestamp), address, sign.hex(), vote, cycle_transaction_signature_hex)
    tx__ = NyzoStringEncoder.encode(tx)
    # Send the tx
    url = "{}/forwardTransaction?transaction={}&action=run".format(ctx.obj['client'], tx__)
    if VERBOSE:
        app_log.info(f"Calling {url}")
    res = get(url)
    if VERBOSE:
        app_log.info(res)
    if path.isdir("tmp"):
        # Store for debug purposes
        with open("tmp/answer.txt", "w") as fp:
            fp.write(res.text)
    print(fake_table_to_json(res.text))

"""
@cli.command()
@click.pass_context
def test(ctx):
    with open("tmp/answer.txt") as fp:
        res = fp.readline()
    # print(res)
    print(fake_table_to_json(res))
"""

if __name__ == '__main__':
    logger = logging.getLogger('push')

    app_log = logging.getLogger()
    app_log.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)-5s] %(message)s')
    ch.setFormatter(formatter)
    app_log.addHandler(ch)

    # Use user private dir
    private_dir = get_private_dir()
    config.NYZO_SEED = private_dir + '/private_seed'
    config.load(private_dir)

    cli(obj={})

