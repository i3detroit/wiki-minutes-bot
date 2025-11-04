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
This worked on pywikibot commit `b78fa049e` on 2021-01-30.
```
# Use a venv
pip3 install -r requirements.txt

pwb generate_family_file.py
# https://www.i3detroit.org/wiki/Main_Page
# i3

# go to https://www.i3detroit.org/wiki/Special:BotPasswords
# make a bot
pwb generate_user_files
# choose i3
# *your* username
# add bot password
# bot username and password

pwb [whatever script you want to run]
```

### google setup
`token.json` is google magic.
