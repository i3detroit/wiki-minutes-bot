#!/usr/bin/env python3

# Can be run from cron daily or just on Tuesdays.
# Checks if there are meeting minutes for a week from now and sends an email
# to the mailing list if so
# copyright 2019 Mike Fink
# MIT License

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pywikibot
import datetime
import re
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
from googleapiclient.errors import HttpError
from pywikibot import pagegenerators


SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SENDTO = 'i3detroit@googlegroups.com'
SECNAME = 'Secretary'
MEMBER_EMAIL_TEMPLATE = '''The next i3Detroit member meeting will be {} at 7:30 pm. Meetings are hybrid meaning simultaneously online & in person. Please add announcements and discussion topics to the agenda below. Zone coordinators, please fill out the zone update for your zone.
<br><br>
Agenda link: https://www.i3detroit.org/wiki/{}
<br><br>
See the following HOWTO for guidelines and tips for adding new agenda topics: https://www.i3detroit.org/wiki/HOWTO_Add_a_Topic_to_Meeting_Minutes_on_the_Wiki
<br><br>
You can join the meeting remotely on Google Meet at https://www.i3detroit.org/meeting. In virtual meetings, use the text chat for raising your hand. Please avoid conversation there so there are not multiple conversations happening at once. Attendance and votes happen in the #meetings slack channel: https://i3detroit.slack.com/archives/C0101CX23LN.
<br><br>
Thanks,<br>
{}'''
BOARD_EMAIL_TEMPLATE = '''The next i3Detroit Board of Directors meeting will be {} at 7:30 pm. Meetings are held virtually on Google Meet. Please add discussion topics to the agenda below. Officers, please fill out the your officer reports.
<br><br>
Agenda link: https://www.i3detroit.org/wiki/{}
<br><br>
See the following HOWTO for guidelines and tips for adding new agenda topics: https://www.i3detroit.org/wiki/HOWTO_Add_a_Topic_to_Meeting_Minutes_on_the_Wiki
<br><br>
You can join the meeting remotely on Google Meet at https://www.i3detroit.org/meeting. In virtual meetings, use the text chat for raising your hand. Please avoid conversation there so there are not multiple conversations happening at once. Attendance and votes happen in the #meetings slack channel: https://i3detroit.slack.com/archives/C0101CX23LN.
<br><br>
Thanks,<br>
{}'''


def write_message(page, meeting_type, meeting_date):
    ''' Write appropriate meeting minutes email '''
    if meeting_type == 'member':
        subject = "{:%B %Y} First Tuesday Member Meeting - Call for Topics".format(meeting_date)
        message_text = MEMBER_EMAIL_TEMPLATE.format('{:%A, %B %d, %Y}'.format(meeting_date), re.sub(" ", "_", page.title()), SECNAME)

    elif meeting_type == 'board':
        subject = "{:%B %Y} Board of Directors Meeting - Call for Topics".format(meeting_date)
        message_text = BOARD_EMAIL_TEMPLATE.format('{:%A, %B %d, %Y}'.format(meeting_date), re.sub(" ", "_", page.title()), SECNAME)
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
    print('{now} Sending message...'.format(now=datetime.datetime.now()))
    try:
        message = (service.users().messages().send(userId='me', body=message)
                   .execute())
        print('Meeting email sent. Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred sending meeting email: %s' % error)


if __name__ == '__main__':
    print('{now} Running...'.format(now=datetime.datetime.now()))
    try:
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
    except:
        print('{now} Error authenticating with google. Exiting'.format(now=datetime.datetime.now()))
        exit()

    site = pywikibot.Site()
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
                send_message(service, write_message(page, 'member', minuteDate))
            elif 'Minutes:Board Meeting Minutes' in page.title():
                send_message(service, write_message(page, 'board', minuteDate))
