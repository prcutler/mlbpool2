[![Documentation Status](https://readthedocs.org/projects/mlbpool2/badge/?version=latest)](
http://mlbpool2.readthedocs.io/en/latest/?badge=latest)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Updates](https://pyup.io/repos/github/prcutler/mlbpool2/shield.svg)](https://pyup.io/repos/github/prcutler/mlbpool2/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
# MLBPool2

## How to Play

MLBPool2 is a fantasy baseball like application originally created by
Jason Theros.  MLBPool2 differs from fantasy baseball in that players
make their picks for where they believe teams will place in their division,
individual statistical leaders and which teams will make the playoffs as a
Wildcard before the season starts.  Each pick is worth a specific point
value.  A unique pick (not made by any other player) is worth double
points.  Players can change their picks at the All Star Break, but those
changes are only half their original value.  Unlike fantasy baseball,
players do not need to make daily lineup changes - just sit back and
watch the season unfold!  For more information on how to play, you can read the 
[user documentation on Read the Docs](http://mlbpool2.readthedocs.io/).

Developer documentation coming soon.

## MLBPool2 Application

The MLBPool2 application is based on [NFLPool](https://github.com/prcutler/nflpool),
with the major difference is that NFLPool does not allow mid-season
changes.  MLBPool2 is licensed under the MIT license.

## Requirements

* Python 3.6+
* MariaDB / MySQL
* Pyramid 1.9
* SQLAlchemy
* [MySportsFeeds](https://www.mysportsfeeds.com) account (for MLB stats)

## Contributing

MLBPool2 and NFLPool are my first Python applications and I'm sure the
code is ugly in places - contributions welcome!  Please see the
[Code of Conduct](https://github.com/prcutler/mlbpool2/blob/master/CODE_OF_CONDUCT.md).

Imposter syndrome disclaimer: I want your help. No really, I do.

There might be a little voice inside that tells you you're not ready; that you need to do one more tutorial, 
or learn another framework, or write a few more blog posts before you can help me with this project.

I assure you, that's not the case.

While I don't have clear contributing guidelines at this time, please fork the repo and send me a pull request!  
I'm new to Python too, and I would love the help and learn how to make things better.

And you don't just have to write code. You can help out by writing documentation, tests, or even by giving 
feedback about MLBPool2. (And yes, that includes giving feedback about the contribution guidelines.)

Thank you for contributing!

(Adapted from 
[Adrienne Lowe's Imposter Syndrome Disclaimer](https://github.com/adriennefriend/imposter-syndrome-disclaimer))

## Installation

* Update the links in  both files in `/email/templates/` to reflect your correct domain name and email addresses
* Update the templates in `/templates/home/` with your own information (such as index, about, credits, etc.)  Update 
the footer in `/templates/shared/_layout.pt`.
* Install a Python virtual environment!
* Deploy your Pyramid app on your web server, including updating production.ini with any API keys needed and config.ini
in the data directory with your superuser email address, database information, MySportsFeed account
information, and Slack webhook
* Run pip to install the dependencies:  `pip install -e setup.py` from the project's root directory (or pip install -e .)
* Start the Pyramid app (I personally created a systemd service)
* Visit the homepage of the MLBPool2 app and register your account, making sure the
email address matches the superuser email in config.py above
* Go to the admin panel at your domain adding `/admin`
* MLBPool2 will automatically detect that the database is empty and redirect you to the `/new_install` page
* Follow the prompts, which will include creating the installation, adding a new season and importing 
active MLB baseball players
* When finished, it will redirect you back to the `/admin` page
* Let your players know the site is ready and they should create an account and submit their picks!


