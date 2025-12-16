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
### Docker

This is utilizing [just](https://just.systems/). If you don't want to install it, go read the `Justfile` to see the full commands.

`just build` tags a `localhost/wiki-minutes-bot` container.

`just run <cmd>` runs a command with the container, with the source mounted, `.env` handled, and such.


### Non-docker

TODO


## Authentication

The container accepts authentication by environment variables:

* `PWB_USERNAME`/`PWB_PASSWORD` if you're using standard password authentication
* `PWB_USERNAME`/`PWB_BOTNAME`/`PWB_BOTPASS` if you're using [bot passwords](https://www.mediawiki.org/wiki/Manual:Pywikibot/BotPasswords)
