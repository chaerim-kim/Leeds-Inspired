
## Overview
This app lets the user select the category of the event they want to attend.

It then redirects and fetches the local Leeds events of user's interest, via leedsinspired's API.

It lists all the events, and users are prompt to choose one event, which then shows the venue information of that event or the restaurants near that venue, using Yelp's API.


## Installation
$ module add python/3.4.3

Creating a virtual environment

$ virtualenv flask

Activating the virtual environment -flask 

$ source flask/bin/activate

Install dependencies. ()-U: update if already installed)

$ pip install -U -r requirements.txt

Setting development environment

$ export FLASK_ENV=development


## Running Server and Client
Running the server

$ python server.py


Running the client

$ cd client

$ python client.py


## License
[Leeds Inspired](http://api.leedsinspired.co.uk/)

[Yelp Fusion](https://www.yelp.com/fusion)
