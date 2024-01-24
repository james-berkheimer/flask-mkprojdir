
This repo is for archival purposes and is not maintained any longer.


# Set up virtual env
py -3 -m venv virtual  # windows
python3 venv virtual # unix

# Gmail Mail Server
set MAIL_SERVER=smtp.googlemail.com

set MAIL_PORT=587

set MAIL_USE_TLS=1

set MAIL_USERNAME=

set MAIL_PASSWORD=


# Viscira Mail Server
set MAIL_SERVER=cybertron02.viscira.local

set MAIL_PORT=25

set MAIL_USE_TLS=1

set MAIL_USERNAME=render

set MAIL_PASSWORD=[CHANGE_ME]

set AUTH=yes

# Python debugging email server
python -m smtpd -n -c DebuggingServer localhost:8025

# Initialize the data repository
py -3 -m flask db init

# The First Database Migration
py -3 -m flask db migrate -m "users table"

# Upgrade Database
py -3 -m flask db upgrade

# Flask shell CMD
py -3 -m flask shell


# Run the flask session WINDOWS
virtual\Scripts\activate

set FLASK_APP=mkprojdir.py

set FLASK_DEBUG=1

py -3 -m flask run

#Run flask session LINUX
source virtual/bin/activate

export FLASK_APP=mkprojdir.py

export FLASK_DEBUG=1