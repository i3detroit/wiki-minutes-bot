#!usr/bin/env python

# Automatic i3 Detroit Meeting Minutes page creation on our wiki at i3detroit.org/wiki
# Can be run from cron daily or just on Tuesdays.
# Creates minutes a week in advance, so checks to see if it's a:
#  - first tuesday: create board minutes
#  - second tuesday: create member minutes
#  - final tuesday: create member minutes
# copyright 2018 Mike Fink
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


def write_minutes():
    ''' Write meeting minutes based on page template for the next meeting '''
    today_date = date.today()
    meeting_date = today_date + timedelta(7)

    is_first_tuesday = nth_weekday(today_date, 1, 1) == today_date
    is_second_tuesday = nth_weekday(today_date, 2, 1) == today_date
    # today is final tuesday if (today is 4th tuesday and 5th tuesday is next month)
    #    or (today is 5th tuesday and next tuesday is a different month)
    is_final_tuesday = ((nth_weekday(today_date, 4, 1) == today_date and 
                        nth_weekday(today_date, 5, 1).month != today_date.month) or 
                        (nth_weekday(today_date, 5, 1) == today_date and
                        today_date.month != meeting_date.month))

    site = pywikibot.Site()

    if is_second_tuesday or is_final_tuesday:
        title = 'Minutes:Meeting Minutes'
        template_page = pywikibot.Page(site, u'Meeting_Minutes_Template')
    elif is_first_tuesday:
        title = 'Minutes:Board Meeting Minutes'
        template_page = pywikibot.Page(site, u'Board_Meeting_Minutes_Template')
    else:
        print(str(today_date) + ' Not first, second, or final Tuesday. Exiting.')
        exit()

    date_str = '{:%m-%d-%Y}'.format(meeting_date)
    date_title_str = '{:%m%d%Y}'.format(meeting_date)

    meeting_page_name = u'{} {}'.format(title, date_title_str)
    newpage = pywikibot.Page(site, meeting_page_name)
    if len(newpage.text) > 0:
        print(str(today_date) + ' Error: Page already exists. Exiting.')
        exit()

    template_text = str(bsoup(template_page.text, 'html.parser').pre)[5:-6]
    newpage.text = sub('01-01-20\d\d', date_str, template_text)
    print(str(today_date) + ' Saving minutes.')
    newpage.save(u'Automatic minutes creation')


if __name__ == '__main__':
    # Exit if it's not Tuesday
    today_date = date.today()
    if today_date.weekday() != 1:
        print(str(today_date) + ' Not Tuesday. Exiting.')
        exit()
    else:
        write_minutes()
