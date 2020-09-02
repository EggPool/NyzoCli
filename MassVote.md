# Mass Voting 101

Nyzocli massvote allows to

- vote for any number of cycle tx
- with any number of in-cycle private keys
- in a safe way (local signing)
- with randomize order, with random pause between votes (makes vote based cluster identification hard)
- makes sure the vote goes through: connects to nyzo.today api not to vote twice but re-vote for missing ones.
- does not leak info about your verifier(s)

## Install

You can install Nyzocli on a local linux computer (prefered) or on a vps of yours (for instance, your sentinel vps: your keys already are there, no extra leak risk, same location)  
It should run on any modern linux. Ubuntu 18 is the recommended setup, 16 and 20 should work as well.

> Note: In the following commands, I suppose you loggued in as a regular user. If you log in as root, then you can omit the "sudo " prefix of the commands.

The "Install" steps you only have to do once.

1. Check you have Python 3 installed  
`python3 --version`
This should report a python >= 3.6

2. Update packages and install possible missing dependencies (some likely already are installed, listing them all for extra safety)
`sudo apt update`
`sudo apt install python3-dev python3-pip build-essential`

> If an error is reported there, come and say on the Discord, #Help channel.

3. Get Nyzocli

make sure you are in your user directory  
`cd`  
Clone the project  
`git clone https://github.com/EggPool/NyzoCli.git`  
move into the project 
`cd NyzoCli`

4. Install required Python packages

You should now be in the Nyzocli directory. if not: `cd;cd NyzoCli`  
Install the packages  
`python3 -m pip install -r requirements.txt`

> If an error is reported there, come and say on the Discord, #Help channel.


NyzoCLi is now installed.

## Mass Voting

1. Move into the util directory of NyzoCli:  
`cd;cd NyzoCli/utils` 

This directory contains only `massvote.py` python script by default.  
You'll now feed him the required keys and cycle sigs.

2. Fill in your in-cycle keys  
To be done once, and updated when a new verifier joins.

Create/Edit the `keys.txt` text file.  
You can upload it from your local pc via ssh/putty, or edit it from command line:  
`nano keys.txt`  
Paste your in-cycle keys. One per line, in "key_xxxxxx" format.  
> To exit from nano, ctrl-x, answer Y for yes to save, enter.

2. Fill in the cycle tx you want to vote for 
To be done for every vote you want to emit.

Create/Edit the `sigs.txt` text file.  
You can upload it from your local pc via ssh/putty, or edit it from command line:  
`nano sigs.txt`  
Paste the cycle tx sigs. One per line, in "sig_xxxxxx" format.  

For instance, for NCFP-3(Part24) and NCFP-3(Part25) you can get the sig from nyzo.co or https://nyzo.today/votes/  
your sigs.txt file should contain  
```
sig_g9cXvrLxbCvI-Ejg_WwJbH6bGCQwNHYDDeWIQFyB_8bkvRBZsDjVWNEWhGYw17A4R9YafX4H3dv9HV39uIZjpgE~aNse
sig_gaaFNNK4DhfXvnvdJBrkDysicE58t60N.KpU.r9M79N-yxuAFLT1ts8zhQ~zJKkFuLoAJhDmLEuJ4.g_Mfa_Nx5S8Arn
```

> By default, votes are set to 1 (YES). If you want to vote 0 (NO) to one cycle tx, the line then has to be like  
> `sig_xxxxxx 0`

3. Optionnal, adjust mass vote params

`nano massvote.py`  

You can adjust the following params:
```
# You can adjust here to your liking. wait will be random between these two.
# these are seconds.
MIN_WAIT_BETWEEN_VOTE = 20
MAX_WAIT_BETWEEN_VOTE = 120

# Set to False if you don't want to query nyzo.today for existing votes.
# Does not give any info about your verifiers, just asks the list of votes for a given sig_
# With ASK_NYZO_TODAY = True, you can re-run the script after a first pass to check and re-submit missing votes.
ASK_NYZO_TODAY = True
```

4. Run massvote.py

Nothing will go out yet, this is safe to do as many times as you want

`python3 massvote.py`

The script will 
- read keys.txt
- read sigs.txt
- gather all votes from nyzo.today (not giving away your verifiers)
- generate vote commands for all keys x sigs, minus existing votes of yours
- report expected time voting will need and number of votes to issue
- save all the commands - with subsequent sleep - in a `vote.sh` file

You can then check that vote.sh file, make sure it does what it's supposed to do (run nyzoCli votes)  
`cat vote.sh`

5. Vote

You're still supposed to be in the NyzoCLi/utils directory. If not, `cd;cd NyzoCli/utils`   

Make sure the script is marked as executable  
`chmod +x vote.sh`

Run the script  
`./vote.sh`

This will run one vote, display its outcome (likely some data with "forwarded": "true" at the end) then sleep before the next vote.  
Do not close the shell, let it run till the end.

6. Recheck and resubmit failed votes

Some votes can fail to be included, and need resubmit.  
Once you ran "vote.sh", do not change anything, just goto step 4 and run `python3 massvote.py` again.  
vote.sh will be rebuild with only missing vote commands.

Rerun `./vote.sh`

repeat until massvote.py does not report any missing vote.


