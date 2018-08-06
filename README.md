# Automatic meeting minutes wiki page creation
Creates meeting minutes wiki page from template page a week in advance. Set up in a venv with pywikibot installed and set up to connect to the wiki at www.i3detroit.org/wiki
Expects to be run on a Tuesday. Add to crontab and fill in paths:
```
59 11 * * 2 /$pypath/bin/python /$path/create_meeting_minutes.py >> /$log_location/minutes_creation.log 2>&1
```
