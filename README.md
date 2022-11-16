# Automatic meeting minutes wiki page creation, and email notification
[pywikibot](https://doc.wikimedia.org/pywikibot/master/) connected to [https://i3detroit.org/wiki](https://i3detroit.org/wiki)

Meeting minutes for board and member meetings are created on the day of the previous meeting, so there is never a time without the agenda for the next meeting.
Email notifications for member and board meetings are emailed out one week in advance to the member list.


`create_meeting_minutes.py` expects to be run on a Tuesday. Add to crontab and fill in paths:
```
0 0 * * 2 /usr/bin/python3 $WIKI_MINUTES_BOT_DIR/create_meeting_minutes.py >> $LOG_LOCATION/minutes_creation.log 2>&1
0 0 * * 2 /usr/bin/python3 $WIKI_MINUTES_BOT_DIR/email_meeting_minutes.py >> $LOG_LOCATION/minutes_email.log 2>&1
```


## Setup
### pywikibot + bot user
This worked on pywikibot commit `2d8d7241` on 2019-06-13.
```
pip3 install requests google-api-python-client auth2client
git clone --recursive --branch stable https://gerrit.wikimedia.org/r/pywikibot/core.git pwb
cd pwb
# to update:
#    git pull origin stable --recurse-submodules # This updates everything
python3 pwb.py generate_family_file.py
# https://www.i3detroit.org/wiki/Main_Page
# i3

# go to https://www.i3detroit.org/wiki/Special:BotPasswords
# make a bot
python3 pwb.py generate_user_files
# choose i3
# add bot password
# put bot username and password in

python3 pwb/pwb.py [whatever script you want to run]
```

### google setup
`token.json` is google magic.
