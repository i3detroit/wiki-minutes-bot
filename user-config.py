import os

family = 'i3detroit'
mylang = 'i3detroit'
usernames[family][mylang] = os.environ['PWB_USERNAME']

family_files[family] = 'https://i3detroit.org/wi/api.php'

# This is written out by envvars by entrypoint.sh
password_file = '/tmp/pwb-password.py'
