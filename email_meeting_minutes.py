#!/usr/bin/env python3

# Can be run from cron daily or just on Tuesdays.
# Checks if there are meeting minutes for a week from now and sends an email
# to the mailing list if so
# copyright 2019 Mike Fink
# MIT License

from bs4 import BeautifulSoup as bsoup
import pywikibot
import datetime
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file
from email.mime.text import MIMEText
import base64
from googleapiclient.errors import HttpError
from pywikibot import pagegenerators

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
SENDTO = 'i3detroit@googlegroups.com'
SECNAME = 'Mike'
MEMBER_EMAIL_TEMPLATE = '''The next i3Detroit member meeting will be Tuesday, {} at 7:30 pm. Please add announcements and discussion topics to the agenda below. Zone coordinators, please fill out the zone update for your zone.
<br><br>
Agenda link: https://www.i3detroit.org/wiki/{}
<br><br>
See the following HOWTO for guidelines and tips for adding new agenda topics: https://www.i3detroit.org/wiki/HOWTO_Add_a_Topic_to_Meeting_Minutes_on_the_Wiki
<br><br>
Thanks,<br>
{}'''
BOARD_EMAIL_TEMPLATE = '''The next i3Detroit Board of Directors meeting will be Tuesday, {} at 7:30 pm. Please add discussion topics to the agenda below. Officers, please fill out the your officer reports.
<br><br>
Agenda link: https://www.i3detroit.org/wiki/{}
<br><br>
See the following HOWTO for guidelines and tips for adding new agenda topics: https://www.i3detroit.org/wiki/HOWTO_Add_a_Topic_to_Meeting_Minutes_on_the_Wiki
<br><br>
Thanks,<br>
{}'''


def write_message(page, meeting_type, meeting_date):
    ''' Write appropriate meeting minutes email '''
    if meeting_type == 'member':
        if meeting_date.day < 8: # if is first tuesday
            subject = "{:%B %Y} First Tuesday Member Meeting - Call for Topics".format(meeting_date)
        else: # else is third tuesday
            subject = "{:%B %Y} Third Tuesday Member Meeting - Call for Topics".format(meeting_date)
        message_text = MEMBER_EMAIL_TEMPLATE.format('{:%B %d, %Y}'.format(meeting_date), re.sub(" ", "_", page.title()), SECNAME)

    elif meeting_type == 'board':
        subject = "{:%B %Y} Board of Directors Meeting - Call for Topics".format(meeting_date)
        message_text = BOARD_EMAIL_TEMPLATE.format('{:%B %d, %Y}'.format(meeting_date), re.sub(" ", "_", page.title()), SECNAME)
    else:
        print("Not a member meeting or board meeting. Nothing to send.")
        exit()

    message = MIMEText(message_text, 'html')
    message['to'] = SENDTO
    message['from'] = 'i3 Secretary'
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, message):
    '''Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        message: Message to be sent.

    Returns:
        Sent Message.
    '''
    try:
        message = (service.users().messages().send(userId='me', body=message)
                   .execute())
        print('Meeting email sent. Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred sending meeting email: %s' % error)


if __name__ == '__main__':
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        print('Google credentials error. Cannot validate to send minutes email.')
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    site = pywikibot.Site()
    cat = pywikibot.Category(site,'Category:Meeting Minutes')
    gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)
    matches = []
    for page in gen:
        match = re.search("[0-9]{8}", page.title())
        if not match:
           continue
        date = match.group(0)
        nextWeek = datetime.date.today() + datetime.timedelta(days=7)
        minuteDate = datetime.datetime.strptime(date, '%Y%m%d')
        if(nextWeek == minuteDate.date()):
            if 'Minutes:Meeting Minutes' in page.title():
                send_message(service, write_message(page, 'member', minuteDate))
            elif 'Minutes:Board Meeting Minutes' in page.tite():
                send_message(service, write_message(page, 'board', minuteDate))
