#!/usr/bin/env python3
"""
Console mode basic Nyzo client - Connects to a peer, console mode.

EggdraSyl - Jan. 2019.

"""

import click
import logging
# import pprint
import sys
# from time import time
import json

from pynyzo.messagetype import MessageType
from pynyzo.message import Message
from pynyzo.messageobject import EmptyMessageObject
from pynyzo.messages.statusresponse import StatusResponse
from pynyzo.connection import Connection
from pynyzo.helpers import tornado_logger
import pynyzo.config as config


__version__ = '0.0.1'


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


@click.group()
@click.option('--host', '-h', default="127.0.0.1", help='Set a specific peer (default=localhost)')
@click.option('--port', '-p', default=9444, help='Peer port (default 9444)')
@click.option('--verbose', '-v', default=False)
@click.pass_context
def cli(ctx, port, host, verbose):
    global VERBOSE
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    ctx.obj['verbose'] = verbose
    VERBOSE = verbose
    ctx.obj['connection'] = None


@cli.command()
@click.pass_context
def version(ctx):
    """Print version"""
    print("Nyzocli version {}".format(__version__))


@cli.command()
@click.pass_context
@click.argument('address', default='', type=str)
def balance(ctx, address):
    """Get balance of an ADDRESS (Uses the one from local id by default)"""
    # connect(ctx)
    # load_keys(ctx, address)
    if VERBOSE:
        print(f"Connected to {ctx.obj['host']}:{ctx.obj['port']}")
        print(f"address {ctx.obj['address']}")
    # print(json.dumps(balance))
    return balance


@cli.command()
@click.pass_context
def status(ctx):
    """Get Status of distant server"""
    connect(ctx)
    if VERBOSE:
        print(f"Connected to {ctx.obj['host']}:{ctx.obj['port']}")
    empty = EmptyMessageObject(app_log=app_log)
    message = Message(MessageType.StatusRequest17, empty, app_log=app_log)
    res = ctx.obj['connection'].fetch(message)
    print(res)
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
    config.NYZO_SEED = 'private_seed'
    config.load()

    cli(obj={})

