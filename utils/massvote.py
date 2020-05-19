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
MIN_WAIT_BETWEEN_VOTE = 1
MAX_WAIT_BETWEEN_VOTE = 10

# ----==---- You should not need to edit below ----==----

from os import path
from random import shuffle, randint


def read_sig_vote(line):
    line = line.strip().split(' ')
    if len(line) < 2:
        # default vote is Yes
        line.append("1")
    return tuple(line)


if __name__ == '__main__':
    if not path.isfile("keys.txt"):
        print("missing keys.Txt file")
        exit()
    if not path.isfile("sigs.txt"):
        print("missing sigs.Txt file")
        exit()
    with open("keys.txt") as fp:
        keys = fp.readlines()
        keys = [line.strip() for line in keys if line.strip() != '']
    with open("sigs.txt") as fp:
        sigs = fp.readlines()
        sigs = [read_sig_vote(line) for line in sigs if line.strip() != '']
    total = len(sigs) * len(keys)
    estimate = ((MIN_WAIT_BETWEEN_VOTE + MAX_WAIT_BETWEEN_VOTE)/2 + 3) * total/60
    print("{} keys and {} sigs, total {} votes.\nEstimated time {} min".format(len(keys), len(sigs), total, estimate))
    total= list()
    for sig in sigs:
        for key in keys:
            total.append((sig, key))
    shuffle(total)
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
