#!/usr/bin/env python3
"""
Mass voter helper

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

"""

# You can adjust here to your liking. wait will be random between these two.
# these are seconds.
MIN_WAIT_BETWEEN_VOTE = 450
MAX_WAIT_BETWEEN_VOTE = 900

# Set to False if you don't want to query nyzo.today for existing votes.
# Does not give any info about your verifiers, just asks the list of votes for a given sig_
# With ASK_NYZO_TODAY = True, you can re-run the script after a first pass to check and re-submit missing votes.
ASK_NYZO_TODAY = True

# ----==---- You should not need to edit below ----==----

import json
# import sys
from os import path
from random import shuffle, randint
from requests import get
from nyzostrings.nyzostringencoder import NyzoStringEncoder
from pynyzo.keyutil import KeyUtil


def read_sig_vote(line):
    line = line.strip().split(' ')
    if len(line) < 2:
        # default vote is Yes
        line.append("1")
    return tuple(line)


VOTED = {}


if __name__ == '__main__':
    if not path.isfile("keys.txt"):
        print("missing keys.txt file")
        exit()
    if not path.isfile("sigs.txt"):
        print("missing sigs.txt file")
        exit()
    with open("keys.txt") as fp:
        keys = fp.readlines()
        keys = [line.strip() for line in keys if line.strip() != '']
    with open("sigs.txt") as fp:
        sigs = fp.readlines()
        sigs = [read_sig_vote(line) for line in sigs if line.strip() != '']
    for sig in sigs:
        if ASK_NYZO_TODAY:
            hex_sig = NyzoStringEncoder.decode(sig[0]).get_bytes().hex()
            res = get(f"https://nyzo.today/api/transactionvotes/{hex_sig}")
            VOTED[sig[0]] = json.loads(res.text)
        else:
            VOTED[sig[0]] = {}

    total_pre = len(sigs) * len(keys)
    estimate = ((MIN_WAIT_BETWEEN_VOTE + MAX_WAIT_BETWEEN_VOTE) / 2 + 3) * total_pre / 60
    print("{} keys and {} sigs, total {} votes.\nEstimated time {} min"
          .format(len(keys), len(sigs), total_pre, estimate))
    total = list()
    for key in keys:
        key_hex = NyzoStringEncoder.decode(key).get_bytes().hex()
        # calc matching id as hex
        id_hex = KeyUtil.private_to_public(key_hex)
        for sig in sigs:
            if id_hex not in VOTED[sig[0]]:
                total.append((sig, key))
    shuffle(total)
    estimate = ((MIN_WAIT_BETWEEN_VOTE + MAX_WAIT_BETWEEN_VOTE) / 2 + 3) * len(total) / 60
    print(f"{len(keys)} keys and {len(sigs)} sigs, total after filter {len(total)} votes "
          f"instead of {total_pre}.\nEstimated time {estimate} min")
    bash = ["#!/bin/bash"]
    for item in total:
        line = "../Nyzocli.py vote {} {} {}".format(item[0][0], item[0][1], item[1])
        bash.append(line)
        delay = randint(MIN_WAIT_BETWEEN_VOTE, MAX_WAIT_BETWEEN_VOTE)
        line = "sleep {}".format(delay)
        bash.append(line)
    # print("\n".join(bash))
    with open("vote.sh", "w") as fp:
        fp.write("\n".join(bash))
    print("Done")
