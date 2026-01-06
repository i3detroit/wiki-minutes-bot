#!/usr/bin/env python3

# Can be run from cron daily or just on Tuesdays.
# Checks if there are meeting minutes for a week from now and sends an email
# to the mailing list if so
# copyright 2019 Mike Fink
# MIT License

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from smtplib import SMTP_SSL
import pywikibot
import datetime
import re
import pickle
from email.message import EmailMessage
import base64
from pywikibot import pagegenerators


SENDTO = 'i3detroit@googlegroups.com'
SENDFROM = 'noreply@i3detroit.org'
SIGNATURE = 'the it cabal'
MEMBER_EMAIL_TEMPLATE = '''The next i3Detroit member meeting will be {} at 19:30.
Meetings are hybrid meaning simultaneously online & in person.
Please add announcements and discussion topics to the agenda below.
Zone coordinators, please fill out the zone update for your zone.

Agenda link: https://www.i3detroit.org/wiki/{}

See the following HOWTO for guidelines and tips for adding new agenda topics: https://www.i3detroit.org/wiki/HOWTO_Add_a_Topic_to_Meeting_Minutes_on_the_Wiki

You can join the meeting remotely on Google Meet at https://www.i3detroit.org/meeting.
In virtual meetings, use the text chat for raising your hand.
Please avoid conversation there so there are not multiple conversations happening at once.
Attendance and votes happen in the #meetings slack channel: https://i3detroit.slack.com/archives/C0101CX23LN.

Thanks,
{}'''
BOARD_EMAIL_TEMPLATE = '''The next i3Detroit Board of Directors meeting will be {} at 19:30.
Meetings are hybrid meaning simultaneously online & in person.
Please add discussion topics to the agenda below.
Officers, please fill out the your officer reports.

Agenda link: https://www.i3detroit.org/wiki/{}

See the following HOWTO for guidelines and tips for adding new agenda topics: https://www.i3detroit.org/wiki/HOWTO_Add_a_Topic_to_Meeting_Minutes_on_the_Wiki

You can join the meeting remotely on Google Meet at https://www.i3detroit.org/meeting.
In virtual meetings, use the text chat for raising your hand.
Please avoid conversation there so there are not multiple conversations happening at once.
Attendance and votes happen in the #meetings slack channel: https://i3detroit.slack.com/archives/C0101CX23LN.

Thanks,
{}'''


def send_message(page, meeting_type, meeting_date):
    ''' Write appropriate meeting minutes email '''
    if meeting_type == 'member':
        subject = "{:%B %Y} First Tuesday Member Meeting - Call for Topics".format(meeting_date)
        message_text = MEMBER_EMAIL_TEMPLATE.format('{:%A, %B %d, %Y}'.format(meeting_date), re.sub(" ", "_", page.title()), SIGNATURE)

    elif meeting_type == 'board':
        subject = "{:%B %Y} Board of Directors Meeting - Call for Topics".format(meeting_date)
        message_text = BOARD_EMAIL_TEMPLATE.format('{:%A, %B %d, %Y}'.format(meeting_date), re.sub(" ", "_", page.title()), SIGNATURE)
    else:
        print("Not a member meeting or board meeting. Nothing to send.")
        exit()

    message = EmailMessage()
    message.set_content(message_text)
    message['to'] = SENDTO
    message['from'] = SENDFROM
    message['subject'] = subject
    print('{now} Sending message...'.format(now=datetime.datetime.now()))
    with SMTP_SSL(host="smtp-relay.gmail.com") as s:
        s.send_message(message)
        s.quit()
    print('Meeting email sent.')



if __name__ == '__main__':
    print('{now} Running...'.format(now=datetime.datetime.now()))

    site = pywikibot.Site()
    site.login()
    cat = pywikibot.Category(site,'Category:Meeting Minutes')
    gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)
    matches = []
    for page in gen:
        match = re.search("[0-9]{8}", page.title())
        if not match:
           continue
        date = match.group(0)
        futureDate = datetime.date.today() + datetime.timedelta(days=14)
        minuteDate = datetime.datetime.strptime(date, '%Y%m%d')
        if(futureDate == minuteDate.date()):
            if 'Minutes:Meeting Minutes' in page.title():
                send_message(page, 'member', minuteDate)
            elif 'Minutes:Board Meeting Minutes' in page.title():
                send_message(page, 'board', minuteDate)
