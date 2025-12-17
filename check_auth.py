"""
Check authentication
"""
import pywikibot

site = pywikibot.Site()

site.login()
print(f"{site.logged_in()=}")
print(f"{site.username()=}")
print(f"{site.family=}")
print(f"{site.codes=}")
