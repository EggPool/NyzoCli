#!/usr/bin/env python3
"""
Console mode Nyzo client - Connects to a peer, console mode.

EggdraSyl - Jan. 2019.

"""

import json
import logging
# import pprint
import sys

import click

import pynyzo.config as config
from modules.helpers import get_private_dir, extract_status_lines
from pynyzo.byteutil import ByteUtil
from pynyzo.connection import Connection
from pynyzo.message import Message
from pynyzo.messageobject import EmptyMessageObject
from pynyzo.messagetype import MessageType
from pynyzo.messages.blockrequest import BlockRequest

__version__ = '0.0.3'


VERBOSE = False


def connect(ctx):
    """Tries to connect to the peer, depending on the context."""
    if ctx.obj.get('connection', None):
        return
    try:
        connection = Connection(ctx.obj['host'], ctx.obj['port'], verbose=ctx.obj['verbose'])
        ctx.obj['connection'] = connection
    except Exception as e:
        app_log.error(f"Error {e} connecting to {ctx.obj['host']}:{ctx.obj['port']}.")
        sys.exit()
    return


def reconnect(ctx):
    """Should not be needed?"""
    ctx.obj['connection'].close()
    ctx.obj['connection'].sdef = None  # Temp hack for pynyzo version
    ctx.obj['connection'].check_connection()


@click.group()
@click.option('--host', '-h', default="127.0.0.1", help='Set a specific peer (default=localhost)')
@click.option('--port', '-p', default=9444, help='Peer port (default 9444)')
@click.option('--json', '-j', is_flag=True, default=False, help='Try to always answer with json (default false)')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Be verbose! (default false)')
@click.pass_context
def cli(ctx, port, host, verbose, json):
    global VERBOSE
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    ctx.obj['json'] = json
    ctx.obj['verbose'] = verbose
    VERBOSE = verbose
    ctx.obj['connection'] = None
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
        print(json.dumps({"private_dir": get_private_dir(),
                          "public_address": ByteUtil.bytes_as_string_with_dashes(config.PUBLIC_KEY.to_bytes()),
                          "default_host": ctx.obj['host'],
                          "default_port": ctx.obj['port'],
                          }))
    else:
        print(f"Your private dir is {get_private_dir()}")
        print(f"Your public address is {ByteUtil.bytes_as_string_with_dashes(config.PUBLIC_KEY.to_bytes())}")
        print(f"Default host is {ctx.obj['host']} on port {ctx.obj['port']}")


@cli.command()
@click.pass_context
@click.argument('block_number', type=int)
def block(ctx, block_number):
    """Get a block detail"""
    connect(ctx)
    if VERBOSE:
        app_log.info(f"Connected to {ctx.obj['host']}:{ctx.obj['port']}")
        app_log.info(f"block {block_number}")
    req = BlockRequest(start_height=block_number, end_height=block_number, include_balance_list=False, app_log=app_log)
    message = Message(MessageType.BlockRequest11, req, app_log=app_log)
    res = ctx.obj['connection'].fetch(message)
    print(res.to_json())


@cli.command()
@click.pass_context
@click.argument('address', default='', type=str)
def balance(ctx, address):
    """Get balance of an ADDRESS (Uses the one from local id by default)"""
    connect(ctx)
    if address == '':
        address = config.PUBLIC_KEY.to_bytes().hex()
    else:
        address = address.replace('-', '')
    if VERBOSE:
        app_log.info(f"Get balance for address {address}")
    assert(len(address) == 64)  # TODO: better user warning

    if VERBOSE:
        app_log.info(f"Connected to {ctx.obj['host']}:{ctx.obj['port']}")
        app_log.info(f"address {address}")
    empty = EmptyMessageObject()
    message = Message(MessageType.StatusRequest17, empty, app_log=app_log)
    res = ctx.obj['connection'].fetch(message)
    status = res.get_lines()
    frozen = int(extract_status_lines(status, "frozen edge")[0])
    if VERBOSE:
        app_log.info(f"Frozen Edge: {frozen}")

    reconnect(ctx)

    req = BlockRequest(start_height=frozen, end_height=frozen, include_balance_list=True, app_log=app_log)
    message2 = Message(MessageType.BlockRequest11, req, app_log=app_log)
    res = ctx.obj['connection'].fetch(message2)
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
    return (0, 0)

@cli.command()
@click.pass_context
def status(ctx):
    """Get Status of distant server"""
    connect(ctx)
    if VERBOSE:
        app_log.info(f"Connected to {ctx.obj['host']}:{ctx.obj['port']}")
    empty = EmptyMessageObject(app_log=app_log)
    message = Message(MessageType.StatusRequest17, empty, app_log=app_log)
    res = ctx.obj['connection'].fetch(message)
    print(res.to_json())
    # print(json.dumps(status))


@cli.command()
@click.pass_context
@click.argument('recipient', type=str)
@click.argument('amount', default=0, type=float)
@click.argument('above', default=0, type=float)
def send(ctx, recipient, amount, above: float=0):
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


if __name__ == '__main__':
    logger = logging.getLogger('push')

    app_log = logging.getLogger()
    app_log.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)-5s] %(message)s')
    ch.setFormatter(formatter)
    app_log.addHandler(ch)

    # TODO: use user private dir
    private_dir = get_private_dir()
    config.NYZO_SEED = private_dir + '/private_seed'
    config.load(private_dir)

    cli(obj={})

