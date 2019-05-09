#!usr/bin/env python

# Automatic i3 Detroit Meeting Minutes page creation on our wiki at i3detroit.org/wiki
# Can be run from cron daily or just on Tuesdays.
# Creates minutes a week in advance, so checks to see if it's a:
#  - first tuesday: create board minutes
#  - second tuesday: create member minutes
#  - final tuesday: create member minutes
# copyright 2019 Mike Fink
# MIT License

from bs4 import BeautifulSoup as bsoup
import pywikibot
from datetime import date, timedelta
from re import sub


def nth_weekday(the_date, nth_week, week_day):
    ''' calculate the nth $weekday in the month of the input date (0 = Monday) '''
    temp = the_date.replace(day=1)
    adj = (week_day - temp.weekday()) % 7
    temp += timedelta(days=adj)
    temp += timedelta(weeks=nth_week - 1)
    return temp


def check_day(today_date):
    ''' Write meeting minutes based on page template for the next meeting '''
    # First Tuesday Member Meeting - next meeting is in 2 weeks
    if today_date == nth_weekday(today_date, 1, 1):
        title = 'Minutes:Meeting Minutes'
        template_page = pywikibot.Page(site, u'Meeting_Minutes_Template')
        meeting_date = today_date + timedelta(14)
        write_minutes(title, template_page, meeting_date)
        # First Tuesday Fundraising Meeting - next meeting first tuesday next month
        title = 'Minutes:Fundraising Committee Meeting Minutes'
        template_page = pywikibot.Page(site, u'Fundraising Committee Meeting Minutes Template')
        meeting_date = nth_weekday(date.today() + timedelta(31), 1, 1)
        write_minutes(title, template_page, meeting_date)
    # Third Tuesday Member Meeting - next meeting is first tuesday of next month
    elif nth_weekday(today_date, 3, 1) == today_date:
        title = 'Minutes:Meeting Minutes'
        template_page = pywikibot.Page(site, u'Meeting_Minutes_Template')
        meeting_date = nth_weekday(today_date + timedelta(weeks=4), 1, 1)
    # Second Tuesday Board Meeting - next meeting is second tuesay of next month
    elif today_date == nth_weekday(today_date, 2, 1):
        title = 'Minutes:Board Meeting Minutes'
        template_page = pywikibot.Page(site, u'Board_Meeting_Minutes_Template')
        meeting_date = nth_weekday(today_date + timedelta(weeks=4), 2, 1)
    else:
        print(str(today_date) + ' Not first, second, or third Tuesday. Exiting.')
        exit()

def write_minutes(title, template_page, meeting_date):
    date_str = '{:%m-%d-%Y}'.format(meeting_date)
    date_title_str = '{:%Y%m%d}'.format(meeting_date)
    meeting_page_name = u'{} {}'.format(title, date_title_str)
    
    newpage = pywikibot.Page(site, meeting_page_name)
    if len(newpage.text) > 0:
        print(str(today_date) + ' Error: Page already exists. Exiting.')
        exit()

    template_text = str(bsoup(template_page.text, 'html.parser').pre)[5:-6]
    newpage.text = sub('01-01-20\d\d', date_str, template_text)
    print('{} Saving minutes for {}'.format(str(today_date), str(meeting_date)))
    newpage.save(u'Automatic minutes creation')


if __name__ == '__main__':
    # Exit if it's not Tuesday
    today_date = date.today()
    if today_date.weekday() == 1:
        site = pywikibot.Site()
        check_day(today_date)
        exit()
    else:
        print(str(today_date) + ' Not Tuesday. Exiting.')
        exit()
